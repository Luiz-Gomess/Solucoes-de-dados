# Documentação do Script `separa_por_mes.py`

## 📄 Descrição

Este script organiza arquivos `.xlsx` de uma pasta de origem em subpastas na pasta de destino. O critério para a organização é o número do mês extraído do nome de cada arquivo.

-   **Nome do Arquivo:** `separa_por_mes.py`
-   **Função:** Mover arquivos de `contas_altas/` para `contas_altas_reformed/` criando subpastas numeradas por mês.
-   **Exemplo de Operação:**
    -   **Arquivo de Origem:** `contas_altas/Contas Altas 22.01.2025.xlsx`
    -   **Resultado:** O arquivo é movido para `contas_altas_reformed/01/Contas Altas 22.01.2025.xlsx`

## 📦 Dependências

Este script utiliza apenas bibliotecas padrão do Python, portanto **não há necessidade de instalar pacotes externos**.
-   `os`: Para manipulação de caminhos de arquivos e diretórios.
-   `shutil`: Para realizar a operação de mover arquivos.

## 📁 Estrutura de Diretórios

O script espera uma estrutura específica para funcionar e irá gerar uma nova estrutura como saída.

### Antes da Execução

O script deve estar no mesmo nível que o diretório de origem `contas_altas`.

```
.
├── separa_por_mes.py
└── contas_altas/
    ├── Contas Altas 22.01.2025.xlsx
    ├── Contas Altas 15.02.2025.xlsx
    └── Contas Altas 30.01.2025.xlsx
```

### Depois da Execução

O script criará o diretório `contas_altas_reformed` e as subpastas necessárias para organizar os arquivos.

```
.
├── separa_por_mes.py
├── contas_altas/
│   (vazio)
└── contas_altas_reformed/
    ├── 01/
    │   ├── Contas Altas 22.01.2025.xlsx
    │   └── Contas Altas 30.01.2025.xlsx
    └── 02/
        └── Contas Altas 15.02.2025.xlsx
```

## ⚙️ Detalhamento do Código

### 1. Importações e Definição de Caminhos

-   O script importa as bibliotecas `os` e `shutil`.
-   **`origin_dir`**: Define o caminho completo para a pasta de origem (`contas_altas`). `os.path.dirname(__file__)` garante que o caminho é relativo à localização do script.
-   **`destiny_dir`**: Define o caminho completo para a pasta de destino (`contas_altas_reformed`).

### 2. Loop e Processamento de Arquivos

-   `for file in os.listdir(origin_dir):`: O script itera sobre cada arquivo encontrado no diretório de origem.

-   **Extração do Mês:** Para cada arquivo, o mês é extraído do nome através de uma série de passos:
    1.  `file.split(" ")[-1]`: Isola a parte da data e extensão do nome do arquivo. Ex: `'22.01.2025.xlsx'`.
    2.  `.removesuffix(".xlsx")`: Remove a extensão do arquivo. Ex: `'22.01.2025'`.
    3.  `raw_date.split(".")`: Divide a data em uma lista de strings. Ex: `['22', '01', '2025']`.
    4.  `_, month, _ = ...`: Desempacota a lista, atribuindo o segundo elemento (o mês) à variável `month`. Os outros valores (dia e ano) são descartados.

### 3. Movendo os Arquivos

-   **`origin_file`**: Monta o caminho completo do arquivo de origem que será movido.
-   **`destiny_file`**: Monta o caminho do diretório de destino, que é a pasta base (`contas_altas_reformed`) mais a subpasta do mês (ex: `01`).
-   **Bloco `try...except`**: Garante que o script não pare caso ocorra um erro de sistema operacional.
    -   `os.makedirs(destiny_file, exist_ok=True)`: Cria o diretório do mês (ex: `contas_altas_reformed/01`). O parâmetro `exist_ok=True` previne um erro caso o diretório já exista.
    -   `shutil.move(...)`: Move o arquivo da origem para o seu novo diretório de destino.
    -   `print(...)`: Imprime o caminho final do arquivo movido para confirmar a operação.

## ▶️ Como Usar

1.  Salve o código como `separa_por_mes.py`.
2.  Crie um diretório chamado `contas_altas` no mesmo local do script.
3.  Popule o diretório `contas_altas` com os arquivos `.xlsx` que seguem o padrão de nome `Nome Qualquer DD.MM.YYYY.xlsx`.
4.  Execute o script a partir do terminal:
    ```bash
    python separa_por_mes.py
    ```
5.  Ao final da execução, um novo diretório chamado `contas_altas_reformed` conterá os arquivos organizados em subpastas por mês.

## 🐍 Código do Script

```python
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
```