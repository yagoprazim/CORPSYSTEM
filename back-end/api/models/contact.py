from django.db import models

class AbstractPerson(models.Model):
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=13, blank=True, null=True, unique=True)

    class Meta:
        abstract = True

class AbstractAddress(models.Model):
    cep = models.CharField(max_length=9, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True



