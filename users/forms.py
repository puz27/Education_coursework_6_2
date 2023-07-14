from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Form for registration user on site"""

    class Meta:
        model = User
        fields = ["email", "phone", "country", "avatar", "password1", "password2"]


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Form of user profile"""

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "phone", "country", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
