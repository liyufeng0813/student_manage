from django.db import models


class Classes(models.Model):
    caption = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.caption


class Student(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=200, unique=True)
    cls = models.ForeignKey(to='Classes')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    cls = models.ManyToManyField(to='Classes')

    def __str__(self):
        return self.name


class Manager(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class Img(models.Model):
    path = models.CharField(max_length=240)
