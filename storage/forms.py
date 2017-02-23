from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
from crispy_forms.bootstrap import TabHolder, Tab


# class UserForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = False
#         self.helper.layout = Layout(
#             TabHolder(
#                 # Tab(
#                 #     'Basic Information',
#                 #     'first_name',
#                 #     'last_name'
#                 # ),
#                 Tab(
#                     'Login',
#                     'username',
#                     'password'
#                 ),
#                 Tab(
#                     'Create Account',
#                     'email',
#                     'username',
#                     'password'
#                 ),
#             )
#         )
#
#     class Meta:
#         model = User
#         fields = "__all__"