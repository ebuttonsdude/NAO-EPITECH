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
        self.debug("%s is waiting for unlock by %s" % (locker, self.locker))
        time.sleep(0.2)
      self.mutex.testandset()
      self.debug("Now locked by %s" % locker)
      self.locker = locker
      
    def unlock(self):
      self.mutex.unlock()
      self.debug("unlocked by %s" % self.locker)
      self.locker = "None"
              
    def clear(self):
      self.lock("clear")
      try:
        values = self.aLoaded.values()
        self.aLoaded.clear()
        self.aRunning.clear()
      except Exception as ex:
        self.debug("clear: an error occured, %s" % ex)
      self.unlock()
        
      for id in values:
        try:
          self.fm.deleteBehavior(id)
        except Exception as ex:
          self.debug("%s could not delete behavior, %s" % (id, ex))
    
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
      except Exception as ex:
        self.debug(ex)
        return None
            
    def unload(self, name):
      if name == None:
        return
      self.lock("unload (%s)" % name)
      try:
        if name in self.aLoaded:
          id = self.aLoaded[name]
          del self.aLoaded[name]
          self.unlock()        
          try:              
            self.fm.deleteBehavior(id)          
          except Exception as ex:
            self.debug("%s could not delete behavior, %s" % (name, ex))
          self.debug("%s removed from loaded array" % name)
        else:
          self.unlock()
      except Exception as ex:
        self.debug("unload: an error occured, %s" % ex)
        self.unlock()
        
    def load(self, name):
      if name == None:
        return
        
      self.lock("load (%s)" % name)
      try:
        # Check if behavior is already loaded    
        if name in self.aLoaded:
          id = self.aLoaded[name]
          self.unlock()
          # If behavior is currently loading, wait until loading has finished
          while id == "":
            time.sleep(0.5)
            try:
              id = self.aLoaded[name]
            except Exception as ex:
              id = None
              self.debug("load: exception, id = None (%s), %s" % (name, ex))
            self.debug("%s is already loading" % name)
          return id                    
        else:
          # Write a temporary empty id while loading
          self.aLoaded[name] = ""
          self.unlock()
        
        try:
          # Do load the behavior
          self.debug("%s start loading" % name)          
          id = self.fm.newBehaviorFromFile(name, "")
        except Exception as ex:        
          # If an error occured during loading, remove the temporary entry in the array
          self.unload(name)
          self.debug( "%s behavior could not be found, %s" % (name, ex))          
          return None
        
        # Write the real id now that it has been loaded
        self.lock("loaded (%s)" % name)
        self.aLoaded[name] = id
        self.unlock()
        self.debug("%s is now loaded with id : %s" % (name, id))

        return id
      except Exception as ex:
        self.debug("load: an error occured, %s" % ex)
        self.unlock()
        return None        
        
    def play(self, name, id, oBehavior, delete, args):
      # If parameters are not valid don't do anything
      if id == None or id == "" or oBehavior == None:
        return
        
      self.lock("play (%s)" % name)
      try:
        # Check if behavior is already running
        if name in self.aRunning:
          self.unlock()
          return
          
        self.aRunning[name] = delete
        self.unlock()
        self.debug("play: %s added to running" % name)

        # The behavior won't be deleted after playing
        if not delete:
          self.play_and_keep(name, id, oBehavior, delete, args)
        # The behavior will be deleted after playing
        else:
          self.play_and_delete(name, id, oBehavior, delete, args)
      except Exception as ex:
        self.debug("play: an error occured, %s" % ex)
        self.unlock()

    def play_and_keep(self, name, id, oBehavior, delete, args):
      # Add a parameter to detect end of behavior
      args["finished"] = False
      # Add to the behaviors some custom parameters
      for k, v in args.items():
        oBehavior.addParameter(k, v, True)
                  
      try:
        # This call is not blocking
        self.fm.playBehavior(id)
        end = False
        go = True
        # Wait until behavior has finished
        while not end and go:
          time.sleep(0.5)
          end = oBehavior.getParameter("finished")
          go = name in self.aRunning        
      except Exception as ex:
        self.debug("play and keep: could not play %s, %s" % (name, ex))
        self.unload(name)
      else:
        self.stop(name)        
        

      
    def play_and_delete(self, name, id, oBehavior, delete, args):
      try:
        # This is a blocking function, so it wont end until the behavior has finished
        self.fm.completeBehavior(id)
      except Exception as ex:
        self.debug("play and delete: could not play %s, %s" % (name, ex))

      self.lock("play and delete (%s)" % name)
      del self.aRunning[name]
      del self.aLoaded[name]
      self.unlock()
                  
    def stop(self, name):
      if name == None:
        return
      self.lock("stop (%s)" % name)
      try:    
        if name in self.aRunning:
          # First get the behavior id
          id = self.aLoaded[name]
          # Check the flag that tells us if we have to delete the behavior after running
          delete = self.aRunning[name]
          # Remove the behavior from the running behavior list
          del self.aRunning[name]
          self.unlock()
          
          if delete==False:
            # Exit the behavior
            self.fm.exitBehavior(id)
          else:
            del self.aLoaded[name]
            try:
              self.fm.deleteBehavior(id)
            except Exception as ex:
              self.debug("%s could not delete behavior with id: %s, %s" % (name, id, ex))
        else:
          self.unlock()
      except Exception as ex:
        self.debug("stop: an error occured, %s" % ex)
        self.unlock()      