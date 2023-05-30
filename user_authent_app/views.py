



from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from user_authent_app.models import Auth
from useradmin_app.models import User
from useradmin_app.views import user_list, home2
from django.contrib import messages
from django.core.mail import send_mail


	
def login_user(request, user_id):
     user = User.objects.get(user_id=user_id)
     if user is not None:
        Auth.login(request, user)
        return redirect('user_info',user_id)



def logout(request):
    Auth.logout(request)
   
    return redirect(home2)

def password_reset(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            subject = 'Réinitialisation de mot de passe'
            message = 'Bonjour,\n\n Veuillez cliquer sur le lien ci-dessous pour réinitialiser votre mot de passe.\n\n http://localhost:8000/password-reset-confirm/{}/'.format(user.user_id) 
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, 'Veuillez vérifier votre boîte de réception pour réinitialiser votre mot de passe.')
            
        else:
            messages.error(request, 'Adresse email invalide.')
    return render(request, 'password_reset.html')

def password_reset_confirm(request, user_id):
    user = User.objects.filter(user_id=user_id).first()
    if user:
        if request.method == 'POST':
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password == confirm_password:
                user.password=password
                user.save()
                messages.success(request, 'Votre mot de passe a été réinitialisé avec succès.')
                
            else:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
        return render(request, 'password_reset_confirm.html')
    else:
        messages.error(request, 'L\'URL de réinitialisation de mot de passe est invalide.')
        return redirect('login')

