from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ImageField(upload_to='blog_images',blank=True)
    blog = models.TextField(max_length=500)
    caption = models.CharField(max_length=100)
    
    def __str__(self):
        return self.caption[:20]