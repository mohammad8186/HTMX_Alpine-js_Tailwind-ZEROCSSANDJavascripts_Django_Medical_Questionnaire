from django.contrib import admin
from .models import Patient , QuestionnaireResponse

class PatientDjangoAdmin(admin.ModelAdmin):
    readonly_fields = ['patient_id']
admin.site.register(Patient , PatientDjangoAdmin)
admin.site.register(QuestionnaireResponse)

