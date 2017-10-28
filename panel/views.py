from django.views import generic
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from assistant_telegram1.models import *
from django.core.urlresolvers import reverse_lazy
from .forms import IntentForm,Story_msgForm
# Create your views here.
class Index_intentsView(generic.ListView):
	template_name="intent/index_intents.html"
	context_object_name="all_intents"

	def get_queryset(self):
		return Intent.objects.all()

# class Detail_intentView(generic.DetailView):
def detail_intent(request,intent_name):
    intent=get_object_or_404(Intent,name=intent_name)
    # if intent.intent_type=="msg":
    form = Story_msgForm()
    return render(request,"intent/detail_intent.html",{"intent":intent,"form":form})

def intent_new(request):
    if request.method == "POST":
        form = IntentForm(request.POST)
        if form.is_valid():
            intent = form.save()
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
            intent = form.save()
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