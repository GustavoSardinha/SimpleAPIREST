from django import forms
from .models import Pessoa

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'sobrenome', 'data_nascimento']
        label = {'nome': '', 'sobrenome': '', 'data_nascimento': ''}