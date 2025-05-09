from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.db.models import Q
from .models import FAQ, Categoria, Contato, Ferramenta, TipoFerramenta, CustomUser, UserDownload
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

# Função auxiliar para verificar se o usuário é admin
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.first_name}!')
                
                # Verificar se o usuário é administrador usando os atributos padrão do Django
                if user.is_staff or user.is_superuser:
                    return redirect('admin_dashboard')
                
                # Se não for admin, redireciona para a página solicitada ou para a página inicial
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu com sucesso!')
    return redirect('index')

@login_required
def profile_view(request):
    user = request.user
    downloads = UserDownload.objects.filter(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'core/auth/profile.html', {
        'form': form,
        'downloads': downloads,
        'title': 'Meu Perfil'
    })

# Rota para registrar downloads
@login_required
def register_download(request, ferramenta_id):
    if request.method == 'POST':
        ferramenta = get_object_or_404(Ferramenta, id=ferramenta_id)
        # Criar o registro de download
        download = UserDownload(user=request.user, ferramenta=ferramenta)
        download.save()
        messages.success(request, f'Download de {ferramenta.nome} registrado!')
        return redirect('detalhes_ferramenta', id=ferramenta_id)
    
    return redirect('ferramentas')

# Views para gestão de recursos (apenas para admins)
@user_passes_test(is_admin)
def admin_dashboard(request):
    categorias = Categoria.objects.all().count()
    ferramentas = Ferramenta.objects.all().count()
    contatos = Contato.objects.all().count()
    faqs = FAQ.objects.all().count()
    usuarios = CustomUser.objects.all().count()
    
    context = {
        'title': 'Dashboard Admin',
        'categorias': categorias,
        'ferramentas': ferramentas,
        'contatos': contatos,
        'faqs': faqs,
        'usuarios': usuarios
    }
    
    return render(request, 'core/admin/dashboard.html', context)

# CRUD para Categorias
@user_passes_test(is_admin)
def admin_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'core/admin/categorias.html', {
        'categorias': categorias,
        'title': 'Gestão de Categorias'
    })

@user_passes_test(is_admin)
def admin_categoria_criar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        icone = request.POST.get('icone')
        
        categoria = Categoria(nome=nome, icone=icone)
        categoria.save()
        
        messages.success(request, 'Categoria criada com sucesso!')
        return redirect('admin_categorias')
    
    return render(request, 'core/admin/categoria_form.html', {
        'title': 'Nova Categoria'
    })

@user_passes_test(is_admin)
def admin_categoria_editar(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.icone = request.POST.get('icone')
        categoria.save()
        
        messages.success(request, 'Categoria atualizada com sucesso!')
        return redirect('admin_categorias')
    
    return render(request, 'core/admin/categoria_form.html', {
        'categoria': categoria,
        'title': 'Editar Categoria'
    })

@user_passes_test(is_admin)
def admin_categoria_excluir(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('admin_categorias')
    
    return render(request, 'core/admin/confirmacao_exclusao.html', {
        'objeto': categoria,
        'tipo': 'Categoria',
        'title': 'Excluir Categoria'
    })

# CRUD para FAQ
@user_passes_test(is_admin)
def admin_faqs(request):
    faqs = FAQ.objects.all()
    return render(request, 'core/admin/faqs.html', {
        'faqs': faqs,
        'title': 'Gestão de FAQs'
    })

@user_passes_test(is_admin)
def admin_faq_criar(request):
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)
        
        faq = FAQ(pergunta=pergunta, resposta=resposta, categoria=categoria)
        faq.save()
        
        messages.success(request, 'FAQ criada com sucesso!')
        return redirect('admin_faqs')
    
    return render(request, 'core/admin/faq_form.html', {
        'categorias': categorias,
        'title': 'Nova FAQ'
    })

@user_passes_test(is_admin)
def admin_faq_editar(request, id):
    faq = get_object_or_404(FAQ, id=id)
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        faq.pergunta = request.POST.get('pergunta')
        faq.resposta = request.POST.get('resposta')
        categoria_id = request.POST.get('categoria')
        faq.categoria = get_object_or_404(Categoria, id=categoria_id)
        faq.save()
        
        messages.success(request, 'FAQ atualizada com sucesso!')
        return redirect('admin_faqs')
    
    return render(request, 'core/admin/faq_form.html', {
        'faq': faq,
        'categorias': categorias,
        'title': 'Editar FAQ'
    })

@user_passes_test(is_admin)
def admin_faq_excluir(request, id):
    faq = get_object_or_404(FAQ, id=id)
    
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'FAQ excluída com sucesso!')
        return redirect('admin_faqs')
    
    return render(request, 'core/admin/confirmacao_exclusao.html', {
        'objeto': faq,
        'tipo': 'FAQ',
        'title': 'Excluir FAQ'
    })

def document_list(request):
    # Lógica para listar documentos
    # Pode ser adaptada conforme seus modelos atuais
    return render(request, 'core/document_list.html', {'documents': []})
