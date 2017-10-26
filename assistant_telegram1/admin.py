from django.contrib import admin
from assistant_telegram1.models import Intent,Story_msg,Story_action,Story_entity
from assistant_telegram1.models import Chat_id,Context_chat,Entity,Log

# Register your models here.
admin.site.register(Intent)
admin.site.register(Story_msg)
admin.site.register(Story_action)
admin.site.register(Story_entity)
admin.site.register(Chat_id)
admin.site.register(Context_chat)
admin.site.register(Entity)
admin.site.register(Log)

