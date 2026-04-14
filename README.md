# Twitter Clone — Projeto Final EBAC

Clone funcional do Twitter construído com **Django monolítico + Tailwind CSS**.

## Stack

| Camada | Tecnologia |
|---|---|
| Back-end | Python 3.11 + Django 4.2 |
| Front-end | HTML + Tailwind CSS (CDN) + JavaScript (Fetch API) |
| Banco de dados | SQLite (dev) |
| Arquivos estáticos | WhiteNoise |
| Servidor produção | Gunicorn |

---

## Funcionalidades

- ✅ Cadastro e login seguro
- ✅ Edição de perfil (nome, bio, foto, capa) — todos os campos opcionais
- ✅ Alteração de senha
- ✅ Sistema de seguir/deixar de seguir (AJAX)
- ✅ Feed inteligente (só mostra quem você segue + seus próprios tweets)
- ✅ Criação de tweets com imagem ou vídeo
- ✅ Curtidas (AJAX, sem recarregar a página)
- ✅ Retweets com toggle (AJAX)
- ✅ Comentários (AJAX)
- ✅ Central de notificações (likes, comentários, retweets, follows)
- ✅ Badge de notificações não lidas no menu
- ✅ Dark mode nativo

---

## Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/meu-twitter.git
cd meu_twitter
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com sua SECRET_KEY
```

### 5. Rode as migrations e inicie o servidor

```bash
python manage.py migrate
python manage.py createsuperuser  # opcional
python manage.py runserver
```

Acesse em: **http://127.0.0.1:8000**

---

## Deploy (Render)

1. Crie um novo **Web Service** no [Render](https://render.com)
2. Conecte seu repositório GitHub
3. Configure:
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn core.wsgi:application`
4. Adicione as variáveis de ambiente:
   - `SECRET_KEY` → uma chave secreta longa
   - `DEBUG` → `False`
   - `ALLOWED_HOSTS` → `seu-app.onrender.c`

---
 Acesse a aplicação em: http://127.0.0.1:8000/ 🌐 Deploy A aplicação está hospedada e pode ser acessada através do link abaixo: 👉https://ebac-projeto-final-clone-twitter.onrender.com

## Autor

**Helbert Guirra** — EBAC Projeto Final
