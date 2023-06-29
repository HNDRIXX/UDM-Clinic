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

    path('consulted', views.consulted, name="consulted"),
    path('illness', views.illness, name="illness"),

    path('tracklogs', views.tracklogs, name="tracklogs"),

    path('test', views.test, name="test"),
]
