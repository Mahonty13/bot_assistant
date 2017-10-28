from django.views import generic
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from assistant_telegram1.models import *
from django.core.urlresolvers import reverse_lazy
from .forms import IntentForm,Story_msgForm,Story_actionForm
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
        if form.is_valid():
            intent = form.save(commit=False)
            intent.save()
            return redirect('panel:detail_intent', pk=intent.name)
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

# def index_intents(request):
# 	all_intents=Intent.objects.all()
# 	return render(request,"intent/index_intents.html",{"all_intents":all_intents})

# def detail_intent(request,intent_name):
# 	intent=get_object_or_404(Intent,name=intent_name)
# 	return render(request,"intent/detail_intent.html",{"intent":intent})