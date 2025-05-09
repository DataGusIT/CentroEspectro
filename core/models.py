from django.db import models
from django.contrib.auth.models import User  # Use o modelo padrão

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    icone = models.CharField(max_length=50, default='fas fa-question-circle')
    
    def __str__(self):
        return self.nome
    
    def get_icone(self):
        icones = {
            'Geral': 'fas fa-info-circle',
            'Diagnóstico': 'fas fa-stethoscope',
            'Tratamento': 'fas fa-heartbeat',
            'Apoio': 'fas fa-hands-helping',
            'Conceitos': 'fas fa-book',
        }
        return icones.get(self.nome, 'fas fa-question-circle')
    
    def nome_slug(self):
        return self.nome.lower().replace(" ", "-")

class FAQ(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='faqs')
    pergunta = models.CharField(max_length=255)
    resposta = models.TextField()
    
    def __str__(self):
        return self.pergunta

class Contato(models.Model):
    TIPO_CHOICES = [
        ('CLINICA', 'Clínica'),
        ('PROFISSIONAL', 'Profissional'),
        ('ASSOCIACAO', 'Associação'),
        ('ESCOLA', 'Escola'),
        ('GRUPO_APOIO', 'Grupo de Apoio'),
        ('EMERGENCIA', 'Emergência')
    ]
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem_url = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    horario_funcionamento = models.CharField(max_length=100)
    avaliacao = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    atendimento_presencial = models.BooleanField(default=True)
    atendimento_online = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'    

# Novo modelo para as ferramentas de apoio ao TEA
class TipoFerramenta(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Ferramenta(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    icone_classe = models.CharField(max_length=50, default='fas fa-tools')
    tipo = models.ForeignKey(TipoFerramenta, on_delete=models.CASCADE, related_name='ferramentas')
    eh_gratuita = models.BooleanField(default=False)
    classificacao = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    categoria = models.CharField(max_length=100, choices=[
        ('comunicacao', 'Ferramentas de Comunicação'),
        ('comportamental', 'Ferramentas Comportamentais'),
        ('educacional', 'Ferramentas Educacionais'),
        ('organizacao', 'Ferramentas de Organização'),
        ('sensorial', 'Ferramentas Sensoriais'),
        ('tecnologica', 'Ferramentas de Tecnologia Assistiva')
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
    ferramenta = models.ForeignKey('Ferramenta', on_delete=models.CASCADE)
    data_download = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.ferramenta.nome} - {self.data_download.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'
        ordering = ['-data_download']
