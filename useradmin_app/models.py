from django.db import models

class User(models.Model):
    user_id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email= models.EmailField(max_length=254)
    password=models.CharField(max_length=50)
    photo = models.ImageField()
    admin=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    

    class Meta:
        db_table="user"


    def __str__(self):
        return self.first_name +" " +self.last_name

