from django import forms
# from .models import QuestionnaireResponse

class LoginForm(forms.Form):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    group = forms.ChoiceField(choices=[('A', 'Group A'), ('B', 'Group B')])

    

# class QuestionnaireForm(forms.ModelForm):
#     class Meta:
#         model = QuestionnaireResponse
#         fields = [
#             'pill_intake',
#             'burning_degree',
#             'sourness_degree',
#             'burning_degree_morning',
#             'sourness_degree_morning',
#             'aluminum_tablets',
#             'other_pills',
#             'side_effects',
#         ]
#         widgets = {
#             'pill_intake': forms.HiddenInput(),
#         }