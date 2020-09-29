import re
import os
import sys
import warnings
import numpy as np
import pandas as pd


delims= [
    
    ('\&',    'AND'),
    ('\~',    'TILDE'),
    (r'\\',   'BACK_SLASH'),
    ('\^',    'HAT'),
    ('\#',   'TAG')

]


regex_parts=[]
group={}
for regex, types in delims:
    regex_parts.append('(?P<%s>%s)' % (types, regex))
regex=re.compile('|'.join(regex_parts))


def parser (message):
    message_array= np.array ([['smack']], dtype='<U200')
    parser=re.compile ('\|')
    position_parser=parser.search(message)
    if not position_parser: 
        message_array[0]=message
        return message_array
    else:
        position_parser=parser.search(message).end()-1
        index=message [: (position_parser)]
        message_array [0]=index
        message=message[(position_parser+1) :]
        position_parser=0
        i=0
        while 1:
            k=parser.search(message)
            if k:
                m=k.end()-1
                if m==position_parser:
                    message_array=np.append (message_array, np.array([['Empty']]), 1)
                    message=message[(position_parser+1) :]
                else:
                    block=message[: m]
                    message_array=np.append (message_array, np.array([[block]]), 1)
                    message=message[(m+1) :]
            else: 
                message_array=np.append(message_array, np.array([message]))
                break
    
        return message_array

def parser_p (message):
    message_array=parser(message)
    block={}
    cc=[]
    mesa=np.reshape (message_array, (len(message_array), ))
    for i in range (len(mesa)):
        block_i=np.array(['Null'], dtype="<U200")
        count=0
        while 1:
            k=regex.search(mesa[i])
            if k:
                if not i in cc:
                    cc.append(i)
                m=k.end()-1
                if m !=0:
                    block_i=np.append (block_i, np.array([mesa[i][:(m)]]))
                    mesa[i]=mesa[i][(m+1):]
                else:
                    mesa[i]=mesa[i][(m+1):]
                count+=1
                block[i]=block_i[1:]
            else:
                if count!= 0 and len(mesa[i])!=0:
                    block_i=np.append(block_i, [mesa[i]])
                    block[i]=block_i[1:]
                break
            
    return block, cc

def listing (message):
    parsed=parser(message)
    parsed_p=parser_p(message)
    t=[]
    check=0
    for i in parsed:
        if check in parsed_p[1]:
            lst=parsed_p[0][check]
            np.reshape(lst, (len(lst)))
            lst=lst.tolist()
            t.append(lst)
        else:
            t.append([i])
        check+=1
    return t


def hl7 (path, file=True):
    if file:
        file=open(path, 'r')
        lines=file.readlines()
        total={}
        i=1
        for line in lines:
            t=listing(line)
            if t[0]==['MSH']:
                t[1]=['^~\\&']
            total['%s' % t[0][0]]=t[1:]
    else:
        t=listing(path)
        if t[0]==['MSH']:
            t[1]=['^~\\&']
        total['%s' % t[0]]=t[1:]
    return total