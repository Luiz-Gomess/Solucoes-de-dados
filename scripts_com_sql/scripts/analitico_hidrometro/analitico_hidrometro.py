"""
Filename: analitico_hidrometro.py
Description: Consulta os dados dos hidrômetros, cria um csv e envia por email.
"""
import os

from loguru import logger
from dotenv import load_dotenv

from utilities.helpers import consulta_banco, cria_conn, cria_arquivo, envia_email
from utilities.constantes import LOG_PATH, LOG_FORMAT, CREATED_FILES_PATH, REMETENTE_ASSIST_GEGM, SENHA_ASSIST_GEGM, DESTINATARIO_ASSIST_GEGM, DESTINATARIO_GEGM, LUIZ, SENHA_LUIZ
from utilities.messages import INFO
from utilities.querys import analitico_jonas

#Configurações iniciais
logpath = LOG_PATH.format(filename = "analitico_jonas.log")
logger.add(sink = logpath, format=LOG_FORMAT)
script_name = os.path.basename(__file__)
filepath = CREATED_FILES_PATH.format(script_folder = script_name[:-3])
os.makedirs(filepath, exist_ok=True)

load_dotenv()

logger.info(INFO[100].format(script_name = script_name))


def formata(lista:list[str]) -> str:
    """
    Recebe uma lista de strings e substitui os espaços em branco por \ .

    Args:
        lista (list[str]): lista de strings.

    Returns:
        str: String com todas os elementos concatenados e os espaços das 
            strings substituidas por \ .
    """
    texto = ''
    for elemento in lista:
        texto += elemento.replace(" ", "\ ") + ' '
    return texto


try:

    regionais = {
        1:'LITORAL',
        2:'BORBOREMA',
        3:'BREJO',
        4:'ESPINHARAS',
        5:'RIO DO PEIXE',
        6:'ALTO PIRANHAS',
    }

    #Conexão com o banco
    CONEXAO = cria_conn('CONEXAO')

    arquivo_litoral_tar = os.path.join(filepath, "analitico_LITORAL.tar.xz")
    comando_para_compactar = "tar -cJvf {arquivo_tar} -C {pasta_arquivo} {arquivo}"
    
    lista_arquivos = []

    ## Endereços para testes
    # remetente = LUIZ
    # senha = SENHA_LUIZ
    # destinatarios = [
    #     LUIZ
    # ]

    remetente = REMETENTE_ASSIST_GEGM
    senha = SENHA_ASSIST_GEGM
    destinatarios = [
        DESTINATARIO_ASSIST_GEGM,
        DESTINATARIO_GEGM
    ]

    for i in range(1,7):
        df = consulta_banco(conexao=CONEXAO, query=analitico_jonas.format(id_regional = i))
    
        filename = f"analitico_hidrometros_{regionais[i]}.csv"
        path = cria_arquivo(df, '.csv', filepath, filename)

        if i == 1:
            os.system(comando_para_compactar.format(
                arquivo_tar=arquivo_litoral_tar, 
                pasta_arquivo=os.path.dirname(path), 
                arquivo=os.path.basename(path))
                )
            
            titulo_litoral = "Analitico de Hidrômetros do LITORAL"
            corpo_litoral = "Bom dia, \n\n\n Segue analítico de hidrômetros do LITORAL." #TODO: Corpo temporário
 
            continue
        
        lista_arquivos.append(os.path.basename(path))


    # Compacta o resto dos arquivos
    os.system(comando_para_compactar.format(
        arquivo_tar = "analitico_regionais.tar.xz",
        pasta_arquivo = os.path.dirname(path),
        arquivo= formata(lista_arquivos)
    ))

    #E-mail
    
    titulo = f"Analitico de Hidrômetros das Regionais" 
    corpo = "Bom dia, \n\n\n Segue analítico de hidrômetros das regionais." 
    
    for destinatario in destinatarios:
        envia_email(
            remetente,
            senha,
            destinatario,
            titulo_litoral,
            corpo_litoral,
            arquivo_litoral_tar)  
        
        envia_email(
            remetente,
            senha,
            destinatario,
            titulo,
            corpo,
            "analitico_regionais.tar.xz")

    os.remove("analitico_regionais.tar.xz")    

except Exception as e:
    print("Exceção: ", e.with_traceback())

finally:
    logger.info(INFO[102].format(script_name = script_name))