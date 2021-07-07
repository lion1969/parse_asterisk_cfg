#!/bin/python
# -*- coding: utf-8 -*-
import inspect
import os.path

'''  CLI arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Parse <filename> - file of Asterisk cfg.",
                    type=str)
args = parser.parse_args()
'''

from tkinter import *
import tkinter.filedialog as tkFileDialog

def doQuit():
    global root
    root.destroy()

def loadFile():
    global file_name
    global ary
    fn = tkFileDialog.Open(root, filetypes=[('*.txt files', '.txt')]).show()
    print('FileOpened:', fn)
    if fn == '':
        return
    textbox.delete('1.0', 'end')
    textbox.insert('1.0', open(fn, 'rt', encoding="utf8").read())
    print('FN = ', fn)
    f = getFileHandler(fn)
    sip_conf_list = f.readlines()
    ary.clear()
    ary = parseAsteriskCfg(sip_conf_list)


def saveFile():
    fn = tkFileDialog.SaveAs(root, filetypes=[('*.txt files', '.txt')]).show()
    if fn == '':
        return
    if not fn.endswith(".txt"):
        fn += ".txt"
    open(fn, 'wt', encoding="utf8").write(textbox.get('1.0', 'end'))

def doProc():
    global ary
    textbox.delete('1.0', 'end')
    txt2insert = ''
    for element in range(len(ary)):
        print(ary[element])
        txt2insert = txt2insert+ary[element]+"\n"
    textbox.insert('1.0', txt2insert)
    ary.clear()
    print('Len of clear list = '+ str(len(ary)))

def getFileHandler(filename):
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        try:
            fn = open(filename, "r", encoding="utf8")
        except EOFError as ex:
            print("Caught the EOF error.")
            raise ex
        except IOError as ex:
            print("Caught the I/O error.")
            raise ex
        return fn
    else:
        #inspect.stack()[0][3]) - Return name of function 'self name'
        print(inspect.stack()[0][3]+'() ERROR. File: ', filename)
        print("Either the file is missing or not readable")
        exit(0)

def parseAsteriskCfg(sip_conf_List):
    #print("Sip_Conf List:", sip_conf_List)
    print(sip_conf_List)
    returnList = []
    dec_email = ''
    i = 1
    for line in sip_conf_List:
        line = line.replace('\n', '')
        m = re.findall(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+', line)
        if m:
            dec_email = dec_email + line + '; '
            i = i + 1
        returnList.append(line)
    return returnList

'''
file_name = 'sip.conf'
f = getFileHandler(file_name)
sip_conf = f.readlines()
ary = parseAsteriskCfg(sip_conf)
print('Ary first call:', ary)
'''
ary = []
root = Tk()
panelFrame = Frame(root, height=44, bg='light gray' )
textFrame = Frame(root, height=340, width=600)

panelFrame.pack(side='top', fill='x')
textFrame.pack(side='bottom', fill='both', expand=1)

textbox = Text(textFrame, font='Arial 10', wrap='word')
scrollbar = Scrollbar(textFrame)

scrollbar['command'] = textbox.yview
textbox['yscrollcommand'] = scrollbar.set

textbox.pack(side='left', fill='both', expand=1)
scrollbar.pack(side='right', fill='y')

loadBtn = Button(panelFrame, text='Load', command = loadFile)
saveBtn = Button(panelFrame, text='Save', command = saveFile)
quitBtn = Button(panelFrame, text='Quit', command = doQuit)
procBtn = Button(panelFrame, text='Proc', command = doProc)

loadBtn.place(x=2, y=2, width=48, height=40)
saveBtn.place(x=52, y=2, width=48, height=40)
quitBtn.place(x=102, y=2, width=48, height=40)
procBtn.place(x=252, y=2, width=48, height=40)


root.mainloop()