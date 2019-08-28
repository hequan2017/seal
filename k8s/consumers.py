from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import threading
import time

from channels.layers import get_channel_layer
from k8s.k8sApi.core import K8sApi

channel_layer = get_channel_layer()


class K8SStreamThread(threading.Thread):

    def __init__(self, ws, container_stream):
        threading.Thread.__init__(self)
        self.ws = ws
        self.stream = container_stream

    def run(self):
        while self.stream.is_open():
            time.sleep(0.1)
            if not self.stream.is_open():
                self.ws.close()
            try:
                if self.stream.peek_stdout():
                    stdout = self.stream.read_stdout()
                    self.ws.send(stdout)
                if self.stream.peek_stderr():
                    stderr = self.stream.read_stderr()
                    self.ws.send(stderr)
            except Exception as err:
                self.ws.close()


class EchoConsumer(WebsocketConsumer):

    def connect(self):
        # 创建channels group， 命名为：用户名 (最好不要中文名字,这里会用名字 建立一个通道，通过这个通道进行通信)，并使用channel_layer写入到redis
        try:
            async_to_sync(self.channel_layer.group_add)(self.scope['user'].username, self.channel_name)
        except Exception as e:
            # 这里是为了配合 seal-vue 使用，实际项目，请删除下面这一行
            async_to_sync(self.channel_layer.group_add)("admin", self.channel_name)


        # 可以在这里根据 用户  要访问的pod 进行 权限控制
        path = self.scope['path'].split('/')
        try:
            k = K8sApi()
            self.container_stream = k.terminal_start(namespace=path[3], pod_name=path[2], container="")
            kub_stream = K8SStreamThread(self, self.container_stream)
            kub_stream.start()
        except Exception as err:
            return
        self.accept()

    def receive(self, text_data):
        try:
            self.container_stream.write_stdin(text_data)
        except Exception as ex:
            self.container_stream.write_stdin('exit\r')

    def user_message(self, event):
        self.send(text_data=event["text"])

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.scope['user'].username, self.channel_name)
            self.container_stream.write_stdin('exit\r')  ## 必须加这个，防止 网页关闭，但是 容器没有退出
        except Exception as e:
            # 这里是为了配合 seal-vue 使用，实际项目，请删除下面这一行
            async_to_sync(self.channel_layer.group_discard)("admin", self.channel_name)
