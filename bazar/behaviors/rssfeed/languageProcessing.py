import os, re, pickle

class LanguageProcessing:
  "This class provides methods to process language (eg: detect lang)."
  def __init__(self, sDictionaryPath = "/opt/appu/data/pkl"):
    "The path where the data are stored/to be stored."
    self.sDictionaryPath = sDictionaryPath # TODO : throw an exception if it's not a real path

  def setDictionaryPath(self, sNewDictionaryPath):
    "If the data path has to be changed."
    self.sDictionaryPath = sNewDictionaryPath # TODO : throw an exception and keep the old value
    if not os.path.isdir(sNewDictionaryPath):
      print(sNewDictionaryPath+" is not a repository")

  def getDictionaryPath(self):
    "Returns the data path."
    return self.sDictionaryPath

  def __sortValues(self, eElem1, eElem2):
    "This private method is a tool for some language processing functions."
    return -cmp(eElem1[1],eElem2[1])

  def createDictionary(self, sStringToProcess):
    "This function creates the trigram dictionary from the input string."
    # Remove uppercase letters and punctuation. Each punctuation character is replaced by a \n.
    sOldCleanString = sStringToProcess.lower()
    sCleanString = re.sub('[ \t\v\f\r]|\d|[!-/:-@[-`{-~]','\n',sOldCleanString)
    #Get all the words
    aString = sCleanString.split('\n')
    dTrigrams = {}
    for sWord in aString:
      if len(sWord) < 4:
        if len(sWord) > 0:
          # The word is a trigram (<= 3 char). Its frequency in the trigram dict is increased.
          try:
            nFreq = dTrigrams[sWord]
          except KeyError:
            dTrigrams[sWord] = 1
          else:
            dTrigrams[sWord] = nFreq + 1
      else:
        # The word contains many trigrams
        nLength = len(sWord)
        nCnt = 0
        while nCnt < nLength - 2:
          sNewTrig = sWord[nCnt:nCnt+3]
          # The frequency of the trigram is increased.
          try:
            nFreq = dTrigrams[sNewTrig]
          except KeyError:
            dTrigrams[sNewTrig] = 1
          else:
            dTrigrams[sNewTrig] = nFreq + 1
          nCnt += 1
    # precomputes the total weight
    rNbrTrigramsCorpus = 0.0
    for nValue in dTrigrams.itervalues():
      rNbrTrigramsCorpus += float(nValue)
    # Store this weight in the trigram dictionary
    dTrigrams["TOTAL_WEIGHT"] = rNbrTrigramsCorpus
    # Returns the trigram dictionary.
    return dTrigrams

  def computeLanguageProbabilities(self, sStringToProcess):
    "Computes the language probabilities for the input string."
    # TODO : optimize the dictionary opening/access

    # Creates the trigram dictionary from the input string.
    dDictionary = self.createDictionary(sStringToProcess)
    if not os.path.isdir(self.sDictionaryPath):
      print(self.sDictionaryPath+" is not a repository!") # TODO : throw error ?
      return
    aDir = os.listdir(self.sDictionaryPath)
    dProb = {}
    # compute the frequency sum of the input trigrams (to normalize)
    rNbrTrigramsInput = dDictionary["TOTAL_WEIGHT"]
    # traversal of the dictionaries
    for sElem in aDir:
      rProba = 0.0
      sFullPath = os.path.join(self.sDictionaryPath, sElem)
      if os.path.isfile(sFullPath):
        fPklFile = open(sFullPath, 'rb')
        try:
          dTrigramCorpus = pickle.load(fPklFile)
        except:
          pass
        else:
          # computes the frequency sum of the learnt trigram dictionary (to normalize)
          rNbrTrigramsCorpus = dTrigramCorpus["TOTAL_WEIGHT"]
          fPklFile.close()
          # computes the probability of the current language
          for k, v in dDictionary.iteritems():
            try:
              rCorpusFreq = float(dTrigramCorpus[k])
            except KeyError:
              rCorpusFreq = 0.0
            rProba = rProba + ((rCorpusFreq/rNbrTrigramsCorpus) * (v/ rNbrTrigramsInput))
        dProb[sElem[:len(sElem)-4]]=rProba
    iDic = dProb.items()
    return(iDic)

  def findLanguage(self, sStringToProcess):
    "Returns the name of the most probable language."
    iDic = self.computeLanguageProbabilities(sStringToProcess)
    iDic.sort(self.__sortValues)
    return iDic[0]

  def findEnglishOrFrench(self, sStringToProcess):
    "Returns the name of the most probable language, between English and French."
    # TODO : use only English and French dictionaries.
    iDic = self.computeLanguageProbabilities(sStringToProcess)
    iDic.sort(self.__sortValues)
    for aElem in iDic:
      if aElem[0] == "french" or aElem[0] == "english":
        return(aElem[0][0].upper() +aElem[0][1:] )
