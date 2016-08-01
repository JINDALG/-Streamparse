from __future__ import absolute_import, print_function, unicode_literals
import traceback; 
import cv2
import numpy as np
import time
# import imutils
import json
import base64
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from datetime import datetime
from streamparse.bolt import Bolt
import os

def build_gif(imgs, show_gif=True, save_gif=True, title='',sID = ''):

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_axis_off()

	ims = map(lambda x: (ax.imshow(x), ax.set_title(title)), imgs)

	im_ani = animation.ArtistAnimation(fig, ims, interval=800, repeat_delay=0, blit=False)

	if save_gif:
		if not os.path.exists(sID):
			os.makedirs(sID)
		im_ani.save(sID+'/animation.gif', writer='imagemagick')
		plt.show()
	return


def json_numpy_obj_hook(dct):
	"""Decodes a previously encoded numpy ndarray with proper shape and dtype.

	:param dct: (dict) json encoded ndarray
	:return: (ndarray) if input was an encoded ndarray
	"""
	if isinstance(dct, dict) and '__ndarray__' in dct:
		data = base64.b64decode(dct['__ndarray__'])
		return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
	return dct


class Motion_Bolt(Bolt):
	def initialize(self, conf, ctx):
		self.gray = [0]*3
		self.diff = [0]*3

	def process(self,tup):
		flag = 0
		frames = tup.values[0]
		for i in xrange(3):
			frames[i] = json.loads(frames[i], object_hook=json_numpy_obj_hook)
		sID = tup.values[1]

		for i in xrange(3):
			self.gray[i] = cv2.cvtColor(frames[i],cv2.COLOR_BGR2GRAY)
			self.gray[i] = cv2.GaussianBlur(self.gray[i], (3,3), 3)
		for i in xrange(2):
			self.diff[i] = cv2.absdiff(self.gray[i],self.gray[i+1])
		self.diff[2] = self.diff[0] & self.diff[1]
		thresh = cv2.threshold(self.diff[2], 25, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		min_area = 500
		for c in cnts:
			if cv2.contourArea(c) < min_area:
				continue
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frames[1], (x, y), (x + w, y + h), (0, 255, 0), 2)
			flag = 1

		if flag == 0:
			z = None
		else:
			z = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S motion'))
			if not os.path.exists(sID):
				os.makedirs(sID)
				with open(sID+'/log.txt','w') as log:
					log.write(z)
				build_gif(imgs =frames,sID=sID)
			else :
				with open(sID+'/log.txt','r+') as log:
					prev = log.read()
					prev = prev.replace(' motion','')
					prev = datetime.strptime(prev, '%Y-%m-%d %H:%M:%S')
					diff = datetime.now()-prev
					diff = diff.seconds
					if diff >= 30:
						log.write(z)
						build_gif(imgs =frames,sID=sID)
		self.emit([z,sID])
		self.log('%s' %(z))