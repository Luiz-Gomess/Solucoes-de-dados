"""
Filename: micromedicoes.py
Description: Consulta 
"""

import os
import datetime

from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
from loguru import logger
from pandas.tseries.offsets import BDay
from utilities.constantes import LOG_FORMAT, LOG_PATH, CREATED_FILES_PATH, LUIZ, SENHA_LUIZ, REMETENTE_SGGP, SENHA_SGGP, DESTINATARIO_ASSIST_GEGM, DESTINATARIO_GEGM
from utilities.helpers import consulta_banco, cria_arquivo, cria_conn, envia_email
from utilities.messages import INFO
from utilities.querys import micromedicoes

load_dotenv()

#Configurações iniciais
logger.add(sink = LOG_PATH.format(filename = "micromedicoes.log"), format=LOG_FORMAT)
script_name = os.path.basename(__file__)
filepath = CREATED_FILES_PATH.format(script_folder = script_name[:-3])
os.makedirs(filepath, exist_ok=True)


logger.info(INFO[100].format(script_name = script_name))

try:
    #Conexão com o banco
    conexao = cria_conn('CONEXAO')


    #Variáveis de data
    data_atual = datetime.date.today() 
    mes_numero = data_atual.strftime('%m')
    ano = data_atual.strftime('%Y')
    primeiro_dia = datetime.date(int(ano), int(mes_numero), 1)
    quatro_dias_uteis = datetime.datetime.strftime((primeiro_dia + BDay(4)), "%d")


    #Dicionário com os meses chaveados com seus respectivos valores.
    mes_nome = {
    '01' : 'JANEIRO',
    '02' : 'FEVEREIRO',
    '03' : 'MARCO',
    '04' : 'ABRIL',
    '05' : 'MAIO',
    '06' : 'JUNHO',
    '07' : 'JULHO',
    '08' : 'AGOSTO',
    '09' : 'SETEMBRO',
    '10' : 'OUTUBRO',
    '11' : 'NOVEMBRO',
    '12' : 'DEZEMBRO',
    }


    #Altera a clausula da consulta e variaveis de data com base no dia atual
    if data_atual.day < int(quatro_dias_uteis):
        #'2024-10-1' - 1 mês -> '2024-09-01' -> '09'
        mes_numero = (data_atual - relativedelta(months=1)).strftime('%m')
        #'2025-01-01' - 1 mês -> '2024-12-01' -> '2024'  
        ano = (data_atual - relativedelta(months=1)).strftime('%Y') 
        clausula_where = f"orse_tmencerramento >= '{primeiro_dia - relativedelta(months=1)}' and orse_tmencerramento < '{primeiro_dia}'"
    else:
        clausula_where = f"orse_tmencerramento >= '{primeiro_dia}' and orse_tmencerramento < '{primeiro_dia + relativedelta(months=1)}'"


    #Realiza a consulta
    query = micromedicoes.format(clausula_where = clausula_where)
    df = consulta_banco(query=query, conexao=conexao)

    #Cria o csv
    filename = f'{mes_numero}-Relatorio Diario de Mov. de Hidro - {mes_nome[mes_numero]}.{ano}.csv'
    path = cria_arquivo(df,'.csv', filepath, filename)


    #Configurações do e-mail
    remetente = REMETENTE_SGGP
    senha = SENHA_SGGP
    destinatarios = [
        DESTINATARIO_ASSIST_GEGM,
        DESTINATARIO_GEGM,
    ]
    # remetente = LUIZ
    # senha = SENHA_LUIZ
    # destinatarios = [remetente]
    
    titulo = ''
    corpo = ''
    arquivo_anexo = path


    #Altera o titulo e o corpo baseado no dia
    if data_atual.day == int(quatro_dias_uteis) - 1:
        titulo = f"Relatório de movimentação final do mês de {mes_nome[mes_numero]}" 
        corpo = f"Bom dia,\nSegue relatório final sobre a movimentação de hidrômetros do estado no mês de {mes_nome[mes_numero]}."
    else:
        titulo = "Relatório de movimentação diário"
        corpo = "Bom dia,\nSegue relatório diário da movimentação de hidrômetros no estado."


    emails_nao_enviados = []

    #Enviando para cada endereço
    for destinatario in destinatarios:
        if envia_email(remetente, senha, destinatario, titulo, corpo, arquivo_anexo):
            pass
        else:
            emails_nao_enviados.append(destinatario)


    DIEGO = os.getenv("DIEGO")

    if len(emails_nao_enviados) > 0:
        envia_email(
            remetente, senha, DIEGO,
            "Micromedições - E-mails não enviados",
            f"Não foi possível enviar a tabela '{filename}' ao(s) seguinte(s) endereço(s): {emails_nao_enviados}")
    else:
        envia_email(remetente, senha, DIEGO, titulo,' E-mails enviados.')

except Exception as e:
    print(e)
finally:   
    logger.info(INFO[102].format(script_name = script_name))
