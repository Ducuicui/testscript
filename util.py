#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import commands
import time

def launchApplication(app):
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

def backHome():
    for i in range(3):
        d.press.back()
    d.press.home()

def _getWifistatus():
    #command of check wifi status
    Wifi_STATUS="adb shell getprop | grep init.svc.dhcpcd_wlan0"
    wifi = commands.getoutput(Wifi_STATUS)
    return wifi

def setWifiOpenClose(status):
    if status != 'running' and status != 'stopped':
        print 'please input running or stopped'
    else:
        #launch setting app
        d.start_activity(component='com.android.settings/.Settings')
        wifivalue = _getWifistatus()
        i = 1
        while status not in wifivalue and i<3:
            print wifivalue
            print status          
            #click wifi switch icon 
            d(resourceId='android:id/list',className="android.widget.ListView").child(index='1',className='android.widget.LinearLayout').child(className='android.widget.Switch').click.wait()
            time.sleep(5)
            wifivalue = _getWifistatus()
            i+=1
            


if __name__ == '__main__':
    setWifiOpenClose('running')


