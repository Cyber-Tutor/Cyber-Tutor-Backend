from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/modules/', views.get_modules_for_course, name='get_modules_for_course'),
    path('courses/<int:course_id>/module/<int:module_id>/', views.module_detail, name='module_detail'),
]