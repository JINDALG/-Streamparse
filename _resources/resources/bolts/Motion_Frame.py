from __future__ import absolute_import, print_function, unicode_literals
import traceback
import cv2
import numpy as np
import time
# import imutils
import base64

from datetime import datetime
from streamparse.bolt import Bolt
import json

class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        """If input object is an ndarray it will be converted into a dict 
        holding dtype, shape and the data, base64 encoded.
        """
        if isinstance(obj, np.ndarray):
            if obj.flags['C_CONTIGUOUS']:
                obj_data = obj.data
            else:
                cont_obj = np.ascontiguousarray(obj)
                assert(cont_obj.flags['C_CONTIGUOUS'])
                obj_data = cont_obj.data
            data_b64 = base64.b64encode(obj_data)
            return dict(__ndarray__=data_b64,
                        dtype=str(obj.dtype),
                        shape=obj.shape)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder(self, obj)


class Motion_Frame(Bolt):
	def initialize(self, conf, ctx):
		self.frames = [0]*3

	'''
	Frames might not be able to get passed, hence generating the error of bad file descriptor
	So, might need to dissolve this bolt and do everything in Motion_Bolt
	# '''
	def process(self, tup):
		x = tup.values[0]
		camera = cv2.VideoCapture(x)
		i=0
		while True:
			a = []
			for i in range(3):
				ret ,self.frames[i] = camera.read()
				lisp = x
				# a = lisp[0]
				a += [json.dumps(self.frames[i], cls=NumpyEncoder)]
	
			self.emit([a,x])
			self.log('%s'%x)
			i+=1