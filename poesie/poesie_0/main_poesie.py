#! /usr/bin/env python3


from time import sleep
import threading

from labo_irc_7 import FableIrcBot
from testing_7 import AiTextGen


# Serveur IRC
SERVER = "irc.freenode.net"
PORT = 6667
CHANNEL = "#labomedia"
NICKNAME = "labo"
REALNAME = "de La Labomedia"


def run():

    bot = FableIrcBot(CHANNEL, NICKNAME, REALNAME, SERVER, PORT)
    thread_dialog = threading.Thread(target=bot.start)
    thread_dialog.setDaemon(True)
    thread_dialog.start()

    atg = AiTextGen()

    sleep(1)
    while bot.alive:
        a = 0
        num = bot.num
        if bot.quest_rep:
            if len(bot.quest_rep) == num + 1:
                if len(bot.quest_rep[num]) == 1:
                    a = 1
                    try:
                        input_list = bot.quest_rep[num][0].split("$$$")
                        # ['je suis surpris ', '50', '0.8']

                        if len(input_list) == 1:
                            question = input_list[0]
                            len_max = 50
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

        if a == 1:

            print(f"Q: {question} Temp: {temp} lenght: {len_max}")
            print(f"Q: {type(question)} Temp: {type(temp)} lenght: {type(len_max)}")

            if len(question) > 30: question = "Quoi"
            if len_max > 200: len_max = 200
            if temp < 0: temp = 0.1
            if temp > 2: temp = 2

            try:
                text_list = atg.get_irc_response(question, len_max, temp)
            except:
                text_list = ["Je ne comprends pas la question!"]

            # Envoi de la réponse
            print("\nQuestion n°:", num)
            print("Question:", bot.quest_rep[num])
            print("Response:", text_list)
            bot.quest_rep[num].append(text_list)


if __name__ == '__main__':
    run()
