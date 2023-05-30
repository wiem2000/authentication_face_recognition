from django.db import models
import face_recognition
import cv2,os
import numpy as np
from django.conf import settings
import keyboard



from useradmin_app.models import User

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

known_face_encodings = []
known_face_users = []


def load_known_face_encodings():
    global known_face_encodings, known_face_users
    known_face_encodings = []
    known_face_users = []
    list_users = User.objects.all()
    for user in list_users:
        known_image = face_recognition.load_image_file(os.path.join("photo", str(user.photo)))
        face_encoding = face_recognition.face_encodings(known_image)[0]
        known_face_encodings.append(face_encoding)
        known_face_users.append(user)

def compare(unknown_image):

	unknown_photo = face_recognition.load_image_file(os.path.join("photo/temp",unknown_image))
	face_locations = face_recognition.face_locations(unknown_photo, model="cnn")
	unknown_encoding = face_recognition.face_encodings(unknown_photo,face_locations)
			
	
	matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding[0])
		
	if True in matches:
		first_match_index = matches.index(True)
		user = known_face_users[first_match_index]
		return user
		
	return None


class VideoCamera(object):
	
	
	
	def __init__(self):
		
		self.video = cv2.VideoCapture(0)
		self.photo_captured=None
		self.image=None
		self.face_detected=False
		
       

	def __del__(self):
		
		self.video.release()

	

	def get_frame(self):

		success, image = self.video.read()

		if not success:
			return None
		


		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		if (len(faces_detected)==1):
			(x, y, w, h)=faces_detected[0]
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
			#cv2.putText(image,"unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
			self.image=image
			self.face_detected=True

		else: 
			self.face_detected=False
			
			"""" commentaire
			if (keyboard.is_pressed('p') ):
				
				cv2.imwrite("photo/temp/photo.jpg", image)
				
				result=compare("photo.jpg")
				
				print(result)
				image_captured="photo.jpg"
				self.photo_captured=image_captured
             """

		frame_flip = cv2.flip(image,1)

		ret, jpeg = cv2.imencode('.jpg', frame_flip)

		return jpeg.tobytes()
	
	
	def getimage(self):
		return self.photo_captured
	
	
	def capture(self):
		
		if self.face_detected == True:
			self.photo_captured="photo.jpg"		
			cv2.imwrite("photo/temp/photo.jpg", self.image)
			self.__del__()

			return compare(self.photo_captured)
		else:
			return None




