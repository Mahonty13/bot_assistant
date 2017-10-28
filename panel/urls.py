"""bankassistantkz1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
from . import views
app_name="panel"
urlpatterns = [
    url(r'^intents/$', views.Index_intentsView.as_view(), name="index_intents"),
    url(r'^intents/(?P<pk>.+)/$', views.Detail_intentView.as_view(), name="detail_intent"),
    url(r'^intent/add/$', views.IntentCreate.as_view(), name="intent-add"),
    url(r'^intent/(?P<pk>.+)/$', views.IntentUpdate.as_view(), name="intent-update"),
    url(r'^intents/(?P<pk>.+)/delete$', views.IntentDelete.as_view(), name="intent-delete"),
]
