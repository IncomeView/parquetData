# Lista de tabelas que serão extraídas do Postgres para o Bronze
BRONZE_TABLES = {
    "public": [
        "clientes",
        "vendas",
        "produtos"
    ]
}

# Caminhos dentro do ADLS (Lakehouse)
ADLS_PATHS = {
    "bronze": "bronze/",
    "silver": "silver/",
    "gold": "gold/"
}

