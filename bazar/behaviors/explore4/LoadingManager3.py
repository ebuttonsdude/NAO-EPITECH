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
        
class LoadingManager(Singleton):
    def __init__(self):
      try:
        self.mutex
      except:
        self.fm = naoqi.ALProxy("ALFrameManager")        
        self.mutex = mutex.mutex()
        self.aLoaded = {}
        self.aRunning = {}

    def __del__(self):
      self.clear()
            
    def debug(self, msg):
      print msg
      pass
      
    def lock(self, locker):
      while self.mutex.test():
        self.debug("waiting for unlock: %s" % self.locker)
        time.sleep(0.2)
      self.mutex.testandset()
      self.debug("locked by %s" % locker)
      self.locker = locker
      
    def unlock(self):
      self.mutex.unlock()
      self.debug("unlocked by %s" % self.locker)
      self.locker = "None"
              
    def clear(self):
      self.lock("clear")
      values = self.aLoaded.values()
      self.aLoaded.clear()
      self.aRunning.clear()
      self.unlock()
        
      for id in values:
        try:
          self.fm.deleteBehavior(id)
        except:
          self.debug("%s could not delete behavior" % id)
    
    def dump(self, logger):
      s = "-"*43 + "\n"
      s += '|' + "loaded".center(20) + '|' + "running".center(20) + '|\n'
      s += "-"*43 + "\n"
      for k in self.aLoaded.keys():
        a = k.split('/')
        b = a[-1].replace(".xar", "")
        if b == "behavior":
          b = a[-2]
              
        if k in self.aRunning:
          s += '|' + b.center(20) + '|' + b.center(20) + '|\n' 
        else:
          s += '|' + b.center(20) + '|' + ' '.center(20) + '|\n'                
      s += "-"*43 + "\n"
      s += '|' + str(len(self.aLoaded)).center(20) + '|' + str(len(self.aRunning)).center(20) + '|\n'
      s += "-"*43 + "\n"
      self.debug(s)
        
    def getId(self, name):
      try:
        return self.aLoaded[name]
      except:
        return None
            
    def unload(self, name):
      self.lock("unload (%s)" % name)
      if name in self.aLoaded:
        id = self.aLoaded[name]
        del self.aLoaded[name]
        self.unlock()        
        try:              
          self.fm.deleteBehavior(id)          
        except:
          self.debug("%s could not delete behavior" % name)
        self.debug("%s removed from loaded array" % name)
      else:
        self.unlock()
        
    def load(self, name):
      self.lock("load (%s)" % name)
      # Check if behavior is already loaded    
      if name in self.aLoaded:
        id = self.aLoaded[name]
        self.unlock()
        # If behavior is currently loading, wait until loading has finished
        while id == "":
          time.sleep(0.5)
          try:
            id = self.aLoaded[name]
          except:
            id = None
          self.debug("%s wait for loading to end" % name)
        return id                    
      else:
        # Write a temporary empty id while loading
        self.aLoaded[name] = ""
        self.debug("%s is currently loading" % name)
        self.unlock()
        
        try:
          # Do load the behavior
          id = self.fm.newBehaviorFromFile(name, "")
        except:        
          # If an error occured during loading, remove the temporary entry in the array
          self.unload(name)
          self.debug( "%s behavior could not be found" % name)          
          return None
        
        # Write the real id now that it has been loaded
        self.lock("load (%s)" % name)
        self.aLoaded[name] = id
        self.unlock()
        self.debug("%s is now loaded with id : %s" % (name, id))

        return id
        
    def play(self, name, id, oBehavior, delete, args):
      if id == None or id == "":
        return
        
      self.lock("play (%s)" % name)
      # Check if behavior is already running
      if name in self.aRunning:
        self.unlock()
        return

      self.aRunning[name] = delete
      self.unlock()
      self.debug("%s added to running array" % name)

      # Add a parameter to detect end of behavior
      args["finished"] = False
      # Add to the behaviors some custom parameters
      for k, v in args.items():
        oBehavior.addParameter(k, v, True)
        self.debug("%s = %s" % (k, v))
                  
      # The behavior won't be deleted after playing
      if not delete:
        try:
          self.fm.playBehavior(id)
        except:
          self.lock("no play %s" % name)
          del self.aRunning[name]
          self.unlock()
          # As we had a probleme playing the behavior, unload it (so we can reload it later)
          self.unload(name)        
          self.debug("%s could not play" % name)
          return
          
        end = False
        go = True
        # Wait until behavior has finished
        while not end and go:
          time.sleep(0.5)
          end = oBehavior.getParameter("finished")
          go = name in self.aRunning
      # The behavior will be deleted after playing
      else:
        try:
          # This is a blocking function, so it wont end until the behavior has finished
          self.fm.completeBehavior(id)
        except:
          self.debug("%s behavior was not properly unloaded" % name)
          return
      # Remove this behavior from running array and eventually delete it
      self.stop(name)
            
    def stop(self, name):
      self.lock("stop (%s)" % name)    
      if name in self.aRunning:
        # First get the behavior id
        id = self.aLoaded[name]
        # Check the flag that tells us if we have to delete the behavior after running
        delete = self.aRunning[name]
        # Remove the behavior from the running behavior list
        del self.aRunning[name]
        self.unlock()
        self.debug("%s removed from running array" % name)
        
        if delete==False:
          # Exit the behavior
          self.fm.exitBehavior(id)
        else:
          del self.aLoaded[name]
          try: 
            self.fm.deleteBehavior(id)
          except:
            self.debug("%s could not delete behavior" % name)
      else:
        self.unlock()