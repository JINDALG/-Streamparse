from __future__ import absolute_import, print_function, unicode_literals
import traceback; 
import cv2
import numpy as np
import time
# import imutils
import json
import base64

from datetime import datetime
from streamparse.bolt import Bolt

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
		self.frames = tup.values[0]
		for i in xrange(3):
			self.frames[i] = json.loads(self.frames[i], object_hook=json_numpy_obj_hook)
			# with open('a.txt','ab+') as f:
			# 	f.write(str(self.frames[i])+'\n')
		self.sID = tup.values[1]

		for i in xrange(3):
			self.gray[i] = cv2.cvtColor(self.frames[i],cv2.COLOR_BGR2GRAY)
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
			cv2.rectangle(self.frames[1], (x, y), (x + w, y + h), (0, 255, 0), 2)
			flag = 1

		if flag == 0:
			z = None
		else:
			z = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S motion\n'))

		self.emit([z,self.sID])
		self.log('%s' %(z))