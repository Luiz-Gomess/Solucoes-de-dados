# Documentação do Script `cadastro_geral.py`

## 🎯 Objetivo

Este script tem como objetivo consultar a quantidade de ligações de serviços que não possuem coordenadas geográficas registradas no sistema. Ele agrupa esses dados por regional, gera uma tabela visual e a envia por e-mail para os responsáveis de cada regional, com um conteúdo que varia de acordo com o dia da semana.

## ⚙️ Etapas de Execução

O script é estruturado nas seguintes etapas:

### 1. Configuração Inicial e Ambiente

* **Importações:** O script importa as bibliotecas necessárias, incluindo `os` para manipulação de caminhos, `datetime` para obter o dia da semana, `plotly` para a criação de gráficos (tabelas) e `loguru` para logs. Também são importados módulos auxiliares do pacote `utilities`.
* **Variáveis de Ambiente:** Carrega configurações de um arquivo `.env` usando `load_dotenv()`, permitindo que informações como credenciais de e-mail e endereços dos destinatários sejam gerenciadas de forma segura.
* **Configuração de Logs:** Inicializa o `loguru` para registrar os eventos de execução em um arquivo (`cadastro_geral.log`), o que facilita o monitoramento e a depuração do script.
* **Criação de Diretório:** O script verifica se o diretório de destino para a imagem da tabela existe e o cria se necessário, prevenindo erros ao salvar o arquivo.

### 2. Lógica Baseada no Dia da Semana

O comportamento do script é dinâmico e muda de acordo com o dia da semana em que é executado.

* **Segunda-feira (`Monday`):** O nome do arquivo gerado será `Relacao_ligacoes_gerais_SEGUNDA.png`, e o corpo do e-mail informa sobre o quantitativo geral da semana.
* **Sexta-feira (`Friday`):** O nome do arquivo será `Relacao_ligacoes_gerais_SEXTA.png`, e o corpo do e-mail é focado nas ligações que não foram atualizadas durante a semana.
* **Outros Dias:** Para qualquer outro dia, o script assume um modo de "teste", gerando um arquivo com o sufixo `_TESTE.png`.

### 3. Consulta ao Banco de Dados

* **Conexão:** Utiliza a função auxiliar `cria_conn` para estabelecer uma conexão com o banco de dados.
* **Execução da Consulta:** A query, definida no módulo `utilities.querys`, é executada pela função `consulta_banco`. O resultado, contendo os dados das ligações agrupadas por regional, é armazenado em um DataFrame do Pandas.

### 4. Geração da Tabela Visual

* **Criação da Figura:** O script usa a biblioteca `plotly.graph_objects` para transformar os dados do DataFrame em uma tabela visualmente agradável.
* **Estilização:** O cabeçalho e as células da tabela são estilizados com cores (`paleturquoise` e `lavender`) para melhorar a legibilidade.
* **Layout e Exportação:** O layout da figura é ajustado (largura e altura) e, em seguida, a tabela é salva como uma imagem no formato **PNG** no diretório de destino.

### 5. Distribuição por E-mail

* **Configuração:** As credenciais do remetente e a lista de destinatários (carregada das variáveis de ambiente) são preparadas para o envio.
* **Loop de Envio:** O script itera sobre a lista de destinatários e envia um e-mail para cada um, contendo o assunto definido e a imagem da tabela como anexo.
* **Sistema de Notificação:**
  * Se o envio para algum destinatário falhar, o script coleta os endereços com falha e envia um **e-mail de alerta** para um contato de suporte.
  * Se todos os e-mails forem enviados com sucesso, um **e-mail de confirmação** é enviado para o mesmo contato de suporte.

### 6. Finalização e Tratamento de Erros

* **Bloco `try...except`:** Todo o fluxo principal é encapsulado em um bloco `try...except` para garantir que qualquer erro durante a execução seja capturado e registrado, permitindo que o script finalize de forma controlada.
* **Log de Conclusão:** Ao final da execução, uma mensagem indicando o término do script é registrada no arquivo de log.
