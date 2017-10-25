from django.db import models


# Create your models here.
class Context_chat(models.Model):
	chat_id=models.BigIntegerField(primary_key=True)
	intent=models.CharField(max_length=60)
	validated_action=models.BooleanField()
	prev_msg_from_bot=models.CharField(max_length=200,default=" ")

	def __str__(self):
		str1=''
		str1=str(self.chat_id)+" " + str(self.intent) + " " + str(self.validated_action)+" "+str(self.prev_msg_from_bot)
		for entity in self.entity_set.all():
			str1+=str(entity)+" | "
		return str1

class Entity(models.Model):
	name=models.CharField(max_length=61)
	value=models.CharField(max_length=60)
	confidence=models.FloatField()
	chat = models.ForeignKey(Context_chat, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.name)+" "+str(self.value)+" " + str(self.confidence)+" "+str(self.chat.chat_id)

class Story(models.Model):
	intent=models.CharField(primary_key=True,max_length=60)

	msg="msg"
	act="action"
	story_type_choices = (
        (msg, 'message'),
        (act, 'action'),
    )

	story_type=models.CharField(max_length=10,choices=story_type_choices,default=msg)
	validation_option=models.BooleanField(default="False")
	message=models.TextField(default=" ")
	action_name=models.CharField(max_length=60,default=" ")
	answer=models.TextField(default=" ")
	name=models.CharField(max_length=60,default=" ")
	desc=models.CharField(max_length=160,default=" ")

	def __str__(self):
		str1=''
		str1=str(self.intent)+": " + str(self.story_type)
		return str1

class Story_entity(models.Model):
	name=models.CharField(max_length=60)
	question=models.CharField(max_length=100)
	intent = models.ForeignKey(Story, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.name)+" "+str(self.question)+" " + str(self.intent)


class Undefined_msg(models.Model):
	msg=models.CharField(max_length=200)
	def __str__(self):
		return str(self.msg)

class Log_msg(models.Model):
	msg=models.TextField(max_length=200, default=" ")
	intent=models.CharField(max_length=200,default=" ")
	def __str__(self):
		return str(self.msg)
