from django import template

register = template.Library()


CATEGORY_TRANSLATIONS = {
    'Beef': 'Carne',
    'Chicken': 'Frango',
    'Dessert': 'Sobremesa',
    'Lamb': 'Cordeiro',
    'Miscellaneous': 'Diversos',
    'Pasta': 'Massa',
    'Pork': 'Porco',
    'Seafood': 'Frutos do mar',
    'Side': 'Acompanhamento',
    'Starter': 'Entrada',
    'Vegan': 'Vegano',
    'Vegetarian': 'Vegetariano',
    'Breakfast': 'Café da manhã',
    'Goat': 'Cabrito',
}


@register.filter
def traduzir_categoria(nome):
    """Traduz nome de categoria da TheMealDB pra pt-BR.
    Se a categoria não estiver no dicionário, retorna o nome original."""
    if not nome:
        return nome
    return CATEGORY_TRANSLATIONS.get(nome, nome)
