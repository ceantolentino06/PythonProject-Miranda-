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
    # url(r'^search_post$', views.search_movie),
    url(r'^my_movies$', views.my_movies),
    url(r'^(?P<movie_id>[0-9]+)/mark_watched$', views.mark_watched),
    url(r'^find_cinema$', views.find_cinema),
    url(r'^username$', views.username),
    url(r'^email$', views.email),
    url(r'^(?P<movie_id>[0-9]+)/rate_movie$', views.rate_movie),
    url(r'^rate$', views.rate),
    url(r'^search_user$', views.search_user_post),
    url(r'^(?P<user_id>[0-9]+)/user$', views.search_user_render),
    url(r'^(?P<user_id>[0-9]+)/follow$', views.follow),
    url(r'^contact_me$', views.contact_me),
    url(r'^send_email$', views.send_email),
]
