# Documentação do Script `capacidade_hidrometro.py`

## 🎯 Objetivo

O objetivo deste script é realizar uma consulta específica no banco de dados para obter um relatório analítico de hidrômetros com capacidade igual ou superior a 4 metros. Após a extração dos dados, o script gera um arquivo CSV e o envia por e-mail para um destinatário específico.

## ⚙️ Etapas de Execução

O script é simples e direto, seguindo um fluxo linear de execução.

### 1. Configuração Inicial e Ambiente

* **Importações:** O script importa as bibliotecas e módulos necessários, incluindo `os`, `loguru`, `dotenv` e as funções auxiliares do pacote `utilities`.
* **Configuração de Logs:** Inicializa o `loguru` para registrar a execução do script no arquivo `capacidade.log`, permitindo o acompanhamento de suas atividades.
* **Variáveis de Ambiente:** Carrega configurações de um arquivo `.env`, uma prática recomendada para gerenciar credenciais e outras informações de forma segura.
* **Estrutura de Diretórios:** Garante que o diretório de destino para o arquivo CSV gerado exista, criando-o se necessário para evitar erros.

### 2. Consulta e Geração do Arquivo

* **Conexão com o Banco:** Utiliza a função `cria_conn` para estabelecer uma conexão com o banco de dados.
* **Execução da Consulta:** Executa a consulta definida em `analitico_hidrometro` através da função `consulta_banco`. O resultado, contendo os dados dos hidrômetros, é armazenado em um DataFrame do Pandas.
* **Criação do CSV:** O DataFrame é salvo em um arquivo CSV com o nome fixo `hidrometros_capacidade.csv`.

### 3. Envio do Relatório por E-mail

* **Configuração do E-mail:** As credenciais do remetente, o destinatário (carregado da variável de ambiente `HELDER`), o título e o corpo do e-mail são definidos.
* **Envio:** A função `envia_email` é chamada para enviar o e-mail com o arquivo CSV (`hidrometros_capacidade.csv`) em anexo para o destinatário configurado.

### 4. Finalização e Tratamento de Erros

* **Bloco `try...except`:** Todo o fluxo principal é encapsulado em um bloco `try...except` para capturar qualquer exceção que possa ocorrer durante a execução (ex: falha na conexão com o banco).
* **Log de Conclusão:** Independentemente de sucesso ou falha, o bloco `finally` garante que uma mensagem de "Fim de execução" seja sempre registrada no arquivo de log, indicando que o script completou seu ciclo.
