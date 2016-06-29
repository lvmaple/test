#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import base64,binascii,zlib
import os,random

base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]

def abc(str):
    return sha.new(str).hexdigest()

def bin2dec(string_num):
    return str(int(string_num, 2))

def hex2dec(string_num):
    return str(int(string_num.upper(), 16))

def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])

def dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])

def hex2bin(string_num):
    return dec2bin(hex2dec(string_num.upper()))

def bin2hex(string_num):
    return dec2hex(bin2dec(string_num))

def reverse(string):
    return string[::-1]

def read_key():
    os.system('cat flag')

def gb2312(string):
    return string.decode('gb2312')

answer='78864179732635837913920409948348078659913609452869425042153399132863903834522365250250429645163517228356622776978637910679538418927909881502654275707069810737850807610916192563069593664094605159740448670132065615956224727012954218390602806577537456281222826375'

func_names = ['fun1', 'fun2', 'fun3', 'fun4', 'fun5', 'fun6', 'fun7', 'fun8', 'fun9']

f={}

f['fun1']=reverse
f['fun2']=base64.b64decode
f['fun3']=zlib.decompress
f['fun4']=dec2hex
f['fun5']=binascii.unhexlify
f['fun6']=gb2312
f['fun7']=bin2dec
f['fun8']=hex2bin
f['fun9']=hex2dec

def check_equal(a, b):
    if a == b:
        return True
    try:
        if int(a) == int(b):
            return True
    except:
        return False
    return False

def main():

    print "Welcome to Secure Passcode System"
    print "First, please choose function combination:"

    in1=raw_input('f1: ')
    f1='fun'+in1[:1]
    in2=raw_input('f2: ')
    f2='fun'+in2[:1]
    in3=raw_input('f3: ')
    f3='fun'+in3[:1]
    in4=raw_input('f4: ')
    f4='fun'+in4[:1]

    if f1 not in func_names or f2 not in func_names or f3 not in func_names or f4 not in func_names:
        print 'invalid function combination'
        exit()

    try:
        answer_hash = f['fun6'](f['fun2'](f[f1](f[f2](f[f3](f[f4](answer))))))
    except:
        print "Wrong function combination, you bad guy!"
        exit()

    if len(answer_hash) == 0:
        print 'You must be doing some little dirty trick! Stop it!'
        exit()

    usercode = raw_input('Your passcode: ')

    try:
        user_hash = f['fun6'](f['fun2'](f[f1](f[f2](f[f3](f[f4](usercode))))))
        if user_hash == answer_hash:
            if check_equal(answer, usercode):
                print "This passcode has been locked, please use the new one\n"
            else:
                print "Welcome back! The door always open for you, your majesty! "
                read_key()
        else:
            print "Sorry, bad passcode.\n"
    except:
        print "Sorry, bad passcode. Please try again."

if __name__ == '__main__':
    main()

