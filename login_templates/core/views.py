from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import ProfileForm, UserForm

def index(request):
    return render(request, 'core.html')

def register(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        user_form = UserForm(request.POST)

        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            #needed to auto-login user after it creation
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        
    else:
        profile_form = ProfileForm()
        user_form = UserForm()
            
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'register.html', context)
