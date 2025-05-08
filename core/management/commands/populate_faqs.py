from django.core.management.base import BaseCommand
from core.models import Categoria, FAQ

class Command(BaseCommand):
    help = 'Popula o banco de dados com categorias e FAQs iniciais'

    def handle(self, *args, **kwargs):
        # Criar categorias
        categorias = {
            'Geral': 'fas fa-info-circle',
            'Diagnóstico': 'fas fa-stethoscope',
            'Tratamento': 'fas fa-heartbeat',
            'Apoio': 'fas fa-hands-helping',
            'Conceitos': 'fas fa-book',
        }
        
        for nome, icone in categorias.items():
            categoria, created = Categoria.objects.get_or_create(
                nome=nome,
                defaults={'icone': icone}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoria "{nome}" criada com sucesso!'))
            else:
                self.stdout.write(f'Categoria "{nome}" já existe.')
        
        # Criar FAQs exemplo
        faqs_data = [
            {
                'categoria': 'Geral',
                'pergunta': 'O que é o Transtorno do Espectro Autista (TEA)?',
                'resposta': 'O Transtorno do Espectro Autista (TEA) é uma condição de neurodesenvolvimento que afeta a comunicação, interação social e comportamento da pessoa. O termo "espectro" reflete a ampla variação de desafios e pontos fortes que cada pessoa com autismo possui.'
            },
            {
                'categoria': 'Diagnóstico',
                'pergunta': 'Em que idade é possível diagnosticar o autismo?',
                'resposta': 'Os sinais de autismo geralmente aparecem antes dos 3 anos de idade, e em muitos casos, é possível identificar sinais a partir dos 18 meses. Diagnósticos confiáveis podem ser feitos por volta dos 2 anos por profissionais experientes, mas algumas crianças podem ser diagnosticadas mais cedo ou mais tarde.'
            },
            {
                'categoria': 'Tratamento',
                'pergunta': 'Quais são as principais abordagens terapêuticas para o autismo?',
                'resposta': 'As principais abordagens incluem: intervenção comportamental, terapia ocupacional, fonoaudiologia, terapias sensoriais, e suporte psicológico. O plano de tratamento deve ser individualizado, considerando as necessidades específicas de cada pessoa.'
            },
            {
                'categoria': 'Apoio',
                'pergunta': 'Como apoiar uma pessoa autista em situações sociais?',
                'resposta': 'Algumas estratégias incluem: preparar a pessoa antecipadamente sobre o que esperar, respeitar seus limites sensoriais, criar um código ou sinal para quando precisar de pausa, oferecer um espaço tranquilo para momentos de sobrecarga, e ser paciente com suas formas de comunicação.'
            },
            {
                'categoria': 'Conceitos',
                'pergunta': 'O que são estereotipias?',
                'resposta': 'Estereotipias são movimentos repetitivos como balançar o corpo, bater palmas, agitar as mãos ("flapping"), entre outros. Esses movimentos geralmente têm função autorreguladora e podem ajudar a pessoa autista a processar emoções, lidar com estímulos sensoriais ou expressar excitação.'
            },
        ]
        
        for faq_data in faqs_data:
            categoria = Categoria.objects.get(nome=faq_data['categoria'])
            faq, created = FAQ.objects.get_or_create(
                pergunta=faq_data['pergunta'],
                defaults={
                    'categoria': categoria,
                    'resposta': faq_data['resposta']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'FAQ "{faq_data["pergunta"][:30]}..." criada com sucesso!'))
            else:
                self.stdout.write(f'FAQ "{faq_data["pergunta"][:30]}..." já existe.')
        
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))