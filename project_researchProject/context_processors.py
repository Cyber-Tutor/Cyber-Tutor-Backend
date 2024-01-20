from app_learningModules.models import Course

# This function allows us to pass courses to all templates, enforcing DRY
def global_course_data(request):
    courses = Course.objects.all() 
    return {'courses': courses} 
