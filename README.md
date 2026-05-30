# Food Explorer

Aplicação web em Django que consome a API do [TheMealDB](https://www.themealdb.com) para explorar receitas, gerenciar favoritos por usuário, ajustar porções, marcar ingredientes durante o preparo e gerar lista de compras. Interface em pt-BR.

## Funcionalidades

### Navegação e busca
- Busca de receitas por nome
- Filtro por categoria (Carne, Frango, Sobremesa, Massa…)
- Filtro por cozinha (Italiana, Mexicana, Japonesa, Chinesa…)
- Paginação (20 receitas por página)
- Botão "× Limpar filtros" quando algum filtro está ativo
- Botão de receita aleatória (🎲)

### Página de detalhe
- Ingredientes com medidas formatadas
- Modo de preparo completo
- Vídeo do YouTube embedado (com fallback de link)
- **Checklist de ingredientes** — marca cada um conforme cozinha, salvo no navegador (localStorage)
- **Ajuste de porções** (1× a 5×) — recalcula medidas numéricas automaticamente

### Usuário
- Cadastro e login
- Sistema de favoritos (adicionar/remover) com contador na navbar
- **Lista de compras** — agrega ingredientes de todas as receitas favoritas, agrupados, com origem visível

### Visual
- **Dark mode** com toggle 🌙/☀️ na navbar (preferência salva no localStorage)
- Design responsivo (mobile-friendly)
- CSS variables pra fácil customização de cores

## Tecnologias

- Python 3 / Django 5.2
- SQLite (banco padrão)
- `requests` para consumir a API
- `python-decouple` para variáveis de ambiente
- JavaScript vanilla (sem frameworks) + localStorage
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
```

Criar arquivo `.env` na raiz com **3 variáveis**:

```env
THEMEALDB_API_KEY=1
SECRET_KEY=cole-aqui-uma-chave-secreta
DEBUG=True
```

Pra gerar uma `SECRET_KEY` aleatória:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> `THEMEALDB_API_KEY=1` é a chave de teste pública do TheMealDB e basta para desenvolvimento.

Em seguida:

```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário pra acessar /admin/
python manage.py createsuperuser

# Rodar o servidor
python manage.py runserver
```

Acesse:
- http://127.0.0.1:8000 — site
- http://127.0.0.1:8000/admin — painel admin (requer superusuário)

## Estrutura

```
food_explorer/
├── config/                       # Settings, urls, wsgi
├── recipes/                      # App principal
│   ├── models.py                 # FavoriteRecipe
│   ├── views.py                  # home, recipe_detail, random, favoritos, lista de compras
│   ├── urls.py
│   ├── admin.py                  # registro do FavoriteRecipe
│   ├── context_processors.py     # favorite_count na navbar
│   ├── templatetags/
│   │   └── recipe_filters.py     # filtros de tradução (categorias e cozinhas)
│   ├── templates/recipes/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── recipe_detail.html
│   │   ├── favorites.html
│   │   └── shopping_list.html
│   └── static/recipes/
│       ├── css/                  # base, home, recipe_detail, favorites, login
│       └── js/                   # checklist, theme, portions
├── templates/                    # login.html, register.html
├── manage.py
├── requirements.txt
└── .env                          # não versionado
```

## API

Dados de receitas fornecidos por [TheMealDB](https://www.themealdb.com/api.php) (gratuita, sem necessidade de cadastro com a chave de teste).

Endpoints utilizados:
- `search.php?s=` — busca por nome
- `lookup.php?i=` — detalhe completo de uma receita
- `random.php` — receita aleatória
- `filter.php?c=` / `?a=` — filtro por categoria / cozinha
- `categories.php` / `list.php?a=list` — listas de categorias e cozinhas
