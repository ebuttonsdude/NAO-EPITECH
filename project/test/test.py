#
# Nao porject test.py
# Made by platel_k
#

## Import
from naoqi import ALProxy

## Code
#nao = "127.0.0.1"
nao = "192.168.0.42"
tts = ALProxy("ALTextToSpeech", nao, 9559)
motion = ALProxy("ALMotion", nao, 9559)
motion.walkInit()
motion.post.walkTo(0.5, 0, 0)
tts.say("Bonjour")