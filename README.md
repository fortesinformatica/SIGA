# SIGA
Coleta e aprendizado de dados de uso dos sistemas para recomendação automatizada de funcionalidades
Desenvolvido entre 2018 e 2019
Sistema Inteligente para Detecção de Próxima Funcionalidade e Fluxos de 
Trabalhos em Software Contábil com Múltiplas Funcionalidades (SIGA), Projeto 
certificado pela empresa Fortes Informática em 21/05/2020., Descrição: 
Projeto que objetiva predizer funcionalidades a partir de funcionalidades 
anteriores em sistemas desktop, visa ainda detectar fluxos de trabalhos 
(sequencias de funcionalidades) recorrentemente utilizados por usuários do 
sistema e, por fim, visa realizar o mapeamento entre entradas para 
funcionalidades com base em entradas anteriores. A informação usada nesse 
projeto tem grande volume de dados (big data) e armazenado em nuvem. Para 
resolver este problema técnicas de inteligência artificial, mais 
especificamente de aprendizagem de máquinas, devem ser aplicadas para 
realizar tal recomendação. , 
Situação: Concluído; 
Natureza: Desenvolvimento. 
Alunos envolvidos: 
Graduação: (1) / 
Mestrado acadêmico: (3) . , 
Integrantes: 
Carlos Henrique Leitao Cavalcante - Integrante / 
Alisson Gomes Linhares - Integrante / 
Ajalmar Rêgo da Rocha Neto - Coordenador / 
LUAN SOUSA CORDEIRO - Integrante / 
AMAURI HOLANDA DE SOUZA JUNIOR - Integrante / 
VICTOR RIBEIRO PRATA - Integrante / 
ALAN RABELO MARTINS - Integrante / 
Açucena De Gois Parente - Integrante / 
Elder Dos Santos Teixeira - Integrante. 

SITE da API
https://siga-api.azurewebsites.net

Para poder rodar os testes em uma máquina desktop, é preciso:

- Instalar o banco de dados não relacional MongoDB
  https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
- Instalar também o MongoDB Compass
  "C:\Users\build\AppData\Local\MongoDBCompass\app-1.27.1\MongoDBCompass.exe"
  localhost:27017//local.startap_log

- Instalar o MsSqlLocalDB
  https://www.sqlshack.com/install-microsoft-sql-server-express-localdb/

- Instalar o emulador do azure blob storage
  https://docs.microsoft.com/pt-br/azure/storage/common/storage-use-emulator
- Iniciar o emulador de storage do azure na máquina local

- Instalar o gerenciador de storage o Microsoft Azure
  https://azure.microsoft.com/en-au/features/storage-explorer/

- Desinstalar o rust compiler
- Instalar o Python 3.6
  python-3.6.1-amd64.exe
- Atualizar o pip para a versão mais nova
  python -m pip install --upgrade pip
  ----pip-21.1.2
- Instalar o utilitário Rust
  rustup-init.exe
- Excluir a pasta .venv caso ela exista
  C:\PROJETOS\SIGA\.venv
- Rodar no VsCode, para configurar o ambiente virtual
  py -3 -m venv .venv
  .venv\scripts\activate
  python -m pip install --upgrade pip
  pip install -r requirements.txt

- Talvez seja necessário alterar no arquivo web.config a linha 
    scriptProcessor="D:\Python34\python.exe|D:\Python34\Scripts\wfastcgi.py"
	para 
	scriptProcessor="C:\Python36\python.exe|C:\Python36\Scripts\wfastcgi.py"

- Criar o arquivo .env na pasta do SIGA, esse arquivo é usado pelo Visual Studio Code para carregar
as variáveis de ambiente automaticamente quando o projeto é carregado. Quando for feito o deploy para
o servidor do azure, essas variáveis terão que ser configuradas nas opções de configuração do projeto no azure.

- Conteúdo do arquivo .env que fica na pasta raiz do SIGA
APP_LOG=C:\PROJETOS\SIGA\LogFiles
APP_ROOT=C:\PROJETOS\SIGA
APP_SITEPACKAGES=C:\PROJETOS\SIGA\.venv\Lib\site-packages
APPINSIGHTS_INSTRUMENTATIONKEY=no_instrumentation_key
AUTH_PASS=no_pass
AUTH_USER=no_user
BLOBS_KEY=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
BLOBS_NAME=devstoreaccount1
DIAGNOSTICS_AZUREBLOBCONTAINERSASURL=no_azure_url
DIAGNOSTICS_AZUREBLOBRETENTIONINDAYS=1
INDEX_LOG=C:\PROJETOS\SIGA\LogFiles
LAST_SESSIONS=C:\PROJETOS\SIGA\last_sessions.pickle
MAX_THROUGHPUT=10000
MIN_THROUGHPUT=1000
__MONGO_COLLECTION_ID=SigaTimeLine
__MONGO_DATABASE=SigaData
__MONGO_DATABASE_HOST=https://siganosql.documents.azure.com
__MONGO_MASTER_KEY=no_master_key
__MONGO_URI=no_uri
MobileAppsManagement_EXTENSION_VERSION=latest
WEBJOBS_RESTART_TIME=1
__WEBSITE_HTTPLOGGING_CONTAINER_URL=no_logging_container_url
WEBSITE_HTTPLOGGING_RETENTION_DAYS=1
WEBSITE_NODE_DEFAULT_VERSION=6.9.1
BLOBS_EMULATED=True

