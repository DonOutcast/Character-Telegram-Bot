from django.contrib import admin

from .models import (
    Doctor,
    Patient,
    Exercise
)

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Exercise)

