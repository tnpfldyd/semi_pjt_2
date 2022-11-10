from django import forms
from .models import Card, Comment


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["title", "content", "is_private"]
        labels = {
            "is_private": "Private",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
