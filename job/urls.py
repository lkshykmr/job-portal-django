from django.urls import path

from .views import (
    home,
    job,
    job_detail,
    apply_job,
    register,
    login_view,
    logout_view,
    saved_job
)

urlpatterns = [
    path('',home,name='home'),
    
    path('job/',job,name='job'),
    
    path('job/<int:id>/',job_detail,name='job_detail'),
    
    path('job/<int:id>/apply/',apply_job,name='apply_job'),
    
    path('register/',register,name='register'),
    
    path('login/',login_view,name='login'),
    
    path('logout/',logout_view,name='logout'),

    path('job/<int:id>/save/', saved_job, name='saved_job'),
]