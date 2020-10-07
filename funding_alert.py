import time
import FTXClient
import TelegramClient
from environs import Env

import logging

def get_logger():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",datefmt='%d/%m/%Y %H:%M:%S')

    file_handler = logging.FileHandler('file.log')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger

logger = get_logger()

def get_funding_rates(LIST_OF_FUTURES="all"):
    
    funding_rates = {}
    if LIST_OF_FUTURES == "all":
        futures = FTXClient.list_all_futures()
        LIST_OF_FUTURES = [_dict["name"] for _dict in futures if _dict["perpetual"] == True] #only perpetual contracts have a next funding rate

    for future in LIST_OF_FUTURES:
        
        try:
            funding_rates[future] = FTXClient.get_future_stats(future)["nextFundingRate"]
            logger.info(f"Funding rate do future {future} adquirido com sucesso.")
        except:
            logger.exception(f"Erro ao buscar funding rate do future {future}.")

    return funding_rates


def message_formatter(funding_rates,OUTPUT_NUMBER=3,OUTPUT_THRESHOLD=0):

    sorted_keys = sorted(funding_rates,key=funding_rates.get,reverse=True)
    top_rates = []
    bottom_rates = []
    for i in range(OUTPUT_NUMBER):

        if abs(funding_rates[sorted_keys[i]]) > OUTPUT_THRESHOLD:
            top_rates.append(f"{sorted_keys[i]} ({funding_rates[sorted_keys[i]]})")

        if abs(funding_rates[sorted_keys[-(i+1)]]) > OUTPUT_THRESHOLD:
            bottom_rates.append(f"{sorted_keys[-(i+1)]} ({funding_rates[sorted_keys[-(i+1)]]})") 

    top_rates_msg = '\n'.join(top_rates)
    bottom_rates_msg = '\n'.join(bottom_rates)

    t = time.localtime()
    current_date = time.strftime("%m/%d/%Y", t)
    current_time = time.strftime("%H:%M:%S", t)
    return (f"[{current_date} - {current_time}]\n"
            f"Top {OUTPUT_NUMBER}:\n"
            f"{top_rates_msg}\n\n"
            f"Bottom {OUTPUT_NUMBER}:\n"
            f"{bottom_rates_msg}")


def main(LIST_OF_FUTURES="all",UPDATE_DELAY=3600,OUTPUT_NUMBER=3,OUTPUT_THRESHOLD=0,TELEGRAM_TOKEN=None,TELEGRAM_CHAT_ID=None):
    
    logger.info("Starting...")

    while True:
        
        try:
            funding_rates = get_funding_rates(LIST_OF_FUTURES)
            logger.info("Sucesso ao adquirir as funding rates.")
        except:
            logger.exception("Falha ao adquirir as funding rates.")

        try:
            funding_rates_message = message_formatter(funding_rates,OUTPUT_NUMBER,OUTPUT_THRESHOLD)
            logger.info("Sucesso ao criar a mensagem.")
        except:
            logger.exception("Falha ao criar a mensagem.")

        print("\n",funding_rates_message,"\n")
        
        if TELEGRAM_TOKEN:
            try:
                TelegramClient.send_message(TELEGRAM_TOKEN,TELEGRAM_CHAT_ID,message=funding_rates_message)
                logger.info("Sucesso ao enviar mensagem no Telegram.")
            except:
                logger.exception("Falha ao enviar mensagem no Telegram.")

        logger.info("Sleeping...")
        time.sleep(UPDATE_DELAY)


if __name__ == "__main__":

    env = Env()
    env.read_env(".env", recurse=False)
    main(LIST_OF_FUTURES=env.str("LIST_OF_FUTURES","all"),
         UPDATE_DELAY=env.int("UPDATE_DELAY",3600),
         OUTPUT_NUMBER=env.int("OUTPUT_NUMBER",3),
         OUTPUT_THRESHOLD=env.int("OUTPUT_THRESHOLD",0),
         TELEGRAM_TOKEN=env.str("TELEGRAM_TOKEN",None),
         TELEGRAM_CHAT_ID=env.str("TELEGRAM_CHAT_ID",None))
    