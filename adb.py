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
This method support user execute adb commands,support push,pull,cat,refresh,ls,launch,rm

usage:  adb=Adb()
------------------------------------------------------------------------------------------------------------
| adb.cmd('cat','xxxx/xxx.xml')                 |  adb shell cat xxxx/xxx.xml,return cat result             | 
------------------------------------------------------------------------------------------------------------
| adb.cmd('refresh','/sdcard/')                 |  refresh media file under path /sdcard/,return ture/false |
------------------------------------------------------------------------------------------------------------
| adb.cmd('ls','/sdcard/')                      |  get the file number under path /sdcard/,return number    |                         
------------------------------------------------------------------------------------------------------------    
| adb.cmd('rm','xxxx/xxxx.jpg')                 |  delete xxxx/xxx.jpg,return true/false                    |
------------------------------------------------------------------------------------------------------------ 
| adb.cmd('launch','com.intel.camera22/.Camera')|  launch social camera app,return adb commands             |
------------------------------------------------------------------------------------------------------------
'''


class Adb():

    def cmd(self,action,path=None,t_path=None):
        #export android serial
        if not os.environ.has_key(ANDROID_SERIAL):
            self._exportANDROID_SERIAL()

        #adb commands
        action1={
        'refresh':self._refreshMedia,
        'ls':self._getFileNumber,
        'cat':self._catFile,
        'launch':self._launchActivity,
        'rm':self._deleteFile
        }
        action2=['pull','push']
        if action in action1:
            action1.get(action)(path)
        elif action in action2:
            self._pushpullFile(action,path,t_path)
        else:
            raise Exception('commands is unsupported,only support [push,pull,cat,refresh,ls,launch,rm] now')

    def _refreshMedia(self,path):
        p = self._shellcmd('am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://' + path)
        out = p.stdout.read().strip()
        print out
        if 'result=0' in out:
            return True
        else:
            return False

    def _getFileNumber(self,path):
        p = self._shellcmd('ls ' + path + ' | wc -l')
        out = p.stdout.read().strip()
        return out

    def _launchActivity(self,component):
        p = self_shellcmd('am start -n ' + component)
        return p

    def _catFile(self,path):
        p = self._shellcmd('cat ' + path)
        out = p.stdout.read().strip()
        return out

    def _deleteFile(self,path):
        p = self._shellcmd('rm -r  ' + path)
        p.wait()
        number = self._getFileNumber(path)
        if number == 0 :
            return True
        else:
            return False

    def _pushpullFile(self,action,path,t_path):
        beforeNO = self._getFileNumber(t_path)
        p = self._t_cmd(action + ' ' + path + ' ' + t_path)
        p.wait()
        afterNO = self._getFileNumber(t_path)
        if string.atoi(afterNO) > string.atoi(beforeNO):
            return True
        else:
            return False

    def _exportANDROID_SERIAL(self):
        #get device number
        device_number = self._getDeviceNumber()
        #export ANDROID_SERIAL=xxxxxxxx
        os.environ[ANDROID_SERIAL] = device_number

    def _getDeviceNumber(self):
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

    def _shellcmd(self,func):
        cmd = ADB_SHELL + ' ' + func
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    def _t_cmd(self,func):
        cmd = ADB + ' ' + func
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

