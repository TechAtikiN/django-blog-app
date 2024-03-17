from django.db import models
import uuid

def getUUID():
  id = uuid.uuid4()
  return id.hex

# Create your models here.
class Blog(models.Model):
  id = models.CharField(primary_key=True, default=getUUID, editable=False, max_length=255)
  title = models.CharField(max_length=255)
  content = models.TextField()
  user_id = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['-created_at']
    