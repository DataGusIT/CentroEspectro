from django.contrib import admin
from .models import Categoria, FAQ

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_icone')
    search_fields = ('nome',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('pergunta', 'resposta')