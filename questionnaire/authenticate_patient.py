from django.contrib.auth.backends import BaseBackend
from .models import Patient

class PatientBackend(BaseBackend):
    def authenticate(self, request, name=None, surname=None, group=None, **kwargs):
        try:
            return Patient.objects.get(name=name, surname=surname, group=group)
        except Patient.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Patient.objects.get(pk=user_id)
        except Patient.DoesNotExist:
            return None
