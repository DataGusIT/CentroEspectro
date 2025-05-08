from django.db import models

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