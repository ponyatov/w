from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Room(models.Model):
    room = models.IntegerField(verbose_name='номер')
    floor = models.IntegerField(verbose_name='этаж', blank=True, default=2)

    class Meta:
        verbose_name = "кабинет"
        verbose_name_plural = "кабинеты"

    def __str__(self): return f'{self.room} / {self.floor}'

class Dept(models.Model):
    name = models.CharField(max_length=0x22, default='IT')
    room = models.ManyToManyField(Room)

    class Meta:
        verbose_name = "отдел"
        verbose_name_plural = "отделы"

    def __str__(self):
        return f'{self.name} @ {self.room.all().values_list("room",flat=True)}'

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='login',
                                on_delete=models.CASCADE)
    second_name = models.CharField(verbose_name='отчество',
                                   max_length=0x22, blank=True)
    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(verbose_name='дата рождения',
                                  null=True, blank=True)
    dept = models.ForeignKey(Dept, verbose_name='отдел',
                             on_delete=models.DO_NOTHING, null=True)
    room = models.ForeignKey(Room, verbose_name='комната',
                             on_delete=models.DO_NOTHING, null=True)

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return f'{self.user} / {self.user.first_name[0]}.{self.second_name[0]}.{self.user.last_name} @ {self.room}'
