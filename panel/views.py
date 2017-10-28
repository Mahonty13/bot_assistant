from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from assistant_telegram1.models import *
from django.core.urlresolvers import reverse_lazy
# Create your views here.
class Index_intentsView(generic.ListView):
	template_name="intent/index_intents.html"
	context_object_name="all_intents"

	def get_queryset(self):
		return Intent.objects.all()

class Detail_intentView(generic.DetailView):
	model=Intent
	template_name="intent/detail_intent.html"

class IntentCreate(CreateView):
	model=Intent
	template_name='intent/intent_form.html'
	fields=["name"]

class IntentUpdate(UpdateView):
	model=Intent
	template_name='intent/intent_form.html'
	fields=["name"]

class IntentDelete(DeleteView):
	model=Intent
	success_url=reverse_lazy('panel:index_intents')

# def index_intents(request):
# 	all_intents=Intent.objects.all()
# 	return render(request,"intent/index_intents.html",{"all_intents":all_intents})

# def detail_intent(request,intent_name):
# 	intent=get_object_or_404(Intent,name=intent_name)
# 	return render(request,"intent/detail_intent.html",{"intent":intent})