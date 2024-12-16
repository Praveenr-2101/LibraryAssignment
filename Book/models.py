from django.db import models

# Create your models here.

class Author(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    bio=models.TextField()

class Book(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name="books")
    isbn=models.CharField(unique=True, max_length=13)
    available_copies=models.IntegerField(default=0)
    
    
class BorrowRecord(models.Model):
    id=models.AutoField(primary_key=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="borrow_records")
    borrowed_by=models.CharField(max_length=255)
    borrowed_date=models.DateField(auto_now_add=True)
    return_date=models.DateField(blank=True, null=True)
     
    
from django.contrib.auth import signals
from rest_framework import serializers
from django.dispatch import receiver

from django.db.models.signals import post_save, pre_delete,pre_save

    
@receiver(post_save, sender=BorrowRecord)
def borrow(sender,instance,created,**kwargs):
    if created:
        book=Book.objects.get(id=instance.book.id)
        book.available_copies -= 1
        book.save()
        
        print("I have done my work")
            