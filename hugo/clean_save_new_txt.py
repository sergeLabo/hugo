#!python3


import os
from time import sleep
import re

from langdetect import detect, detect_langs
from mytools import MyTools


mt = MyTools()

files = mt.get_all_files_list('./roman_txt', ['.txt'])


def clean_one_txt(txt):

    lines = txt.splitlines()

    new_txt = ''
    for line in lines:
        good = 1

        # Numéro de ligne ou Majuscules ou i
        if line.isdigit() or line.isupper():
            good = 0

        # ................48
        if '........' in line:
            good = 0

        # Mots interdits
        for item in [   '[', ']', '_', '*', '•',
                        'Scène', 'Théâtre',
                        'MDSERIES',
                        'PREMIÈRE SÉRIE',
                        'NOUVELLE SÉRIE',
                        'DERNIÈRE SÉRIE',
                        'ÉDITION COLLECTIVE',
                        'Édition originale',
                        'Publication',
                        'Source : Livres & Ebooks',
                        'http:', '©', ]:

            if item in line:
                good = 0
                break

        # ligne de 0 à 5 caractères non conservé
        if len(line) < 6:
            good = 0

        if good and line:
            new_txt += line + '\n'

    new_txt = apply_regex(new_txt)
    new_txt = delete_english(new_txt)

    return new_txt


def apply_regex(txt):
    """
    https://regex101.com/r/yfD01K/2
    """

    txt = re.sub( r"^{\w*}[ *\w’.,;*]*|{\d*}",
                    "",
                    txt,
                    flags=re.M)

    return txt


def delete_english(txt):

    lines = txt.splitlines()
    n = 0
    new_txt = ''
    for line in lines:
        try:
            langue = detect_langs(line)[0]
        except:
            langue = None

        if langue:
            if langue.lang == 'fr' and langue.prob > 0.4:
                new_txt += line + '\n'
            else:
                print(langue.lang, langue.prob, line)
                n += 1
    print(f"Suppression de {n} lignes")
    return new_txt


def clean_all_txt():
    n = 0
    for fichier in files:
        n += 1
        if n < 10000:  # Pour tester avec peu de fichier
            print("Fichier à lire:", fichier)
            # roman_txt/hugo_le_roi_s_amuse.txt
            txt = mt.read_file(fichier)
        else:
            break

        new_txt = clean_one_txt(txt)

        new_fichier = './' + fichier.replace('txt/', 'new_txt/')
        # #print("Fichier amélioré:", new_fichier)
        mt.write_data_in_file(new_txt, new_fichier, mode="w")
        print('\n\n')


clean_all_txt()
