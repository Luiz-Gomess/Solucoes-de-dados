"""
Filename: capacidade_hidrometro.py
Description: Consulta os dados dos hidrômetros, cria um csv e envia por email.
"""
import os

from loguru import logger
from dotenv import load_dotenv

from utilities.helpers import consulta_banco, cria_conn, cria_arquivo, envia_email
from utilities.constantes import LOG_PATH, LOG_FORMAT, CREATED_FILES_PATH, REMETENTE_SGGP, SENHA_SGGP
from utilities.messages import INFO
from utilities.querys import capacidade_hidrometro

#Configurações iniciais
logpath = LOG_PATH.format(filename = "capacidade.log")
logger.add(sink = logpath, format=LOG_FORMAT)
script_name = os.path.basename(__file__)
filepath = CREATED_FILES_PATH.format(script_folder = script_name[:-3])
os.makedirs(filepath, exist_ok=True)
load_dotenv()

logger.info(INFO[100].format(script_name = script_name))

try:

    #Conexão com o banco
    conexao = cria_conn('CONEXAO')
    df = consulta_banco(conexao=conexao, query=capacidade_hidrometro)
    
    filename = "hidrometros_capacidade.csv"
    path = cria_arquivo(df, '.csv', filepath, filename)

    #E-mail
    remetente = REMETENTE_SGGP
    senha = SENHA_SGGP
    titulo = "Regional-Hidrômetro de Capacidades"
    corpo = "Bom dia, \n\n\n Segue cadastro comercial das ligações nos regionais com hidrômetros de capacidade maior ou igual a 4 metros."
    destinatario = os.getenv("HELDER")
    

    envia_email(
        remetente,
        senha,
        destinatario,
        titulo,
        corpo,
        path)    

except Exception as e:
    print("Execeção: ", e)

finally:
    logger.info(INFO[102].format(script_name = script_name))
