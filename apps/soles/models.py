from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    fav_skater = models.CharField(max_length=200,null=True,blank=True)
    fav_shoe = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    prof_pic = models.ImageField(upload_to='media',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class Post(models.Model):
    shoe_brand = models.CharField(max_length=120)
    shoe_model = models.CharField(max_length=120)
    post_pic = models.ImageField(upload_to='media',null=True,blank=True)
    purchase_link = models.TextField(null=True,blank=True)
    life_span =models.IntegerField()
    content = models.TextField()
    user_post = models.ForeignKey(User,related_name='all_user_post',on_delete=models.CASCADE)
    recommend = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)