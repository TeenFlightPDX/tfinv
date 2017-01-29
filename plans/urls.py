"""Plans URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

import plans.forms
import plans.views

app_name = 'plans'
urlpatterns = [
    url(r'^$', plans.views.home, name='home'),
    url(r'^view/(?P<section_number>[0-9][0-9]?[A-Z]?)/$', plans.views.section, name='section'),
    url(r'^view/(?P<section_number>[0-9][0-9]?[A-Z]?)/(?P<page_number>[0-9][0-9]?)/(?P<step_number>[0-9][0-9]?)/$',
        plans.views.step, name='step'),
    url(r'^upload/$', plans.views.upload, name='upload'),
    url(r'^confirm/$', plans.views.confirm, name='confirm'),
    url(r'^progress/$', plans.views.progress, name='progress'),
    url(r'^view/(?P<section_number>[0-9][0-9]?[A-Z]?)/(?P<page_number>[0-9][0-9]?)/(?P<step_number>[0-9][0-9]?)/update/$',
        plans.views.update, name='update'),
]
