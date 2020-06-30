#!python3

import pypandoc

from mytools import MyTools


mt = MyTools()

files = mt.get_all_files_list('./roman', ['.epub'])

for f in files:
    name = f.split('.')[0]
    print(name)
    pypandoc.convert_file(f, to='plain', outputfile=name + '.txt')
