from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = (
            "username",
            "password1",
            "password2",
            "email",
        )
        model = get_user_model()


class UpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ("nickname", "gender", "email", "profileimage", "introduce")
