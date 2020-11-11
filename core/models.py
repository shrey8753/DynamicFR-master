from django.db import models
from django.contrib.postgres.fields import ArrayField
import face_recognition

# Create your models here.


class Person(models.Model):
    uid = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(default='admin@gmail.com')
    pic = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ['uid']


class Station(models.Model):
    station_no = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Log(models.Model):
    log_id = models.AutoField(primary_key=True, unique=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    entry_station = models.ForeignKey(Station, related_name='entry', on_delete=models.CASCADE)
    entry_datetime = models.DateTimeField(auto_now_add=True)
    entry_image = models.ImageField(upload_to='entry/{}'.format(entry_station), null=True)

    exit_station = models.ForeignKey(Station,related_name='exit', on_delete=models.CASCADE, null=True)
    exit_datetime = models.DateTimeField(blank=True, null=True)
    exit_image = models.ImageField(upload_to='entry/{}'.format(exit_station), null=True)

    status = models.BooleanField(default=0)
    fare = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.person) + ' ' + str(self.status)