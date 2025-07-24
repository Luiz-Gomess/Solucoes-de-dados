"""
Filename: contas_altas.py
Description: Consulta as contas altas do estado referentes ao mês atual.
"""

import datetime
import os

from dotenv import load_dotenv
from loguru import logger
from utilities.constantes import CREATED_FILES_PATH, LOG_FORMAT, LOG_PATH, REMETENTE_SGGP, SENHA_SGGP
from utilities.helpers import consulta_banco, cria_arquivo, cria_conn, envia_email 
from utilities.messages import INFO
from utilities.querys import contas_altas

load_dotenv()

#Configurações iniciais
logger.add(sink = LOG_PATH.format(filename = "contas_altas.log"), format=LOG_FORMAT)
script_name = os.path.basename(__file__)
filepath = CREATED_FILES_PATH.format(script_folder = script_name[:-3])
os.makedirs(filepath, exist_ok=True)


logger.info(INFO[100].format(script_name = script_name))

try:
    #Conexão com o banco
    conexao = cria_conn('CONEXAO')

    # Variáveis referentes a data
    data_atual = datetime.date.today() 
    mes_numero = data_atual.strftime('%m') 
    ano = data_atual.strftime('%Y')

    #Valores a serem substituidos na query
    data_where = ano+mes_numero # --> '202409'

    #Consulta o banco e cria o Dataframe
    query = contas_altas.format(data_where=data_where)
    df = consulta_banco(query=query, conexao=conexao)
    df.drop('Referencia', axis=1, inplace=True)

    df.sort_values(by="Valor da Conta", ascending=False, inplace=True)
    # df.to_excel("teste.xlsx", index=False)

    #Nome do arquivo
    filename = f"Contas Altas {data_atual.strftime('%d.%m.%Y')}.xlsx"

    #Cria o xlsx
    path = cria_arquivo(df, '.xlsx', filepath, filename)

    #Envio dos e-mails
    remetente = REMETENTE_SGGP
    senha = SENHA_SGGP
    destinatarios = [
    os.getenv('EMAIL1'),
    os.getenv('EMAIL2'),
    os.getenv('EMAIL3'),
    ]
    assunto = filename.replace('.xlsx', '')
    corpo = "Bom dia.\nSegue dados em anexo."
    arquivo_anexo = path
    qtde_emails_enviados = 0


    emails_nao_enviados = []

    #Enviando para cada endereço
    for destinatario in destinatarios:
        if envia_email(remetente, senha, destinatario, assunto, corpo, arquivo_anexo):
            pass
        else:
            emails_nao_enviados.append(destinatario)

    DIEGO = os.getenv("DIEGO")

    if len(emails_nao_enviados) > 0:
        envia_email(
            remetente, senha, DIEGO,
            "Contas Altas - E-mails não enviados",
            f"Não foi possível enviar a tabela '{filename}' ao(s) seguinte(s) endereço(s): {emails_nao_enviados}")
    else:
        envia_email(remetente, senha, DIEGO, assunto,' E-mails enviados.')

except Exception as e:
    print(e.with_traceback())
finally:
    logger.info(INFO[102].format(script_name = script_name))


