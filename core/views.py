from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import FAQ, Categoria, Contato, Ferramenta, TipoFerramenta
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
    # Obter todas as ferramentas agrupadas por categoria
    ferramentas_comunicacao = Ferramenta.objects.filter(categoria='comunicacao')
    ferramentas_comportamentais = Ferramenta.objects.filter(categoria='comportamental')
    ferramentas_educacionais = Ferramenta.objects.filter(categoria='educacional')
    ferramentas_organizacao = Ferramenta.objects.filter(categoria='organizacao')
    ferramentas_sensoriais = Ferramenta.objects.filter(categoria='sensorial')
    ferramentas_tecnologicas = Ferramenta.objects.filter(categoria='tecnologica')
    
    context = {
        'title': 'Ferramentas',
        'ferramentas_comunicacao': ferramentas_comunicacao,
        'ferramentas_comportamentais': ferramentas_comportamentais,
        'ferramentas_educacionais': ferramentas_educacionais,
        'ferramentas_organizacao': ferramentas_organizacao,
        'ferramentas_sensoriais': ferramentas_sensoriais,
        'ferramentas_tecnologicas': ferramentas_tecnologicas,
    }
    
    return render(request, 'core/ferramentas.html', context)

def detalhes_ferramenta(request, id):
    ferramenta = Ferramenta.objects.get(id=id)
    return render(request, 'core/detalhes_ferramenta.html', {
        'title': ferramenta.nome,
        'ferramenta': ferramenta
    })

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
    # Busca todos os contatos agrupados por tipo
    contatos_clinicas = Contato.objects.filter(tipo='CLINICA')
    contatos_profissionais = Contato.objects.filter(tipo='PROFISSIONAL')
    contatos_associacoes = Contato.objects.filter(tipo='ASSOCIACAO')
    contatos_escolas = Contato.objects.filter(tipo='ESCOLA')
    contatos_apoio = Contato.objects.filter(tipo='GRUPO_APOIO')
    contatos_emergencia = Contato.objects.filter(tipo='EMERGENCIA')
    
    # Lógica para saber se está tudo vazio
    sem_contatos = not (
        contatos_clinicas.exists() or 
        contatos_profissionais.exists() or 
        contatos_associacoes.exists() or 
        contatos_escolas.exists() or 
        contatos_apoio.exists() or 
        contatos_emergencia.exists()
    )

    context = {
        'title': 'Contatos',
        'contatos_clinicas': contatos_clinicas,
        'contatos_profissionais': contatos_profissionais,
        'contatos_associacoes': contatos_associacoes,
        'contatos_escolas': contatos_escolas,
        'contatos_apoio': contatos_apoio,
        'contatos_emergencia': contatos_emergencia,
        'sem_contatos': sem_contatos,  # <--- Aqui está o que você precisa
    }
    
    return render(request, 'core/contatos.html', context)


def detalhes_contato(request, id):
    contato = Contato.objects.get(pk=id)
    return render(request, 'core/detalhes_contato.html', {'contato': contato})

def sobre(request):
    return render(request, 'core/sobre.html', {'title': 'Sobre'})

def privacy(request):
    return render(request, 'core/privacy.html', {'title': 'Privacy Policy'})