import os,sys,re

dirs = ['.','.vscode','bin','doc','lib','src','tmp','test']

files = ['README.md','Makefile','apt.dev','apt.txt']

merge = files +['.gitignore']

json = ['settings','tasks','launch','extensions']

files += map(lambda j:f'.vscode/{j}.json',json)

gitz = ['*~','*.swp','*.log','','/lib/python*/']

def giti(d):
    if d in ['.vscode']: return
    with open(f'{d}/.gitignore','w') as F:
        if d == '.': map(F.write,gitz)
        if d in ['bin','tmp']: F.write('*\n')
        F.write(f'!.gitignore\n')

for d in dirs:
    try: os.mkdir(d)
    except FileExistsError: pass
    finally: giti(d)

for f in files:
    with open(f,'w') as F: pass
