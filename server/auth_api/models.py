from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

def getUUID():
  id = uuid.uuid4()
  return id.hex

class User(AbstractUser):
  id = models.CharField(primary_key=True, default=getUUID, editable=False, max_length=255)
  name = models.CharField(max_length=255)
  email = models.EmailField(max_length=255, unique=True)
  password = models.CharField(max_length=255)
  username = None

  USERNAME_FIELD = 'email' # email will be used as the username field
  REQUIRED_FIELDS = [] # no other fields are required