# FTXFundingAlerter

FTX Funding Alerter é um projeto simples que notifica o usuário com os instrumentos de maiores e menores funding rates na exchange FTX. O monitoramento é feito ao executar o arquivo funding_alert.py que verifica as funding rates dos futures periodicamente e envia uma mensagem pelo Telegram caso seja desejado.

Para rodar o alerta de funding rates é necessário necessário criar um arquivo .env no diretório do projeto. Esse arquivo deve conter os inputs do projeto:

 - **LIST_OF_FUTURES**: lista de nomes dos instrumentos para monitorar. Default: "all".

 - **UPDATE_DELAY**: delay, em segundos, entre cada checagem/report. Default: 3600.

 - **OUTPUT_NUMBER**: a quantidade de instrumentos a se mostrar (maiores e menores). Exemplo: se OUTPUT_NUMBER=3 então deve-se mostrar a lista dos 3 maiores e 3 dos menores funding rates. Default: 3.

 - **OUTPUT_THRESHOLD**: se o valor absoluto do funding rate for menor que OUTPUT_THRESHOLD, então o instrumento deve ser omitido da saída (apenas mostre na saída instrumentos com funding rate > OUTPUT_THRESHOLD). Default: 0.

 - **TELEGRAM_TOKEN**: token telegram. Opcional. Envia a mensagem dos maiores e menores funding rates caso usado.

 - **TELEGRAM_CHAT_ID**: chat_id telegram. Opcional. É necessário o token.
