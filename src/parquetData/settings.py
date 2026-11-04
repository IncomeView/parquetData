
# Lista de tabelas que serão extraídas do Postgres para o Bronze
BRONZE_TABLES = {
    "public": [
        "bankmovement",
        "bankmovementbuldingcosts",
        "bankmovementfinancialcategories",
        "creditors",
        "customers",
        "income",
        "incomebankmovements",
        "incomecategoriesreceipts",
        "incomefinancialcategories",
        "incomereceipts",
        "incomereceiptsbankmovements",
        "incomereceiptsbankmovementsfinancialcategories",
        "incomereceiptscategories",
        "outcome",
        "outcomeauthorizations",
        "outcomebuildingscosts",
        "outcomecategoriespayments",
        "outcomepayments",
        "outcomepaymentsbankmovements",
        "outcomepaymentsbankmovementspaymentscategories"
    ]
}

# Caminhos dentro do ADLS (Lakehouse)
ADLS_PATHS = {
    "bronze": "bronze/",
    "silver": "silver/",
    "gold": "gold/"
}

