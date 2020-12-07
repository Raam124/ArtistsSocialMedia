from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from account.forms import RegistrationForm, LoginForm, AccountUpdateForm, ProfileEditForm
from django.contrib import messages
from images.models import Pictures
from account.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


def registration_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            new_user.save()
            Profile.objects.create(user=new_user)
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            messages.success(request,"Welcome to Drawild now it's time to be wild")
            return redirect(reverse('home'))
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    messages.success(request,"Welcome to Drawild now it's time to be wild")
    return redirect(reverse('home'))


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request,"Loggeed in Successfully.... U+1F609 ")
                return redirect(reverse('home'))

        else:
            messages.error(request, 'Username or Password incorrect')
            return redirect(reverse('login'))
    else:
        form = LoginForm()

    context['login_form'] = form
    return render(request, "account/login.html", context)

@login_required(login_url='must_authenticate')
def account_view(request):

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(
            request.POST, instance=request.user.profile, files=request.FILES or None)
        if form.is_valid() and profile_form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],

            }
            profile_form.initial = {
                "date_of_birth": request.POST['date_of_birth'],
                "profile_photo": request.POST.get('profile_photo'),
                "seld_description": request.POST['seld_description'],
            }
            form.save()
            profile_form.save()
            messages.success(request,'Account Updated Succesfully')
            return redirect(reverse('profile'))
    else:

        form = AccountUpdateForm(

            initial={
                "email": request.user.email,
                "username": request.user.username,

            }
        )
        profile_form = ProfileEditForm(

            initial={
                "date_of_birth": request.user.profile.date_of_birth,
                "profile_photo": request.user.profile.profile_photo,
                "seld_description": request.user.profile.seld_description,

            }
        )

    context = {
        'account_form': form,
        'profile_form': profile_form,

    }

    images = Pictures.objects.filter(author=request.user)
    context["images"] = images

    return render(request, "account/account.html", context)

@login_required(login_url='must_authenticate')
def profile_view(request):

    context = {}

    images = Pictures.objects.filter(author=request.user)
    context["images"] = images

    images_count = Pictures.objects.filter(author = request.user).count()
    context['images_count'] = images_count

    total_likes_user_got = []
    for image in images:
        total_likes_user_got.append(image.users_like.count()*10)

    karma = sum(total_likes_user_got) 
    context["karma"] = karma
   
    
    return render(request,'account/profile.html',context)
    

@login_required(login_url='must_authenticate')
def user_list(request):
    User  = get_user_model()
    users = User.objects.filter(is_active=True)
    context ={
        'users':users
    }
    return render(request,'account/users_list.html',context)

@login_required(login_url='must_authenticate')
def user_profile(request,username):
    User  = get_user_model()
    user = get_object_or_404(User,username=username)

    images_count = Pictures.objects.filter(author = user).count()
    
    images = Pictures.objects.filter(author=user)

    total_likes_user_got = []
    for image in images:
        total_likes_user_got.append(image.users_like.count()*10)

    karma = sum(total_likes_user_got) 
   
    context  = {
        'user':user,
        'images_count':images_count,
        'images':images,
        'karma':karma,
    }
    
    return render(request,'account/user_profile.html',context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})


def topContributors(request):


    top_liked_arts = Pictures.objects.all().order_by('users_like')

    context ={

        'top_liked_arts':top_liked_arts,
    }

    return render(request,'account/topcontributors.html',context)