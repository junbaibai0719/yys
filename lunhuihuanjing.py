from yysLib import *
from auto import Capture,MatchAndClick,auto
from os import listdir
from time import time

wdName=u'阴阳师-网易游戏'
path = 'lunhuihuanjing'
temp_path = 'lunhuihuanjing/temp'
template_path = 'lunhuihuanjing/template'
hwnd = win32gui.FindWindow(0, wdName)
hwnd_title = {}
get_all_hwnds(hwnd_title)




	


class LunHuiHuanJing(MatchAndClick):
	def mc_p(self,path,hwnd):
		imgPathList = listdir(path)
		for i in imgPathList:
			try:
				self.pos = match(waitmatch=temp_path + '/%s.bmp' % hwnd, example=path+'/'+i)
				if self.pos:
					move_click(position = self.pos,hwnd=hwnd)
					log('click:%s,path:%s'%(self.pos,path+'/%s'%i))
			except Exception as e:
				log('%s'%e)
				log('example:%s'%path+'/%s'%i)
		
			
	def run(self):
		count = 0
		x0, y0, _w, _h = 170, 270, 936, 116
		t = time()
		while True:
			hwnd = self.waitMatchQ.get()
			self.mc_p(template_path,hwnd)
			self.mc_p(path+'/y',hwnd)
			self.mc_p(path+'/bx',hwnd)

			self.mc_p(path+'/yl',hwnd)	

			self.mc_p(path+'/xyc',hwnd)
			self.mc_p(path+'/tz',hwnd)

		
			log('capture:%s/%s.bmp'%(path,hwnd))	
			capture(path, handle=hwnd, x0=x0, y0=y0, w=_w, h=_h)
			try:
				pos = match(waitmatch=path + '/%s.bmp' % hwnd, example=path + '/' + 'block.png')
			except Exception as e:
				log('%s'%e)
			if pos != None:
				move_click(x=pos[0] + x0, y=pos[1] + y0, hwnd=hwnd)
				log('点击%s,%s' % (pos[0] + x0, pos[1] + y0))
				last = t
				t = time()
				if t-last<=3:
					capture(path, handle=hwnd)
					pos = match(waitmatch=path + '/%s.bmp' % hwnd, example=path + '/' + 'block.png')
					if pos != None:
						move_click(position=pos, hwnd=hwnd)
						log('点击%s,%s' % (pos[0] + x0, pos[1] + y0))
			else:
				capture(path, handle=hwnd)
				pos = match(waitmatch=path + '/%s.bmp' % hwnd, example=path + '/' + 'block.png')
				if pos != None:
					move_click(position=pos, hwnd=hwnd)
					log('点击%s,%s' % (pos[0] + x0, pos[1] + y0))

if __name__ == '__main__':
	auto(Capture,LunHuiHuanJing,path)

