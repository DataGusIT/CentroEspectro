from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Categoria, FAQ, Contato, Ferramenta, TipoFerramenta, CustomUser, UserDownload

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_icone')
    search_fields = ('nome',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('pergunta', 'resposta')

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'cidade', 'estado', 'avaliacao')
    list_filter = ('tipo', 'estado', 'atendimento_presencial', 'atendimento_online')
    search_fields = ('nome', 'descricao', 'cidade')

@admin.register(TipoFerramenta)
class TipoFerramentaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Ferramenta)
class FerramentaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'categoria', 'eh_gratuita', 'classificacao')
    list_filter = ('categoria', 'tipo', 'eh_gratuita')
    search_fields = ('nome', 'descricao')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin')
    fieldsets = UserAdmin.fieldsets + (
        ('Permissões Adicionais', {'fields': ('is_admin',)}),
    )
    list_filter = UserAdmin.list_filter + ('is_admin',)

@admin.register(UserDownload)
class UserDownloadAdmin(admin.ModelAdmin):
    list_display = ('user', 'ferramenta', 'data_download')
    list_filter = ('user', 'ferramenta')