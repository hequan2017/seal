from functools import wraps


def get_list(function):
    """
    列表页面  获取 搜索
    :param function: self.model
    :return:
    """

    @wraps(function)
    def wrapped(self):
        # user = self.request.user
        # groups = [x['name'] for x in self.request.user.groups.values()]
        # request_type = self.request.method
        # model = str(self.model._meta).split(".")[1]

        filter_dict = {}
        not_list = ['page', 'order_by', 'csrfmiddlewaretoken']
        for k, v in dict(self.request.GET).items():
            if [i for i in v if i != ''] and (k not in not_list):
                if '__in' in k:
                    filter_dict[k] = v
                else:
                    filter_dict[k] = v[0]

        self.filter_dict = filter_dict
        self.queryset = self.model.objects.filter(**filter_dict).order_by('-id')
        order_by_val = self.request.GET.get('order_by', '')
        if order_by_val:
            self.queryset = self.queryset.order_by(order_by_val) if self.queryset else self.queryset
        result = function(self)
        return result

    return wrapped
