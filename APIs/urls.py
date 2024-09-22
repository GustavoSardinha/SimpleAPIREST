
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pessoas, name = 'pessoas'),
    path('pessoa/<pessoa_id>/', views.pessoa_por_id, name = 'pessoa'),
    path('criarpessoa', views.criar_pessoa, name = 'criarpessoa'),
    path('atualizarpessoa/<pessoa_id>/', views.atualiza_pessoa, name = 'atualizarpessoa'),
    path('removerpessoa/<pessoa_id>/', views.remove_pessoa, name = 'removepessoa'),
]
