# Documentação do Script `contas_altas.py`

## 🎯 Objetivo

Este script tem como finalidade consultar e relatar as "contas altas" (contas de alto valor) do estado, referentes ao mês corrente. Após extrair os dados, ele os processa, gera uma planilha em formato Excel (`.xlsx`), e a distribui por e-mail para uma lista de destinatários.

## ⚙️ Etapas de Execução

O script segue um fluxo de trabalho bem definido, desde a preparação do ambiente até a notificação final.

### 1. Configuração Inicial e Ambiente

* **Importações:** Importa as bibliotecas necessárias, incluindo `os`, `datetime`, `loguru` e as funções e constantes auxiliares do pacote `utilities`.
* **Configuração de Logs:** Inicializa o `loguru` para registrar a execução do script no arquivo `contas_altas.log`.
* **Estrutura de Diretórios:** Garante que o diretório de destino para a planilha gerada exista, criando-o se necessário.
* **Variáveis de Ambiente:** Carrega configurações de um arquivo `.env` para gerenciar de forma segura informações como credenciais de e-mail e endereços dos destinatários.

### 2. Consulta e Processamento de Dados

* **Conexão com Banco:** Utiliza a função `cria_conn` para estabelecer uma conexão com o banco de dados.
* **Definição do Período:** O script obtém o ano e o mês atuais e os formata em uma string (ex: `202409`) que será usada para filtrar a consulta.
* **Execução da Consulta:** A query (`contas_altas`) é formatada com a data do período e executada. Os resultados são carregados em um DataFrame do Pandas.
* **Processamento do DataFrame:**
  * A coluna `'Referencia'`, considerada desnecessária, é removida (`drop`).
  * Os dados são ordenados pela coluna `"Valor da Conta"` em ordem decrescente, para que as contas de maior valor apareçam primeiro.

### 3. Geração do Relatório em Excel

* **Nomeação do Arquivo:** O nome do arquivo de saída é gerado dinamicamente para incluir a data completa da execução (ex: `Contas Altas 24.07.2025.xlsx`).
* **Criação do Arquivo:** O DataFrame processado é salvo em uma planilha do Excel no caminho previamente definido.

### 4. Distribuição por E-mail

* **Configuração do E-mail:** As credenciais do remetente e a lista de destinatários (carregada das variáveis de ambiente) são preparadas. O assunto do e-mail é o próprio nome do arquivo, sem a extensão `.xlsx`.
* **Loop de Envio:** O script itera sobre a lista de destinatários, enviando uma cópia do e-mail com a planilha em anexo para cada um.

### 5. Sistema de Notificação

* **Controle de Falhas:** O script mantém uma lista (`emails_nao_enviados`) para rastrear quaisquer falhas no envio.
* **Alerta de Falha:** Se a lista de falhas não estiver vazia ao final do loop, um e-mail de alerta é enviado a um contato de suporte, informando quais destinatários não receberam o relatório.
* **Confirmação de Sucesso:** Se todos os e-mails forem enviados com sucesso, uma notificação de confirmação é enviada para o mesmo contato de suporte.

### 6. Finalização e Tratamento de Erros

* **Bloco `try...except`:** Todo o fluxo principal está encapsulado para capturar exceções, garantindo que o script não seja interrompido abruptamente e que os erros sejam registrados.
* **Log de Conclusão:** O bloco `finally` garante que, independentemente do resultado, uma mensagem de "Fim de execução" seja sempre registrada no log.
