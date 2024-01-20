from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from app_learningModules.models import Course, Module
from .forms import AddCourseForm, AddModuleForm, ModuleFormSet


@login_required
def admin_course_list(request):
    if not request.user.has_perm("app_learningModules.view_course"):
        return HttpResponseForbidden()

    courses = Course.objects.all().order_by('order') 
    return render(request, "admin_course_list.html", {"courses": courses})


@login_required
@permission_required("app_learningModules.add_course", raise_exception=True)
def add_course(request):
    if request.method == "POST":
        course_form = AddCourseForm(request.POST)
        module_formset = ModuleFormSet(request.POST)

        if course_form.is_valid() and module_formset.is_valid():
            course = course_form.save()
            module_instances = module_formset.save(commit=False)
            for module_instance in module_instances:
                module_instance.course = course
                module_instance.save()
            return redirect("admin_course_list")
    else:
        course_form = AddCourseForm()
        module_formset = ModuleFormSet()

    return render(
        request,
        "course_CRUD.html",
        {"course_form": course_form, "module_formset": module_formset},
    )


@login_required
@permission_required("app_learningModules.change_course", raise_exception=True)
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        course_form = AddCourseForm(request.POST, instance=course)
        module_formset = ModuleFormSet(request.POST, queryset=course.module_set.all())

        if course_form.is_valid() and module_formset.is_valid():
            course_form.save()
            module_formset.save()
            return redirect("admin_course_list")
        else:
            print(course_form.errors, module_formset.errors)
    else:
        course_form = AddCourseForm(instance=course)
        module_formset = ModuleFormSet(queryset=course.module_set.all())

    modules = course.module_set.all().order_by('order')

    return render(
        request,
        "course_CRUD.html",
        {
            "course_form": course_form,
            "module_formset": module_formset,
            "modules": modules,
        },
    )


@login_required
@permission_required("app_learningModules.delete_course", raise_exception=True)
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        course.delete()
        return redirect("admin_course_list")
    else:
        return render(request, "course_confirm_delete.html", {"course": course})


@login_required
@permission_required("app_learningModules.add_module", raise_exception=True)
def add_module(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        module_form = AddModuleForm(request.POST)
        if module_form.is_valid():
            module = module_form.save(commit=False)
            module.course = course
            module.save()
            return redirect("edit_course", course_id)
        else:
            print(module_form.errors)
    else:
        module_form = AddModuleForm()

    return render(
        request, "module_CRUD.html", {"module_form": module_form, "course": course}
    )


@login_required
@permission_required("app_learningModules.change_module", raise_exception=True)
def edit_module(request, course_id, module_id):
    course = get_object_or_404(Course, pk=course_id)
    module = get_object_or_404(Module, pk=module_id, course=course)

    if request.method == "POST":
        module_form = AddModuleForm(request.POST, instance=module)
        if module_form.is_valid():
            module_form.save()
            return redirect("edit_course", course_id)
        else:
            print(module_form.errors)
    else:
        module_form = AddModuleForm(instance=module)

    return render(
        request,
        "module_CRUD.html",
        {"module_form": module_form, "course": course, "module": module},
    )


@login_required
@permission_required("app_learningModules.delete_module", raise_exception=True)
def delete_module(request, course_id, module_id):
    course = get_object_or_404(Course, pk=course_id)
    module = get_object_or_404(Module, pk=module_id, course=course)

    if request.method == "POST":
        module.delete()
        return redirect("edit_course", course_id)
    else:
        return render(
            request, "module_confirm_delete.html", {"module": module, "course": course}
        )
