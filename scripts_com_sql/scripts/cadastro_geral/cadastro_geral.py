"""
Filename: cadastro_geral.py
Description: Consulta a quantidade de ligações registradas, por regional, que não possuem 
             coordenadas geográficas e envia uma tabela para os emails das regionais.
"""

import datetime
import plotly.graph_objects as go
import os

from dotenv import load_dotenv
from loguru import logger
from utilities.constantes import CREATED_FILES_PATH, LOG_FORMAT, LOG_PATH, REMETENTE_SGGP, SENHA_SGGP
from utilities.helpers import consulta_banco, cria_conn, envia_email 
from utilities.messages import INFO
from utilities.querys import cadastro_geral

load_dotenv()

#Configurações iniciais
logger.add(sink = LOG_PATH.format(filename = "cadastro_geral.log"), format=LOG_FORMAT)
script_name = os.path.basename(__file__)
filepath = CREATED_FILES_PATH.format(script_folder = script_name[:-3])
os.makedirs(filepath, exist_ok=True)

logger.info(INFO[100].format(script_name = script_name))

try:
    #Conexão com o banco
    conexao = cria_conn('CONEXAO')


    #Altera o nome do arquivo e o corpo do email baseado no dia da semana.
    if datetime.date.today().strftime("%A") == 'Monday':
        arquivo = 'Relacao_ligacoes_gerais_SEGUNDA.png'
        corpo = 'Bom dia!\nSegue quantitativo das ligações novas sem coordenadas geográficas no GSAN.'

    elif datetime.date.today().strftime("%A") == 'Friday':
        arquivo = 'Relacao_ligacoes_gerais_SEXTA.png'
        corpo = 'Boa tarde!\nSegue quantitativo das ligações novas sem coordenadas geográficas que não foram atualizadas essa semana.'

    else:
        arquivo = 'Relacao_ligacoes_gerais_TESTE.png'
        corpo = 'TESTE'
    


    #Consulta o banco e retorna o DataFrame
    df = consulta_banco(cadastro_geral, conexao)


    #Cria tabela 
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(df.columns),
            fill_color='paleturquoise',
            align='left'),
            
        cells=dict(
            values=[df.cod_regional, df.regional, df.coordenadas, df.quantidade],
            fill_color='lavender',
            align='left'))
    ])

    # Ajusta o layout para reduzir ou remover as margens
    fig.update_layout(
        width=800,  
        height=500,
        autosize=True
    )

    # Salva a tabela como imagem PNG
    destinacao_arquivo = os.path.join(filepath, arquivo)
    fig.write_image(destinacao_arquivo, scale=1)

    remetente = REMETENTE_SGGP
    senha = SENHA_SGGP
    destinatarios = [
        os.getenv("DIEGO"),
        os.getenv("LITORAL"),
        os.getenv("BORBOREMA"),
        os.getenv("BREJO"),
        os.getenv("ESPINHARIAS"),
        os.getenv("RIO_DO_PEIXE"),
        os.getenv("ALTO_PIRANHAS"),
    ]
    assunto = "Relação das ligações novas com e sem coordenadas nos regionais."
    arquivo_anexo = destinacao_arquivo
    emails_nao_enviados = []

    for destinatario in destinatarios:
        if envia_email(remetente, senha, destinatario, assunto, corpo, arquivo_anexo):
            pass
        else:
            emails_nao_enviados.append(destinatario)

    DIEGO = os.getenv("DIEGO")

    if len(emails_nao_enviados) > 0:
        envia_email(
            remetente, senha, DIEGO,
            "Micromedições - E-mails não enviados",
            f"Não foi possível enviar a tabela '{arquivo}' ao(s) seguinte(s) endereço(s): {emails_nao_enviados}")
    else:
        envia_email(remetente, senha, DIEGO, assunto,' E-mails enviados.')

except Exception as e:
    print(e)
finally:
    logger.info(INFO[102].format(script_name = script_name))