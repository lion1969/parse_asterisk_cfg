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
    ary.clear()
    ary = f.readlines()


def saveFile():
    fn = tkFileDialog.SaveAs(root, filetypes=[('*.txt files', '.txt')]).show()
    if fn == '':
        return
    if not fn.endswith(".txt"):
        fn += ".txt"
    open(fn, 'wt', encoding="utf8").write(textbox.get('1.0', 'end'))


def doProc():
    global ary
    # copy loaded file as array
    sip_conf_list = []
    sip_conf_list = ary.copy()
    ary.clear()
    # parse loaded file to global array 'ary'
    ary = parseAsteriskCfg(sip_conf_list)
    textbox.delete('1.0', 'end')
    txt2insert = ''
    for element in range(len(ary)):
        # print(ary[element])
        txt2insert = txt2insert + ary[element] + "\n"
    textbox.insert('1.0', txt2insert)
    print("Ary after parse:")
    print(ary)
    ary.clear()
    print('Len of clear list = ' + str(len(ary)))


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
        # inspect.stack()[0][3]) - Return name of function 'self name'
        print(inspect.stack()[0][3] + '() ERROR. File: ', filename)
        print("Either the file is missing or not readable")
        exit(0)


def parseAsteriskCfg(sip_conf_List):
    # print(''.join(sip_conf_List))
    global cvs_header
    returnList = []
    extension_hash_table = []
    extension_hash = {}

    for line in sip_conf_List:
        line = line.replace('\n', '')
        # m = re.findall(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+', line)
        match_extension = re.findall(r'^\[(\d+)\]$', line)
        match_comment = re.findall(r'^\s*;.*$', line)
        match_empty = re.findall(r'^\w*$', line)
        match_var_val = re.findall(r'(\w+)=(.+)$', line)
        if match_comment:  # skip comment line
            pass
            # returnList.append('_COMMENT_LINE')
        if match_empty:  # skip empty line
            pass
            # returnList.append('_EMPTY_LINE')
        if match_extension:
            print("ext matched: " + match_extension[0])
            if bool(extension_hash):
                print("new hash ID = ", match_extension[0])
                extension_hash = {}
            # init CSV header vars
            for field in cvs_header:
                extension_hash[field] = ""
            extension_hash['extension'] = match_extension[0]
            extension_hash_table.append(extension_hash)
            # returnList.append(match_extension[0])
        if match_var_val:
            # returnList.append(line)
            print(match_var_val[0][0] + '=' + match_var_val[0][1])
            extension_hash[match_var_val[0][0]] = match_var_val[0][1]
    print("=== call from ===    " + inspect.stack()[1].function + "()    === call from ===")

    # make header
    tmpline = ""
    for hh in cvs_header[:-1]:
        tmpline = tmpline + hh + ","
    tmpline = tmpline + str(cvs_header[-1])
    returnList.append(tmpline)

    # process extension_hash_table
    tmpline = ""
    for current_hash in extension_hash_table:
        tmpline = "dial=SIP/" + current_hash['extension'] + ","
        tmpline = tmpline + "icesupport" + "=" + current_hash['icesupport'] + ","
        tmpline = tmpline + "icesupport" + "=" + current_hash['icesupport'] + ","
    returnList.append(tmpline)
    return returnList


'''
file_name = 'sip.conf'
f = getFileHandler(file_name)
sip_conf = f.readlines()
ary = parseAsteriskCfg(sip_conf)
print('Ary first call:', ary)
'''
# Global array to store line from files.
ary = []
# Array of headers for CSV file
cvs_header = ["extension", "icesupport", "transport", "secret"]

# Interface init
root = Tk()
root.title('Parse Asterisk Cfg file.')
panelFrame = Frame(root, height=44, bg='light gray')
textFrame = Frame(root, height=340, width=600)

panelFrame.pack(side='top', fill='x')
textFrame.pack(side='bottom', fill='both', expand=1)

textbox = Text(textFrame, font='Arial 10', wrap='word')
scrollbar = Scrollbar(textFrame)

scrollbar['command'] = textbox.yview
textbox['yscrollcommand'] = scrollbar.set

textbox.pack(side='left', fill='both', expand=1)
scrollbar.pack(side='right', fill='y')

loadBtn = Button(panelFrame, text='Load', command=loadFile)
saveBtn = Button(panelFrame, text='Save', command=saveFile)
quitBtn = Button(panelFrame, text='Quit', command=doQuit)
procBtn = Button(panelFrame, text='Proc', command=doProc)

loadBtn.place(x=2, y=2, width=48, height=40)
saveBtn.place(x=52, y=2, width=48, height=40)
quitBtn.place(x=102, y=2, width=48, height=40)
procBtn.place(x=252, y=2, width=48, height=40)

root.mainloop()
