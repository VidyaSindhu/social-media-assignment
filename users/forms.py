from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import model_to_dict, ModelForm

from .models import User


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)