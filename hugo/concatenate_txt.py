#!python3


from mytools import MyTools


mt = MyTools()

files = mt.get_all_files_list('./roman_new_txt', ['.txt'])

one_string = ""

for f in files:
    txt = mt.read_file(f)
    one_string += txt + '\n'

fichier = 'roman_wo_en.txt'
mt.write_data_in_file(one_string, fichier, mode="w")
