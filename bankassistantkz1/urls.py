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
from django.conf.urls import url
from django.contrib import admin
from assistant_telegram.views import story_response
from assistant_telegram.views import save_story_json
from assistant_telegram.views import get_undef_msgs
from assistant_telegram.views import delete_story
from assistant_telegram.views import save_first_story


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^assistant_telegram/get_story/$', story_response),
    url(r'^assistant_telegram/save_story_json/', save_story_json),
    url(r'^assistant_telegram/get_undef_msgs/', get_undef_msgs),
    url(r'^assistant_telegram/delete_story/(?P<intent>.+)/$', delete_story),
    url(r'^assistant_telegram/save_first_story/$', save_first_story),

]
