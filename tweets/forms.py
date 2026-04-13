from django import forms
from .models import Tweet, Comment


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content", "image", "video")
        widgets = {
            "content": forms.Textarea(attrs={
                "placeholder": "O que está acontecendo?",
                "rows": 3,
                "maxlength": 280,
                "class": "tweet-input",
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={
                "placeholder": "Escreva uma resposta...",
                "rows": 2,
                "maxlength": 280,
                "class": "tweet-input",
            }),
        }
