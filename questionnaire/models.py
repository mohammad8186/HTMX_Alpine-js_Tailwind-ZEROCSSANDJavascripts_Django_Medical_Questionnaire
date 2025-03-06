import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator



class Patient(AbstractUser):
    patient_id = models.UUIDField(primary_key=True , editable=False, default = uuid.uuid4,)
    count_days = models.PositiveIntegerField(
        null=False,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(56)
        ]
    )
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    group = models.CharField(max_length=1, choices=[('A', 'Group A'), ('B', 'Group B')])
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname} - Group {self.group}"


class QuestionnaireResponse(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    already_completed = models.BooleanField(null=True , default=False , blank=True)

    
    pill_after_breakfast = models.BooleanField(default=False)
    pill_after_lunch = models.BooleanField(default=False)
    pill_after_dinner = models.BooleanField(default=False)
    pill_at_bedtime = models.BooleanField(default=False)
    pill_before_breakfast = models.BooleanField(default=False)
    pill_before_dinner = models.BooleanField(default=False)

    
    burning_degree = models.IntegerField(null=True, blank=True) 
    sourness_degree = models.IntegerField(null=True, blank=True)  
    burning_degree_morning = models.IntegerField(null=True, blank=True) 
    sourness_degree_morning  = models.IntegerField(null=True, blank=True)  
     
    aluminum_tablets = models.IntegerField(null=True, blank=True)
    other_pills = models.TextField(null=True, blank=True)
    side_effects = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('patient', 'date')

    def __str__(self):
        return f"Response from {self.patient.name} on {self.date}"