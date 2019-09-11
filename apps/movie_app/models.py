from django.db import models
from django.contrib import messages
import re
from datetime import datetime, date

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        onlyLetters_REGEX = re.compile("^[a-zA-Z]+$")
        email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        result = User.objects.filter(email=postData['email'])
        
        ############# FIRST NAME VALIDATIONS #############
        if len(postData['fname']) > 2:
            if not onlyLetters_REGEX.match(postData['fname']):
                errors['fname'] = 'First name should contain letters only'
        else:
            errors['fname'] = 'First name should be at least 2 characters'

        ############# LAST NAME VALIDATIONS #############
        if len(postData['lname']) > 2:
            if not onlyLetters_REGEX.match(postData['lname']):
                errors['lname'] = 'Last name should contain letters only'
        else:
            errors['lname'] = 'Last name should be at least 2 characters'

        ############# USERNAME VALIDATIONS ##############
        if len(postData['uname']) < 3:
            errors['uname'] = 'Username should be at least 2 characters'

        ############# BIRTHDAY VALIDATIONS ############# 
        if datetime.strptime(postData['bday'], '%Y-%m-%d') > datetime.today():
            errors['bday'] = "Birthday must be a valid date"
        else:
            today = date.today().year
            bday = datetime.strptime(postData['bday'], '%Y-%m-%d').year
            if (today-bday) < 13:
                errors['bday'] = "Must be at least 13 years old to be eligible to register"
        ############# EMAIL VALIDATIONS #############
        if len(postData['email']) > 2:
            if not email_REGEX.match(postData['email']):
                errors['email'] = 'Please enter a valid email'
            else:
                if len(result) > 0:
                    errors['email'] = 'This email is already registered'
        else:
            errors['email'] = 'Email should be at least 2 characters'

        ############# PASSWORD VALIDATIONS #############
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        ############# CONFIRM PASSWORD VALIDATIONS #############
        if postData['password'] != postData['confpw']:
            errors['confpw'] = 'Password does not match'

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Like(models.Model):
    movie_id = models.IntegerField()
    users_who_like = models.ManyToManyField(User, related_name="my_movies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    created_by = models.ForeignKey(User, related_name="my_reviews",on_delete=models.PROTECT)
    movie_id = models.IntegerField()
    movie_title = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Follow(models.Model):
    followed_by = models.ForeignKey(User, related_name="my_followers", on_delete=models.PROTECT)       
    user_followed = models.ForeignKey(User, related_name="users_followed", on_delete=models.PROTECT)       
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
