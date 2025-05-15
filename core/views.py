from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.db.models import Q
from .models import (
    FAQ, CategoriaFAQ, CategoriaContato, CategoriaFerramenta, 
    Contato, Ferramenta, CustomUser, UserDownload
)
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
    # Obter todas as ferramentas agrupadas por categoria (usando as novas categorias)
    ferramentas_pictogramas = Ferramenta.objects.filter(categoria='pictogramas_escolares')
    ferramentas_alfabetizacao = Ferramenta.objects.filter(categoria='alfabetizacao')
    ferramentas_brinquedos = Ferramenta.objects.filter(categoria='brinquedos_brincadeiras')
    ferramentas_historias = Ferramenta.objects.filter(categoria='historias_sociais')
    ferramentas_atividades = Ferramenta.objects.filter(categoria='atividades_diversas')
    
    context = {
        'title': 'Ferramentas',
        'ferramentas_pictogramas': ferramentas_pictogramas,
        'ferramentas_alfabetizacao': ferramentas_alfabetizacao,
        'ferramentas_brinquedos': ferramentas_brinquedos,
        'ferramentas_historias': ferramentas_historias,
        'ferramentas_atividades': ferramentas_atividades,
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
    categorias = CategoriaFAQ.objects.all()
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
    # Busca todas as categorias disponíveis
    categorias = CategoriaContato.objects.all()
    
    # Cria um dicionário para armazenar contatos por categoria
    contatos_por_categoria = {}
    
    # Para cada categoria, busca os contatos correspondentes
    for categoria in categorias:
        contatos_categoria = Contato.objects.filter(categoria=categoria)
        if contatos_categoria.exists():
            contatos_por_categoria[categoria.nome] = contatos_categoria
    
    # Verifica se não há contatos cadastrados
    sem_contatos = not contatos_por_categoria
    
    context = {
        'title': 'Contatos',
        'contatos_por_categoria': contatos_por_categoria,
        'sem_contatos': sem_contatos,
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
    categorias_faq = CategoriaFAQ.objects.all().count()
    categorias_contato = CategoriaContato.objects.all().count()
    categorias_ferramenta = CategoriaFerramenta.objects.all().count()
    
    ferramentas = Ferramenta.objects.all().count()
    contatos = Contato.objects.all().count()
    faqs = FAQ.objects.all().count()
    usuarios = CustomUser.objects.all().count()
    
    context = {
        'title': 'Dashboard Admin',
        'categorias_faq': categorias_faq,
        'categorias_contato': categorias_contato,
        'categorias_ferramenta': categorias_ferramenta,
        'ferramentas': ferramentas,
        'contatos': contatos,
        'faqs': faqs,
        'usuarios': usuarios
    }
    
    return render(request, 'core/admin/dashboard.html', context)

# CRUD para Categorias FAQ
@user_passes_test(is_admin)
def admin_categorias_faq(request):
    categorias = CategoriaFAQ.objects.all()
    return render(request, 'core/admin/categorias_faq.html', {
        'categorias': categorias,
        'title': 'Gestão de Categorias FAQ'
    })

@user_passes_test(is_admin)
def admin_categoria_faq_criar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        icone = request.POST.get('icone')
        
        categoria = CategoriaFAQ(nome=nome, icone=icone)
        categoria.save()
        
        messages.success(request, 'Categoria FAQ criada com sucesso!')
        return redirect('admin_categorias_faq')
    
    return render(request, 'core/admin/categoria_form.html', {
        'title': 'Nova Categoria FAQ'
    })

@user_passes_test(is_admin)
def admin_categoria_faq_editar(request, id):
    categoria = get_object_or_404(CategoriaFAQ, id=id)
    
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.icone = request.POST.get('icone')
        categoria.save()
        
        messages.success(request, 'Categoria FAQ atualizada com sucesso!')
        return redirect('admin_categorias_faq')
    
    return render(request, 'core/admin/categoria_form.html', {
        'categoria': categoria,
        'title': 'Editar Categoria FAQ'
    })

@user_passes_test(is_admin)
def admin_categoria_faq_excluir(request, id):
    categoria = get_object_or_404(CategoriaFAQ, id=id)
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria FAQ excluída com sucesso!')
        return redirect('admin_categorias_faq')
    
    return render(request, 'core/admin/confirmacao_exclusao.html', {
        'objeto': categoria,
        'tipo': 'Categoria FAQ',
        'title': 'Excluir Categoria FAQ'
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
    categorias = CategoriaFAQ.objects.all()
    
    if request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(CategoriaFAQ, id=categoria_id)
        
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
    categorias = CategoriaFAQ.objects.all()
    
    if request.method == 'POST':
        faq.pergunta = request.POST.get('pergunta')
        faq.resposta = request.POST.get('resposta')
        categoria_id = request.POST.get('categoria')
        faq.categoria = get_object_or_404(CategoriaFAQ, id=categoria_id)
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

# Adicione estas funções ao seu arquivo views.py

# CRUD para Categorias de Contato
@user_passes_test(is_admin)
def admin_categorias_contato(request):
    categorias = CategoriaContato.objects.all()
    return render(request, 'core/admin/categorias_contato.html', {
        'categorias': categorias,
        'title': 'Gestão de Categorias de Contato'
    })

@user_passes_test(is_admin)
def admin_categoria_contato_criar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        icone = request.POST.get('icone')
        
        categoria = CategoriaContato(nome=nome, icone=icone)
        categoria.save()
        
        messages.success(request, 'Categoria de Contato criada com sucesso!')
        return redirect('admin_categorias_contato')
    
    return render(request, 'core/admin/categoria_form.html', {
        'title': 'Nova Categoria de Contato'
    })

@user_passes_test(is_admin)
def admin_categoria_contato_editar(request, id):
    categoria = get_object_or_404(CategoriaContato, id=id)
    
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.icone = request.POST.get('icone')
        categoria.save()
        
        messages.success(request, 'Categoria de Contato atualizada com sucesso!')
        return redirect('admin_categorias_contato')
    
    return render(request, 'core/admin/categoria_form.html', {
        'categoria': categoria,
        'title': 'Editar Categoria de Contato'
    })

@user_passes_test(is_admin)
def admin_categoria_contato_excluir(request, id):
    categoria = get_object_or_404(CategoriaContato, id=id)
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria de Contato excluída com sucesso!')
        return redirect('admin_categorias_contato')
    
    return render(request, 'core/admin/confirmacao_exclusao.html', {
        'objeto': categoria,
        'tipo': 'Categoria de Contato',
        'title': 'Excluir Categoria de Contato'
    })

# CRUD para Contatos
@user_passes_test(is_admin)
def admin_contatos(request):
    contatos = Contato.objects.all()
    return render(request, 'core/admin/contatos.html', {
        'contatos': contatos,
        'title': 'Gestão de Contatos'
    })

@user_passes_test(is_admin)
def admin_contato_criar(request):
    categorias = CategoriaContato.objects.all()
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        imagem_url = request.POST.get('imagem_url')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        telefone = request.POST.get('telefone')
        horario_funcionamento = request.POST.get('horario_funcionamento')
        categoria_id = request.POST.get('categoria')
        atendimento_presencial = 'atendimento_presencial' in request.POST
        atendimento_online = 'atendimento_online' in request.POST
        
        categoria = get_object_or_404(CategoriaContato, id=categoria_id) if categoria_id else None
        
        contato = Contato(
            nome=nome,
            descricao=descricao,
            imagem_url=imagem_url,
            cidade=cidade,
            estado=estado,
            telefone=telefone,
            horario_funcionamento=horario_funcionamento,
            categoria=categoria,
            atendimento_presencial=atendimento_presencial,
            atendimento_online=atendimento_online
        )
        contato.save()
        
        messages.success(request, 'Contato criado com sucesso!')
        return redirect('admin_contatos')
    
    return render(request, 'core/admin/contato_form.html', {
        'title': 'Novo Contato',
        'categorias': categorias
    })

@user_passes_test(is_admin)
def admin_contato_editar(request, id):
    contato = get_object_or_404(Contato, id=id)
    categorias = CategoriaContato.objects.all()
    
    if request.method == 'POST':
        contato.nome = request.POST.get('nome')
        contato.descricao = request.POST.get('descricao')
        contato.imagem_url = request.POST.get('imagem_url')
        contato.cidade = request.POST.get('cidade')
        contato.estado = request.POST.get('estado')
        contato.telefone = request.POST.get('telefone')
        contato.horario_funcionamento = request.POST.get('horario_funcionamento')
        
        categoria_id = request.POST.get('categoria')
        contato.categoria = get_object_or_404(CategoriaContato, id=categoria_id) if categoria_id else None
        
        contato.atendimento_presencial = 'atendimento_presencial' in request.POST
        contato.atendimento_online = 'atendimento_online' in request.POST
        contato.save()
        
        messages.success(request, 'Contato atualizado com sucesso!')
        return redirect('admin_contatos')
    
    return render(request, 'core/admin/contato_form.html', {
        'contato': contato,
        'title': 'Editar Contato',
        'categorias': categorias
    })

@user_passes_test(is_admin)
def admin_contato_excluir(request, id):
    contato = get_object_or_404(Contato, id=id)
    
    if request.method == 'POST':
        contato.delete()
        messages.success(request, 'Contato excluído com sucesso!')
        return redirect('admin_contatos')
    
    return render(request, 'core/admin/confirmacao_exclusao.html', {
        'objeto': contato,
        'tipo': 'Contato',
        'title': 'Excluir Contato'
    })

# CRUD para Categorias de Ferramenta
@user_passes_test(is_admin)
def admin_categorias_ferramenta(request):
    categorias = CategoriaFerramenta.objects.all()
    return render(request, 'core/admin/categorias_ferramenta.html', {
        'categorias': categorias,
        'title': 'Gestão de Categorias de Ferramenta'
    })

@user_passes_test(is_admin)
def admin_categoria_ferramenta_criar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        icone = request.POST.get('icone')
        
        categoria = CategoriaFerramenta(nome=nome, icone=icone)
        categoria.save()
        
        messages.success(request, 'Categoria de Ferramenta criada com sucesso!')
        return redirect('admin_categorias_ferramenta')
    
    return render(request, 'core/admin/categoria_form.html', {
        'title': 'Nova Categoria de Ferramenta'
    })

@user_passes_test(is_admin)
def admin_categoria_ferramenta_editar(request, id):
    categoria = get_object_or_404(CategoriaFerramenta, id=id)
    
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.icone = request.POST.get('icone')
        categoria.save()
        
        messages.success(request, 'Categoria de Ferramenta atualizada com sucesso!')
        return redirect('admin_categorias_ferramenta')
    
    return render(request, 'core/admin/categoria_form.html', {
        'categoria': categoria,
        'title': 'Editar Categoria de Ferramenta'
    })

@user_passes_test(is_admin)
def admin_categoria_ferramenta_excluir(request, id):
    categoria = get_object_or_404(CategoriaFerramenta, id=id)
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria de Ferramenta excluída com sucesso!')
        return redirect('admin_categorias_ferramenta')
    
    return render(request, 'core/admin/confirmacao_exclusao.html', {
        'objeto': categoria,
        'tipo': 'Categoria de Ferramenta',
        'title': 'Excluir Categoria de Ferramenta'
    })

# CRUD para Ferramentas
@user_passes_test(is_admin)
def admin_ferramentas(request):
    ferramentas = Ferramenta.objects.all()
    return render(request, 'core/admin/ferramentas.html', {
        'ferramentas': ferramentas,
        'title': 'Gestão de Ferramentas'
    })

@user_passes_test(is_admin)
def admin_ferramenta_criar(request):
    categorias = CategoriaFerramenta.objects.all()
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        icone_classe = request.POST.get('icone_classe')
        tipo_id = request.POST.get('tipo')
        tipo = get_object_or_404(CategoriaFerramenta, id=tipo_id)
        eh_gratuita = 'eh_gratuita' in request.POST
        categoria = request.POST.get('categoria')
        
        ferramenta = Ferramenta(
            nome=nome,
            descricao=descricao,
            icone_classe=icone_classe,
            tipo=tipo,
            eh_gratuita=eh_gratuita,
            categoria=categoria
        )
        ferramenta.save()
        
        messages.success(request, 'Ferramenta criada com sucesso!')
        return redirect('admin_ferramentas')
    
    return render(request, 'core/admin/ferramenta_form.html', {
        'title': 'Nova Ferramenta',
        'categorias': categorias,
        'opcoes_categoria': dict(Ferramenta._meta.get_field('categoria').choices)
    })

@user_passes_test(is_admin)
def admin_ferramenta_editar(request, id):
    ferramenta = get_object_or_404(Ferramenta, id=id)
    categorias = CategoriaFerramenta.objects.all()
    
    if request.method == 'POST':
        ferramenta.nome = request.POST.get('nome')
        ferramenta.descricao = request.POST.get('descricao')
        ferramenta.icone_classe = request.POST.get('icone_classe')
        tipo_id = request.POST.get('tipo')
        ferramenta.tipo = get_object_or_404(CategoriaFerramenta, id=tipo_id)
        ferramenta.eh_gratuita = 'eh_gratuita' in request.POST
        ferramenta.categoria = request.POST.get('categoria')
        ferramenta.save()
        
        messages.success(request, 'Ferramenta atualizada com sucesso!')
        return redirect('admin_ferramentas')
    
    return render(request, 'core/admin/ferramenta_form.html', {
        'ferramenta': ferramenta,
        'title': 'Editar Ferramenta',
        'categorias': categorias,
        'opcoes_categoria': dict(Ferramenta._meta.get_field('categoria').choices)
    })

@user_passes_test(is_admin)
def admin_ferramenta_excluir(request, id):
    ferramenta = get_object_or_404(Ferramenta, id=id)
    
    if request.method == 'POST':
        ferramenta.delete()
        messages.success(request, 'Ferramenta excluída com sucesso!')
        return redirect('admin_ferramentas')
    
    return render(request, 'core/admin/confirmacao_exclusao.html', {
        'objeto': ferramenta,
        'tipo': 'Ferramenta',
        'title': 'Excluir Ferramenta'
    })

def document_list(request):
    # Lógica para listar documentos
    # Pode ser adaptada conforme seus modelos atuais
    return render(request, 'core/document_list.html', {'documents': []})