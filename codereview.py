#!/usr/bin/python
# -*- coding:utf-8 -*- 

import unittest
import commands
from uiautomator import device as d
import time
import string
import util as u


Delete_CMD = 'adb shell rm -r sdcard/DCIM/100ANDRO/'


class CameraTest(unittest.TestCase):

	def setUp(self):
		u.launchcamera()
		#show menu bar at top
		commands.getoutput('adb shell input swipe 530 6 523 22')
		time.sleep(1)

	#case 1 summary:test capture picture with sence auto
	def testcapturewithsenceauto(self):
		#set back camera
		u.SingleCamera.setcamerastatus('back')
		#set sence auto
		u.SingleCamera.setsencestatus('auto')
		#capture picture
		u.SingleCamera.takesinglepicture()


	def tearDown(self):
		for i in range(3):
			d.press.back()
		commands.getoutput(Delete_CMD)