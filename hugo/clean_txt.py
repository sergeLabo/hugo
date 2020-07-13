#!python3


from mytools import MyTools


mt = MyTools()

oeuvre = 'roman'
fichier = oeuvre + '.txt'

ROMAN = ["M", "CM", "D", "CD", "C", "XC",
        "L", "VL", "XL", "X", "IX", "V", "IV", "I"]

txt = mt.read_file(fichier)

# Nettoyage
lines = txt.splitlines()
txt_clean = ""
for line in lines:
    good = 1
    # Numéro de ligne ou Majuscules
    if line.isdigit() or line.isupper() or line == 'i':
        good = 0

    # ................48
    if '........' in line:
        good = 0

    # Mots interdits
    for item in [   '[', ']', '_', '*', '•', '{', '}',
                    'MDSERIES',
                    'PREMIÈRE SÉRIE',
                    'NOUVELLE SÉRIE',
                    'DERNIÈRE SÉRIE',
                    'ÉDITION COLLECTIVE',
                    'Édition originale',
                    'Publication',
                    'Source : Livres & Ebooks',
                    'Victor Hugo',
                    'Victor',
                    'Hugo',
                    'http:', '©', ]:

        if item in line:
            good = 0
            break
    if good and line:
        txt_clean += line + '\n'

# Suppression de caractères
# #'…', '{', '}'

f = oeuvre + '_clean.txt'
mt.write_data_in_file(txt_clean, f, mode="w")
