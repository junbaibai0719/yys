from random import random
from time import time,sleep
import win32api, win32gui, win32con, win32ui
from os import listdir
from cv2 import cv2
from PIL import Image
from threading import active_count, Thread
from queue import Queue

from yysLib import *


class Capture(Thread):
	def __init__(self, path,hwndQueue,waitMatchQ):
		super().__init__()
		self.path = path
		self.hwndQueue= hwndQueue
		self.waitMatchQ = waitMatchQ

	def run(self):
		while True:
			hwnd = self.hwndQueue.get()
			capture(self.path + '/temp', handle=hwnd)
			# print(hwnd)
			self.waitMatchQ.put(hwnd)

class MatchAndClick(Thread):
	def __init__(self, path,waitMatchQ):
		super().__init__()
		self.path = path
		self.waitMatchQ = waitMatchQ
		self.pos = None

	def run(self):
		count = 0
		while True:
			hwnd = self.waitMatchQ.get()
			imgPathList = listdir(self.path + '/template')
			for i in imgPathList:
				try:
					pos = match(self.path + '/temp/' + str(hwnd) + '.bmp', self.path + '/template/' + i)

				except Exception:
					print('match error')
				try:
					if pos != None:
						if i == 'aaaa.png':
							move_click(hwnd=hwnd, position=pos, t=0.1)
							move_click(hwnd=hwnd, position=pos, t=0.1)
							move_click(hwnd=hwnd, position=pos, t=0.1)
						# elif i == '111.png':
						# .sleep(10)
						# win32api.keybd_event(27,0,0,0)
						# win32api.keybd_event(27,0,win32con.KEYEVENTF_KEYUP,0)
						# .sleep(3)
						# win32api.keybd_event(13,0,0,0)
						# win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
						elif i == 'start.png':
							move_click(hwnd=hwnd, position=pos, t=0.5)
							print('开始战斗')
							print('第', count, '次-----------------------------------------')
						elif i == 'jsyq.png':
							move_click(hwnd=hwnd, position=pos, t=0.5)
							print('接受邀请')
							count += 1
						else:
							move_click(hwnd=hwnd, position=pos, t=0.5)
							print(str(hwnd) + str(pos) + 'wait 3s\n')
						break
				except Exception as e:
					print('click Error',e)


from yysLib import get_all_hwnds

def auto(Capture,MatchAndClick,path = './img'):
	hwndQueue = Queue(maxsize=2)
	waitMatchQ = Queue(maxsize=2)
	while True:

		hwnd_title = dict()
		hwnd_title = get_all_hwnds(hwnd_title)
		li = []
		for h, t in hwnd_title.items():
			if t == '阴阳师-网易游戏':
				hwndQueue.put(h)
				li.append(h)
		if active_count() <= li.__len__():
			cap = Capture(path=path,hwndQueue=hwndQueue,waitMatchQ=waitMatchQ)
			cap.setDaemon(True)
			cap.start()
			mac = MatchAndClick(path=path,waitMatchQ=waitMatchQ)
			mac.setDaemon(True)
			mac.start()

if __name__ == '__main__':
	auto(Capture,MatchAndClick)