from django import forms
from .models import Cadastro
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class MedicaoForm(forms.ModelForm):
    #name_medicao = forms.CharField()
    #descricao = forms.CharField(widget=forms.Textarea)
    #ption = forms.ChoiceField(choices=[('novas_Medicao','Novas medições'),('importar','Importar Medições')], widget=forms.RadioSelect())
    file_csv = forms.FileField(required=False)

    class Meta:
        model = Cadastro
        fields = ('title', 'description','file_csv',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'myfieldclass'}),
        }
