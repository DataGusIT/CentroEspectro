from django.db import models
from django.contrib.auth.models import User

# Categoria base (abstrata)
class CategoriaBase(models.Model):
    nome = models.CharField(max_length=100)
    icone = models.CharField(max_length=50, blank=True, null=True)  # Removido o valor default
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.nome
        
    def nome_slug(self):
        return self.nome.lower().replace(" ", "-")

# Categorias específicas
class CategoriaFAQ(CategoriaBase):
    class Meta:
        verbose_name = 'Categoria de Dúvida'
        verbose_name_plural = 'Categorias de Dúvidas'
    
    def get_icone(self):
        icones = {
            'Geral': 'fas fa-info-circle',
            'Diagnóstico': 'fas fa-stethoscope',
            'Tratamento': 'fas fa-heartbeat',
            'Apoio': 'fas fa-hands-helping',
            'Conceitos': 'fas fa-book',
        }
        return icones.get(self.nome, 'fas fa-question-circle')

class CategoriaContato(CategoriaBase):
    class Meta:
        verbose_name = 'Categoria de Contato'
        verbose_name_plural = 'Categorias de Contatos'

class CategoriaFerramenta(CategoriaBase):
    class Meta:
        verbose_name = 'Categoria de Ferramenta'
        verbose_name_plural = 'Categorias de Ferramentas'

# Modelos principais
class FAQ(models.Model):
    categoria = models.ForeignKey(CategoriaFAQ, on_delete=models.CASCADE, related_name='faqs')
    pergunta = models.CharField(max_length=255)
    resposta = models.TextField()
    
    def __str__(self):
        return self.pergunta

class Contato(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    # Alteração: Substituir campo imagem_url por ImageField
    imagem = models.ImageField(upload_to='contatos/', blank=True, null=True)
    
    # Campos de endereço melhorados
    rua = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=9, blank=True, null=True)  # Formato: 00000-000
    
    telefone = models.CharField(max_length=20)
    horario_funcionamento = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaContato, on_delete=models.CASCADE, related_name='contatos', null=True, blank=True)
    atendimento_presencial = models.BooleanField(default=True)
    atendimento_online = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
    def endereco_completo(self):
        """Retorna o endereço completo formatado"""
        endereco = []
        if self.rua:
            endereco.append(f"{self.rua}")
            if self.numero:
                endereco[-1] += f", {self.numero}"
        if self.complemento:
            endereco.append(self.complemento)
        if self.bairro:
            endereco.append(self.bairro)
        endereco.append(f"{self.cidade}, {self.estado}")
        if self.cep:
            endereco.append(f"CEP: {self.cep}")
        return " - ".join(endereco)

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'

class Ferramenta(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    icone_classe = models.CharField(max_length=50, default='fas fa-tools')
    tipo = models.ForeignKey(CategoriaFerramenta, on_delete=models.CASCADE, related_name='ferramentas')
    eh_gratuita = models.BooleanField(default=False)
    classificacao = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    categoria = models.CharField(max_length=100, choices=[
        ('pictogramas_escolares', 'Pictogramas Escolares'),
        ('alfabetizacao', 'Alfabetização'),
        ('brinquedos_brincadeiras', 'Brinquedos e Brincadeiras'),
        ('historias_sociais', 'Histórias Sociais'),
        ('atividades_diversas', 'Atividades Diversas')
    ])
    
    def __str__(self):
        return self.nome

class CustomUser(User):
    # Campos adicionais
    is_admin = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class UserDownload(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='downloads')
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.CASCADE)
    data_download = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.ferramenta.nome} - {self.data_download.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'
        ordering = ['-data_download']