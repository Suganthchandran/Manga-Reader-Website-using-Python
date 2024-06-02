from django.db import models
import datetime
import os

# Create your models here.

def getFileName(request,FileName):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_FileName = "%s%s"%(now_time,FileName)
    return os.path.join('uploads/',new_FileName)

class Genre(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    status = models.BooleanField(default=False,help_text="0-show , 1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self)   :
        return self.name
    
class Mangas(models.Model):
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
    name = models.CharField(max_length=250,null=False,blank=False)
    japanese_name = models.CharField(max_length=250,null=False,blank=False)
    author = models.CharField(max_length=150,null=False,blank=False)
    manga_image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    work_status = models.BooleanField(default=False,help_text="0-ongoing , 1-Completed")
    tot_chapters = models.IntegerField(null=False,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-show , 1-Hidden")
    trending = models.BooleanField(default=False,help_text="0-default , 1-trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self)   :
        return self.name