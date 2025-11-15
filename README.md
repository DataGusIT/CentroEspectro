

# Centro Espectro - Plataforma de Apoio ao Autismo

> Plataforma web de apoio e informação sobre o Transtorno do Espectro Autista (TEA), desenvolvida como um TCC para uma escola municipal, conectando famílias e educadores.

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue)](https://github.com/DataGusIT/CentroEspectro)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-Framework-092E20)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

## Sobre o Projeto

O **Centro Espectro** é uma aplicação web desenvolvida como um Trabalho de Conclusão de Curso (TCC), com o objetivo de criar uma ferramenta centralizada de informação e apoio para a comunidade de uma escola municipal. A plataforma visa desmistificar o Transtorno do Espectro Autista (TEA), fornecer recursos valiosos e facilitar a comunicação e o acompanhamento dos alunos no espectro.

Construída com Python e Django, a solução oferece um portal informativo para famílias e uma área restrita e segura para que os professores possam gerenciar informações acadêmicas e de desenvolvimento dos seus alunos com autismo.

## 🖼️ Demonstração Visual

| Tela Inicial | Dúvidas Frequentes | Rede de Contatos |
| :---: | :---: | :---: |
| <img width="1902" height="1079" alt="Image" src="https://github.com/user-attachments/assets/27904553-eaa4-4f22-9ab6-8c5db5a596c8" /> | <img width="1899" height="1079" alt="Image" src="https://github.com/user-attachments/assets/ad408d98-d9df-4936-9fd9-4522cc8c1132" /> | <img width="1903" height="1079" alt="Image" src="https://github.com/user-attachments/assets/d8a43fe6-ec5f-4cbd-8d58-61ea51bc5ee6" /> |
| **Detalhes de Contato** | **Perfil do Usuário** | **Área do Professor** |
| <img width="1899" height="1079" alt="Image" src="https://github.com/user-attachments/assets/4acd96b1-923d-4a62-bc2e-74427938fab9" /> | 
<img width="1904" height="1079" alt="Image" src="https://github.com/user-attachments/assets/68dbd11c-5223-41a1-bf57-a0ec6d1e83fc" />
 | <img width="1899" height="1077" alt="Image" src="https://github.com/user-attachments/assets/c5840390-8512-4237-b6fb-54f4f570200d" /> |

## ✨ Funcionalidades

### 🌐 Portal Informativo (Acesso Público)
-   **Conteúdo sobre Autismo:** Uma seção de "Dúvidas Frequentes" com artigos e informações claras para ajudar pais e educadores a entender melhor o TEA.
-   **Rede de Contatos Especializados:** Um diretório com contatos de profissionais e instituições especializadas no atendimento a pessoas no espectro.

### 👤 Área Pessoal do Usuário
-   **Autenticação Segura:** Sistema de cadastro e login, incluindo autenticação social com Google para facilitar o acesso.
-   **Perfil Personalizado:** Os usuários podem salvar dúvidas e contatos favoritos em seu perfil para acesso rápido e fácil.

### 👩‍🏫 Área Restrita do Professor
-   **Gestão de Alunos:** Visualização de uma lista de alunos com autismo em suas turmas.
-   **Acesso a Documentação:** Acesso seguro ao laudo e ao nível de suporte de cada aluno, centralizando informações importantes.
-   **Relatórios de Desempenho:** Ferramenta para que o professor possa criar, aplicar e acompanhar relatórios de desempenho e desenvolvimento dos alunos, auxiliando no planejamento pedagógico.

## Tecnologias

### Backend
-   **Python 3.9+**
-   **Django** - Framework web principal.
-   **Django Allauth** - Para autenticação local e social (Google).

### Frontend
-   **HTML5**
-   **CSS3**
-   **JavaScript**

### Banco de Dados
-   **SQLite3** - Banco de dados padrão para desenvolvimento.

### Deploy
-   Scripts de build (`build.sh`) e configuração para deploy em ambiente de produção.

## Pré-requisitos

-   Python 3.9 ou superior
-   Pip (gerenciador de pacotes do Python)

## Instalação e Uso

1.  **Clone o repositório**
    ```bash
    git clone https://github.com/DataGusIT/CentroEspectro.git
    cd CentroEspectro
    ```

2.  **Crie e ative um ambiente virtual**
    ```bash
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplique as migrações do banco de dados**
    ```bash
    python manage.py migrate
    ```

5.  **Crie um superusuário**
    Utilize o script customizado para facilitar a criação do administrador:
    ```bash
    python createu.py
    ```

6.  **Execute a aplicação**
    ```bash
    python manage.py runserver
    ```
    Acesse o sistema em `http://127.0.0.1:8000`.

## Contribuição

Contribuições são bem-vindas! Se você tem ideias para melhorar a plataforma:

1.  Faça um Fork do projeto.
2.  Crie sua Feature Branch (`git checkout -b feature/NovaFuncionalidade`).
3.  Faça Commit de suas mudanças (`git commit -m 'Adiciona funcionalidade X'`).
4.  Faça Push para a Branch (`git push origin feature/NovaFuncionalidade`).
5.  Abra um Pull Request.

## Suporte e Contato

-   **Email**: [g.moreno.souza05@gmail.com](mailto:g.moreno.souza05@gmail.com)
-   **LinkedIn**: [Gustavo Moreno](https://www.linkedin.com/in/gustavo-moreno-8a925b26a/)

## Licença

Este projeto está licenciado sob uma Licença Proprietária.

**Uso Restrito**: Este software é de propriedade exclusiva do autor. Uso comercial ou redistribuição requer autorização expressa.

---

<div align="center">
  Desenvolvido por Gustavo Moreno
  <br><br>
  <a href="https://www.linkedin.com/in/gustavo-moreno-8a925b26a/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" alt="LinkedIn"/>
  </a>
</div>
