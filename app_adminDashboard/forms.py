from django import forms
from django.forms import inlineformset_factory
from app_learningModules.models import Course, Module


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }


class AddModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["title", "description", "prompt"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "prompt": forms.Textarea(attrs={"class": "form-control"}),
        }


ModuleFormSet = inlineformset_factory(
    Course, Module, form=AddModuleForm, extra=0, can_delete=True
)