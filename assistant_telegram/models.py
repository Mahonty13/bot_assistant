from django.db import models


# Create your models here.

class Intent(models.Model):
	name=models.CharField(primary_key=True,max_length=60)

	def __str__(self):
		str1=str(self.name)
		return str1

class Chat_id(models.Model):
	idnumber=models.BigIntegerField(primary_key=True)

	def __str__(self):
		str1=str(self.idnumber)
		return str1



class Context_chat(models.Model):
	chat_id=models.OneToOneField(
        Chat_id,
        on_delete=models.CASCADE,
        primary_key=True,
    )
	intent=models.OneToOneField(
        Intent,
        on_delete=models.CASCADE
    )
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


class Story_msg(models.Model):
	intent=models.OneToOneField(
        Intent,
        on_delete=models.CASCADE,
        primary_key=True,
    )
	msg_example=models.TextField(default=" ")
	answer=models.TextField(default=" ")

	def __str__(self):
		str1=str(self.intent)+": " + str(self.answer)
		return str1

class Story_action(models.Model):
	intent=models.OneToOneField(
        Intent,
        on_delete=models.CASCADE,
        primary_key=True,
    )
	validation_option=models.BooleanField(default="False")
	action_name=models.CharField(max_length=60,default=" ")
	action_answer=models.TextField(default=" ")
	transcript=models.CharField(max_length=60,default=" ")
	desc=models.TextField(default=" ")

	def __str__(self):
		str1=str(self.intent)+": " + str(self.action_name)
		return str1

class Story_entity(models.Model):
	name=models.CharField(max_length=60)
	question=models.CharField(max_length=100)
	intent = models.ForeignKey(Story_action, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.name)+" "+str(self.question)+" " + str(self.intent)

class Log(models.Model):
	msg=models.TextField(max_length=200, default=" ")
	intent=models.ForeignKey(Intent,on_delete=models.SET_NULL,null=True)
	date_in_s=models.BigIntegerField()
	chat_id=models.ForeignKey(Chat_id,on_delete=models.SET_NULL,null=True)
	viewed=models.BooleanField(default="False")


	def __str__(self):
		str1=str(self.msg)+" | "+str(self.intent)+" | "+str(self.chat_id.idnumber)+" | "+str(self.viewed)
		return str1