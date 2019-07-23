from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register_render),
    url(r'^login_post$', views.login_post),
    url(r'^register_post$', views.register_post),
    url(r'^main$', views.main),
    url(r'^logout$', views.logout),
    url(r'^(?P<movie_id>[0-9]+)/view$', views.view),
    url(r'^account$', views.account),
    url(r'^search$', views.search),
]
