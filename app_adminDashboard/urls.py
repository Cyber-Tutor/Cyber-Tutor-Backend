from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("admin_course_list/", views.admin_course_list, name="admin_course_list"),
    
    path("course/add/", views.add_course, name="add_course"),
    path("course/edit/<int:course_id>/", edit_course, name="edit_course"),
    path("course/delete/<int:course_id>/", delete_course, name="delete_course"),

    path("course/edit/<int:course_id>/module/add/", add_module, name="add_module"),
    path("course/edit/<int:course_id>/module/edit/<int:module_id>/", edit_module, name="edit_module"),
    path("course/edit/<int:course_id>/module/delete/<int:module_id>/", delete_module, name="delete_module"),
]
