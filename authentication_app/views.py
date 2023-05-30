

import datetime
import time
from django.shortcuts import render,redirect
from django.http.response import StreamingHttpResponse


from user_authent_app.models import Auth
from .models import VideoCamera, load_known_face_encodings


from django.contrib import messages


new_camera=None

def login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

		user = Auth.authenticate(request, email,password)	
		if user is not None:
			Auth.login(request, user)
			return redirect('user_info',user.user_id)
		else:
			messages.error(request, 'Adresse email ou mot de passe incorrect.')
			render(request,"login.html")
			
	
	return render(request,"login.html")



def index(request):
	return render(request,'camera.html')


def gen(camera):
	
	while True:
		frame= camera.get_frame()	
		if frame==None:		
			return None
		
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
               
def stop_video():
	global new_camera
	if new_camera!=None:
		new_camera.__del__()
    

def video_feed(request):
	global new_camera
	new_camera=VideoCamera()
	
	response= StreamingHttpResponse(gen(new_camera),
						content_type='multipart/x-mixed-replace; boundary=frame')
	
	return response

def compare(request):

	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

		user = Auth.authenticate(request, email,password)	
		if user is not None:
			Auth.login(request, user)
			return redirect('user_info',user.user_id)
		else:
			messages.error(request, 'Adresse email ou mot de passe incorrect.')
			render(request,"login.html")

	start_time = time.time()
	load_known_face_encodings()
	user=new_camera.capture()
	end_time = time.time()
	execution_time = end_time - start_time
	formatted_time = str(datetime.timedelta(seconds=execution_time))
	print(f"Temps d'exécution : {formatted_time}")
	print(user)
	
	context={"user":user}
	return render(request,'verif_user.html',context)
