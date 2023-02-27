import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=1000)
    location = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100,db_index=True)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
            if self.slug == 'create':
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})
    
class Age_restriction(models.Model):
    restriction = models.CharField(max_length=100)
    
    def __str__(self):
        return self.restriction
    
class Event(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)
    poster = models.ImageField(upload_to="photos/%Y/%m/%d/")
    program = models.CharField(max_length=1000)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,null=True)
    location = models.ForeignKey(Location,on_delete=models.PROTECT,null=True)
    date = models.DateField()
    time = models.TimeField()
    time_create = models.DateTimeField(auto_now_add=True)
    age_restriction = models.ForeignKey(Age_restriction, on_delete=models.PROTECT,null=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("detail_event", kwargs={"event_slug": self.slug})
    
    def save(self, *args, **kwargs):
    
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
            if self.slug == 'create':
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Event'
        ordering = ['-time_create','date','name']
    
