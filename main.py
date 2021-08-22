from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
procurar_var = 0

# funções que são chamadas pelos handlers

def start(update, context):  # quando o usuario dar start
    username = update.message.from_user
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Olá,{username['first_name']}, eu sou o BicoBot e hoje vou te ajudar! Vamos dar início? ")
    return oferecer_procurar_int


def oferecer_procurar(update, context):  # após o olá
    username = update.message.from_user['first_name']
    context.bot.send_message(chat_id=update.effective_chat.id, text="Me diz, você deseja oferecer o serviço ou está procurando alguém para realizar o serviço?")
    return oferecer_resp_int

def oferecer(update, context):
    global procurar_var
    procurar_var = 0
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ok, qual é a sua área de atuação?\nEletricista\nEncanador\nPedreiro")
    return eletric_int

def procurar(update, context):
    username = update.message.from_user['first_name']
    global procurar_var
    procurar_var = 1
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bom, {username}, esses são os serviços disponíveis no momento\n\t- Eletricista\n\t- Encanador\n\t- Pedreiro\nDe quem você está precisando?")
    return eletric_int
def eletric(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Você pode descrever brevemente o que precisa ser feito?")
    return lugar_int 

def lugar(update, context):
    if procurar_var == 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Agora preciso saber em qual região o serviço será realizado.\n\t- Zona Norte?\n\t- Zona Leste?\n\t- Zona Sul?\n\t- Zona Oeste?")
        
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="- Agora preciso saber em qual região o serviço será realizado.\n- Zona Norte: 1\n- Zona Leste: 2\n- Zona sul: 3\n- Zona Oeste4\nOferece o serviço em todas: 5\nMande apenas o dígito da opção")
    return display_final_int

def display_final(update, context):
    username = update.message.from_user['first_name']
    global procurar_var
    if procurar_var == 1:
        ans = 'Aqui está a lista de eletricistas que podem fazer esse serviço:\nGustavo, 34 anos, recomendado para: reparo de chuveiros (1)\nGustavo, 21 anos, recomendado para: troca de chuveiros (2)\nGustavo, 50 anos, recomendado para instalação de chuveiros (3)\nCom qual deles gostaria de iniciar o contato?'
        context.bot.send_message(chat_id=update.effective_chat.id, text=ans)
        return adzin_int
    else:
        ans = 'Sua oferta foi cadastrada, assim que alguém quiser efetuar contato, você será avisado. Para cancelar a sua oferta digite /cancelaroferta'
        context.bot.send_message(chat_id=update.effective_chat.id, text=ans)
        return ConversationHandler.END

def adzin(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Obrigado por escolher os nossos serviços! Baseado em sua necessidade, temos essa recomendação de produto www.lojagenerica.com/produto')
    context.bot.send_message(chat_id=update.effective_chat.id, text='O contato do escolhido é @gustavo_trabalhador_ssi')
    return ConversationHandler.END

def cancelar(update, context):
    return ConversationHandler.END


# inteiros que contralam os estados
oferecer_procurar_int, oferecer_resp_int, eletric_int, lugar_int, display_final_int, adzin_int= range(6)
# Inicialização do Updater com o Token
token = "" # n foi mantido no repo para evitar usos indevidos do bot
updater = Updater(token=token, use_context=True)  # updater importante com o token   
dispatcher = updater.dispatcher 


start_handler = CommandHandler('start', start)
ofe_proc_handler = MessageHandler(Filters.text & ~Filters.command, oferecer_procurar)
proc_handler = MessageHandler(Filters.regex('[Pp]rocurando') & ~Filters.command, procurar)
ofe_handler = MessageHandler(Filters.regex('[Oo]ferecer') & ~Filters.command, oferecer)
eletric_handler = MessageHandler(Filters.text & ~Filters.command, eletric)
local_handler = MessageHandler(Filters.text & ~Filters.command, lugar)
display_final_handler = MessageHandler(Filters.text & ~Filters.command, display_final)
adzin_handler = MessageHandler(Filters.text & ~Filters.command, adzin)
conv_handler = ConversationHandler(entry_points=[start_handler], states={
    oferecer_procurar_int : [ofe_proc_handler], oferecer_resp_int : [ofe_handler, proc_handler], eletric_int : [eletric_handler], lugar_int : [local_handler], display_final_int : [display_final_handler], adzin_int : [adzin_handler]
}, fallbacks=[CommandHandler('cancelar', cancelar)],)

dispatcher.add_handler(conv_handler)
print("Iniciou")
updater.start_polling()
updater.idle()
updater.stop()
