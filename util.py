import commands
from uiautomator import device as d
import time
import string
import os

PACKAGE_NAME = 'com.intel.camera2'
ACTIVITY_NAME = PACKAGE_NAME + '.Camera'
DCIM_PATH = 'adb shell ls /sdcard/DCIM'
CAMERA_FOLDER = '100ANDRO'
CAMERA_ID = 'adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'
Flash_STATE= 'adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_flashmode_key'
Exposure_STATE= 'adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_exposure_key'
Scene_STATE = 'adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_scenemode_key'
FDFR_STATE ='adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_fdfr_key'
PictureSize_STATE ='adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_picture_size_key'
Geolocation_STATE ='adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_geo_location_key' 
Hints_STATE ='adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_hints_key'
WhiteBalance_STATE='adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_whitebalance_key'
ISO_STATE='adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_iso_key'
SelfTimer_STATE='adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep pref_camera_delay_shooting_key'
Delete_CMD = 'adb shell rm -r sdcard/DCIM/100ANDRO/'
CAMERA_ID_FRONT = '1'
CAMERA_ID_BACK = '0'
PICTURE_PATH = '' + os.sep + 'mnt'+os.sep+ DCIM_PATH+'/'+CAMERA_FOLDER
Switch_desceiption = 'Front and back camera switch'
Shuttor_description = 'Shutter button'
Setting_description = 'Camera settings'
Flash_description = 'Flash settings'
FDFR_description = 'Face recognition'



def launchcamera():
    d(description='Apps').click.wait()
    while not d.exists(text='Camera'):
        d().swipe.right()
        time.sleep(3)
    d(text='Camera').click.wait()
    d(description="Shutter button").wait.exists(timeout=3000)
    time.sleep(5)


class SingleCamera():
    def setcamerastatus(status):
		#check back/front camera and set
        if status == 'back':
            #check camera back? if yes--pass, if no--set to back camera and check
            camera = commands.getoutput(CAMERA_ID)
            cameravalue = camera.find(CAMERA_ID_BACK)
            if cameravalue == -1:
	        	commands.getoutput('adb shell input swipe 530 6 523 22')
	        	d(description=Switch_desceiption).click.wait()
	        	camera = commands.getoutput(CAMERA_ID)
	        	cameravalue = camera.find(CAMERA_ID_BACK)
	        	assert cameravalue != -1
        if status == 'front':
            #check camera front? if yes--pass, if no--set to front camera and check
            camera = commands.getoutput(CAMERA_ID)
            cameravalue = camera.find(CAMERA_ID_FRONT)
            if cameravalue == -1:
	        	commands.getoutput('adb shell input swipe 530 6 523 22')
	        	d(description=Switch_desceiption).click.wait()
	        	camera = commands.getoutput(CAMERA_ID)
	        	cameravalue = camera.find(CAMERA_ID_FRONT)
	        	assert cameravalue != -1  

    def takesinglepicture():
        #get picture number before capture
        result = commands.getoutput('adb shell ls '+ DCIM_PATH)
        if result.find(CAMERA_FOLDER) == -1:
	    	beforeNO = 0
        else:
	    	beforeNO = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep IMG | wc -l')
        	time.sleep(2)
        #capture
        d(description=Shuttor_description).click.wait()
        time.sleep(3)
        #check picture number after capture
        afterNO = commands.getoutput('adb shell ls /sdcard/DCIM/* | grep IMG | wc -l')
        #assert
        assert string.atoi(beforeNO) == string.atoi(afterNO) - 1



    def setsencestatus(status):
        #tap setting icon
        d(description=Setting_description).click.wait()
        #tap sence icon
        commands.getoutput('adb shell input tap 531 165')
        time.sleep(1)
        #set sence mode
        def setsenceauto():
            commands.getoutput('adb shell input swipe 660 285 66 285')
            commands.getoutput('adb shell input tap 657 294')
        def setsencesports():
            commands.getoutput('adb shell input swipe 660 285 66 285')
            commands.getoutput('adb shell input tap 534 290')
        def setsencenight():
            commands.getoutput('adb shell input tap 643 290')
        def setsencelandscape():
            commands.getoutput('adb shell input tap 512 290')
        def setsenceportrait():
            commands.getoutput('adb shell input tap 385 290')
        def setsencenp():
            commands.getoutput('adb shell input tap 285 290')
        def setsencebarcode():
            commands.getoutput('adb shell input tap 177 290')
        def setsencefireworks():
            commands.getoutput('adb shell input tap 58 290')

        sence = {'auto': setsenceauto,
                'sports':setsencesports,
                'night':setsencenight,
                'landscape':setsencelandscape,
                'portrait':setsenceportrait,
                'night-portrait':setsencenp,
                'barcode':setsencebarcode,
                'fireworks':setsencefireworks}

        sence[status]()	
        time.sleep(3)
        #check sence mode set successful?
        state = commands.getoutput(Scene_STATE)
        statevalue = state.find(status)
        assert statevalue != -1

