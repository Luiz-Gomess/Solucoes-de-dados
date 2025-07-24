# Documentação do Script `atendimentos_sem_cadastro.py`

## 🎯 Objetivo

Este script identifica Registros de Atendimento (RAs) vinculados a clientes com dados cadastrais desatualizados (como CPF e telefone). Ele consulta um banco de dados, gera relatórios em formato CSV separados por unidade de atendimento e os envia por e-mail para os responsáveis correspondentes. A lógica de consulta e o conteúdo do e-mail são adaptados de acordo com o horário de execução do script.

## ⚙️ Etapas de Execução

O script opera através da seguinte sequência de passos:

### 1. Configuração Inicial e Ambiente

* **Importações:** O script importa as bibliotecas necessárias, incluindo `os`, `sys` (para finalizar a execução), `time` (para verificar a hora), `loguru` e as funções auxiliares do pacote `utilities`.
* **Variáveis de Ambiente:** Utiliza `load_dotenv()` para carregar configurações de um arquivo `.env`, garantindo que credenciais e endereços de e-mail sejam gerenciados de forma segura.
* **Configuração de Logs:** Inicializa o `loguru` para registrar a execução do script no arquivo `atendimentos.log`.
* **Estrutura de Diretórios:** Assegura que o diretório de destino para os arquivos CSV exista, criando-o se necessário.

### 2. Lógica de Consulta Baseada no Horário

O comportamento do script é determinado pela hora em que é executado:

* **Execução às 12:00 (meio-dia):**
  * Utiliza a query `atendimentos_sem_cadastro12hrs`, que busca os registros abertos no dia corrente.
  * Define um corpo de e-mail específico para os atendimentos do dia.
* **Execução em Outros Horários (ex: 07:00):**
  * Utiliza a query `atendimentos_sem_cadastro7hrs`, que busca os registros abertos na tarde do dia anterior (entre 12:00 e 00:00).
  * Define um corpo de e-mail correspondente a esse período.

### 3. Processamento de Dados

* **Conexão e Consulta:** Estabelece uma conexão com o banco de dados e executa a query selecionada, armazenando os resultados em um DataFrame do Pandas chamado `df_geral`.
* **Limpeza de Dados:** A coluna `email_usuario_gsan`, considerada desnecessária para o relatório, é removida do DataFrame.
* **Verificação de Dados:** O script verifica se o `df_geral` está vazio. Se não houver registros, ele registra uma mensagem no log e encerra a execução com `sys.exit(1)`, evitando o processamento desnecessário.

### 4. Criação dos Arquivos CSV

* **CSV Geral:** Um arquivo CSV principal (`atendimentos-geral.csv`), contendo os dados de todas as unidades, é criado.
* **Filtragem por Unidade:** O DataFrame geral é filtrado para criar dois DataFrames menores, um para a `unidade_origem == 31501` (`df_01`) и um para a `unidade_origem == 31502` (`df_02`).
* **CSVs Específicos:** Se os DataFrames filtrados (`df_01` e `df_02`) não estiverem vazios, o script cria os respectivos arquivos CSV para cada unidade (`atendimentos-unidade-31501.csv` e `atendimentos-unidade-31502.csv`).

### 5. Envio de E-mails

O script realiza três envios de e-mail distintos:

1. **E-mail Geral:**
   * Envia o relatório geral (`atendimentos-geral.csv`) para uma lista de destinatários principais (gestores e equipe de suporte).
   * O corpo do e-mail é formatado dinamicamente para incluir o número total de registros encontrados.
2. **E-mail para Unidade 31501:**
   * Se o CSV para esta unidade foi criado, um e-mail é enviado para o endereço específico da unidade (`UNI_31501`).
   * O corpo do e-mail é personalizado com o número de registros e a identificação da unidade.
3. **E-mail para Unidade 31502:**
   * Da mesma forma, se o CSV para a unidade 31502 existe, um e-mail é enviado para o endereço correspondente (`UNI_31502`) com conteúdo personalizado.

### 6. Finalização e Tratamento de Erros

* **Bloco `try...except`:** Todo o fluxo é encapsulado para capturar exceções, registrando-as no console e permitindo que o script finalize de forma controlada.
* **Log de Conclusão:** Independentemente do resultado, uma mensagem de "Fim de execução" é gravada no arquivo de log.
