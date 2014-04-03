#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import commands
import time
import subprocess
import os

ADB = 'adb'
ADB_SHELL = ADB + ' shell'
ADB_DEVICES = ADB + ' devices'
ANDROID_SERIAL='ANDROID_SERIAL'


class Util():

    def launchApplication(self,app):
        application = {'camera':'com.intel.camera22/.Camera',
                        'setting':'com.android.settings/.Settings',
                        'contact':'com.android.contacts/.activities.PeopleActivity',
                        'message':'com.android.mms/.ui.ConversationList',
                        'gallery':'com.intel.android.gallery3d/.app.Gallery',
                        'browser':'com.android.browser/.BrowserActivity',
                        'soundrecorder':'com.android.soundrecorder/.SoundRecorder'}
        #get all support application
        all_application = str(application.keys())
        if app not in all_application:
            print 'applicaiton name is wrong, only support ' + all_application
        else:
            #get the value of app
            component = application.get(app)
            #start activity
            d.start_activity(component = component)


    def backHome(self):
        for i in range(3):
            d.press.back()
        d.press.home()

    def setWifiOpenClose(self,status):
        all_status = {'on':'running','off':'stopped'}

        if status != 'on' and status != 'off':
            print 'please input on or off'
        else:
            wifivalue = self._getWifistatus()
            i = 1
            while all_status.get(status) not in wifivalue and i<3:
                #launch setting app
                d.start_activity(component='com.android.settings/.Settings')
                #print wifivalue
                #print status          
                #click wifi switch icon 
                d(resourceId='android:id/list',className="android.widget.ListView").child(index='1',className='android.widget.LinearLayout').child(className='android.widget.Switch').click.wait()
                self.sleep(5)
                wifivalue = self._getWifistatus()
                i+=1
            assert all_status.get(status) in wifivalue, 'set wifi status failed'
        self.backHome()

    def sleep(self,sec):
        time.sleep(sec)

    def _getWifistatus(self):
        #command of check wifi status
        Wifi_STATUS="adb shell getprop | grep init.svc.dhcpcd_wlan0"
        wifi = commands.getoutput(Wifi_STATUS)
        return wifi


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



