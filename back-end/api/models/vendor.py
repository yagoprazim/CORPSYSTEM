from django.db import models
from django.contrib.auth.models import User
from api.models.contact import AbstractPerson, AbstractAddress

class Vendor(AbstractPerson, AbstractAddress):
    credential_code = models.CharField(max_length=10, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_dttm = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    