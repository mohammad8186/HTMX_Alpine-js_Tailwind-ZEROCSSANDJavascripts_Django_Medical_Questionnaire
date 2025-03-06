from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .models import Patient
from .forms import  LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib import messages
from .models import Patient
from django.core.exceptions import ObjectDoesNotExist
from .models import Patient, QuestionnaireResponse
from datetime import date
from django.contrib.auth import login
from django.contrib.sessions.models import Session






def home(request):
    

    if request.user.is_authenticated:
        
          return  redirect('pill_intake')
    
    request.session['current_page'] = 'home'

    return render(request, 'questionnaire/home.html')



def login_view(request):
    
    
    if request.user.is_authenticated:
        return redirect('pill_intake')
    
    if request.session.get('current_page') and request.session['current_page'] not in ['login', 'home']:
        return redirect(request.session['current_page'])
    

    request.session['current_page'] = 'login'
    
   
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            group = form.cleaned_data['group']

            
            user = authenticate(request, name=name, surname=surname, group=group)
            if user is not None:

                today = date.today()
                already_completed = QuestionnaireResponse.objects.filter(patient=user, date=today).exists()

                if already_completed:
                    return render(request, 'questionnaire/login.html', {
                        'form': form,
                        'error_message': "شما امروز پرسشنامه را تکمیل کرده‌اید. لطفاً فردا دوباره امتحان کنید."
                    })
                
                login(request, user)  
                request.session['patient_id'] = str(user.patient_id)
                QuestionnaireResponse.objects.get_or_create(
                    patient=user, date=date.today()
                )
                return redirect("pill_intake")
            else:
                return render(request, 'questionnaire/login.html', {
                    'form': form,
                    'error_message': "کاربر یافت نشد"
                })
    else:
        form = LoginForm()
    return render(request, 'questionnaire/login.html', {'form': form})
                 
        
                
             







def pill_intake_view(request):
    
    if not request.user.is_authenticated:
         return redirect("home")
    
  
    
    request.session['current_page'] = 'pill_intake'
    
    
    
    patient = get_object_or_404(Patient, patient_id=request.user.patient_id)
    response = QuestionnaireResponse.objects.filter(patient=patient, date=date.today()).first()

    if response is None:
          request.session.flush()

    group_a_options = ['قبل صبحانه', 'بعد ناهار', 'بعد شام', 'زمان خواب']
    group_b_options = ['قبل صبحانه', 'قبل شام', 'زمان خواب']
    pill_options = group_a_options if patient.group == 'A' else group_b_options
    
      
    if request.method == 'POST':
        pill_intake_data = request.POST.getlist('pill_intake[]')


    
        pill_data = {
            'قبل صبحانه': 'pill_before_breakfast',
            'بعد ناهار': 'pill_after_lunch',
            'بعد شام': 'pill_after_dinner',
            'زمان خواب': 'pill_at_bedtime',
            'قبل شام': 'pill_before_dinner',
        }


        for field in pill_data.values():
            setattr(response, field, False)
        for pill in pill_intake_data:
            setattr(response, pill_data[pill], True)
        response.save()

        
        return redirect('symptom_degrees')
    
    

   
    
    
    return render(request, 'questionnaire/pill_intake.html', {
        'patient': patient,
        'pill_options': pill_options,  
        'response': response,
        
       
    })


def symptom_degrees_view(request):

    
    if not request.user.is_authenticated:
         return redirect("home")
   
    
    request.session['current_page'] = 'symptom_degrees'

   

    response = QuestionnaireResponse.objects.filter(patient=request.user, date=date.today()).first()

    if response is None:
          request.session.flush()

    
    if request.method == "POST":
        
        burning_degree = request.POST.get('burning_degree')
        sourness_degree = request.POST.get('sourness_degree')
        burning_degree_morning  = request.POST.get('burning_degree_morning')
        sourness_degree_morning = request.POST.get('sourness_degree_morning')
        

        response.burning_degree = int(burning_degree) if burning_degree else None
        response.sourness_degree = int(sourness_degree) if sourness_degree else None
        response.burning_degree_morning = int(burning_degree_morning) if burning_degree_morning else None
        response.sourness_degree_morning = int(sourness_degree_morning) if sourness_degree_morning else None
        
        response.save()


        

    
        return redirect('tablet_info')

    return render(request, 'questionnaire/symptom_degrees.html' , {
        'numbers': range(5),
        'response': response,
       
        })




def tablet_info_view(request):
    
    if not request.user.is_authenticated:
         return redirect("home")

    if request.session.get('current_page') and request.session['current_page'] not in ['login', 'home' , 'symptom_degrees' , 'tablet_info']:
        return redirect(request.session['current_page'])
       

    request.session['current_page'] = 'tablet_info'

    response = QuestionnaireResponse.objects.filter(patient=request.user, date=date.today()).first()

    if response is None:
          request.session.flush()

    if request.method == "POST":
        
        aluminum_tablets = request.POST.get('aluminum_tablets')
        other_pills = request.POST.get('other_pills')
        side_effects = request.POST.get('side_effects')

        
        response.aluminum_tablets = int(aluminum_tablets) if aluminum_tablets else None
        response.other_pills = other_pills
        response.side_effects = side_effects
        response.save()

       
        return redirect('thank_you')

    return render(request, 'questionnaire/tablet_info.html' ,{'response': response ,})



def thank_you_view(request):
    if not request.user.is_authenticated:
        return redirect("home")
    
    request.session['current_page'] = 'thank_you'
    response = QuestionnaireResponse.objects.filter(patient=request.user, date=date.today()).first()
    response.already_completed = True
    response.save()

    render_response = render(request, 'questionnaire/thank_you.html' , )
    
    request.session.flush()

    return render_response