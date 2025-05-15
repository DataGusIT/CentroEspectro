from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CategoriaFAQ, CategoriaContato, CategoriaFerramenta, FAQ, Contato, Ferramenta, CustomUser, UserDownload

# Registros de Categorias
@admin.register(CategoriaFAQ)
class CategoriaFAQAdmin(admin.ModelAdmin):
    list_display = ('nome', 'icone')
    search_fields = ('nome',)

@admin.register(CategoriaContato)
class CategoriaContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'icone')
    search_fields = ('nome',)

@admin.register(CategoriaFerramenta)
class CategoriaFerramentaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'icone')
    search_fields = ('nome',)

# Registros de modelos principais
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('pergunta', 'resposta')

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'cidade', 'estado', 'telefone')
    list_filter = ('categoria', 'estado', 'atendimento_presencial', 'atendimento_online')
    search_fields = ('nome', 'descricao', 'cidade', 'rua', 'bairro', 'cep')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'imagem', 'categoria')
        }),
        ('Endereço', {
            'fields': ('rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep')
        }),
        ('Contato', {
            'fields': ('telefone', 'horario_funcionamento')
        }),
        ('Tipo de Atendimento', {
            'fields': ('atendimento_presencial', 'atendimento_online')
        }),
    )

@admin.register(Ferramenta)
class FerramentaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'eh_gratuita', 'classificacao', 'get_tipo_funcionalidade')
    list_filter = ('categoria', 'eh_gratuita', 'tipo')
    search_fields = ('nome', 'descricao')

    @admin.display(description='Tipo de Funcionalidade')
    def get_tipo_funcionalidade(self, obj):
        return obj.tipo.nome

# Registros de usuários e downloads
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin', 'is_staff')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('is_admin',)}),
    )
    
@admin.register(UserDownload)
class UserDownloadAdmin(admin.ModelAdmin):
    list_display = ('user', 'ferramenta', 'data_download')
    list_filter = ('data_download',)
    search_fields = ('user__username', 'ferramenta__nome')