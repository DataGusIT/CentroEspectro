from django.contrib import admin
from .models import Categoria, FAQ, Contato, Ferramenta, TipoFerramenta

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