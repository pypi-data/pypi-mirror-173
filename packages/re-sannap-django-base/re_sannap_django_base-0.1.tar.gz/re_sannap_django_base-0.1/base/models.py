
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = 'user'
        ordering = ('-id',)


class Province(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "province"
        verbose_name_plural = "provinces"
        db_table = 'province'
        ordering = ('-id',)


class County(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE,
                                 related_name='counties', related_query_name='county')

    class Meta:
        verbose_name = "county"
        verbose_name_plural = "counties"
        db_table = 'county'
        ordering = ('-id',)


def phone_number_valid(value):
    if value[:2] == "09" and len(value) == 11:
        return value
    else:
        raise ValidationError("This file must bigen 09 !!")


class CrmProfile(models.Model):

    name = models.OneToOneField(User, related_name='crm_profiles',
                                related_query_name='crm_profile',
                                on_delete=models.CASCADE
                                )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, unique=True,
                                    validators=[]
                                    )
    class Meta:
        verbose_name = "crm_profile"
        verbose_name_plural = "crm_profiles"
        db_table = 'crm_profile'
        ordering = ('-id',)
