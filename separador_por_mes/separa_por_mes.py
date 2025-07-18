"""
Filename: separa_por_mes.py
Description: Separa os arquivos criados pelo script contas_altas.py em pastas pelo 
             numero do mês presente no nome.
             Ex.: 
             --- contas_altas/'Contas Altas 22.01.2025.xlsx' -->
             --> contas_altas_reformed/01/'Contas Altas 22.01.2025.xlsx'

"""

import os 
import shutil

origin_dir = os.path.join(os.path.dirname(__file__), "contas_altas")
destiny_dir = os.path.join(os.path.dirname(__file__), "contas_altas_reformed")


for file in os.listdir(origin_dir): # --> 'Contas Altas 22.01.2025.xlsx'
    
    filedate = file.split(" ")[-1] # -->'22.01.2025.xlsx'
    raw_date = filedate.removesuffix(".xlsx") # --> '22.01.2025' 
    _, month, _ = list(map(str, raw_date.split("."))) #  month -->  01

    #Une o caminho de origem ao arquivo da iteração
    origin_file = os.path.join(origin_dir, file)

    #Une o caminho de destino ao mês do arquivo da iteração
    destiny_file = os.path.join(destiny_dir, month)

    try:
        #Cria o caminho de destino 
        os.makedirs(destiny_file, exist_ok=True)
        #Move o arquivo para a pasta do seu mês
        print(shutil.move(src= origin_file, dst= os.path.join(destiny_file, file)))

    except OSError as oe:
        print(oe)

