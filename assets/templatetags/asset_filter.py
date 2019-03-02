from django import template
from django.apps import apps
from assets.models import Ecs
register = template.Library()


@register.filter(name='ecs_model_choices')
def ecs_model_choices(model_name, choice_name):
    asset_app = apps.get_app_config('assets')
    return getattr(asset_app.get_model(model_name), choice_name)


@register.filter(name='ecs_type_choices')
def ecs_type_choices(value):
    return  Ecs.TYPE_CHOICES