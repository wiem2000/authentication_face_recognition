from django.shortcuts import redirect, render
from authentication_app.views import stop_video
from registration_app.forms import user_form_without_mdp
from django.contrib import messages

from user_authent_app.models import Auth
from .models import User

def user_list(request):
    stop_video()
    list_users=User.objects.all()
    authenticated=Auth.is_authenticated(request)

    context={"users":list_users,"authenticated":authenticated}
    return render (request,"users_list.html",context)

def home2(request):
    stop_video()
    
    authenticated=Auth.is_authenticated(request)

    context={"authenticated":authenticated}
    return render (request,"home.html",context)


def user_info(request,user_id):

    stop_video()
    authenticated=Auth.is_authenticated(request)
    user_id=authenticated.user_id
    
    user=User.objects.get(user_id=user_id)
    
    

    context={"user":user,"authenticated":authenticated}
    return render(request,'profile_info.html',context)


def update_user(request,pk):  

    authenticated=Auth.is_authenticated(request)

    user=User.objects.get(user_id=pk)
    form = user_form_without_mdp(instance=user)


    if request.method == 'POST':
        form = user_form_without_mdp(request.POST, request.FILES , instance=user)    

        
        if form.is_valid():  
            form.save()  

            if(user==authenticated):
                return redirect('user_info',pk) 
            else:
                return redirect('user_list')

  
    return render(request,'update_user.html', {'form': form ,'authenticated':authenticated}) 


def update_mdp(request):

    user=Auth.is_authenticated(request)
   
    if request.method == "POST":
        mdp_anc=request.POST['recent_mdp']
        mdp1=request.POST['mdp1']
        mdp2=request.POST['mdp2']

        if user.password == mdp_anc:
            
            if mdp1 == mdp2:
                user.password=mdp1
                user.save()
                return redirect('user_info',user.user_id)
            else:
                messages.error(request," les mots de passes ne correspondent pas ! ")
                return render(request, 'update_mdp.html', {'authenticated':user})
            
         
        else:
            messages.error(request," l'ancien mot de passe est invalide  ! ")
            return render(request, 'update_mdp.html', {'authenticated':user})


    return render(request, 'update_mdp.html', {'authenticated':user})  


def delete_user(request,pk):
    user=User.objects.get(user_id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
   
    return render(request, 'user_confirm_delete.html', {'deleted':user,'authenticated':Auth.is_authenticated(request)}) 

