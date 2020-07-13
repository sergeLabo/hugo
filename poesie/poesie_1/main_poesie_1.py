#! /usr/bin/env python3


from time import sleep
import threading

from poesie_irc_1 import PoesieIrcBot
from testing_poesie_1 import Poesie


# Serveur IRC
SERVER = "irc.freenode.net"
PORT = 6667
CHANNEL = "#labomedia"
NICKNAME = "CadavresExquis"
REALNAME = "de Victor Hugo"


def run():

    bot = PoesieIrcBot(CHANNEL, NICKNAME, REALNAME, SERVER, PORT)
    thread_dialog = threading.Thread(target=bot.start)
    thread_dialog.setDaemon(True)
    thread_dialog.start()

    poesie = Poesie()

    sleep(1)
    bot.new = 0
    while bot.alive:
        num = bot.num
        if bot.new == 0 and bot.quest_rep:
            if len(bot.quest_rep) == num + 1:
                if len(bot.quest_rep[num]) == 1:
                    bot.new = 1
                    try:
                        input_list = bot.quest_rep[num][0].split("$$$")
                        # ['je suis surpris ', '50', '0.8']

                        if len(input_list) == 1:
                            question = input_list[0]
                            len_max = 20
                            temp = 1
                        elif len(input_list) == 2:
                            question = input_list[0]
                            len_max = int(input_list[1])
                            temp = 1
                        elif len(input_list) == 3:
                            question = input_list[0]
                            len_max = int(input_list[1])
                            temp = float(input_list[2])
                        else:
                            question = "Je suis heureux "
                            len_max = 50
                            temp = 1
                    except:
                        question = "Quoi"
                        len_max = 50
                        temp = 1

                    print(f"Q: {question} Temp: {temp} lenght: {len_max}")

                    if len(question) > 30: question = "Quoi"
                    if len_max > 200: len_max = 200
                    if temp < 0: temp = 0.1
                    if temp > 2: temp = 2
                    bot.new = 1

        if bot.new == 1:
            len_max = 20
            temp = 0.8
            text_list = poesie.get_irc_response(question, len_max, temp)
            try:
                text_list = poesie.get_irc_response(question, len_max, temp)
            except:
                text_list = ["Je ne comprends pas la question!"]

            # Envoi de la réponse
            print("\nN°:", num)
            print("Question:", bot.quest_rep[num])
            print("Response:", text_list[0])

            lines = text_list[0].splitlines()
            for line in lines:
                print(f"envoi de: {line}")
                bot.send_pubmsg(line)
                sleep(0.5)
            bot.num += 1

            # Boucle
            mots = text_list[0].replace("\n", " ").split(" ")

            # Récup de x mots
            nbmots = 3
            fin_list = mots[-nbmots:]
            fin = ""
            for i in range(nbmots):
                fin += fin_list[i] + " "
            print("Nouvelle question:", fin)

            # Nouvelle question
            sleep(20)
            num = bot.num
            # pour relance
            if num > 0:
                bot.quest_rep[num] = [fin]  # liste
                question = fin # str



if __name__ == '__main__':
    run()
