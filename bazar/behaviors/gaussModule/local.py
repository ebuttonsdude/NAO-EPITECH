from naoqi import ALModule
from naoqi import ALProxy



class BasicModule(ALModule):
	"""module description"""
	"""this is a main module"""
	def gaussfunc(self,a):
		"""method description (mandotory )"""
		tts= ALProxy("ALTextToSpeech")
		tts.say(a)
		print 'inside module method'+a
		#return a
		
class GaussModule(ALModule):
	"""This is gauss Module"""
	def movefunc(self,a):
		"""method to move head"""
		motion=ALProxy("ALMotion")
		print 'Head is moving!'
		motion.angleInterpolation ("HeadPitch", a, 2.0, True)
