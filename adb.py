#!/usr/bin/python
# coding:utf-8

import subprocess
import os
import string

ADB = 'adb'
ADB_SHELL = ADB + ' shell'
ADB_DEVICES = ADB + ' devices'
ANDROID_SERIAL='ANDROID_SERIAL'

'''
This method support user execute adb commands,support push,pull,cat,refresh,ls,launch,delete,export
usage:  
------------------------------------------------------------------------------------------------------------
| adbcmd('cat','xxxx/xxx.xml')                 |  adb shell cat xxxx/xxx.xml,return cat result             | 
------------------------------------------------------------------------------------------------------------
| adbcmd('refresh','/sdcard/')                 |  refresh media file under path /sdcard/,return ture/false |
------------------------------------------------------------------------------------------------------------
| adbcmd('ls','/sdcard/')                      |  get the file number under path /sdcard/,return number    |                         
------------------------------------------------------------------------------------------------------------    
| adbcmd('rm','xxxx/xxxx.jpg')                 |  delete xxxx/xxx.jpg,return true/false                    |
------------------------------------------------------------------------------------------------------------ 
| adbcmd('launch','com.intel.camera22/.Camera')|  launch social camera app,return adb commands             |
------------------------------------------------------------------------------------------------------------
'''

def adbcmd(action,path=None,t_path=None):
    #export android serial
    if not os.environ.has_key(ANDROID_SERIAL):
        _exportANDROID_SERIAL()
    #adb commands
    action1={
    'refresh':_refreshMedia,
    'ls':_getFileNumber,
    'cat':_catFile,
    'launch':_launchActivity,
    'rm':_deleteFile
     }
    action2=['pull','push']
    if action in action1:
        action1.get(action)(path)
    elif action in action2:
        pushpullFile(action,path,t_path)
    else:
        raise Exception('commands is unsupported,only support [push,pull,cat,refresh,ls,launch,delete,export] now')

def _refreshMedia(path):
    p = _shellcmd('am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://' + path)
    out = p.stdout.read().strip()
    print out
    if 'result=0' in out:
        return True
    else:
        return False

def _getFileNumber(path):
    p = _shellcmd('ls ' + path + ' | wc -l')
    out = p.stdout.read().strip()
    print out
    return out

def _launchActivity(component):
    p = _shellcmd('am start -n ' + component)
    return p

def _catFile(path):
    p = _shellcmd('cat ' + path)
    out = p.stdout.read().strip()
    print out
    return out

def _deleteFile(path):
    p = _shellcmd('rm -r  ' + path)
    p.wait()
    number = getFileNumber(path)
    if number == 0 :
        return True
    else:
        return False

def _pushpullFile(action,path,t_path):
    beforeNO = getFileNumber(t_path)
    p = _cmd(action + ' ' + path + ' ' + t_path)
    p.wait()
    afterNO = getFileNumber(t_path)
    if string.atoi(afterNO) > string.atoi(beforeNO):
        return True
    else:
        return False

def _exportANDROID_SERIAL():
    #get device number
    device_number = _getDeviceNumber()
    #export ANDROID_SERIAL=xxxxxxxx
    os.environ[ANDROID_SERIAL] = device_number

def _getDeviceNumber():
    #get device number, only support 1 device now
    #show all devices
    cmd = ADB_DEVICES
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    out=p.stdout.read().strip()
    #out is 'List of devices attached /nRHBxxxxxxxx/t device'
    words_before = 'List of devices attached'
    word_after = 'device'
    #get device number through separate str(out)
    device_number = out[len(words_before):-len(word_after)].strip()
    if len(device_number) >= 15:
        raise Exception('more than 1 device connect,only suppport 1 device now')
    else:
        return device_number

def _shellcmd(func):
    #export ANDROID_SERIAL=xxxxx
    #run exportANDROID_SERIAL() before
    #adb command
    #device_number = _getDeviceNumber()
    cmd = ADB_SHELL + ' ' + func
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

def _cmd(func):
    cmd = ADB + ' ' + func
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)



if __name__ == '__main__':
    adbcmd('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml')

