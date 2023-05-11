from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.forms import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Post, Comment


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'}),
                  'first_name': forms.TextInput(attrs={'class':'form-control'}),
                  'last_name': forms.TextInput(attrs={'class':'form-control'}),
                  'email': forms.TextInput(attrs={'class':'form-control'}),}


class LoginForm(AuthenticationForm):
     username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class': 'form-control'}))
     password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class': 'form-control'}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        labels = {'title':'Title', 'body': 'Body'}



from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': 'Your Name',
            'body': 'Leave a comment',
        }
