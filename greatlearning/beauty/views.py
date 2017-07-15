from django.shortcuts import render
from beauty.forms import UserForm,UserProfileForm
# Create your views here.
# Django Built In's
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'beauty/index.html')

@login_required
def specialk(request):
    return render(request,'beauty/specialk.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('specialk'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'beauty/registration.html',{'registered':registered,
                                                    'user_form':user_form,
                                                    'profile_form':profile_form})

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('specialk'))

            else:
                return HttpResponse("NU &gt;:O")
        else :
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponseRedirect(reverse('loginagain'))

    else:
        return render(request,'beauty/login.html',{})

def loginagain(request):
    return render(request,'beauty/loginagain.html')
