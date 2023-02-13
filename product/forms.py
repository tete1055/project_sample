from django import forms
from django.forms import CharField

class ProfileModifyForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id': 'profile_image',
            'style': 'display:none;',
        }),
        required=False,
    )
    name = CharField(max_length=50)
    username = CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'id': 'username',
            'pattern':'^([a-zA-Z0-9]{6,})$',
        }),
    )
    context = forms.CharField(
        max_length=160,
    )
    email = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'id': 'email',
            'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
        })
    )
    gender = forms.ChoiceField(
        choices=(
            ('男性', '男性'),
            ('女性', '女性')
        ),
        required=True,
    )