from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required, login_required
from wit import Wit
from pydub import AudioSegment
import json
import requests
from assistant_telegram1.views import assistant_body

# Create your views here.
token_telegram ='465116134:AAEBZ9TEMk1b2kx8uySx-GZllAcHIy5I4js'
client = Wit('OHNOVUONWOIA3NPRI2ER4CNMDBAWAJBX')

def handler_commands(data):
    if data['text'] == '/start':
        start(data['chat']['id'],"Добро пожаловать! Отправьте мне аудиозапись с Вашим вопросом, и Я постараюсь ответить на него.")
        return HttpResponse(status=200)
    if data['text'] == '/help':
        help(data['chat']['id'],"Наш бот может все")
        return HttpResponse(status=200)
    if data['text'] == '/login':
        create_session(data['chat']['id'])
        return HttpResponse(status=200)
    # if data['text'] == '/loc':
        # visit(data['chat']['id'])
        # return HttpResponse(status=200)
    #add here



    #end here
    #if command not found:
    not_found(data['chat']['id'],"Команды не найдено")
    return HttpResponse(status=200)

def start(chat_id, text):
    send_tg_message(chat_id,text)
    send_tg_voice(chat_id, text)
    return HttpResponse(status=200)
def help(chat_id, text):
    send_tg_message(chat_id,text)
    send_tg_voice(chat_id, text)
    return HttpResponse(status=200)
def not_found(chat_id, text):
    send_tg_message(chat_id,text)
    send_tg_voice(chat_id, text)
    return HttpResponse(status=200)

def send(chat_id,text):
    send_tg_message(chat_id, text)
    send_tg_voice(chat_id, text)
def send_tg_message(chat_id, text):
    r = requests.get('http://api.telegram.org/bot'+token_telegram+'/sendMessage', params={'chat_id':chat_id, 'text':text})
    return r.text
def send_tg_voice(chat_id, text):
    payload={'key':'6e796575-7aef-4cf0-a227-ad4b55370a59',
        'text': text,
        'format':"mp3",
        'speaker': "oksana"
    }
    r=requests.get('https://tts.voicetech.yandex.net/generate? ',params=payload,stream=True)
    with open("voice.mp3", "wb") as o:
        o.write(r.content)
    file1 = {'voice': open('voice.mp3', 'rb')}
    payload = {'chat_id': chat_id}
    # r = requests.post('https://api.telegram.org/bot'+token_telegram+ "/sendVoice", params=payload, files=file)
    g = requests.post('https://api.telegram.org/bot'+token_telegram+ "/sendVoice", params=payload, files=file1)




##ADD HERE##

def template_action(entities):

    #add your actions

    #create dictionary with name of variables(key) and values of variables required for your answer
    answer_vars={}
    answer_vars['variable_name']='value'
    return answer_vars


def find_nearest(entities):

    #add your actions
    payload={
    "key":"AIzaSyCXpzQv9l2oSOFyXzm5KMqDDiFFoaxLgA0",
    "address":entities['loc'],
    }
    r =json.loads(requests.get("https://maps.googleapis.com/maps/api/geocode/json",params=payload).text)
    lat=r['results'][0]["geometry"]["location"]['lat']
    lng=r['results'][0]["geometry"]["location"]['lng']
    #create dictionary with name of variables(key) and values of variables required for your answer
    answer_vars={}
    answer_vars['geo_type']=entities['geo_type']
    answer_vars['coordinates']=str(lat)+" " + str(lng)
    return answer_vars


actions_story={
"find_nearest":find_nearest
}


#пример handler-а, который будет отправлять нашему боту текст
@csrf_exempt
@require_POST
def bot_new(request):
    #в request все данные из сообщения
    data=json.loads(request.body)
    print("data      " + str(data))
    chat_id=data['message']['chat']['id']
    #text handler
    if 'text' in data['message']:
        #if commands / as start,help
        if data['message']['text'][0] == '/':
            #command handler
            handler_commands(data['message'])
            return HttpResponse(status=200)
        else:
            #текст сообщения, которое мы отправим app assistant 
            message=data['message']['text']
    else:

		# if voice message
        if 'voice' in data['message']:
            message=" "
            #Если пустое аудио, то сообщение останется пустым и не отвеченным
            if data['message']['voice']['file_size']<2500:
                return HttpResponse(status=200)
            #Находим file_path, чтобы скачать аудио
            r = json.loads(str(requests.get('http://api.telegram.org/bot'+token_telegram+'/getFile', params={'file_id':data['message']['voice']['file_id']}).text))
            #Скачиваем аудио по file_path
            g=requests.get('http://api.telegram.org/file/bot'+token_telegram+'/'+str(r['result']['file_path']), stream=True)
            print("Request from telegram audio file_path" + str(g))
            #Записываем аудио в файл voice.ogg, который хранится в главной папке django проекта
            with open("voice.ogg", "wb") as o:
                o.write(g.content)
            #convert ogg to wav
            AudioSegment.from_ogg("voice.ogg").export("voice.mp3", format="mp3")
            #recognition
            
            with open('voice.mp3', 'rb') as f:
                try:
                    resp = client.speech(f, None, {'Content-Type': 'audio/mpeg3'})
                    print('Yay, got Wit.ai response: ' + str(resp))
                    if "_text" in resp:
                        #текст сообщения, которое мы отправим app assistant 
                        message = resp['_text']
                except:
                    pass
            print(message)
            #Если не смог распознать, то меняем None на " ", чтобы не возникла ошибка
            if message==None:
                message=" "
            print(message)
    #Отправляем сообщение app assistant, app assistant отправляет нам ответ в json формате
    #структура answer {"text": "текст ответа инф вопроса"}
    #структура answer для action {"action": "name_of_function", "answer": "Ваш почтовый индекс - {post_index}","entities": entities}
    #entities - это dictionary, где key - name of entity, нужный для осуществления конкретного action, value - его value
    answer=assistant_body(chat_id,message)
    if 'text' in answer:
        send(chat_id,answer['text'])
    if "action" in answer:
        try:
            #тут вызывается action, assistant возвращает название функции, и функция вызывается через actions_story
            #answer vars это variables нужный для ответа action
            answer_vars=actions_story[answer['action']](answer['entities'])
            print("answer_vars body :" + str(answer_vars))
            #формируется готовый ответ
            answer_to_user=answer['answer'].format(**answer_vars)
            print("Answer:   " +  answer_to_user)
            send(chat_id, answer_to_user)
        except:
            send(chat_id, "Ваш запрос не удался")
            

    return HttpResponse(status=200)


def browser_api(requests,message):
    answer=assistant_body(1,message)
    if 'text' in answer:
        return HttpResponse(answer['text'])
    if 'action' in answer:
        try:
            #тут вызывается action, assistant возвращает название функции, и функция вызывается через actions_story
            #answer vars это variables нужный для ответа action
            answer_vars=actions_story[answer['action']](answer['entities'])
            print("answer_vars body :" + str(answer_vars))
            #формируется готовый ответ
            answer_to_user=answer['answer'].format(**answer_vars)
            print("Answer:   " +  answer_to_user)
            return HttpResponse(answer_to_user)
        except:
            return HttpResponse("Ваш запрос не удался")
