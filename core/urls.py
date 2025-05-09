# core/urls.py (atualização do arquivo existente)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ferramentas/', views.ferramentas, name='ferramentas'),
    path('ferramentas/detalhes/<int:id>/', views.detalhes_ferramenta, name='detalhes_ferramenta'),    
    path('duvidas/', views.duvidas, name='duvidas'),
    path('contatos/', views.contatos, name='contatos'),
    path('contatos/<int:id>/', views.detalhes_contato, name='detalhes_contato'),
    path('sobre/', views.sobre, name='sobre'),
    path('privacy/', views.privacy, name='privacy'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('pesquisar-faqs/', views.pesquisar_faqs, name='pesquisar_faqs'),
    
    # Rotas de autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.register_view, name='register'),
    path('perfil/', views.profile_view, name='profile'),
    path('ferramenta/<int:ferramenta_id>/download/', views.register_download, name='register_download'),

    path('documentos/', views.document_list, name='document_list'),
    
    # Rotas de administração
    path('administracao/', views.admin_dashboard, name='admin_dashboard'),
    
    # CRUD Categorias
    path('administracao/categorias/', views.admin_categorias, name='admin_categorias'),
    path('administracao/categorias/criar/', views.admin_categoria_criar, name='admin_categoria_criar'),
    path('administracao/categorias/editar/<int:id>/', views.admin_categoria_editar, name='admin_categoria_editar'),
    path('administracao/categorias/excluir/<int:id>/', views.admin_categoria_excluir, name='admin_categoria_excluir'),
    
    # CRUD FAQs
    path('administracao/faqs/', views.admin_faqs, name='admin_faqs'),
    path('administracao/faqs/criar/', views.admin_faq_criar, name='admin_faq_criar'),
    path('administracao/faqs/editar/<int:id>/', views.admin_faq_editar, name='admin_faq_editar'),
    path('administracao/faqs/excluir/<int:id>/', views.admin_faq_excluir, name='admin_faq_excluir'),
    
    # Adicione rotas para Contatos e Ferramentas de maneira similar
]