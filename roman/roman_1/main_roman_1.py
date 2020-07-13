#! /usr/bin/env python3


from time import sleep
import threading
from random import randint

from roman_irc_0 import RomanIrcBot
from testing_roman_0 import Roman


# Serveur IRC
SERVER = "irc.freenode.net"
PORT = 6667
CHANNEL = "#labomedia"
NICKNAME = "CadavresExquis"
REALNAME = "de Victor Hugo"

TEST = 1

class Bidon:

    def __init__(self):
        self.question = "Qui es-tu ?"
        self.response = "I'm stupid"
        self.num = 0
        self.quest_rep = {}
        self.quest_rep[0] = ["Le colonel décida"]
        self.alive = 1

    def send_pubmsg(self, what):
        pass


def run():
    if not TEST:
        bot = RomanIrcBot(CHANNEL, NICKNAME, REALNAME, SERVER, PORT)
        thread_dialog = threading.Thread(target=bot.start)
        thread_dialog.setDaemon(True)
        thread_dialog.start()
    else:
        bot = Bidon()
    roman = Roman()

    sleep(1)
    bot.new = 0
    while bot.alive:
        num = bot.num
        if bot.new == 0 and bot.quest_rep:
            if len(bot.quest_rep) == num + 1:
                if len(bot.quest_rep[num]) == 1:
                    bot.new = 1
                    try:
                        question = bot.quest_rep[num][0]
                    except:
                        question = "Quoi"
                        len_max = 50
                        temp = 1
                    if len(question) > 50:
                        question = "Quoi"
                    # Il y a une nouvelle question
                    bot.new = 1
                    print('\n\n', question)
        if bot.new == 1:
            len_max = 100
            temp = 1

            try:
                text_list = roman.get_irc_response(question, len_max, temp)
            except:
                text_list = ["Je ne comprends pas la question!"]
            lines = text_list[0].splitlines()

            # Pas d'envoi du dernier mot de la dernière ligne
            last_line = lines[-1]

            # La dernière ligne sans le dernier mot en liste
            new_last_line_list = last_line.split(" ")[:-1]

            # Conversion de list to str
            new_last_line = ""
            for item in new_last_line_list:
                new_last_line += item + ' '

            # Je change la dernière ligne de lines
            lines[-1] = new_last_line

            # Pretty print
            # #print("\nN°:", num)
            # #print("Question:", question)
            resp = ""
            for item in lines:
                resp += item + '\n'
            resp = resp[:-2]
            # Sauf le prompt = question
            reponse = resp.replace(question, "")
            print(reponse)

            # Envoi de la réponse
            new_question = ""
            for line in lines:
                bot.send_pubmsg(line)
                new_question += line + '\n'
                sleep(0.5)
            # A la fin de l'envoi, je touche
            new_question = new_question[:-2]
            bot.num += 1

            # Nouvelle question
            sleep(randint(10, 20))
            num = bot.num

            mots = text_list[0].replace("\n", " ").split(" ")
            # Récup de x mots
            nbmots = 20
            new_question_list = mots[-nbmots:]
            new_question = ""
            for i in range(nbmots):
                new_question += new_question_list[i] + " "

            # pour relance
            if num > 0:
                bot.quest_rep[num] = [new_question]  # liste
                question = new_question # str



if __name__ == '__main__':
    run()


            # Boucle
            # ##
