from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Доктор"
        verbose_name_plural = "Доктора"


class Patient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    frequency = models.CharField(max_length=60)
    doctors = models.ManyToManyField(Doctor, related_name="doctor")


