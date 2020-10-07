import telegram

def send_message(TOKEN,CHAT_ID,message):
    
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(CHAT_ID,message)
    
    return True

