from django.contrib import admin
# from .models import Person
from .models import ConsultData, Employee, Illness

# Register your models here.
# admin.site.register(Person)
admin.site.register(ConsultData)
admin.site.register(Employee)
admin.site.register(Illness)
