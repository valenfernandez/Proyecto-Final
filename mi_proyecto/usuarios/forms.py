from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']