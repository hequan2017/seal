from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import paramiko
import threading
import time
from seal import settings

from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


class MyThread(threading.Thread):
    def __init__(self, chan):
        threading.Thread.__init__(self)
        self.chan = chan
        self.number = 0

    def run(self):

        while not self.chan.chan.exit_status_ready():
            time.sleep(0.1)
            try:
                data = self.chan.chan.recv(1024)
                str_data = data.decode(encoding='utf-8')
                if getattr(settings, 'webssh_name') in data.decode(encoding='utf-8'):
                    self.number += 1

                if "kubectl exec -it" in str_data:
                    #不返回内容
                    pass
                else:
                    if "rpc error" in str_data:
                        async_to_sync(self.chan.channel_layer.group_send)(
                            self.chan.scope['user'].username,
                            {
                                "type": "user.message",
                                "text": "连接错误,已断开连接! 此 pod  不支持sh 或者其他未知错误!\r"
                            },
                        )
                        self.chan.sshclient.close()
                    elif self.number > 1:
                        async_to_sync(self.chan.channel_layer.group_send)(
                            self.chan.scope['user'].username,
                            {
                                "type": "user.message",
                                "text": "程序退出,已断开连接!\r"
                            },
                        )
                        self.chan.sshclient.close()
                    else:
                        async_to_sync(self.chan.channel_layer.group_send)(
                            self.chan.scope['user'].username,
                            {
                                "type": "user.message",
                                "text": bytes.decode(data)
                            },
                        )

            except Exception as ex:
                pass
        self.chan.sshclient.close()
        return False


class EchoConsumer(WebsocketConsumer):

    def connect(self):
        # 创建channels group， 命名为：用户名 (最好不要中文名字)，并使用channel_layer写入到redis
        async_to_sync(self.channel_layer.group_add)(self.scope['user'].username, self.channel_name)

        self.sshclient = paramiko.SSHClient()
        self.sshclient.load_system_host_keys()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(getattr(settings, 'webssh_ip'), getattr(settings, 'webssh_port'),
                               getattr(settings, 'webssh_username'), getattr(settings, 'webssh_password'))
        self.chan = self.sshclient.invoke_shell(term='xterm')
        self.chan.settimeout(0)
        t1 = MyThread(self)
        t1.setDaemon(True)
        t1.start()
        path = self.scope['path'].split('/')
        cmd = f"kubectl exec -it {path[2]}  -n  {path[3]}  sh  \r"
        self.chan.send(cmd)

        self.accept()

    def receive(self, text_data):
        try:
            self.chan.send(text_data)
        except Exception as ex:
            pass
            # print(str(ex))

    def user_message(self, event):
        self.send(text_data=event["text"])

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.scope['user'].username, self.channel_name)
