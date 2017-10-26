from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from wit import Wit
import json
import requests
from assistant_telegram1.models import *

client = Wit('TCLMX5YEBCRG5TO2TLW3VJCOGFOWMOJW')

@csrf_exempt
def assistant_body(chat_id,date_in_s,message):
    #Сохраняем чат id в БД
    if not Chat_id.objects.filter(idnumber=chat_id).exists():
        chat_idmodel=Chat_id(idnumber=int(chat_id))
        chat_idmodel.save()
    current_chat_id=Chat_id.objects.get(idnumber=chat_id)

    #Получаем значение сообщения
    resps=client.message(message)
    # #создаем list всех существующих интентов в stories
    story_intents=[]
    for intent in Intent.objects.all():
        story_intents.append(intent.name)

    print(str(chat_id) + "   get_msg:    "+str(resps))
    resps=resps['entities']
    msg_entities={}
    # create dictionary with entities in message
    for ent in resps:
        msg_entities[ent]=resps[ent][0]
    print(str(chat_id) + "  msg entities:    "+str(msg_entities))


    #сохраняем логи

    # #if the First chat with the user
    if not hasattr(current_chat_id,"context_chat"):
        #identify intent
        intent="undefined"
        if 'intent' in msg_entities:
            if msg_entities['intent']['confidence']>0.8:
                intent = msg_entities['intent']['value']
        # if story for this intent does not exist
        if intent not in story_intents:
            intent='undefined'
        #save new context_chat for the new user with intent
        current_intent=Intent.objects.get(name=intent)
        new_chat = Context_chat(chat_id= current_chat_id, intent = current_intent, validated_action = False,prev_msg_from_bot=" ")
        new_chat.save()
    else:
        if 'intent' in msg_entities:
            #Если есть новый интент, то удаляем context и начинаем обрабатывать новый запрос
            if msg_entities['intent']['confidence']>0.8:
                intent=msg_entities['intent']['value']
                current_chat.delete()
    #             #Если интента нет в Stories, то сохраняем его в undefined_msg, и делаем его general
                if intent not in story_intents:
                    intent='undefined'
                current_intent=Intent.objects.get(name=intent)    
                new_chat = Context_chat(chat_id= current_chat_id, intent = current_intent, validated_action = False,prev_msg_from_bot=" ")
                new_chat.save()

    current_chat=current_chat_id.context_chat
    #Подтверждения нужны, чтобы не прошли ненужные запросы
    if "confirmation" in msg_entities:
    # 	#Если нет, запускается интент cancel
        if msg_entities['confirmation']['value'].lowercase=="нет":
            if hasattr(current_chat.intent,"story_action"):
                if current_chat.intent.story_action.validation_option==True:
                    current_chat.validated_action=False
                    current_chat.intent=Intent.objects.get(name='cancel')
                    current_chat.save()      
        else:
            if msg_entities['confirmation']['value'].lowercase=="да":
                current_chat.validated_action=True
                current_chat.save()

    current_chat=current_chat_id.context_chat
    # #if there was a question from bot for particular entity:
    if not current_chat.prev_msg_from_bot==" ":
    #     #addition of prev_msg_from_bot to entire msg
        message=current_chat.prev_msg_from_bot+" " + message
        print("message with prev_msg_from_bot: " + str(message))
        resps=client.message(message)
        print(str(chat_id) + "   get_new_msg_with_prev_bot_msg:    "+str(resps))
        resps=resps['entities']
        msg_entities={}
    #     #create dictionary with entities in new message with prev_msg_from_bot
        for ent in resps:
            msg_entities[ent]=resps[ent][0]
        print(str(chat_id) + "  new msg entities with prev_msg_from_bot:    "+str(msg_entities))


    necessary_story_entities=[]
    if hasattr(current_chat.intent,"story_action"):
        current_story=current_chat.intent.story_action
        for story_ent in current_story.story_entity_set.all():
            if story_ent.name!=" ":  
                necessary_story_entities.append(story_ent.name)
        print(str(chat_id) + "   necessary entities for story: "+str(necessary_story_entities))
        #add entities to the context
        for entity in msg_entities.keys():
            if 'intent' not in entity and msg_entities[entity]['confidence']>0.65:
                #add only entities required for story
                if entity in necessary_story_entities:
                    # if entity in new msg already exist, rewrite entity
                    if Entity.objects.filter(chat=current_chat,name=entity).exists():
                        current_entity=Entity.objects.get(chat=current_chat,name=entity)
                        current_entity.value=msg_entities[entity]['value']
                        current_entity.save()
                    else:
                        # save new entities in context
                        new_entity = Entity(name=entity, chat=current_chat, value = msg_entities[entity]['value'],confidence=msg_entities[entity]['confidence'])
                        new_entity.save()




    print("current_chat:   " + str(current_chat))
    #create dictionary context with saved entities and its values
    context_entities_list={}
    for entity in current_chat.entity_set.all():
        context_entities_list[entity.name]=entity.value
    print(str(chat_id) + "  context:     " + str(context_entities_list))

    if hasattr(current_chat.intent,'story_msg'):
        answer=current_chat.intent.story_msg.answer
        print(answer)
        current_chat.delete()
        return {"text":answer}
    else:
        if hasattr(current_chat.intent,'story_action'):
            if all(ent in context_entities_list for ent in necessary_story_entities):
                if current_chat.intent.story_action.validation_option:
                    if current_chat.validated_action:
                        entities ={}
                        for entity in current_chat.entity_set.all():
                            entities[entity.name]=entity.value
                        current_chat.delete()
                        return {"action": current_chat.intent.story_action.action_name,"answer":current_chat.intent.story_action.action_answer,"entities":entities}
                    else:
                        context_entities_list=[]
                        for entity in current_chat.entity_set.all():
                            context_entities_list.append(entity.value)
                        parameters=', '.join(''.join(v) for v in context_entities_list)
                        print(parameters)
                        answer="Вы хотите " + current_chat.intent.story_action.transcript+" с параметрами " + parameters+"? Скажите да для подтверждения или нет для отмены запроса."
                        current_chat.prev_msg_from_bot=answer
                        current_chat.save()
                        return {"text": answer}
                else:
                #In case of an apocalypse
                    print("Команды не найдено")
                    current_chat.delete()
                    return {"text": "Команды не найдено"}                
            else:
        	#if something is missing
            for ent in necessary_story_entities:
                if ent not in context_entities_list:
                #send question of missing entity
                    current_story=current_chat.intent.story_action
                    entity_question=Story_entity.objects.get(intent=current_story,name=ent).question
                    print(entity_question)
                    current_chat.prev_msg_from_bot=entity_question
                    current_chat.save()
                    print("current_chat in the end "+str(current_chat))
                    return {"text": entity_question}
    return HttpResponse(status=200)