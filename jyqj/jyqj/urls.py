"""jyqj URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from backend.accounts.urls import account_urls
from backend.simple.urls import simple_urls
from backend.accounts.views import index
from backend.upload.urls import upload_urls
from backend.institution.urls import institution_urls
from backend.musicballoon.urls import musicballoon_urls
from backend.teacher.urls import teacher_urls
from backend.video.urls import video_urls
from backend.score.urls import score_urls
from backend.operation_log.urls import operationlog_urls

from backend.bukaopu.urls import bkp_urls

from backend.score_optional.urls import score_optional_urls
from backend.score_enjoy.urls import score_enjoy_urls
from backend.classes.urls import class_urls
from backend.student.urls import student_urls
from backend.unit.urls import unit_urls
from backend.course.urls import course_urls
from backend.hzq_score.urls import hzq_score_urls
from backend.teacher_version.urls import teacherversion_urls
from backend.course_system.urls import course_system_urls
from backend.wechart.urls import wechart_urls



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(account_urls, namespace='accounts')),
    url(r'^simple/', include(simple_urls, namespace='simple')),
    url(r'^institution/', include(institution_urls, namespace='institution')),
    url(r'^musicballoon/', include(musicballoon_urls, namespace='musicballoon')),
    url(r'^bkp/', include(bkp_urls, namespace='bukaopu')),
    url(r'^upload/', include(upload_urls, namespace='upload')),
    url(r'^teacher/', include(teacher_urls, namespace='teacher')),
    url(r'^video/', include(video_urls, namespace='video')),
    url(r'^score/', include(score_urls, namespace='score')),
    url(r'^hzqscore/', include(hzq_score_urls, namespace='hzqscore')),
    url(r'^operationlog/', include(operationlog_urls, namespace='operationlog')),

    url(r'^score_optional/', include(score_optional_urls, namespace='score_optional')),
    url(r'^score_enjoy/', include(score_enjoy_urls, namespace='score_enjoy')),
    url(r'^class/', include(class_urls, namespace='class')),
    url(r'^student/', include(student_urls, namespace='student')),

    url(r'^unit/', include(unit_urls, namespace='unit')),
    url(r'^course/', include(course_urls, namespace='course')),
    url(r'^teacherversion/', include(teacherversion_urls, namespace='teacherversion')),
    url(r'^course_system/', include(course_system_urls, namespace='course_system')),
    url(r'^wechart/', include(wechart_urls, namespace='wechart')),
    url(r'^$', index),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
