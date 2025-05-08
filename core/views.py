from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import FAQ, Categoria
from collections import defaultdict

def index(request):
    return render(request, 'core/index.html', {'title': 'Início'})

def newsletter_signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        # Aqui você pode adicionar lógica para salvar o e-mail na sua lista de newsletter
        return HttpResponse(f"Obrigado por se inscrever! Seu e-mail: {email}")
    return redirect('index')  # ou para qualquer outra página

def ferramentas(request):
    return render(request, 'core/ferramentas.html', {'title': 'Ferramentas'})

def duvidas(request):
    # Busca todas as categorias e FAQs
    categorias = Categoria.objects.all()
    faqs_por_categoria = defaultdict(list)
    
    # Verifica se há um termo de pesquisa
    termo_pesquisa = request.GET.get('termo', None)
    if termo_pesquisa:
        # Filtra FAQs pela pesquisa
        faqs = FAQ.objects.filter(
            Q(pergunta__icontains=termo_pesquisa) | 
            Q(resposta__icontains=termo_pesquisa)
        )
    else:
        # Busca todas as FAQs
        faqs = FAQ.objects.all()
    
    # Organiza FAQs por categoria
    for faq in faqs:
        faqs_por_categoria[faq.categoria.nome].append(faq)
    
    context = {
        'faqs_por_categoria': dict(faqs_por_categoria),
        'categorias': categorias,
        'termo_pesquisa': termo_pesquisa,
    }
    
    return render(request, 'core/duvidas.html', context)

def pesquisar_faqs(request):
    if request.method == 'POST':
        termo = request.POST.get('termo', '')
        # Redireciona para a mesma página com o termo como parâmetro GET
        return redirect(f'/duvidas/?termo={termo}')
    return redirect('duvidas')

def contatos(request):
    return render(request, 'core/contatos.html', {'title': 'Contatos'})

def sobre(request):
    return render(request, 'core/sobre.html', {'title': 'Sobre'})

def privacy(request):
    return render(request, 'core/privacy.html', {'title': 'Privacy Policy'})

