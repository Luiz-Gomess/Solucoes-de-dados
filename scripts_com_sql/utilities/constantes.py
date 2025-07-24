import os
from dotenv import load_dotenv

load_dotenv()

CREATED_FILES_PATH = os.path.join(os.path.expanduser('~'),'cron_created_data','{script_folder}')

LOG_PATH = os.path.join(os.path.expanduser('~'), "script_com_sql", "logs", "{filename}")
LOG_FORMAT = "{time:DD/MM/YYYY HH:mm:ss} - {level} - {message}"

REMETENTE_SGGP = os.getenv("REMETENTE")
SENHA_SGGP = os.getenv("SENHA")

LUIZ = os.getenv("luiz")
SENHA_LUIZ = os.getenv("senha_luiz")

REMETENTE_ASSIST_GEGM = os.getenv("assist_gegm")
SENHA_ASSIST_GEGM = os.getenv("SENHA_ASSIST")

DESTINATARIO_ASSIST_GEGM = REMETENTE_ASSIST_GEGM
DESTINATARIO_GEGM = os.getenv("gegm")



