from django.contrib.auth.models import Group
from django import forms
from django.forms import Textarea
from .models import Post, Reply
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category_link', 'title', 'text']
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class AuthUserForm(AuthenticationForm,forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_text',)
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['reply_text'].widget = Textarea(attrs = { 'rows': 5})
