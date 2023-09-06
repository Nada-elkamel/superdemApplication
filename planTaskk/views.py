from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from urllib import request
from django.contrib.auth import authenticate, login as auth_login,logout  
from django.urls import reverse 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password  
from planTaskk.models import UserProfile
from .forms import TodoForm
from django.utils import timezone
from .models import Todo
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import parse_qs


current_datetime = timezone.now()
emp = User.objects.filter(is_active=True)
employes = [employe.username for employe in emp]
sources = {'Mail','Appel reçu','Interne'}
natures= {'Commercial','Logistique','Point interne','Facture Client'}

# Cette fonction permet a l'utilisateur de s'authentifier
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Your account is not active. Please contact support.")
                print("User is not active.")
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
            print("Invalid login credentials.")

    return render(request, 'login.html')


#cette fonction permet a l'utilisateur de se déconnecter
@login_required(login_url='login')
def signOut(request):
    logout(request) 
    return HttpResponseRedirect(reverse('login_view'))

#fonction qui permet de lister les taches
@login_required(login_url='login')
def TaskList(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Récupérez toutes les tâches
    toDo = Todo.objects.all()
    
    # Récupérez le filtre de l'URL
    filter_option = request.GET.get('filter')
    
    # Si l'option de filtre est "tasks_for_me", filtrez les tâches pour l'utilisateur connecté
    if filter_option == 'tasks_for_me':
        toDo = toDo.filter(responsable=request.user)
    
    paginator = Paginator(toDo, 4)  # 4 tâches par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user_profile': user_profile,
        'page_obj': page_obj,
        'employes' : employes,  # Assurez-vous que cette variable est correctement définie
        'current_page' : 1,
        'filter_option': filter_option  # Ajoutez l'option de filtre au contexte
    }
    
    return render(request, 'TaskList.html', context)


#fonction qui affiche le tableau de bord 
@login_required(login_url='login')
def dashboard (request):
    user_profile = UserProfile.objects.get(user=request.user)

    # Count total tasks
    total_tasks_count = Todo.objects.count()
    
    # Count tasks with nature 'Commercial'
    commercial_tasks_count = Todo.objects.filter(nature='Commercial').count()

    # Count tasks with nature 'Logistique'
    logistic_tasks_count = Todo.objects.filter(nature='Logistique').count()
    
    # Count tasks with nature 'Point interne'
    pointinterne_tasks_count = Todo.objects.filter(nature='Point interne').count()

    # Count tasks with nature 'Facture client'
    factureclient_tasks_count = Todo.objects.filter(nature='Facture client').count()

    # Calculate the percentage of commercial tasks
    if total_tasks_count > 0:
        commercial_tasks_percentage = (commercial_tasks_count / total_tasks_count) * 100
    else:
        commercial_tasks_percentage = 0
    
    # Calculate the percentage of logistic tasks
    if total_tasks_count > 0:
        logistic_tasks_percentage = (logistic_tasks_count / total_tasks_count) * 100
    else:
        logistic_tasks_percentage = 0

    # Calculate the percentage of point interne tasks
    if total_tasks_count > 0:
        pointinterne_tasks_percentage = (pointinterne_tasks_count / total_tasks_count) * 100
    else:
        pointinterne_tasks_percentage = 0

    # Calculate the percentage of facture client tasks
    if total_tasks_count > 0:
        factureclient_tasks_percentage = (factureclient_tasks_count / total_tasks_count) * 100
    else:
        factureclient_tasks_percentage = 0


    # Calculate task counts for different sources
    tasks_count_appel = Todo.objects.filter(source='Appel reçu').count()
    tasks_count_mail = Todo.objects.filter(source='Mail').count()
    tasks_count_interne = Todo.objects.filter(source='Interne').count()


    template = loader.get_template('dashboard.html')
    context = {
        'user_profile':user_profile,
        'commercial_tasks_count': commercial_tasks_count,
        'commercial_tasks_percentage':commercial_tasks_percentage,
        'logistic_tasks_count':logistic_tasks_count,
        'logistic_tasks_percentage':logistic_tasks_percentage,
        'pointinterne_tasks_count':pointinterne_tasks_count,
        'pointinterne_tasks_percentage':pointinterne_tasks_percentage,
        'factureclient_tasks_count':factureclient_tasks_count,
        'factureclient_tasks_percentage':factureclient_tasks_percentage,
        'tasks_count_appel': tasks_count_appel,
        'tasks_count_mail': tasks_count_mail,
        'tasks_count_interne': tasks_count_interne,
        }
    return HttpResponse(template.render(context, request))

#cette fonction affiche le profil de l'utilisateur
@login_required(login_url='login')
def profile (request):
    user_profile = UserProfile.objects.get(user=request.user)
    template = loader.get_template('profile.html')
    context={
        'user_profile':user_profile
    }
    return HttpResponse (template.render(context,request))

#fonction pour modifier le profil
@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)  


    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        position = request.POST['position']
        biography = request.POST['biography']
        email = request.POST['email']
        phone = request.POST['phone']
        studies = request.POST['studies']
        image = request.FILES.get('image') 
        
        # Update user and profile fields
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
       
        
        user_profile.position = position
        user_profile.biography = biography
        user_profile.phone = phone
        user_profile.studies = studies
        
        if len(request.FILES) != 0:
           user_profile.image=request.FILES['image']
               
        user_profile.save()
        request.user.save()
        
        messages.success(request, 'Votre profil a été mis a jour avec succès .')
        return redirect('profile')  

    context = {
        'user_profile': user_profile,
        'user':user
    }
    return render(request, 'profile.html', context)

#fonction d'ajout d'une tache
@login_required(login_url='login')
def add_todo(request,current_page,filter_option):
    if request.method == 'POST':
        status = request.POST.get('status')
        current_datetime = timezone.now()
        createur = request.user.username
        responsable = request.POST.get('responsable')
        source = request.POST.get('source')
        nature = request.POST.get('nature')
        deadline = request.POST.get('deadline') 
        tache = request.POST.get('tache')
        todo = Todo(
            datecreation=current_datetime,
            status=status,
            createur = createur,
            responsable = responsable, 
            source = source,
            nature = nature,
            tache = tache,
            deadline = deadline
        )

        todo.save()
        messages.success(request, "La tâche a été ajoutée avec succès")

        return HttpResponseRedirect('/planTaskk/TaskList?page='+ str(current_page)+'&filter='+filter_option) 

#fonction qui affiche la page de l'edition
@login_required(login_url='login')
def edit(request,task_id,current_page,filter_option):
    user_profile = UserProfile.objects.get(user=request.user)
    task = Todo.objects.get( id=task_id)
    context = {
        'task' : task,
        'employes' : employes,
        'sources' : sources,
        'natures' : natures,
        'current_page' : current_page,
        'user_profile': user_profile,
        'current_page' : current_page,
        'filter_option' : filter_option

    }
    return render(request, 'edit.html',context)

#fonction qui permet de modifier une tache
@login_required(login_url='login')
def update_task(request, task_id):
    task = Todo.objects.get( id=task_id)
    if request.method == 'POST':
        # Update the task data based on the submitted form
        task.responsable = request.POST['responsable']
        task.source = request.POST['source']
        task.nature = request.POST['nature']
        task.tache = request.POST['tache']
        if task.status != 'En cours' :
            task.status = request.POST['status']
        task.save()
        messages.success(request, "La tâche a été modifiée avec succès")
        current_page = request.POST['current_page']
        filter_option = request.POST['filter_option']
        return HttpResponseRedirect('/planTaskk/TaskList?page='+ str(current_page)+'&filter='+filter_option) 
    return render(request, 'edit_task.html', {'task': task})

#fonction qui permet de marquer une tache en cours
@login_required(login_url='login')
def start_task(request,task_id,current_page,filter_option):
    task = Todo.objects.get( id=task_id)
    task.status = "En cours"
    task.save()
    messages.success(request, "La tâche est en cours d'exécution")

    
    return HttpResponseRedirect('/planTaskk/TaskList?page='+ str(current_page)+'&filter='+filter_option)  # redirige vers la page actuelle 

#fonction qui permet de marquer une tache comme terminée
@login_required(login_url='login')
def task_done(request,current_page,filter_option):
    task_id = request.POST['task_id']
    task = Todo.objects.get( id=task_id)
    task.status = "Completé"
    task.commentaire = request.POST['commentaire']
    task.save()
    messages.success(request, "La tâche terminée  ")

    return HttpResponseRedirect('/planTaskk/TaskList?page='+ str(current_page)+'&filter='+filter_option)  # redirige vers la page actuelle 

