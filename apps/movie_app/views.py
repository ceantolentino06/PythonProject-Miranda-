from django.shortcuts import render, HttpResponse,redirect
import urllib, json, requests
from datetime import date, datetime
############ INDEX LOGIN RENDER PAGE #############
def index(request):
    return render(request, 'movie_app/index.html')

############ REGISTER USER RENDER ################
def register_render(request):

    return render(request, 'movie_app/register.html')

############ LOGIN-POST PROCESS FUNCTION ################
def login_post(request):

    return redirect('/main')


############ LOGIN-POST PROCESS FUNCTION ################
def register_post(request):

    return redirect('/main')

############ MAIN PAGE RENDER ###############
def main(request):

    return render(request, 'movie_app/main.html')

############ VIEW MOVIE RENDER ############
def view(request, movie_id):
    url = 'https://api.themoviedb.org/3/movie/'+ movie_id +'?api_key=5d576382955ff5829fc3844390db4427&language=en-US'
    r = requests.get(url)
    result = r.json()
    poster_BASEURL = 'https://image.tmdb.org/t/p/w500'
    context = {
        'movie': result,
        'poster': poster_BASEURL+result['poster_path'],
        'backdrop': poster_BASEURL+result['backdrop_path']
    }
    print(context['backdrop'])
    return render(request, 'movie_app/view.html', context)

############ USER ACCOUNT RENDER ############
def account(request):

    return render(request, 'movie_app/account.html')

############ SEARCH MOVIE RENDER ###########
def search(request):

    return  render(request, 'movie_app/search.html')

############ LOG OUT ############
def logout(request):

    return redirect('/')
