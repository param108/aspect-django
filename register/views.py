from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import django.contrib.auth
from django.views.decorators.csrf import ensure_csrf_cookie
import random
from models import EmailVerify
__choice="abcdefghijklmnopqrstuvABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def random_string(l):
  random.seed()
  st = ""
  for i in range(l):
    st += __choice[random.randint(0,len(__choice)-1)] 
  return st

# Create your views here.
def register(request):
  if request.method == 'POST':
    username = request.POST.get('email', "")
    password = request.POST.get('password', "")
  
    if (len(username) == 0 or len(password) == 0):
      return JsonResponse({'status': 1, 'msg': "User or Password is invalid"})
 
    user = User.objects.create_user(username=username, password=password, email=username)
    # need to verify through email verification
    user.is_active = False
    user.save()
    # create the email verification stuff
    ev = EmailVerify(user=user, secret = random_string(50))
    ev.save()
    print "http://localhost/doitgym/user/verify/?code="+ev.secret+"&email="+user.username
    return JsonResponse({'status': 0})
  return JsonResponse({'status': 1,'msg': "need to post not get"})

def login(request):
  if request.method == 'POST':
    username = request.POST.get('email', "");
    password = request.POST.get('password', "")
  
    if (len(username) == 0 or len(password) == 0):
      return JsonResponse({'status': 1, 'msg': "User or Password is invalid"})
 
    user = authenticate(username=username, password=password) 
    if user: 
      if user.is_active:
        django.contrib.auth.login(request, user)
        return JsonResponse({'status':0})
      else:
        return JsonResponse({'status':1, 'msg': "User is inactive, pls contact lifeundamned@gmail.com"})
    else:
      return JsonResponse({'status':1, 'msg': "User or Password is invalid"})

@ensure_csrf_cookie
def getcsrf(request):
  return JsonResponse({'status':0})

def verify(request):
  if request.method == 'GET':
    code = request.GET.get('code',"");
    email = request.GET.get('email',"");
    if len(code) == 0 or len(email) == 0:
      return HttpResponse("Invalid");
    user = User.objects.get(username__exact=email)
    if user and user.is_active == False:
      ev = EmailVerify.objects.get(user=user)
      if ev:
        if ev.secret == code:
          user.is_active = True
          user.save()
          ev.is_verified = True
          ev.save()
          return HttpResponse("Success");
      return HttpResponse("Invalid");
    else:
      return HttpResponse("Invalid");
  return HttpResponse("Invalid");
