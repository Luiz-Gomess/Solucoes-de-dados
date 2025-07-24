import os
import sys
import pandas as pd
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy import Engine

from loguru import logger
from utilities.messages import INFO, ERROR, SUCESS, CRITICAL
from dotenv import load_dotenv

load_dotenv()


def formatar_valor(valor: float) -> str:
    """Formata um valor numérico para o padrão brasileiro. 
        Ex.: 100000000.00 -> 100.000.000,00

    Args:
        valor (float): Valor numérico 

    Returns:
        str: Valor numérico formatado.
    """
    return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def cria_conn(env_var: str) -> Engine:
    """
    Cria a conexão com o banco

    Args:
        env_var (str): Nome da variável da ambiente com a conexão ao banco.

    Returns:
        Engine: Conexão estabelecida com o banco.
    """
    try:
        conexao = os.getenv(env_var)
        engine = create_engine(conexao) 

        logger.info(INFO[101])

        return engine

    except Exception as e:
        logger.error(ERROR[400].format(exception_msg = e))
        logger.critical(CRITICAL[500])

        #Encerra a execução do script
        sys.exit(1)


def consulta_banco(query: str, conexao: Engine) -> DataFrame:
    """
    Faz a consulta ao banco e retorna um DataFrame

    Args:
        query (str): Consulta a ser executada.
        conexao (Engine): Conexão estabelecida com o banco.

    Returns:
        DataFrame: DataFrame com os dados consultados.
    """
    try:
        logger.info(INFO[104])
        df = pd.read_sql(query, conexao)
        logger.success(SUCESS[200])

        return df

    except Exception as e:
        logger.error(ERROR[401].format(exception_msg = e))
        logger.critical(CRITICAL[500])
        sys.exit(1)


def cria_arquivo(df: DataFrame, file_extension: str, path: str, filename: str , columns: list = None) -> str:
    """
    Cria um arquivo com a extensão e o caminho fornecidos.

    Args:
        df (DataFrame): DataFrame a ser tranformado em arquivo.
        file_extension (str): Extensão do arquivo. Ex.: '.csv', '.xlsx'
        path (str): Caminho do arquivo.
        filename (str): Nome do arquivo.
    """
    try:

        path = os.path.join(path, filename)

        if file_extension == '.csv':
            df.to_csv(path, columns=columns, index=False)
        elif file_extension == '.xlsx':
            df.to_excel(path, columns=columns, index=False)

        logger.success(SUCESS[201].format(filename = filename))

        return path

    except Exception as e:
        logger.error(ERROR[402].format(filename = filename, exception_msg = e))
        logger.critical(CRITICAL[500])

        #Encerra a execução do script
        sys.exit(1)



class EmailException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

def envia_email(remetente:str, senha:str, destinatario:str, assunto:str, corpo:str, arquivos_anexos:list[str] | str =None):
    """ Envia e-mail.

    Args:
        remetente (str): E-mail de quem envia.
        senha (str): Senha do e-mail de origem. Deve ser gerada uma senha de app conforme tutorial https://support.google.com/mail/answer/185833?hl=pt-BR.
        destinatario (str): E-mail do destinatário.
        assunto (str): Título.
        corpo (str): Conteúdo.
        arquivo_anexo (str, optional): Caminho de um arquivo a ser enviado. Padrão = None.
    """
    # Configurações do email

    # Criação do objeto de mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    # Corpo do email
    msg.attach(MIMEText(corpo, 'plain'))

    # Anexo
    if arquivos_anexos:
        with open(arquivos_anexos, "rb") as anexo:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(anexo.read())
            encoders.encode_base64(part)
            filename = os.path.basename(arquivos_anexos)  # Obtém o nome correto do arquivo
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            msg.attach(part)
            
    # Conexão com o servidor SMTP do Gmail
    try:
       
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()  # Inicializa a conexão TLS
        servidor.login(remetente, senha)
        texto = msg.as_string()
        servidor.sendmail(remetente, destinatario, texto)
        servidor.quit()
        logger.info(SUCESS[202].format(email = destinatario.split("@")[0][:3]) + (destinatario.split("@")[0][3:].replace(destinatario.split("@")[0][3:], "*********")) + (destinatario.split("@")[1]))
        return True
    
    except smtplib.SMTPException as smtpe:
        logger.error(ERROR[403].format(exception_msg = smtpe))
        return False
    
    except Exception as e:
        print(e.with_traceback())
        logger.error(ERROR[404].format(exception_msg = e))
        return False
        
