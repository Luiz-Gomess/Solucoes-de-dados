# Documentação do Script `cadastro_regional.py`

## 🎯 Objetivo

Este script foi projetado para consultar, para cada regional, a lista de ligações de serviço que ainda não possuem coordenadas geográficas registradas. Ele gera um relatório em formato CSV para cada regional com dados pendentes e o envia por e-mail para o endereço correspondente. O conteúdo do relatório e do e-mail é adaptado com base no dia da semana.

## ⚙️ Etapas de Execução

O script opera em um fluxo contínuo, iterando sobre cada regional para executar sua tarefa.

### 1. Configuração Inicial e Ambiente

* **Importações:** O script importa as bibliotecas necessárias, incluindo `os`, `datetime`, `loguru` e as funções auxiliares do pacote `utilities`.
* **Variáveis de Ambiente:** Carrega configurações de um arquivo `.env` para gerenciar de forma segura informações como senhas e endereços de e-mail.
* **Configuração de Logs:** Inicializa o `loguru` para registrar a execução em um arquivo (`cadastro_regional.log`), facilitando o monitoramento.
* **Estrutura de Diretórios:** Garante que o diretório para salvar os arquivos CSV exista.

### 2. Configuração de E-mails e Regionais

* **Credenciais e Dicionários:** As credenciais do remetente são definidas. Dois dicionários são criados para mapear o ID de cada regional ao seu respectivo nome e ao endereço de e-mail do destinatário, o que organiza e facilita o envio direcionado.

### 3. Loop Principal de Processamento

O script entra em um loop `for` que itera de 1 a 6, representando cada uma das regionais.

* **Conexão com Banco:** A cada iteração, uma conexão com o banco de dados é estabelecida.
* **Consulta por Regional:** Uma consulta SQL (`cadastro_regional`) é formatada dinamicamente com o ID da regional (`i`) e executada. O resultado é armazenado em um DataFrame do Pandas.
* **Verificação de Dados:** O script verifica se o DataFrame resultante está vazio. Se estiver, significa que não há pendências para aquela regional, e o script avança para a próxima iteração com `continue`.

### 4. Lógica de Geração de Arquivo (Baseada no Dia)

Se o DataFrame contiver dados, o script procede com a criação do relatório.

* **Lógica Condicional:** O nome do arquivo CSV e o corpo do e-mail são definidos com base no dia da semana:
  * **Segunda-feira:** O relatório é focado nas "novas ligações" da semana.
  * **Sexta-feira:** O relatório foca nas ligações "não atualizadas" durante a semana.
  * **Outros Dias:** Um modo de "teste" é ativado, com nomes de arquivo e corpo genéricos.
* **Criação do CSV:** O DataFrame é salvo em um arquivo CSV com o nome definido na etapa anterior.

### 5. Envio de E-mail

* **Envio Direcionado:** A função `envia_email` é chamada para enviar o relatório gerado.
  * O destinatário é selecionado do dicionário `destinatarios` usando o ID da regional (`i`).
  * O e-mail é enviado com o assunto, corpo e o arquivo CSV em anexo.

### 6. Tratamento de Erros e Finalização

* **Bloco `try...except`:** Todo o fluxo de execução está contido em um bloco para tratamento de exceções. Se ocorrer qualquer erro (por exemplo, falha na conexão com o banco ou no envio do e-mail), o erro é registrado no log, uma mensagem crítica é exibida e o script é finalizado com `exit(1)`.
* **Log de Conclusão:** Se o loop for concluído sem erros, uma mensagem de "Fim de execução" é registrada no log.
