import os
import pandas as pd
from utils.password_generator import generate_strong_password

# Nomes dos arquivos
arquivo_usuarios = "data/usuarios_arcgis.csv"
arquivo_template = "data/template.csv"
arquivo_final = "data/final_usuarios_arcgis.csv"

# Lê os csv's e cria dataframes
df_usuarios = pd.read_csv(arquivo_usuarios)
df_template = pd.read_csv(arquivo_template)

# Associa as colunas correlacionadas a um dicionário
cabecalho = {
    "Email" : "E-mail",
    "Role" : "Papel",
    "User Type" : "Tipo de Usuário",
    "Name" : "Nome",
    "Username" : "Nome de Usuário",
}

# Popula o df_template com as colunas relacionadas do df_usuarios
for coluna_usuarios, coluna_template in cabecalho.items():
    df_template[coluna_template] = df_usuarios[coluna_usuarios]

### Funções

# Preenche a coluna 'Sobrenome' do template com o ultimo valor de cada célula da coluna 'Nome'
def preencher_sobrenome(row):
    row["Sobrenome"] = row["Nome"].strip().split(" ")[-1]
    return row["Sobrenome"]

# Cria uma senha aleatória e atribui a cada célula da coluna 'Senha'
def criar_senha(row):
    row["Senha"] = generate_strong_password()
    return row["Senha"] 

# Renomeia os valores de 'Tipo de Usuário' para o formato aceito no novo sistema
def renomear_usertype(row):
    match row["Tipo de Usuário"] :

        case "viewerUT":
            return "Viewer"
        case "creatorUT":
            return "Creator"

# Renomeia os valores de 'Papel' para o formato aceito no novo sistema
def renomear_role(row):
    match row["Papel"]:
        case "account_publisher":
            return "Publicador"
        case "account_user":
            return "Usuário"
        case "account_admin":
            return "Administrador"
        case "Data Editor":
            return "Editor de Dados"
        case "Viewer":
            # return row["Papel"]
            return "Viewer"
        
# Aplica as funções nas colunas correspondentes
df_template["Sobrenome"] = df_template.apply(preencher_sobrenome, axis=1)
df_template["Senha"] = df_template.apply(criar_senha, axis=1)
df_template["Tipo de Usuário"] = df_template.apply(renomear_usertype, axis=1)
df_template["Papel"] = df_template.apply(renomear_role, axis=1)

# Cria o csv com os usuários atualizados, formatados e prontos para import.
df_template.to_csv(arquivo_final, index=False)