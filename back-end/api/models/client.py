from django.db import models
from api.models.contact import AbstractPerson, AbstractAddress

class Client(AbstractPerson, AbstractAddress):
    registered_dttm = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


