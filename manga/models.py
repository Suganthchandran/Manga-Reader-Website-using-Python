from django.db import models
from django.contrib.auth.models import User
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
    genre_description = models.TextField(max_length=500,null=True,blank=True)
    status = models.BooleanField(default=False,help_text="0-show , 1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self)   :
        return self.name
    
class Mangas(models.Model):
    COLOR_CHOICES = [
        ('black_and_white', 'Black and White'),
        ('color', 'Color'),
    ]
    
    ADAPTION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False, blank=False)
    japanese_name = models.CharField(max_length=250, null=False, blank=False)
    author = models.CharField(max_length=150, null=False, blank=False)
    artist = models.CharField(max_length=150, null=True, blank=True)
    released_date = models.DateField(null=True, blank=True)
    manga_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    banner_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    work_status = models.BooleanField(default=False, help_text="0-ongoing , 1-Completed")
    tot_chapters = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show , 1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-default , 1-trending")
    recommend = models.BooleanField(default=False, help_text="0-default , 1-recommend")
    color = models.CharField(max_length=15, choices=COLOR_CHOICES, default='color')  # New field
    adaption = models.CharField(max_length=3, choices=ADAPTION_CHOICES, default='no')  # New field
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_files = models.ManyToManyField('PDFFile', blank=True)

    def __str__(self):
        return self.name

class PDFFile(models.Model):
    file = models.FileField(upload_to='pdf_files/')
    chapter_number = models.IntegerField(default=0)

    def __str__(self):
        return self.file.name
    
class Library(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Mangas,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    