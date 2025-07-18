# Documentação do Script de Processamento e Importação de Usuários para o ArcGIS

Este script em Python foi projetado para automatizar a preparação de uma lista de usuários para importação no ArcGIS. Ele lê dados de um arquivo CSV de origem, os mapeia para um arquivo de modelo (template), gera senhas, formata nomes e traduz papéis (roles) e tipos de usuário para os valores esperados pelo sistema de destino.

## 📜 Visão Geral

O script realiza as seguintes operações:
1.  **Carrega Dados:** Lê dois arquivos CSV: um com a lista de usuários original (`usuarios_arcgis.csv`) e outro que serve como modelo para o arquivo final (`template.csv`).
2.  **Mapeia Colunas:** Copia os dados relevantes (Email, Papel, Tipo de Usuário, Nome, Nome de Usuário) do arquivo original para as colunas correspondentes no modelo.
3.  **Processa e Transforma Dados:**
    * Extrai o sobrenome a partir do nome completo.
    * Gera uma senha forte e segura para cada usuário.
    * Converte os valores das colunas "Tipo de Usuário" e "Papel" para o formato exigido pelo novo sistema.
4.  **Exporta o Resultado:** Salva o DataFrame processado em um novo arquivo CSV (`final_usuarios_arcgis.csv`), pronto para ser importado.

## 📦 Dependências

-   **Python 3.x**
-   **Pandas:** Para manipulação de dados e operações com CSV.
    ```bash
    pip install pandas
    ```
-   **utils.password_generator:** Um módulo customizado que deve conter a função `generate_strong_password()`. Certifique-se de que este módulo esteja acessível no caminho do Python.

## 📁 Estrutura de Arquivos

O script espera a seguinte estrutura de arquivos para funcionar corretamente:

```
.
├── import_users_arcgis.py
├── usuarios_arcgis.csv     # Arquivo de ENTRADA com os dados dos usuários.
├── template.csv            # Arquivo de ENTRADA com o cabeçalho do arquivo final.
└── utils/
    └── password_generator.py # Módulo que contém a função de gerar senha.
```

O arquivo de saída, `final_usuarios_arcgis.csv`, será gerado no diretório `dados/resultado/` relativo à localização do script.

## ⚙️ Detalhamento do Código

### Inicialização e Carregamento

-   **Importações:** Importa as bibliotecas `os` e `pandas`, além da função `generate_strong_password`.
-   **Definição de Nomes de Arquivos:** As variáveis `arquivo_usuarios`, `arquivo_template` e `arquivo_final` definem os nomes dos arquivos de entrada e saída.
-   **Leitura de CSV:** Os arquivos `usuarios_arcgis.csv` e `template.csv` são lidos e carregados em DataFrames do Pandas.

### Mapeamento e População de Dados

-   **Dicionário `cabecalho`:** Este dicionário é crucial, pois mapeia os nomes das colunas do arquivo de origem (`df_usuarios`) para os nomes das colunas no arquivo de destino (`df_template`).
-   **Loop de Preenchimento:** Um loop `for` itera sobre o dicionário `cabecalho` para copiar os dados da origem para o destino, coluna por coluna.

### Funções de Transformação

O script define quatro funções principais que são aplicadas a cada linha do DataFrame:

1.  **`preencher_sobrenome(row)`**
    -   **Objetivo:** Extrair o último nome do campo "Nome".
    -   **Lógica:** Pega o valor da coluna `Nome`, remove espaços extras no início/fim (`strip()`), divide a string em uma lista de palavras e retorna o último elemento (`[-1]`).

2.  **`criar_senha(row)`**
    -   **Objetivo:** Gerar uma senha segura.
    -   **Lógica:** Chama a função externa `generate_strong_password()` e atribui o resultado à coluna `Senha`.

3.  **`renomear_usertype(row)`**
    -   **Objetivo:** Traduzir os códigos de "Tipo de Usuário" para um formato legível.
    -   **Lógica:** Utiliza uma estrutura `match-case` (similar a um `switch`) para converter `viewerUT` em "Viewer" e `creatorUT` em "Creator".

4.  **`renomear_role(row)`**
    -   **Objetivo:** Traduzir os códigos de "Papel" (Role) para um formato legível.
    -   **Lógica:** Também usa `match-case` para converter valores como `account_publisher` para "Publicador", `account_user` para "Usuário", etc.

### Aplicação das Funções e Exportação

-   **`df.apply()`:** As funções de transformação são aplicadas ao DataFrame `df_template` usando o método `.apply(..., axis=1)`, que itera sobre cada linha.
-   **`df.to_csv()`:** O DataFrame final, agora formatado e completo, é salvo no arquivo `final_usuarios_arcgis.csv