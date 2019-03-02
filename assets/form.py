from django import forms
from assets.models import Ecs


class EcsForm(forms.ModelForm):
    class Meta:
        model = Ecs
        fields = '__all__'

        widgets = {
            'type': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': '----请选择环境----'}),
        }

        help_texts = {
            'type': '* 请选择 资产所在平台.',

        }

    def clean_type(self):
        """
        自定义验证
        :return:
        """
        type = self.cleaned_data['type']
        return type
