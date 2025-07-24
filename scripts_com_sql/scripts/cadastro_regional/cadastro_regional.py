import datetime
import os

from dotenv import load_dotenv
from loguru import logger
from utilities.constantes import CREATED_FILES_PATH, LOG_FORMAT, LOG_PATH, REMETENTE_SGGP, SENHA_SGGP
from utilities.helpers import consulta_banco, cria_conn, cria_arquivo, envia_email 
from utilities.messages import INFO, ERROR
from utilities.querys import cadastro_regional

load_dotenv()

#Configurações iniciais
logger.add(sink = LOG_PATH.format(filename = "cadastro_regional.log"), format=LOG_FORMAT)
script_name = os.path.basename(__file__)
filepath = CREATED_FILES_PATH.format(script_folder = script_name[:-3])
os.makedirs(filepath, exist_ok=True)

logger.info(INFO[100].format(script_name = script_name))

#Configurações de email
remetente = REMETENTE_SGGP
senha = SENHA_SGGP
destinatarios = {
    1 : os.getenv("LITORAL"),
    2 : os.getenv("BORBOREMA"),
    3 : os.getenv("BREJO"),
    4 : os.getenv("ESPINHARIAS"),
    5 : os.getenv("RIO_DO_PEIXE"),
    6 : os.getenv("ALTO_PIRANHAS"),
}
regionais = {
    1:'LITORAL',
    2:'BORBOREMA',
    3:'BREJO',
    4:'ESPINHARAS',
    5:'RIO DO PEIXE',
    6:'ALTO PIRANHAS',
}

try:
    #Conexão com o banco
    conexao = cria_conn('CONEXAO')

    for i in range(1,7):
        #Consulta no banco
        query = cadastro_regional.format(id_regional = i)
        df = consulta_banco(query, conexao)

        if df.empty is False:
            
            #Altera o nome do arquivo e o corpo do email dependendo do dia.
            if datetime.date.today().strftime('%A') == 'Monday':
                arquivo = f'Regional_{regionais[i]}_SEGUNDA.csv'
                corpo = f'Bom dia!\nSegue planilha com as ligações novas sem coordenadas geográficas no GSAN do regional {regionais[i]}'

            elif datetime.date.today().strftime("%A") == 'Friday':
                arquivo = f'Regional_{regionais[i]}_SEXTA.csv'
                corpo = f'Boa tarde!\nSegue planilha com as ligações novas sem coordenadas geográficas no GSAN do regional {regionais[i]} que não foram atualizadas essa semana.'
            else:
                arquivo = 'Relacao_ligacoes_gerais_TESTE.csv'
                corpo = 'TESTE.csv'

            path = cria_arquivo(df,'.csv', filepath, arquivo)

            envia_email(
                remetente,
                senha,
                destinatarios[i],
                assunto= 'Ligações novas sem coordenadas.',
                corpo=corpo,
                arquivos_anexos=path
            )

        else: 
            continue
    
except Exception as e:
    logger.error(ERROR[404].format(exception_msg = e))
    logger.critical(INFO[500])
    exit(1)

logger.info(INFO[102].format(script_name = script_name))

