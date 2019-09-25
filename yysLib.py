from random import random
from time import time,sleep
from datetime import datetime
import win32api, win32gui, win32con, win32ui

from cv2 import cv2
from PIL import Image
from threading import active_count, Thread
from queue import Queue


def log(sentence = ''):
	nowTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
	with open('./log.txt','a') as f:
		f.writelines(sentence+',\t%s\n'%nowTime)
	print(sentence)

# 注意中文路径
def match(waitmatch, example, value=10000000):
	img = cv2.imread(waitmatch, 0)
	template = cv2.imread(example, 0)

	res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	flag = False
	if min_val < int(value):
		top_left = min_loc
		w, h = template.shape[::-1]
		return [top_left[0] + w // 2, top_left[1] + h // 2]
	else:
		return None


def get_window_info(wdName=u'阴阳师-网易游戏'):  # 获取阴阳师窗口信息
	handle = win32gui.FindWindow(0, wdName)  # 获取窗口句柄
	if handle == 0:
		return None
	else:
		return win32gui.GetWindowRect(handle)


def move_click(x=None, y=None, t=0, wdname=u'阴阳师-网易游戏', hwnd=None, position=[]):
	try:
		if position != []:
			x = position[0]
			y = position[1]
	except:
		print("坐标返回错误" + str(position))
	if hwnd is not None:
		handle = hwnd
	else:
		handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
	# client_pos = win32gui.ScreenToClient(handle, pos)
	tmp = win32api.MAKELONG(x, y)
	win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
	win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
	win32api.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
	if t == 0:
		sleep(random() * 2 + 1)  # sleep一下
	else:
		sleep(t)


def capture(path='', wdName=u'阴阳师-网易游戏', handle=None,x0=0,y0=0,w=0,h=0):
	try:
		# 获取要截取窗口的句柄

		if handle != None:
			hwnd = handle
		else:
			hwnd = win32gui.FindWindow(0, wdName)

		# 获取句柄窗口的大小信息
		# 可以通过修改该位置实现自定义大小截图
		if w == 0 or h == 0:
			left, top, right, bot = win32gui.GetWindowRect(hwnd)
			w = right - left
			h = bot - top

		# 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
		hwndDC = win32gui.GetWindowDC(hwnd)

		# 创建设备描述表
		mfcDC = win32ui.CreateDCFromHandle(hwndDC)

		# 创建内存设备描述表
		saveDC = mfcDC.CreateCompatibleDC()

		# 创建位图对象
		saveBitMap = win32ui.CreateBitmap()
		saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
		saveDC.SelectObject(saveBitMap)

		# 截图至内存设备描述表
		img_dc = mfcDC
		mem_dc = saveDC
		mem_dc.BitBlt((0, 0), (w, h), img_dc, (x0, y0), win32con.SRCCOPY)
		# mem_dc.BitBlt((0,0), (916,116), img_dc, (170, 270), win32con.SRCCOPY)

		# 将截图保存到文件中
		saveBitMap.SaveBitmapFile(mem_dc, path + '/%s.bmp'%hwnd)

		# 释放内存，不然会造成资源泄漏
		win32gui.DeleteObject(saveBitMap.GetHandle())
		saveDC.DeleteDC()
	# png = Image.open(path + '/temp.bmp')
	# png.save(path + '/temp.png')
	# return png
	except Exception as e:
		print("截图失败,%s,%s"%(e,path))

def get_all_hwnds(hwnd_title:dict):
	def get_all_hwnd(hwnd, mouse):
		if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
			hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

	win32gui.EnumWindows(get_all_hwnd, 0)
	return hwnd_title