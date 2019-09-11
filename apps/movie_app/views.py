from django.shortcuts import render, HttpResponse, redirect
import urllib
import json
import requests
import geocoder
from datetime import date, datetime, timedelta
from .models import *
from django.contrib import messages
import bcrypt
import guidebox
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
guidebox.api_key = "8e6f33e2d698d80013892d271f7a711eecc9b2a6"


############ INDEX LOGIN RENDER PAGE #############

def index(request):
    if 'userid' in request.session:
        return redirect('/main')
    return render(request, 'movie_app/index.html')

############ REGISTER USER RENDER ################


def register_render(request):

    return render(request, 'movie_app/register.html')

############ LOGIN-POST PROCESS FUNCTION ################


def login_post(request):
    result = User.objects.filter(username=request.POST['username'])
    if len(result) > 0:
        if bcrypt.checkpw(request.POST['password'].encode(), result[0].password.encode()):
            request.session['userid'] = result[0].id
            request.session['fname'] = result[0].first_name
            messages.add_message(
                request, messages.INFO, 'Successfully logged in!', extra_tags='userflash')
            return redirect('/main')

    messages.add_message(request, messages.INFO,
                         'Login Failed', extra_tags="loginError")
    return redirect('/')


############ REGISTER-POST PROCESS FUNCTION ################
def register_post(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/register')
    else:
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        bday = request.POST['bday']
        hashed = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        newUser = User.objects.create(first_name=fname, last_name=lname,
                                      birthday=bday, username=uname, email=email, password=hashed.decode())
        request.session['userid'] = newUser.id
        request.session['fname'] = newUser.first_name
        messages.add_message(
            request, messages.INFO, 'User successfully created!', extra_tags="userflash")
        return redirect('/main')

############# USERNAME AJAX #############


def username(request):
    context = {
        'found': False,
        'valid': True
    }
    result = User.objects.filter(username=request.POST['uname'])
    if len(result) > 0:
        context['found'] = True
    if len(request.POST['uname']) < 3:
        context['valid'] = False
    return render(request, 'movie_app/username.html', context)

############# EMAIL AJAX #############


def email(request):
    email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    context = {
        'found': False,
        'valid': True
    }
    result = User.objects.filter(email=request.POST['email'])
    if len(result) > 0:
        context['found'] = True
    if not email_REGEX.match(request.POST['email']):
        context['valid'] = False
    return render(request, 'movie_app/email.html', context)


############ MAIN PAGE RENDER ###############
def main(request):
    if 'userid' not in request.session:
        messages.add_message(
            request, messages.INFO, 'You need to be logged in to access the next page', extra_tags="loginError")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['userid'])
        reviews = user.my_reviews.all().order_by('-created_at')[:3]
        context = {
            'reviews': reviews,
            'user': user
        }
        return render(request, 'movie_app/main.html', context)

############ VIEW MOVIE RENDER ############


def view(request, movie_id):
    url = 'https://api.themoviedb.org/3/movie/' + movie_id + \
        '?api_key=5d576382955ff5829fc3844390db4427&language=en-US'
    trailer_url = 'https://api.themoviedb.org/3/movie/' + movie_id + \
        '/videos?api_key=5d576382955ff5829fc3844390db4427&language=en-US'

    ####### movie information json ######
    r = requests.get(url)
    result = r.json()

    user = User.objects.get(id=request.session['userid'])
    is_result = user.my_movies.filter(movie_id=movie_id)
    t = requests.get(trailer_url)
    if len(t.json()['results']) < 1:
        trailer = False
    else:
        trailer = t.json()['results'][0]['key']
    poster_BASEURL = 'https://image.tmdb.org/t/p/w500'

    ######## get user reviews ########
    reviews = Review.objects.filter(movie_id=movie_id)
    total_rev = 0
    for rev in reviews.all():
        total_rev += rev.rating

    ####### if not showing get data ######
    test = guidebox.Search.movies(
        field='id', id_type='themoviedb', query=movie_id)
    if len(test) > 0:
        testing = guidebox.Movie.retrieve(id=test.id)
        test_movie = testing['purchase_web_sources']
    else:
        test_movie = []

    context = {
        'movie': result,
        'poster': poster_BASEURL+result['poster_path'],
        'backdrop': poster_BASEURL+result['backdrop_path'],
        'this_movie': is_result,
        'user': user,
        'trailer_key': trailer,
        'showtimes': showtimes(result['original_title']),
        'time_now': datetime.isoformat(datetime.now()-timedelta(hours=0.5)),
        'user_reviews': total_rev,
        'total_vote': len(reviews),
        'reviews': Review.objects.filter(movie_id=movie_id),
        'buy_links': test_movie
    }
    return render(request, 'movie_app/view.html', context)


def showtimes(search_title):
    g = geocoder.ip('me')
    title = 'https://api.internationalshowtimes.com/v4/movies?apikey=G3XX9LFx7Q7ZU8XpjqPN5FW2wTwbL4WZ&search_query=' + \
        search_title + '&search_field=original_title&fields=id,title,ratings'
    t = requests.get(title)
    if len(t.json()['movies']) < 1:
        return []
    movie_id = t.json()['movies'][0]['id']
    url = 'https://api.internationalshowtimes.com/v4/showtimes?apikey=G3XX9LFx7Q7ZU8XpjqPN5FW2wTwbL4WZ&movie_id=' + movie_id + \
        '&location={},{}&distance=13&fields=cinema_id,start_at,is_3d,booking_link&append=cinemas&cinema_fields=name,id'.format(
            g.lat, g.lng)
    r = requests.get(url)
    result = r.json()
    newShow = result
    for cinema in newShow['cinemas']:
        cinema['dates'] = []
    for el in newShow['showtimes']:
        start_at = el['start_at']
        el['convdate'] = datetime.fromisoformat(
            start_at).strftime('%B-%d-%Y (%A)')
        el['convtime'] = datetime.fromisoformat(start_at).strftime('%I:%M%p')

    for cinema in newShow['cinemas']:
        for showtime in newShow['showtimes']:
            if cinema['id'] == showtime['cinema_id']:
                if showtime['convdate'] not in cinema['dates']:
                    cinema['dates'].append(showtime['convdate'])
    return newShow

############ USER ACCOUNT RENDER ############


def account(request):
    user = User.objects.get(id=request.session['userid'])
    review_list = user.my_reviews.all().order_by('-created_at')
    paginator = Paginator(review_list, 6)  # Show 25 contacts per page

    page = request.GET.get('page')
    review = paginator.get_page(page)

    likes = user.my_movies.all().order_by('-created_at')
    result = []
    for like in likes:
        url = "https://api.themoviedb.org/3/movie/" + \
            str(like.movie_id) + \
            "?api_key=5d576382955ff5829fc3844390db4427&language=en-US"
        r = requests.get(url)
        result.append(r.json())
    context = {
        'user': user,
        'reviews': review,
        'likes': result
    }
    return render(request, 'movie_app/account.html', context)

############ SEARCH MOVIE RENDER ###########


def search(request):

    return render(request, 'movie_app/search.html')

############ MY MOVIE RENDER  #############


def my_movies(request):
    user = User.objects.get(id=request.session['userid'])
    likes = user.my_movies.all()
    result = []
    for like in likes:
        url = "https://api.themoviedb.org/3/movie/" + \
            str(like.movie_id) + \
            "?api_key=5d576382955ff5829fc3844390db4427&language=en-US"
        r = requests.get(url)
        result.append(r.json())
    context = {
        'likes': result
    }
    return render(request, 'movie_app/my_movies.html', context)

############ PROFILE RENDER ##############


def profile(request):
    return HttpResponse("test")

########### MARK WATCHED #############


def mark_watched(request, movie_id):
    movie = Like.objects.create(movie_id=movie_id)
    user = User.objects.get(id=request.session['userid'])
    user.my_movies.add(movie)
    return redirect('/'+str(movie_id)+'/view')

########### FIND CINEMA ############


def find_cinema(request):
    g = geocoder.ip('me')
    url = 'https://api.internationalshowtimes.com/v4/cinemas/?apikey=G3XX9LFx7Q7ZU8XpjqPN5FW2wTwbL4WZ&location={},{}&distance=20'.format(
        g.lat, g.lng)
    r = requests.get(url)
    result = r.json()
    context = {
        'cinemas': result['cinemas']
    }
    return render(request, 'movie_app/find_cinemas.html', context)

########### RATE MOVIE POST ############


def rate_movie(request, movie_id):

    ###### create review ######
    user = User.objects.get(id=request.session['userid'])
    rating = request.POST['star']
    comment = request.POST['comment']
    movie_title = request.POST['movie_title']
    Review.objects.create(created_by=user, movie_id=movie_id, movie_title=movie_title,
                          rating=rating, comment=comment)

    ###### mark watched #######
    movie = Like.objects.create(movie_id=movie_id)
    user = User.objects.get(id=request.session['userid'])
    user.my_movies.add(movie)

    return redirect('/'+str(movie_id)+'/view')

############ RATE MOVIE AJAX #############


def rate(request):
    context = {
        'valid': True,
    }
    if 'star' not in request.POST:
        context['valid'] = False
    return render(request, 'movie_app/rate.html', context)

############ SEARCH USER RENDER ############


def search_user_render(request, user_id):
    user = User.objects.get(id=user_id)
    logged_in_user = User.objects.get(id=request.session['userid'])
    review_list = user.my_reviews.all().order_by('-created_at')

    is_followed = False
    for n in logged_in_user.users_followed.all():
        if user == n.followed_by:
            is_followed = True
    paginator = Paginator(review_list, 6)  # Show 25 contacts per page

    page = request.GET.get('page')
    review = paginator.get_page(page)

    likes = user.my_movies.all().order_by('-created_at')
    result = []
    for like in likes:
        url = "https://api.themoviedb.org/3/movie/" + \
            str(like.movie_id) + \
            "?api_key=5d576382955ff5829fc3844390db4427&language=en-US"
        r = requests.get(url)
        result.append(r.json())

    context = {
        'user': user,
        'is_followed': is_followed,
        'reviews': review,
        'likes': result
    }
    return render(request, 'movie_app/search_user.html', context)

############ SEARCH USER POST ############


def search_user_post(request):
    user_in_session = User.objects.get(id=request.session['userid'])
    user = User.objects.get(username=request.POST['username'])
    if user.username == user_in_session.username:
        return redirect('/account')
    return redirect('/'+str(user.id)+'/user')

########### ADD FRIEND POST ###########


def follow(request, user_id):
    user = User.objects.get(id=request.session['userid'])
    friend_user = User.objects.get(id=user_id)

    Follow.objects.create(followed_by=friend_user, user_followed=user)
    return redirect('/'+str(user_id)+'/user')


########### CONTACT ME RENDER ###########
def contact_me(request):

    return render(request, 'movie_app/contact_me.html')


########## CONTACT ME POST MESSAGE ########
def send_email(request):
    if request.method == 'POST':
        name = request.POST['name']
        message = request.POST['message']
        subject = request.POST['subj']
        email = request.POST['email']
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = "%s: %s via %s"%(name, message, email)
        send_mail(subject, contact_message, from_email, to_email, fail_silently=False)
    return redirect('/contact_me')

############ LOG OUT ############


def logout(request):
    del request.session['userid']
    del request.session['fname']
    return redirect('/')
