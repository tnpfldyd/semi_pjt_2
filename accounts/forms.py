from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


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
        fields = (
            "nickname",
            "gender",
            "email",
            "profileimage",
            "introduce",
            "age_range",
        )
        widgets = {
            "age_range": forms.TimeInput(
                attrs={
                    "class": "form-range",
                    "type": "range",
                    "min": "0",
                    "max": "100",
                    "step": "1",
                    "id": "customRange3",
                    "oninput": "document.getElementById('value2').innerHTML=this.value;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)

        self.fields["nickname"].widget.attrs = {
            "class": "form-control my-3",
            "placeholder": "닉네임을 입력해주세요.",
        }

        self.fields["gender"].widget.attrs = {
            "class": "form-control my-3",
            "placeholder": "성별을 입력해주세요.",
        }

        self.fields["email"].widget.attrs = {
            "class": "form-control my-3",
            "placeholder": "이메일을 입력해주세요.",
        }

        self.fields["introduce"].widget.attrs = {
            "class": "form-control my-3",
            "placeholder": "자기소개를 입력해주세요.",
        }

        self.fields["profileimage"].widget.attrs = {
            "class": "form-control my-3",
        }
