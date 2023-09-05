from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
path('', views.login_view,name='login_view'),

path('TaskList', views.TaskList,name='TaskList'),
path('add_todo/', views.add_todo, name='add_todo'),

path('Dashboard', views.dashboard,name='dashboard'),


path('profile/', views.profile, name='profile'),
path('edit_profile/', views.edit_profile, name='edit_profile'),
path('edit/<int:task_id>', views.edit, name='edit'),
path('update/<int:task_id>',views.update_task, name='update_task'),
path('start_task/<int:task_id>',views.start_task,name='start_task'),
path('task_done/',views.task_done,name='task_done'),

path('disconnect/', views.signOut, name='disconnect'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)