# Documentação do Script `analitico_hidrometro.py`

## 🎯 Objetivo

O objetivo deste script é gerar relatórios analíticos de hidrômetros, separados por regional. Ele consulta um banco de dados para cada uma das seis regionais, cria um arquivo CSV para cada uma, compacta esses arquivos em dois pacotes distintos (`.tar.xz`) e os envia por e-mail para os destinatários designados.

## ⚙️ Etapas de Execução

O script é organizado da seguinte forma:

### 1. Configuração Inicial e Ambiente

* **Importações:** Importa as bibliotecas e módulos necessários, incluindo `os` para interações com o sistema operacional (como executar comandos de compactação), `loguru` para logging, e funções auxiliares do pacote `utilities`.
* **Variáveis de Ambiente:** Carrega configurações de um arquivo `.env` para gerenciar informações como credenciais de forma segura.
* **Configuração de Logs:** Inicializa o `loguru` para registrar a execução do script em um arquivo de log (`analitico_jonas.log`).
* **Estrutura de Diretórios:** Garante que a pasta de destino para os arquivos CSV gerados exista.

### 2. Função Auxiliar `formata()`

* O script define uma função local chamada `formata`, que recebe uma lista de nomes de arquivos e a converte em uma única string. Ela substitui os espaços nos nomes dos arquivos por `\ ` para garantir que o comando de compactação no terminal (`tar`) interprete os nomes corretamente.

### 3. Loop de Processamento por Regional

O núcleo do script é um loop `for` que itera de 1 a 6 (representando cada regional).

* **Consulta ao Banco:** Para cada regional, ele executa uma consulta SQL (formatada com o ID da regional) para obter os dados analíticos dos hidrômetros.
* **Criação de CSV:** O resultado da consulta é salvo em um arquivo CSV com um nome padronizado (ex: `analitico_hidrometros_LITORAL.csv`).
* **Caso Especial (Litoral):** A primeira regional (`i == 1`, Litoral) tem um tratamento especial:
  * Seu arquivo CSV é **imediatamente compactado** em um arquivo `.tar.xz` separado (`analitico_LITORAL.tar.xz`).
  * O título e o corpo do e-mail específico para esta regional são definidos.
  * O loop então pula para a próxima iteração usando `continue`.
* **Demais Regionais:** Para as outras regionais (2 a 6), o nome do arquivo CSV gerado é adicionado a uma lista (`lista_arquivos`) para compactação posterior.

### 4. Compactação dos Arquivos

Após o loop, o script executa dois processos de compactação usando o comando `tar` do sistema:

1. **Compactação do Litoral:** Já realizada dentro do loop.
2. **Compactação das Demais Regionais:**
   * Os nomes dos arquivos acumulados na `lista_arquivos` são formatados pela função `formata`.
   * Um comando `os.system` é executado para chamar o `tar` e criar um segundo arquivo compactado (`analitico_regionais.tar.xz`) contendo os CSVs das outras cinco regionais.

### 5. Envio de E-mails

O script envia **dois e-mails separados** para cada destinatário da lista:

1. **E-mail do Litoral:** Envia o e-mail com o título, corpo e anexo (`analitico_LITORAL.tar.xz`) específicos para a regional Litoral.
2. **E-mail das Outras Regionais:** Envia um segundo e-mail com um título genérico e o arquivo `analitico_regionais.tar.xz` em anexo.

### 6. Limpeza e Finalização

* **Remoção de Arquivo:** Após o envio dos e-mails, o arquivo `analitico_regionais.tar.xz` é removido do disco para liberar espaço.
* **Tratamento de Erros:** Todo o processo é envolvido em um bloco `try...except...finally` para capturar e registrar exceções, garantindo que o script sempre registre uma mensagem de "Fim de execução" no log, independentemente de ter ocorrido um erro ou não.

![foto do perfil](https://lh3.googleusercontent.com/a/ACg8ocJjRqIPKZcF1SuuofhdGfTMY17WFqti3kAu9aTqMwyprYNqKjM=s64-c-mo)
