from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ferramentas/', views.ferramentas, name='ferramentas'),
    path('duvidas/', views.duvidas, name='duvidas'),
    path('contatos/', views.contatos, name='contatos'),
    path('sobre/', views.sobre, name='sobre'),
    path('privacy/', views.privacy, name='privacy'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('pesquisar-faqs/', views.pesquisar_faqs, name='pesquisar_faqs'),
]