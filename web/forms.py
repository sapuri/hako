from django import forms
from django.forms.fields import CharField

from .models import Post, Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mdl-textfield__input'})
        }


class PostForm(forms.ModelForm):
    name = CharField(
        label='名前',
        max_length=191,
        required=False,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
    )
    body = CharField(
        label='コメント内容',
        max_length=1000,
        required=True,
        help_text='Ctrl (MacOS の場合は Command) + Enter でも投稿できます。',
        widget=forms.Textarea(attrs={'class': 'mdl-textfield__input', 'cols': '50', 'rows': '5'}),
    )

    class Meta:
        model = Post
        fields = ('name', 'body')
