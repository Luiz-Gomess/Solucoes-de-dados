"""
Filename: atendimentos_sem_cadastro.py
Description: Consulta as RAs cujo os clientes possuem dados não atualizados e envia para os emails correspondentes.
Fluxo de execução:
    - Cria conexão
    - Altera a consulta baseado no seu horário de execução
    - Cria um DataFrame com todos os atendimentos e exclui a coluna 'email_usuario_gsan'.
    - Define o nome e o caminho dos csvs gerados.
    - Cria um csv com ambas as unidades, um csv referente a unidade 31501 e um csv referente a unidade 31502.
    - Envia os csvs para seus respectivos endereços
"""
import os
import sys

import time
from loguru import logger
from dotenv import load_dotenv

from utilities.helpers import consulta_banco, cria_conn, cria_arquivo, envia_email
from utilities.constantes import LOG_PATH, LOG_FORMAT, CREATED_FILES_PATH
from utilities.messages import INFO
from utilities.querys import atendimentos_sem_cadastro12hrs, atendimentos_sem_cadastro7hrs

load_dotenv()

#Configurações iniciais
logpath = LOG_PATH.format(filename = "atendimentos.log")
logger.add(sink = logpath, format=LOG_FORMAT)
script_name = os.path.basename(__file__)
filepath = CREATED_FILES_PATH.format(script_folder = script_name[:-3])
os.makedirs(filepath, exist_ok=True)

logger.info(INFO[100].format(script_name = script_name))

try:
    #Cria conexao com o banco
    conexao = cria_conn('CONEXAO')

    
    #Altera a query de acordo com a hora atual
    if time.localtime().tm_hour == 12:
        query = atendimentos_sem_cadastro12hrs
        corpo = "Prezados,\n\n\nIdentificamos no sistema GSAN que no dia de hoje foram abertos {numero_registros} registros de atendimento(RA){unidade} em que os clientes usuários vinculados as matrículas dos RA não tiveram os seus dados cadastrais (cpf, telefone) atualizados."

    else:
        query = atendimentos_sem_cadastro7hrs
        corpo = "Prezados,\n\n\nIdentificamos no sistema GSAN que no dia de ontem no horário compreendido entre 12:00 e 00:00 foram abertos {numero_registros} registros de atendimento(RA){unidade} em que os clientes usuários vinculados as matrículas dos RA não tiveram os seus dados cadastrais (cpf, telefone) atualizados."
    
    df_geral = consulta_banco(query, conexao)

    # Exclui coluna indesejada
    df_geral.drop('email_usuario_gsan', axis=1, inplace=True)


    #Nome dos arquivos
    atendimento_geral = "atendimentos-geral.csv"
    atendimento_01 =  "atendimentos-unidade-31501.csv"
    atendimento_02 =  "atendimentos-unidade-31502.csv"

    #Se a query não retornar registros, interrompe a execução do script
    if df_geral.empty:
        logger.info("Não há atendimentos com cadastro incompleto.")
        logger.info(INFO[102].format(script_name = script_name))
        sys.exit(1)

    #Cria o csv de atendimento de ambas as unidades
    path_geral = cria_arquivo(df_geral, '.csv', filepath, atendimento_geral)

    #Cria Dataframes separados com base na unidade
    df_01 = df_geral.query("unidade_origem == 31501")
    df_02 = df_geral.query("unidade_origem == 31502")

    df01_ok = False
    df02_ok = False

    #Cria csvs para cada unidade
    if df_01.empty is False:
        df01_ok = True
        path_01 = cria_arquivo(df_01, '.csv', filepath, atendimento_01)

    if df_02.empty is False:
        df02_ok = True
        path_02 = cria_arquivo(df_02, '.csv', filepath, atendimento_02)


    #Envio dos emails
    remetente = os.getenv("SGPC")
    senha = os.getenv("SENHA_SGPC")

    destinatarios = [
        os.getenv("DIEGO"),
        os.getenv("VALMAN"),
        os.getenv("ATEND_1"),
        os.getenv("ATEND_2"),
        os.getenv("ATEND_3"),
        os.getenv("ATEND_4"),
        os.getenv("ATEND_5"),
    ]

    uni31501 = os.getenv("UNI_31501")
    uni31502 = os.getenv("UNI_31502")

    titulo = 'RAs DO ATENDIMENTO - CLIENTE NÃO ATUALIZADO'

    #Envia o csv geral
    for destinatario in destinatarios:
        corpo_ = corpo.format(numero_registros = len(df_geral), unidade = '')
        envia_email(remetente, senha, destinatario, titulo, corpo_, path_geral)

    #Caso o Dataframe da unidade 31501 não for vazio, cria o csv e envia para o email especifico
    if df01_ok:
        corpo_ = corpo.format(numero_registros = len(df_01), unidade = " na unidade 31501")
        envia_email(remetente, senha, uni31501, titulo, corpo_, path_01)

    #Mesma coisa abaixo para a unidade 31502
    if df02_ok:
        corpo_ = corpo.format(numero_registros = len(df_02), unidade = " na unidade 31502")
        envia_email(remetente, senha, uni31502, titulo, corpo_, path_02)

except Exception as e:
    print("Exceção: ", e)

finally:
    logger.info(INFO[102].format(script_name = script_name))