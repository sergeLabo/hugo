#! /usr/bin/env python3


from time import sleep
import threading
from random import randint

from roman_irc_2 import RomanIrcBot
from testing_roman_2 import Roman


# Serveur IRC
SERVER = "irc.freenode.net"
PORT = 6667
CHANNEL = "#labomedia"
NICKNAME = "Roman"
REALNAME = "de Victor Hugo"

print("\n"*200)

class Bidon:

    def __init__(self):
        self.num = 0
        self.quest_rep = {}
        self.quest_rep[0] = ["Jean Valjean emmena Cosette devant la maison"]
        self.alive = 1


def get_reponse_new_question(text, question):
    """
    lines = ['Romeo n'est pas gentil',
             'et juliette aussi, elle esp']
    reponse['Romeo n'est pas gentil',
             'et juliette aussi, elle']
    new_question = 'est pas gentil et juliette aussi, elle'
    """

    lines = text.splitlines()

    # Pas d'envoi du dernier mot de la dernière ligne
    # La dernière ligne = lines[-1]
    # La dernière ligne sans le dernier mot en liste
    last_line_list = lines[-1].split(" ")[:-1]
    # Conversion de la liste de mots en une ligne
    last_line = ""
    for mot in last_line_list:
        last_line += mot + ' '
    lines[-1] = last_line

    # la réponse en str
    resp = ""
    for item in lines:
        resp += item + '\n'
    # sans le \n de la dernière ligne
    resp = resp[:-2]
    # Sauf le prompt = question
    resp = resp.replace(question, "")
    # La réponse en liste
    reponse = resp.splitlines()

    # La nouvelle question
    mots = resp.replace("\n", " ").split(" ")
    # Récup de x mots
    nbmots = 5  # 20
    new_question_list = mots[-nbmots:]
    new_question = ""
    for mot in new_question_list:
        new_question += mot + ' '

    return reponse, new_question


def generate_local(vocab_size):

    bot = Bidon()
    roman = Roman(vocab_size)
    print("\n"*200)

    sleep(1)
    bot.new = 0
    while bot.alive:
        num = bot.num
        if bot.new == 0 and bot.quest_rep:
            if len(bot.quest_rep) == num + 1:
                if len(bot.quest_rep[num]) == 1:
                    bot.new = 1
                    question = bot.quest_rep[num][0]
                    if len(question) > 50:
                        question = "Quoi"
                    # Il y a une nouvelle question
                    bot.new = 1
                    print('\n\n', question)
        if bot.new == 1:
            len_max = 100
            temp = 0.8
            text_list = roman.get_irc_response(question, len_max, temp)

            reponse, new_question = get_reponse_new_question(text_list[0],
                                                             question)

            for line in reponse:
                sleep(4)
                print(line)

            # Nouvelle question
            sleep(4)
            bot.num += 1
            num = bot.num
            bot.quest_rep[num] = [new_question]  # liste
            question = new_question # str


def generate_irc(vocab_size):
    bot = RomanIrcBot(CHANNEL, NICKNAME, REALNAME, SERVER, PORT)
    thread_dialog = threading.Thread(target=bot.start)
    thread_dialog.setDaemon(True)
    thread_dialog.start()
    roman = Roman(vocab_size)

    sleep(1)
    bot.new = 0
    while bot.alive:
        num = bot.num
        sleep(0.1)
        if not bot.stop:
            if bot.new == 0 and bot.quest_rep:
                if not bot.init:
                    if len(bot.quest_rep) == num + 1:
                        if len(bot.quest_rep[num]) == 1:
                            print("début", bot.quest_rep)
                            try:
                                question = bot.quest_rep[num][0]
                            except:
                                question, len_max, temp = "Quoi", 50, 1
                            # Il y a une nouvelle question
                            bot.new = 1
                else:
                    print("relance avec $$$", bot.quest_rep)
                    try:
                        question = bot.quest_rep[1]
                    except:
                        question = "Quoi"
                    # Il y a une nouvelle question
                    bot.new = 1
                    bot.init = 0

                # Seulement les 50 premiers
                question = question[:100]
                bot.send_pubmsg("Ceci n'est pas un nouveau roman de Victor Hugo:")
                sleep(5)
                bot.send_pubmsg(question)
                print('\n\nNouvelle question:', question, '\n\n')

            if bot.new == 1:
                len_max, temp = 60, 1
                try:
                    text_list = roman.get_irc_response(question, len_max, temp)
                except:
                    text_list = ["Je ne comprends pas la question!"]
                # text_list[0] est le 1er texte généré
                reponse, new_question = get_reponse_new_question(text_list[0],
                                                                 question)

                # #bot.send_pubmsg("Nouveau calcul ...")
                # #sleep(0.4)

                for line in reponse:
                    try:
                        bot.send_pubmsg(line)
                        sleep(4)
                        print(line)
                    except:
                        pass

                # Boucle
                if not bot.new and not bot.init:
                    num = bot.num = 1
                    bot.quest_rep[num] = [new_question]  # liste
                    question = new_question # str



if __name__ == '__main__':
    vocab_size = 40000

    generate_local(vocab_size)

    # #generate_irc(vocab_size)
