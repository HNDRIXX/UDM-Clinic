from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.home, name="home"),
    path('base', views.base, name="base"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    
    path('profile', views.profile, name="profile"),
    path('employee', views.employee, name="employee"),
    path('consultation', views.consultation, name="consultation"),
    # path('consultation_edit', views.consultation_edit, name='consultation_edit'),
    path('consultation/<int:consult_id>', views.consultation_edit, name='consultation_edit'),


    path('create_person', views.create_person, name="create_person"),
    path('insert_consult', views.insert_consult, name="insert_consult"),
    path('consulted', views.consulted, name="consulted"),
    path('tracklogs', views.tracklogs, name="tracklogs"),
]
