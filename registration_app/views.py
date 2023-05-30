from django.shortcuts import redirect, render
from django.contrib import messages
from authentication_app.views import stop_video

from registration_app.forms import user_form
from useradmin_app.models import User

# Create your views here.


def register(request):  
    stop_video()
    if request.method == 'POST':  
        form = user_form(request.POST, request.FILES)  
        if form.is_valid() and form.cleaned_data['password'] != form.cleaned_data['mdp2']:  
            messages.error(request,"les mots de passes ne correspondent pas ! ")
            return render(request, 'register.html', {'form': form })

        elif form.cleaned_data['password'] == form.cleaned_data['mdp2']:
            mail=request.POST['email']
            mdp=request.POST['password']
            if User.objects.filter(email=mail,password=mdp ).exists():
                messages.error(request," Vous etes deja inscrit !")
                return render(request, 'register.html', {'form': form })
            else:
                form.save()  
                return redirect('login') 
    else:  
        form = user_form()  
  
    return render(request, 'register.html', {'form': form })  
