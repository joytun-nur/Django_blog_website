from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from .decorators import not_logged_in_required  

from django.views.decorators.cache import never_cache
from .models import user

from .forms import (
    UserRegistrationForm,
    LoginForm,
    UserProfileUpdateForm,
    ProfilePictureUpdateForm,
)


@never_cache 
@not_logged_in_required
def login_user(request):
    form = LoginForm()

    if request.method == "POST":
       form = LoginForm(request.POST)
       if form.is_valid():
           user = authenticate(
               username = form.cleaned_data.get('username'),
               password = form.cleaned_data.get('password')
           )
           if user:
               login(request, user)
               return redirect('home')
           else:
               messages.warning(request, "Wrong credentials")

    context = {
        "form": form
    }
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@never_cache
@not_logged_in_required
def register_user(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "Registraton Successfull ")
            return redirect('login')

    context = {
        "form" : form
    }

    return render(request, 'registration.html',context)


@login_required
def change_profile_picture(request):
   
    if request.method == "POST":
        
        form = ProfilePictureUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            # user = get_object_or_404(user , pk=request.user.pk)
            loggedin_user = get_object_or_404(user, pk=request.user.pk)
            image = request.FILES['profile_image']
            
            if request.user.pk != loggedin_user.pk:
                return redirect('home')

            loggedin_user.profile_image = image
            loggedin_user.save()
            messages.success(request, "Profile image updated successfully")

        else:
            print(form.errors)

    return redirect('profile')


@login_required(login_url='login')
def profile(request):
    account = get_object_or_404(user, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=account)
    
    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('home')
        
        form = UserProfileUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated sucessfully")
            return redirect('profile')
        else:
            print(form.errors)

    context = {
        "account": account,
        "form": form
    }
    return render(request, 'profile.html', context)

