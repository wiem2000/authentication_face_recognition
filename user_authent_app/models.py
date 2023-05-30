

from useradmin_app.models import User



class Auth():



    def authenticate(request, email, password):
        
        if email and password:
                
                user = User.objects.filter(email=email,password=password).first()
                if user is not None:
                     return user
        return None
    
    def login(request,user):
         if user is not None:
              request.session['user_id'] = user.user_id
    
    def is_authenticated(request):
         
         if request.session.has_key('user_id') :
              user_id = request.session['user_id']
              user = User.objects.get(user_id=user_id)
              return user
         return None
              
    def logout(request):
         if request.session.has_key('user_id') :
              del request.session['user_id']
              
         