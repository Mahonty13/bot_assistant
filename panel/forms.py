from django import forms

from assistant_telegram1.models import *

class IntentForm(forms.ModelForm):

    class Meta:
        model = Intent
        labels={
        'name':'наименование',
        'intent_type':'тип'
        }
        fields = ('name', 'intent_type')

class Story_msgForm(forms.ModelForm):

    class Meta:
        model = Story_msg
        labels={
        'msg_example':'Пример сообщения',
        'answer':'ответ'
        }
        fields = ('msg_example', 'answer')

# class Story_actionForm(forms.ModelForm):

#     class Meta:
#         model = Story_action
#         labels={
#         'msg_example':'Пример сообщения',
#         'validation_option':'Уточнение перед действием',
#         'action_name':'Название вызываемой функции',
#         'action_answer':'Ответ с переменными',
#         'transcript':"Краткий смысл функции на русском",
#         'desc':'Описание'
#         }
#         fields = ('msg_example', 'validation_option',"action_name","action_answer","transcript","desc")
