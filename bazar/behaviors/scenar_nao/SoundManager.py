import time
import mutex
import naoqi

class Singleton(object):
    # Dict referencing already created instance
    instances = {}
    def __new__(cls, *args, **kargs): 
      if Singleton.instances.get(cls) is None:
        Singleton.instances[cls] = object.__new__(cls, *args, **kargs)
      return Singleton.instances[cls]

class Sound:
  def __init__(self, uid, path):
    self.id = None
    self.proxy = None
    self.uid = uid
    self.path = path
    self.mutex = mutex.mutex()
    self.loaded = False

  def __del__(self):
    pass

  def debug(self, msg):
    print msg
    pass
      
  def lock(self):
      while self.mutex.test():
        self.debug("waiting for unlock: %s" % self.uid)
        time.sleep(0.2)
      self.mutex.testandset()
      self.debug("locked by %s" % self.uid)
      
  def unlock(self):
      self.mutex.unlock()
      self.debug("unlocked by %s" % self.uid)
          
  def load(self, proxy):
    self.lock()
    # Do not load twice the same audio file
    if self.loaded == True:
      self.debug("Audio file %s is already loaded")
      self.unlock()
      return True
    # Check if provided proxy is valid
    if proxy == None:
      if self.proxy == None:
        self.debug("Cannot load an audio file with an invalid proxy")
        self.unlock()
        return False
    # if proxy has changed (?) update it
    else:
      # Here I should probably unload audio file on old proxy ??
      self.proxy = proxy

    try:
      self.id = self.proxy.loadFile(self.path)
      self.loaded = True
    except:
      self.debug("Could not load audio file : %s" % self.path)
      self.unlock()
      return False
      
    self.unlock()
    return True
    
  def play(self, proxy):
    self.lock()
    # Check if audio file is loaded
    if not self.loaded:
      self.unlock()
      self.load(proxy)
      self.lock()
    # The audio file should now be loaded
    if self.loaded == True:
      self.unlock()
      self.proxy.play(self.id)
    else:
      self.unlock()

  def stop(self):
    self.lock()
    if self.loaded == True and self.proxy != None:
      self.proxy.stop(self.id)
    self.unlock()
              
  def unload(self):
    self.lock()
    if self.id != None and self.proxy != None:
      self.proxy.unloadFile(self.id)
      self.id = None
      self.loaded = False
    self.unlock()
    
                
class SoundManager(Singleton):
    def __init__(self):
      try:
        self.mutex
      except:
        self.audioProxy = naoqi.ALProxy("ALAudioPlayer")        
        self.mutex = mutex.mutex()
        self.aSoundBank = {}

    def __del__(self):
      self.lock("clear")
      sounds = self.aSoundBank.values()
      self.aSoundBank.clear()
      self.unlock()
      for sound in sounds:
        try:
          sound.unload()
        except:
          self.debug("%s could not delete audio file" % id)

    def debug(self, msg):
      print msg
      pass
    
    def lock(self, locker):
      while self.mutex.test():
        self.debug("%s : waiting to unlock" % self.locker)
        time.sleep(0.2)
      self.mutex.testandset()
      self.debug("%s: has locked" % locker)
      self.locker = locker
      
    def unlock(self):
      self.mutex.unlock()
      self.debug("%s: has unlocked" % self.locker)
      self.locker = "None"
            
    def load(self, uid, path):
      self.lock(uid)
      if uid not in self.aSoundBank:
        sound = Sound(uid, path)
        if sound.load(self.audioProxy) == True:
          self.aSoundBank[uid] = sound
      self.unlock()
      
    def play(self, uid, path):
      self.lock(uid)
      # If sound not yet loaded, try to load it
      if uid not in self.aSoundBank:
        self.unlock()
        self.load(uid, path)
        self.lock(uid)
        
      # The audio file should be loaded now
      if uid in self.aSoundBank:
        sound = self.aSoundBank[uid]
        self.unlock()
        sound.play(self.audioProxy)
      else:
        self.unlock()
        self.debug("%s could not be play/loaded" % uid)

    def stop(self, uid):
      self.lock(uid)
      if uid in self.aSoundBank:
        self.aSoundBank[uid].stop()
      self.unlock()
            
    def unload(self, uid):
      self.lock(uid)
      if uid in self.aSoundBank:
        sound = self.aSoundBank[uid]
        sound.unload()
        del self.aSoundBank[uid]
      self.unlock()