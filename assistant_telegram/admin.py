from django.contrib import admin
from assistant_telegram.models import Context_chat
from assistant_telegram.models import Entity
from assistant_telegram.models import Undefined_msg
from assistant_telegram.models import Story
from assistant_telegram.models import Story_entity
# Register your models here.
admin.site.register(Context_chat)
admin.site.register(Entity)
admin.site.register(Undefined_msg)
admin.site.register(Story)
admin.site.register(Story_entity)
