INFO = {
    100 : "Iniciando {script_name}",
    101 : "Conexão com o banco estabelecida.",
    102 : "{script_name} finalizado. \n",
    103 : "Email de notificação enviado para Diego.",
    104 : "Iniciando consulta",

}

SUCESS = {
    200 : "Consulta realizada com sucesso.", 
    201 : "'{filename}' criado com sucesso!",
    202 : "Email enviado para: {email}"
}

ERROR = {
    400 : "Não foi possível estabelecer a conexão: {exception_msg}",
    401 : "Não foi possível realizar a consulta: {exception_msg}",
    402 : "Não foi possível criar o arquivo {filename}: {exception_msg}",
    403 : "Não foi possível enviar o email: {exception_msg}",
    404 : "Houve um erro insperado: {exception_msg}",
}
CRITICAL = {
    500 : "Interrompendo execução do script.",
}
