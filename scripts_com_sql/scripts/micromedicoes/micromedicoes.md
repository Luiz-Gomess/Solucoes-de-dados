# Documentação do Script `micromedicoes.py`

## 🎯 Objetivo

Este script automatiza a extração de dados de "micromedições" de um banco de dados, gera um relatório em formato CSV e o distribui por e-mail para destinatários pré-definidos. A principal característica do script é sua capacidade de ajustar o período do relatório (mês atual ou mês anterior) com base no dia do mês em que é executado.

## ⚙️ Etapas de Execução

O script opera em uma sequência clara de passos, desde a configuração inicial até o envio das notificações.

### 1. Configuração Inicial e de Ambiente

* **Importações:** Importa as bibliotecas necessárias, incluindo `os` para manipulação de caminhos, `datetime` e `dateutil` para cálculos de data, e `loguru` para registro de logs. Também importa módulos de um pacote `utilities`, que contém funções auxiliares (como `cria_conn`, `envia_email`) e constantes.
* **Variáveis de Ambiente:** Utiliza `load_dotenv()` para carregar configurações de um arquivo `.env`. Isso permite que dados como credenciais de banco e e-mail sejam gerenciados fora do código-fonte, uma prática recomendada para segurança.
* **Configuração de Logs:** Inicializa o `loguru` para salvar os registros de execução em um arquivo (`micromedicoes.log`), o que é essencial para monitorar o comportamento do script e diagnosticar problemas.
* **Estrutura de Diretórios:** O script cria automaticamente a pasta de destino para o arquivo de relatório, garantindo que o caminho exista antes de tentar salvar o arquivo.

### 2. Lógica de Datas e Período do Relatório

Esta é a parte central da lógica de negócios do script.

* **Cálculo de Datas:** O script determina a data atual, o primeiro dia do mês e, crucialmente, o **quarto dia útil** do mês.
* **Definição do Período:** A lógica condicional (`if data_atual.day < int(quatro_dias_uteis)`) verifica se a execução está ocorrendo antes do quarto dia útil.
  * Se  **sim** , o script entende que o "mês de trabalho" ainda não virou, então ele ajusta as datas para gerar o relatório referente ao  **mês anterior** .
  * Se  **não** , ele gera o relatório para o  **mês atual** , buscando dados desde o primeiro dia do mês corrente.
* **Cláusula `WHERE` Dinâmica:** Com base na lógica acima, uma cláusula `WHERE` para a consulta SQL é montada dinamicamente para filtrar os registros no período de tempo correto.

### 3. Interação com o Banco de Dados

* **Conexão:** Uma função auxiliar, `cria_conn`, é usada para estabelecer a conexão com o banco de dados.
* **Execução da Consulta:** A consulta SQL, formatada com a `clausula_where` dinâmica, é executada através da função `consulta_banco`. O resultado é retornado e armazenado em um DataFrame do Pandas.

### 4. Geração do Relatório CSV

* **Nomeação do Arquivo:** Um nome de arquivo padronizado e descritivo é gerado, contendo o mês e o ano do relatório (ex: `10-Relatorio Diario de Mov. de Hidro - OUTUBRO.2024.csv`).
* **Criação do Arquivo:** A função `cria_arquivo` é chamada para salvar o DataFrame no arquivo CSV, no caminho previamente definido.

### 5. Envio de E-mail e Notificações

* **Configuração do E-mail:** As variáveis para remetente, senha e destinatários são definidas.
* **Conteúdo do E-mail Dinâmico:** O script personaliza o título e o corpo do e-mail. Se a execução ocorrer no dia útil anterior ao marco (o "dia do fechamento"), o e-mail é rotulado como o  **"relatório final do mês"** . Caso contrário, é tratado como um relatório diário padrão.
* **Loop de Envio:** O script itera sobre a lista de destinatários, enviando uma cópia do e-mail com o relatório em anexo para cada um.
* **Sistema de Alerta:**
  * Caso o envio para algum dos destinatários falhe, o script envia um e-mail de alerta para um endereço de suporte, listando quais e-mails não puderam ser entregues.
  * Se todos os envios forem bem-sucedidos, uma notificação de sucesso é enviada para o mesmo endereço de suporte, confirmando que a tarefa foi concluída.

### 6. Finalização e Tratamento de Erros

* **Bloco `try...except`:** Todo o fluxo principal é envolvido por um bloco de tratamento de exceções para capturar e registrar qualquer erro que possa ocorrer, evitando que o script pare abruptamente.
* **Log de Conclusão:** Ao final da execução, seja ela bem-sucedida ou não, uma mensagem de "Fim de execução" é registrada no arquivo de log.
