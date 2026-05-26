# Food Explorer

Aplicação web em Django que consome a API do [TheMealDB](https://www.themealdb.com) para explorar receitas, ver detalhes (ingredientes, modo de preparo, vídeo) e gerenciar uma lista de favoritos por usuário.

## Funcionalidades

- Busca de receitas por nome
- Filtro por categoria
- Página de detalhe com ingredientes, modo de preparo e vídeo do YouTube embedado
- Cadastro e login de usuários
- Sistema de favoritos (adicionar/remover) com contador na navbar
- Interface em pt-BR

## Tecnologias

- Python 3 / Django 5.2
- SQLite (banco padrão)
- `requests` para consumir a API
- `python-decouple` para variáveis de ambiente
- TheMealDB (API externa de receitas)

## Como rodar

```bash
# Clonar e entrar na pasta
git clone <url-do-repo>
cd food_explorer

# Criar venv e instalar dependências
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac
pip install -r requirements.txt

# Criar arquivo .env na raiz com a chave da API
# (a chave "1" é a de teste pública e basta para desenvolvimento)
echo THEMEALDB_API_KEY=1 > .env

# Aplicar migrações
python manage.py migrate

# (Opcional) Criar superusuário pra acessar o admin
python manage.py createsuperuser

# Rodar o servidor
python manage.py runserver
```

Acesse http://127.0.0.1:8000

## Estrutura

```
food_explorer/
├── config/                 # Settings, urls, wsgi
├── recipes/                # App principal
│   ├── models.py           # FavoriteRecipe
│   ├── views.py            # home, recipe_detail, favoritos, auth
│   ├── urls.py
│   ├── context_processors.py
│   ├── templates/recipes/  # base, home, recipe_detail, favorites
│   └── static/recipes/css/ # base, home, recipe_detail, favorites, login
├── templates/              # login.html, register.html
├── manage.py
├── requirements.txt
└── .env                    # não versionado
```

## API

Dados de receitas fornecidos por [TheMealDB](https://www.themealdb.com/api.php) (gratuita, sem necessidade de cadastro com a chave de teste).
