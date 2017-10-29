from django.views import generic
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from assistant_telegram1.models import *
from django.core.urlresolvers import reverse_lazy
from .forms import IntentForm,Story_msgForm,Story_actionForm,Story_entityForm
from handler.views import send
import re
import json,requests
# Create your views here.
class Index_intentsView(generic.ListView):
	template_name="intent/index_intents.html"
	context_object_name="all_intents"

	def get_queryset(self):
		return Intent.objects.all()

# class Detail_intentView(generic.DetailView):
def detail_intent(request,pk):
    intent=get_object_or_404(Intent,name=pk)
    if request.method == "POST":
        if intent.intent_type=="msg":
            if hasattr(intent,"story_msg"):
                form = Story_msgForm(request.POST, instance=intent.story_msg)
            else:
                form = Story_msgForm(request.POST)
            if form.is_valid():
                if hasattr(intent,"story_action"):
                    intent.story_action.delete()
                story_msg=form.save(commit=False)
                story_msg.intent=intent
                story_msg.save()
                return redirect('panel:index_intents')
        else:
            if intent.intent_type=="action":
                if hasattr(intent,"story_action"):
                    form = Story_actionForm(request.POST, instance=intent.story_action)
                else:
                    form = Story_actionForm(request.POST)
                if form.is_valid():
                    if hasattr(intent,"story_msg"):
                        intent.story_msg.delete()
                    story_action=form.save(commit=False)
                    story_action.intent=intent
                    story_action.save()
                    return redirect('panel:index_intents')
    else:
        if intent.intent_type=="msg":
            if hasattr(intent,"story_msg"):
                form = Story_msgForm(instance=intent.story_msg)
            else:
                form = Story_msgForm()
        else:
            if hasattr(intent,"story_action"):
                form = Story_actionForm(instance=intent.story_action)
            else:
                form = Story_actionForm()
        return render(request,"intent/detail_intent.html",{"intent":intent,"form":form})

def intent_new(request):
    if request.method == "POST":
        form = IntentForm(request.POST)
        updated_data = request.POST.copy()
        updated_data.update({'name': form.data['name'].lower()})
        form = IntentForm(data=updated_data)
        
        try:
            if form.is_valid():
                if not re.match("\w+", form.data['name']):
                    form = IntentForm()
                    return render(request, 'intent/intent_edit.html', {'form': form}) 
                else:
                    intent = form.save(commit=False)
                    intent.save()
                    return redirect('panel:detail_intent', pk=intent.name)
        except:
            form = IntentForm()
            return render(request, 'intent/intent_edit.html', {'form': form})
    else:
        form = IntentForm()
    return render(request, 'intent/intent_edit.html', {'form': form})

def intent_edit(request, pk):
    intent = get_object_or_404(Intent, pk=pk)
    if request.method == "POST":
        form = IntentForm(request.POST, instance=intent)
        if form.is_valid():
            intent = form.save(commit=False)
            intent.save()
            return redirect('panel:detail_intent', pk=intent.name)
    else:
        form = IntentForm(instance=intent)
    return render(request, 'intent/intent_edit.html', {'form': form})

class Index_logsView(generic.ListView):
    template_name="intent/index_logs.html"
    context_object_name="all_logs"

    def get_queryset(self):
        return Log.objects.all().order_by("-pk")

class Index_chat_idsView(generic.ListView):
    template_name="intent/index_chat_ids.html"
    context_object_name="all_chat_ids"

    def get_queryset(self):
        return Chat_id.objects.all()

def detail_chat_id(request,pk):
    chat_id = get_object_or_404(Chat_id, pk=pk)

    return render(request, 'intent/detail_chat_id.html', {'chat_id': chat_id})
def send_all(request):
    if request.method == "POST":
        text=request.POST.get("text")
        chat_ids=Chat_id.objects.all()
        for chat_id in chat_ids:
            send(chat_id.idnumber,text)
        return redirect('panel:index_intents')
    else:
        return render(request, 'intent/send_all.html',{})

def send_chat_id(request,pk):
    chat_id = get_object_or_404(Chat_id, pk=pk)
    if request.method == "POST":
        text=request.POST.get("text")
        send(chat_id.idnumber,text)
        return redirect('panel:index_intents')
    else:
        return render(request, 'intent/send_chat_id.html',{"chat_id":chat_id})

def story_entity_add(request,pk):
    intent = get_object_or_404(Intent, pk=pk)
    if request.method == "POST":
        form = Story_entityForm(request.POST)
        updated_data = request.POST.copy()
        updated_data.update({'name': form.data['name'].lower()})
        form = Story_entityForm(data=updated_data)
        if form.is_valid():
            story_entity = form.save(commit=False)
            story_entity.save()
            return redirect('panel:story_entity_add', pk=intent.name)
    else:
        form = Story_entityForm()
    return render(request, 'intent/story_entity_add.html', {'form': form})
# class IntentCreate(CreateView):
# 	model=Intent
# 	template_name='intent/intent_form.html'
# 	fields=["name"]

# class IntentUpdate(UpdateView):
# 	model=Intent
# 	template_name='intent/intent_form.html'
# 	fields=["name"]

class IntentDelete(DeleteView):
	model=Intent
	success_url=reverse_lazy('panel:index_intents')

