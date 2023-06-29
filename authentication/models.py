from django.db import models

# Create your models here.
# class Person(models.Model):
#     name = models.CharField(max_length=100, null=False, blank=False)
#     age = models.IntegerField(null=False, blank=False)

#     def __str__(self):
#         return self.name
    
    # class Meta:
    #     db_table = "Persons"

    # class Meta:
    #     app_label = 'authentication'

class ConsultData(models.Model):
    consultID = models.AutoField(primary_key=True)
    patientName = models.CharField(max_length=100, null=False, blank=False)
    assistName = models.CharField(max_length=100, null=False, blank=False)
    patientRole = models.CharField(max_length=50, null=False, blank=False)
    dateConsult = models.DateField(max_length=140, default='0000-00-00', null=False)
    illness = models.CharField(max_length=50, default="Ongoing")

    def __str__(self):
        return self.patientName
    
    # class Meta:
    #     db_table = "Consult"

class Employee(models.Model):
    empID = models.AutoField(primary_key=True)
    empName = models.CharField(max_length=100, null=False, blank=False)
    empRole = models.CharField(max_length=10, null=False, blank=False)
    empPhoneNum = models.IntegerField(max_length=11, null=False, blank=False, default=0)

    def __str__(self):
        return self.empName
    
class Illness(models.Model):
    illnessID = models.AutoField(primary_key=True)
    illnessName = models.CharField(max_length=100, null=False, blank=False)
    illnessDesc = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.illnessName