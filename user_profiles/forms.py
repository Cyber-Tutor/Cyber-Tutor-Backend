# FormHelper helps simplify the rendering of forms in templates by providing a way to customize the form's layout, structure, and HTML attributes
# https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
# https://django-crispy-forms.readthedocs.io/en/latest/layouts.html
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# The following code initializes a FormHelper for a Django form, allowing customization of the form's rendering and behavior in templates.
    # class ExampleForm(forms.Form):
    #     def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self.helper = FormHelper(self)

# 'reverse_lazy' derives URLs by referring to their name, rather than their path, before the project's URLConf is loaded.
# https://docs.djangoproject.com/en/5.0/ref/urlresolvers/#reverse-lazy
from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class register_form(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('register')
        self.helper.add_input(Submit('submit', 'Register', css_class='btn btn-primary'))

class login_form(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('login')
        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-primary'))
