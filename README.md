# Centro Espectro - Sistema de Apoio ao Autismo

> Plataforma web completa de apoio aos profissionais da educação para atendimento de alunos com TEA desenvolvida em Django com PostgreSQL

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)](https://github.com/seu-usuario/centro-espectro)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20)](https://djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791)](https://postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)
[![TCC](https://img.shields.io/badge/TCC-2025-blue)](https://github.com/seu-usuario/centro-espectro)

## Sobre

O Centro Espectro é uma plataforma web educacional desenvolvida para apoiar os profissionais da educação de escolas municipais no atendimento de alunos com Transtorno do Espectro Autista (TEA). Criado como Trabalho de Conclusão de Curso (TCC), oferece ferramentas especializadas, base de conhecimento e rede de contatos para capacitar educadores e gestores escolares no trabalho com a neurodiversidade.

## Funcionalidades

### 🎓 Gerenciamento de Alunos com TEA
- Cadastro completo dos alunos com perfil individualizado
- Registro de características e necessidades específicas do TEA
- Planos educacionais individualizados (PEI)
- Histórico de desenvolvimento e acompanhamento pedagógico
- Dashboard para professores e coordenadores
- Sistema de observações comportamentais

### ❓ Sistema de FAQs sobre Autismo
- Base de conhecimento abrangente sobre TEA para educadores
- Categorização por temas (estratégias pedagógicas, comportamento, inclusão)
- Sistema de busca inteligente por palavras-chave
- Perguntas frequentes de professores e gestores
- Glossário de termos técnicos especializados
- Área para contribuições da equipe pedagógica

### 🌐 Rede de Contatos Especializados
- Diretório de profissionais especializados em autismo
- Cadastro de psicólogos, terapeutas ocupacionais, fonoaudiólogos
- Sistema de avaliações e recomendações da equipe escolar
- Filtros por localização, especialidade e disponibilidade
- Formulário de contato direto com especialistas
- Histórico de encaminhamentos realizados

## Tecnologias

### Backend
- **Django 4.2+** - Framework web robusto
- **Python 3.9+** - Linguagem de programação
- **PostgreSQL 13+** - Banco de dados relacional
- **Django REST Framework** - APIs RESTful
- **Celery** - Processamento assíncrono

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript/jQuery** - Interatividade
- **Bootstrap 5** - Framework CSS responsivo
- **Chart.js** - Gráficos e relatórios visuais
- **DataTables** - Tabelas interativas

### Infraestrutura
- **Docker** - Containerização da aplicação
- **Nginx** - Servidor web e proxy reverso
- **Redis** - Cache e broker de mensagens
- **WhiteNoise** - Servir arquivos estáticos

### Conformidade
- **LGPD** - Proteção de dados dos alunos
- **Acessibilidade WCAG** - Interface inclusiva
- **Padrões Educacionais** - Alinhado com diretrizes do MEC

## Pré-requisitos

- [Python 3.9+](https://python.org/downloads/)
- [PostgreSQL 13+](https://postgresql.org/download/)
- [Git](https://git-scm.com/)
- Sistema operacional Linux, Windows ou macOS

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/centro-espectro.git
cd centro-espectro
```

### 2. Configure o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados
```bash
# Crie um banco PostgreSQL
createdb centro_espectro

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 7. Execute o servidor de desenvolvimento
```bash
python manage.py runserver
```

Acesse: `http://localhost:8000`

## Estrutura do Projeto

```
centro-espectro/
├── manage.py                    # Gerenciador Django
├── requirements.txt             # Dependências Python
├── docker-compose.yml          # Configuração Docker
├── .env.example               # Variáveis de ambiente
├── README.md                  # Documentação
├── LICENSE                    # Licença MIT
│
├── centro_espectro/           # Configurações principais
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/                      # Aplicações Django
│   ├── accounts/              # Autenticação e usuários
│   ├── students/              # Gerenciamento de alunos
│   ├── faqs/                  # Sistema de FAQs
│   ├── contacts/              # Rede de contatos
│   ├── reports/               # Relatórios e analytics
│   └── core/                  # Funcionalidades compartilhadas
│
├── templates/                 # Templates HTML
│   ├── base.html
│   ├── accounts/
│   ├── students/
│   ├── faqs/
│   └── contacts/
│
├── static/                    # Arquivos estáticos
│   ├── css/
│   ├── js/
│   ├── img/
│   └── vendors/
│
├── media/                     # Uploads de usuários
│   ├── student_photos/
│   └── documents/
│
└── docs/                      # Documentação adicional
    ├── api.md
    ├── deployment.md
    └── user_guide.md
```

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de dados
DATABASE_NAME=centro_espectro
DATABASE_USER=postgres
DATABASE_PASSWORD=sua-senha
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Email (para notificações)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha

# Cache Redis (opcional)
REDIS_URL=redis://localhost:6379/0
```

### Deploy com Docker

```bash
# Build e execução
docker-compose up --build

# Apenas execução
docker-compose up -d
```

## Testes

Execute os testes automatizados:

```bash
# Todos os testes
python manage.py test

# Testes de uma app específica
python manage.py test apps.students

# Com coverage
coverage run manage.py test
coverage report
```

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Diretrizes de Desenvolvimento

- Siga o padrão PEP 8 para código Python
- Use Django best practices
- Documente novas funcionalidades
- Escreva testes para novas features
- Use mensagens de commit descritivas em português

## Roadmap

- [ ] Integração com sistema acadêmico da escola
- [ ] Módulo de comunicação com famílias
- [ ] Aplicativo mobile para professores
- [ ] Relatórios avançados com BI
- [ ] Integração com plataformas de videoconferência
- [ ] Sistema de notificações em tempo real

## FAQ

**P: O sistema funciona offline?**
R: Não, é uma aplicação web que requer conexão com internet.

**P: Posso personalizar os campos dos alunos?**
R: Sim, através do painel administrativo Django.

**P: Como fazer backup dos dados?**
R: Use os comandos `python manage.py dumpdata` ou backup direto do PostgreSQL.

**P: O sistema atende à LGPD?**
R: Sim, implementa controles de acesso e proteção de dados pessoais.

## Suporte

Para suporte técnico ou dúvidas sobre o TCC:

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/centro-espectro/issues)
- **Email**: [g.moreno.souza05@gmail.com](mailto:g.moreno.souza05@gmail.com)
- **Documentação**: [Wiki do Projeto](https://github.com/seu-usuario/centro-espectro/wiki)

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">
  Desenvolvido por Gustavo, Carla e Giovanna para apoiar a educação inclusiva<br>
  <strong>TCC - Curso de Gestão da Tecnologia da Informação - FATEC - 2025</strong>
</div>
