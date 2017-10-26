from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from wit import Wit
import json
import requests
from assistant_telegram.models import *

client = Wit('TCLMX5YEBCRG5TO2TLW3VJCOGFOWMOJW')

@csrf_exempt
def assistant_body(chat_id,message):
    # #Получаем значение сообщения
    # resps=client.message(message)
    # #создаем list всех существующих интентов в stories
    # story_intents=[]
    # for story in Story.objects.all():
    # 	story_intents.append(story.intent)

    # print(str(chat_id) + "   get_msg:    "+str(resps))
    # resps=resps['entities']
    # msg_entities={}
    # #create dictionary with entities in message
    # for ent in resps:
    #     msg_entities[ent]=resps[ent][0]
    # print(str(chat_id) + "  msg entities:    "+str(msg_entities))

    # #if the First chat with the user
    # if not Context_chat.objects.filter( chat_id = chat_id).exists():
    #     #identify intent
    #     intent="general"
    #     if 'intent' in msg_entities:
    #         if msg_entities['intent']['confidence']>0.8:
    #             intent = msg_entities['intent']['value']
    #             logmsg=Log_msg(msg=message,intent=intent)
    #             logmsg.save()
    #     else:
    #         und_msg=Undefined_msg(msg=message)
    #         und_msg.save()
    #         intent = 'general'
    #     # if story for this intent does not exist
    #     if intent not in story_intents:
    #         und_msg=Undefined_msg(msg=message)
    #         und_msg.save()
    #         intent='general'
    #     #save new context_chat for the new user with intent
    #     new_chat = Context_chat(chat_id= chat_id, intent = intent, validated_action = False,prev_msg_from_bot=" ")
    #     new_chat.save()
    # else:
    #     current_chat=Context_chat.objects.get(chat_id = chat_id)
    #     if 'intent' in msg_entities:
    #     	#Если есть новый интент, то удаляем context и начинаем обрабатывать новый запрос
    #         if msg_entities['intent']['confidence']>0.8:
    #             intent=msg_entities['intent']['value']
    #             logmsg=Log_msg(msg=message,intent=intent)
    #             logmsg.save()
    #             current_chat=Context_chat.objects.get(chat_id=chat_id)
    #             current_chat.delete()
    #             #Если интента нет в Stories, то сохраняем его в undefined_msg, и делаем его general
    #             if intent not in story_intents:
    #                 und_msg=Undefined_msg(msg=message)
    #                 und_msg.save()
    #                 intent='general'
    #             new_chat = Context_chat(chat_id= chat_id, intent = intent, validated_action = False,prev_msg_from_bot=" ")
    #             new_chat.save()

    # #Подтверждения нужны, чтобы не прошли ненужные запросы
    # if "confirmation" in msg_entities:
    # 	#Если нет, запускается интент cancel
    #     if msg_entities['confirmation']['value']=="Нет":
    #         current_chat=Context_chat.objects.get(chat_id=chat_id)
    #         current_chat.validated_action=False
    #         current_chat.intent='cancel'
    #         current_chat.save()
    #     else:
    #         if msg_entities['confirmation']['value']=="Да":
    #             current_chat=Context_chat.objects.get(chat_id=chat_id)
    #             current_chat.validated_action=True
    #             current_chat.save()

    # current_chat=Context_chat.objects.get(chat_id=chat_id)

    # #if there was a question from bot for particular entity:
    # if not current_chat.prev_msg_from_bot==" ":
    #     #addition of prev_msg_from_bot to entire msg
    #     message=current_chat.prev_msg_from_bot+" " + message
    #     print("message with prev_msg_from_bot: " + str(message))
    #     resps=client.message(message)
    #     print(str(chat_id) + "   get_new_msg_with_prev_bot_msg:    "+str(resps))
    #     resps=resps['entities']
    #     msg_entities={}
    #     #create dictionary with entities in new message with prev_msg_from_bot
    #     for ent in resps:
    #         msg_entities[ent]=resps[ent][0]
    #     print(str(chat_id) + "  new msg entities with prev_msg_from_bot:    "+str(msg_entities))


    # current_chat=Context_chat.objects.get(chat_id=chat_id)
    # current_story=Story.objects.get(intent=current_chat.intent)
    # necessary_story_entities=[]
    # for story_ent in current_story.story_entity_set.all():
    # 	if story_ent.name!=" ":
    #     	necessary_story_entities.append(story_ent.name)
    # print(str(chat_id) + "   necessary entities for story: "+str(necessary_story_entities))
    # #add entities to the context
    # for entity in msg_entities.keys():
    #     if 'intent' not in entity and msg_entities[entity]['confidence']>0.65:
    #         #add only entities required for story
    #         if entity in necessary_story_entities:
    #             #if entity in new msg already exist, rewrite entity
    #                 if Entity.objects.filter(chat=current_chat,name=entity).exists():
    #                     current_entity=Entity.objects.get(chat=current_chat,name=entity)
    #                     current_entity.value=msg_entities[entity]['value']
    #                     current_entity.save()
    #                 else:
    #                     #save new entities in context
    #                     new_entity = Entity(name=entity, chat=current_chat, value = msg_entities[entity]['value'],confidence=msg_entities[entity]['confidence'])
    #                     new_entity.save()

    # print("current_chat:   " + str(current_chat))
    # #create dictionary context with saved entities and its values
    # context_entities_list={}
    # for entity in current_chat.entity_set.all():
    #     context_entities_list[entity.name]=entity.value


    # print(str(chat_id) + "  context:     " + str(context_entities_list))
    # #if all required entities are in context, run actions or send msg
    # if all(ent in context_entities_list for ent in necessary_story_entities):
    #     current_chat=Context_chat.objects.get(chat_id=chat_id)
    #     command=Story.objects.get(intent=current_chat.intent)
    #     if command.story_type==Story.msg:
    #         print(command.message)
    #         current_chat.delete()
    #         return {"text":command.message}
    #     else:
    #         if command.story_type==Story.act:
    #             #if user validated request
    #             if current_chat.validated_action==True and command.validation_option:
    #                 current_chat=Context_chat.objects.get(chat_id=chat_id)
    #                 entities ={}
    #                 for entity in current_chat.entity_set.all():
    #                     entities[entity.name]=entity.value
    #                 current_chat.delete()
    #                 return {"action": command.action_name,"answer":command.answer,"entities":entities}
    #             else:
    #                 #if user has not validated request yet
    #                 if current_chat.validated_action==False and command.validation_option:
    #                     #create context entities list with entity values for parameters
    #                     context_entities_list=[]
    #                     for entity in current_chat.entity_set.all():
    #                         context_entities_list.append(entity.value)
    #                     parameters=', '.join(''.join(v) for v in context_entities_list)
    #                     print(parameters)
    #                     answer="Вы хотите " + command.name+" с параметрами " + parameters+"? Скажите да для подтверждения или нет для отмены запроса."
    #                     current_chat.prev_msg_from_bot=" "
    #                     current_chat.save()
    #                     return {"text": answer}
    #         else:
    #             #In case of an apocalypse
    #             print("Команды не найдено")
    #             current_chat.delete()
    #             return {"text": "Команды не найдено"}
                
    # else:
    #     #if something is missing
    #     for ent in necessary_story_entities:
    #         if ent not in context_entities_list:
    #             #send question of missing entity
    #             current_chat=Context_chat.objects.get(chat_id=chat_id)
    #             current_story=Story.objects.get(intent=current_chat.intent)
    #             entity_question=Story_entity.objects.get(intent=current_story,name=ent).question
    #             print(entity_question)
    #             current_chat.prev_msg_from_bot=entity_question
    #             current_chat.save()
    #             print("current_chat in the end "+str(current_chat))
    #             return {"text": entity_question}
    return HttpResponse(status=200)

# def story_response(request):
#     story_dict={}
#     for current_story in Story.objects.all():
#         story_dict[current_story.intent]={}
#         story_dict[current_story.intent]['entities']=[]
#         story_dict[current_story.intent]['entities'].append({})
#         story_dict[current_story.intent]['entities'].append({})
#         if current_story.story_type==current_story.msg:
#             story_dict[current_story.intent]['entities'][0]['msg']=current_story.message
#             for current_story_ent in current_story.story_entity_set.all():
#                 if current_story_ent.name!=" ":
#                     story_dict[current_story.intent]['entities'][1][current_story_ent.name]={}
#                     story_dict[current_story.intent]['entities'][1][current_story_ent.name]['value']=""
#                     story_dict[current_story.intent]['entities'][1][current_story_ent.name]['question']=current_story_ent.question
#         else:
#             if current_story.story_type==current_story.act:
#                 story_dict[current_story.intent]['entities'][0]['action']=current_story.action_name
#                 story_dict[current_story.intent]['entities'][0]['answer']=current_story.answer
#                 story_dict[current_story.intent]['entities'][0]['name']=current_story.name
#                 story_dict[current_story.intent]['entities'][0]['desc']=current_story.desc
#                 for current_story_ent in current_story.story_entity_set.all():
#                     if current_story_ent.name!=" ":
#                         story_dict[current_story.intent]['entities'][1][current_story_ent.name]={}
#                         story_dict[current_story.intent]['entities'][1][current_story_ent.name]['value']=""
#                         story_dict[current_story.intent]['entities'][1][current_story_ent.name]['question']=current_story_ent.question

#     return JsonResponse(story_dict)

# @csrf_exempt
# @require_POST
# def save_story_json(request):
#     try:
#         print(json.loads(request.body))
#         story=json.loads(request.body)
#         for intent in story:
#             if Story.objects.filter(intent=intent).exists():
#                 current_story=Story.objects.filter(intent=intent)
#                 current_story.delete() 
#             if "msg" in story[intent]['entities'][0]:
#                 message=story[intent]['entities'][0]['msg']
#                 new_story=Story(intent=intent,story_type=Story.msg,message=message)
#                 new_story.save()
#                 current_story=Story.objects.get(intent=intent)
#                 no_entity_in_story=True
#                 for entity in story[intent]['entities'][1]:
#                     question=story[intent]['entities'][1][entity]["question"]
#                     new_entity=Story_entity(intent=current_story,name=entity,question=question)
#                     new_entity.save()           
#                     no_entity_in_story=False
#                 if no_entity_in_story:
#                     new_entity=Story_entity(intent=current_story,name=" ",question=" ")
#                     new_entity.save()
#             else:
#                 if "action" in story[intent]['entities'][0]:
#                     action_name=story[intent]['entities'][0]['action']
#                     answer=story[intent]['entities'][0]['answer']
#                     name=story[intent]['entities'][0]['name']
#                     desc=story[intent]['entities'][0]['desc']
#                     validation_option=story[intent]['entities'][0]['validation_option']
#                     new_story=Story(intent=intent,story_type=Story.act,action_name=action_name,answer=answer,name=name,desc=desc,validation_option=validation_option)
#                     new_story.save()
#                     current_story=Story.objects.get(intent=intent)
#                     no_entity_in_story=True
#                     for entity in story[intent]['entities'][1]:
#                         question=story[intent]['entities'][1][entity]["question"]
#                         new_entity=Story_entity(intent=current_story,name=entity,question=question)
#                         new_entity.save()           
#                         no_entity_in_story=False
#                     if no_entity_in_story:
#                         new_entity=Story_entity(intent=current_story,name=" ",question=" ")
#                         new_entity.save()
#         return JsonResponse({"response":"Story был успешно добавлен"})
#     except:
#         return JsonResponse({"response":"Произошла ошибка"}) 

# def save_first_story(request):
#     story=requests.get("https://res.cloudinary.com/di0b74pyt/raw/upload/v1503915916/story1.json").json()
#     for intent in story:
#         if Story.objects.filter(intent=intent).exists():
#             current_story=Story.objects.filter(intent=intent)
#             current_story.delete() 
#         if "msg" in story[intent]['entities'][0]:
#             message=story[intent]['entities'][0]['msg']
#             new_story=Story(intent=intent,story_type=Story.msg,message=message)
#             new_story.save()
#             current_story=Story.objects.get(intent=intent)
#             no_entity_in_story=True
#             for entity in story[intent]['entities'][1]:
#                 question=story[intent]['entities'][1][entity]["question"]
#                 new_entity=Story_entity(intent=current_story,name=entity,question=question)
#                 new_entity.save()           
#                 no_entity_in_story=False
#             if no_entity_in_story:
#                 new_entity=Story_entity(intent=current_story,name=" ",question=" ")
#                 new_entity.save()
#         else:
#             if "action" in story[intent]['entities'][0]:
#                 action_name=story[intent]['entities'][0]['action']
#                 answer=story[intent]['entities'][0]['answer']
#                 name=story[intent]['entities'][0]['name']
#                 desc=story[intent]['entities'][0]['desc']
#                 new_story=Story(intent=intent,story_type=Story.act,action_name=action_name,answer=answer,name=name,desc=desc)
#                 new_story.save()
#                 current_story=Story.objects.get(intent=intent)
#                 no_entity_in_story=True
#                 for entity in story[intent]['entities'][1]:
#                     question=story[intent]['entities'][1][entity]["question"]
#                     new_entity=Story_entity(intent=current_story,name=entity,question=question)
#                     new_entity.save()           
#                     no_entity_in_story=False
#                 if no_entity_in_story:
#                     new_entity=Story_entity(intent=current_story,name=" ",question=" ")
#                     new_entity.save()
#     return HttpResponse(status=200)

    
# def get_undef_msgs(request):
#     undef_msgs=Undefined_msg.objects.all()
#     msgs={'msgs':[]}
#     for undef_msg in undef_msgs:
#         msgs['msgs'].append(undef_msg.msg)
#     return JsonResponse(msgs)

# def log_msgs(request):
#     log_msgs=Log_msg.objects.all()
#     msgs={'msgs':[]}
#     for log_msg in log_msgs:
#         msgs['msgs'].append({log_msgs.msg:log_msgs.intent})
#     return JsonResponse(msgs)

# def delete_story(request,intent):
#     print(intent)
#     try:
#         target_story=Story.objects.get(intent=intent)
#         print("Deleted story:"+str(target_story))
#         target_story.delete()
#         return JsonResponse({"response":"Story был успешно удален"})
#     except:
#         return JsonResponse({"response":"Произошла ошибка"})
