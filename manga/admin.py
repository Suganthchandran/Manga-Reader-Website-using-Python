from django.contrib import admin
from .models import *

# Register your models here.

class PDFFileInline(admin.TabularInline):
    model = Mangas.pdf_files.through
    extra = 1

class PDFFileAdmin(admin.ModelAdmin):
    pass

admin.site.register(PDFFile, PDFFileAdmin)

admin.site.register(Genre)
admin.site.register(Mangas)

    