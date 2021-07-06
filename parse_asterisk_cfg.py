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
    textbox.insert('1.0', open(fn, 'rt').read())
    print('FN = ', fn)
    f = getFileHandler(fn)
    sip_conf = f.readlines()
    ary.clear()
    ary = parseAsteriskCfg(sip_conf)


def saveFile():
    fn = tkFileDialog.SaveAs(root, filetypes=[('*.txt files', '.txt')]).show()
    if fn == '':
        return
    if not fn.endswith(".txt"):
        fn += ".txt"
    open(fn, 'wt').write(textbox.get('1.0', 'end'))

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
            fn = open(filename, "r")
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

def parseAsteriskCfg(emailList):
    print("Email List:", emailList)
    returnList = []
    dec_email = ''
    i = 1
    for email in emailList:
        email = email.replace('\n', '')
        m = re.findall(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+', email)
        if m:
            dec_email = dec_email + email + '; '
            if (i % 10 == 0):
                dec_email = re.sub(r'(.*)(; )($)', r'\1\3', dec_email)
                prefix = ""
                if ((i // 10) % 2 == 0):
                    prefix = "Cc: "
                else:
                    prefix = "To: "
                returnList.append(prefix+dec_email)
                dec_email = ''
            if (i % 20 == 0):
                print("")
            i = i + 1
    if dec_email:
        #dec_email = dec_email[:-2]  # remove 2 chars '; ' at the end of line.
        if prefix == "Cc: " :
            prefix = "To: "
        else :
            prefix = "Cc: "
        dec_email = re.sub(r'(.*)(; )($)', r'\1\3', dec_email)
        returnList.append(prefix + dec_email)
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