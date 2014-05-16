def isEnglish(letter):
    return u"A" <= letter <= u"Z"

def isRussian(letter):
    return letter == u"Ё" or u"А" <= letter <= u"Я"

def isVowel(letter):
    if letter in u"AEIOUY" or letter in u"АУОЫИЭЯЮЕЁ":
        return True
    else:
        return False

class DoubleMetaphon:
    '''
        @version: Version 1.1 from 10.04.2014
        @author: Alex Kuzmin
        @return: Double Metaphon transcription of the word
    '''

    def __init__(self):
        self.numbersOfTranscriptionSymbols = []
        self.amountsOfReplacedSymbols = []

    def getTranscription(self, word):
        self.numbersOfTranscriptionSymbols = []
        self.amountsOfReplacedSymbols = []
        self.indent = 4 #const
        self.length = len(word) + self.indent #about extra +'self.indent' see the first 'self.indent' symbols ('#' * 'self.indent') of the next line
        self.word = ""
        for idx in range(self.indent):
            self.word += '#'
        self.word = self.word + word.upper() + '########' #for safe indexing
        self.current = self.indent # Attention! (because of 'self.indent' safe index in the begin of self.word)
        self.transcription = "" #the first answer
        #self.extraTranscription = "" #the second answer

        while self.current < self.length:
            #English language
            if isEnglish(self.word[self.current]):

                #Case Vowel
                if isVowel(self.word[self.current]):
                    if self.current == self.indent:
                        self.__addLetter(u"A")   
                    self.current += 1
                    continue
                
                #Case u"B"
                elif self.word[self.current] == u"B":
                    if self.word[self.current - 1] == u"M" and self.current == self.length - 1:
                        if len(self.amountsOfReplacedSymbols) > 0:
                            self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1
                        self.current += 1
                        continue
                    self.__addLetter(u"P")
                    self.current += 1
                    while self.word[self.current] == u"B":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"C"
                elif self.word[self.current] == u"C":
                    if (not isVowel(self.word[self.current - 2]) and self.searchOfString(self.current - 1, 3, u"ACH") 
                            and self.word[self.current + 2] not in u"IE"
                            or self.searchOfString(self.current - 2, 6, u"BACHER", u"MACHER")):
                        self.__addLetter(u"K", 2)
                        self.current += 2
                        continue
                    elif self.word[self.current + 1] == u"H":
                        if self.searchOfString(self.current + 2, 2, u"IA"):
                            self.__addLetter(u"K")
                        elif self.current > self.indent and self.searchOfString(self.current + 2, 2, u"AE"):
                            self.__addLetter(u"K")
                            #self.extraAdd(u"X")
                        elif (self.searchOfString(self.indent, 4, 'VAN ', 'VON ') 
                            or self.word[self.current - 2] in u"TS" 
                            or (self.word[self.current - 1] in u"AOUE" or self.current == self.indent) 
                                and self.word[self.current + 2] in 'LRNMBHFVW '):
                              self.__addLetter(u"K")
                        elif self.searchOfString(self.indent, 3, u"SCH") or self.searchOfString(self.current - 2, 6, u"ORCHES", u"ARCHIT", u"ORCHID"):
                            self.__addLetter(u"K", 2)
                        elif (self.current == self.indent and 
                                (self.searchOfString(self.current + 2, 4, u"ARAC", u"ARIS") 
                                or self.searchOfString(self.current + 2, 4, u"OR", u"YM", u"IA", u"EM"))
                                    and not self.searchOfString(self.indent, 5, u"CHORE")):
                            self.__addLetter(u"K")
                        else:
                            if self.current > self.indent:
                                if self.searchOfString(self.indent, 2, u"MC"):
                                    self.__addLetter(u"K")
                                else:
                                    self.__addLetter(u"X")
                                    #self.extraAdd(u"K")
                            else:
                                self.__addLetter(u"X")
                        self.current += 2
                        continue
    
                    elif self.word[self.current + 1] == u"Z" and not self.searchOfString(self.current - 2, 4, u"WICZ"):
                        self.__addLetter(u"S")
                        #self.extraAdd(u"X")
                        self.current += 2
                        continue
    
                    elif self.searchOfString(self.current + 1, 2, u"IA"):
                        self.__addLetter(u"X")
                        self.current += 3
                        continue
    
                    elif self.word[self.current + 1] == u"C" and not (self.current == self.indent + 1 and self.word[self.indent] == u"M"):
                        if self.word[self.current + 2] in u"IEH" and not self.searchOfString(self.current + 2, 2, u"HU"):
                            if (self.current == self.indent + 1 and self.word[self.current - 1] == u"A" 
                                or self.searchOfString(self.current - 1, 5, u"UCCEE", u"UCCES")):
                                self.__addLetter(u"KS", 1, 1)
                            else:
                                self.__addLetter(u"X", 2)
                            self.current += 3
                            continue
                        else:
                            self.__addLetter(u"K", 2)
                            self.current += 2
                            continue
    
                    elif self.word[self.current + 1] in u"KGQ":
                        self.__addLetter(u"K")
                        self.current += 2
                        while self.word[self.current + 1] in u"KGQ":
                            self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1
                            self.current += 1
                        continue
    
                    elif self.word[self.current + 1] in u"IEY":
                        if self.searchOfString(self.current + 1, 2, u"IO", u"IE", u"IA"):
                            self.__addLetter(u"S")
                            #self.extraAdd(u"X")
                        else:
                            self.__addLetter(u"S")
                        self.current += 2
                        continue
    
                    elif self.current == self.indent and self.searchOfString(self.current + 1, 5, u"AESAR"):
                        self.__addLetter(u"S")
                        self.current += 2
                        continue
    
                    self.__addLetter(u"K")
                    self.current += 1
                    while self.word[self.current + 1] in u"CKQ":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
                
                #Case u"D"
                elif self.word[self.current] == u"D":
                    if self.word[self.current + 1] == u"G":
                        if self.word[self.current + 2] in u"IEY":
                            self.__addLetter(u"J", 2)
                            self.current += 3
                            continue
                        else:
                            self.__addLetter(u"TK", 1, 1)
                            self.current += 2
                    else:
                        self.__addLetter(u"T")
                        self.current += 1
                    while self.word[self.current] in u"DT":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"F"
                elif self.word[self.current] == u"F":
                    self.__addLetter(u"F")
                    self.current += 1
                    while self.word[self.current] == u"F":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
                
                #Case u"G"
                elif self.word[self.current] == u"G":
                    if self.word[self.current + 1] == u"H":
                        if self.current == self.indent:
                            if self.word[self.current + 2] == u"I":
                                self.__addLetter(u"J", 2)
                                self.current += 3
                            else:
                                self.__addLetter(u"K", 2)
                                self.current += 2
                            continue

                        elif not isVowel(self.word[self.current - 1]):
                            self.__addLetter(u"K", 2)
                            self.current += 2
                            continue

                        if self.searchOfString(self.current - 4, 7, u"DRAUGHT"):
                            self.__addLetter(u"F", 2)
                            self.current += 2
                            self.__addLetter(u"T")
                            self.current += 1
                            continue
                        elif self.word[self.current + 2] == u"T":
                            self.__addLetter(u"T", 3)
                            self.current += 3
                            continue
                        elif self.searchOfString(self.current - 2, 2, u"OU"):
                            if (self.word[self.current - 3] in u"CNT" or 
                                (self.current - 3 == self.indent and self.word[self.current - 3] == u"R" ) or
                                (self.word[self.current - 4] == u"S" and self.word[self.current - 3] == u"L")):
                                self.__addLetter(u"F", 2)
                                self.current += 2
                                continue
                            elif (self.word[self.current - 3] in u"BD" or self.searchOfString(self.current - 4, 2, u"TH") or
                                (self.current - 3 != self.indent and self.word[self.current - 3] == u"R")):
                                self.current += 2
                                continue
                            elif self.word[self.current - 3] == u"L":
                                self.__addLetter(u"K", 2)
                                self.current += 2
                                continue
                            else:
                                #when I don't know read u"ouGH" or don't
                                self.current += 2
                                continue
                        elif self.word[self.current - 1] == u"I":
                            if self.searchOfString(self.current + 2, 3, u"EAD", u"EAT", u"AND", u"OLE", u"OLD", u"ILL") or self.searchOfString(self.current + 2, 2, u"AI"):
                                self.__addLetter(u"GH", 1, 1)
                                self.current += 2
                                continue
                            else:
                                self.current += 2
                                continue
                        else:
                            if self.word[self.current - 1] == u"U" and self.word[self.current - 3] in u"CGLRT":
                                self.__addLetter(u"F", 2)
                            else:
                                if self.word[self.current - 1] != u"I":
                                    self.__addLetter(u"K", 2)
                            self.current += 2
                            continue

                    elif self.word[self.current + 1] == u"N":
                        if self.current == self.indent:
                            self.__addLetter(u"N", 2)
                        elif self.current == self.indent + 1 and isVowel(self.word[self.indent]) and not self.__slavoGermanic():
                            self.__addLetter(u"KN", 1, 1)
                            #self.extraAdd(u"N")
                        else:
                            if not self.searchOfString(self.current + 2, 2, u"EY") and not self.__slavoGermanic():
                                self.__addLetter(u"N", 2)
                                #self.extraAdd(u"KN")
                            else:
                                self.__addLetter(u"KN", 1, 1)
                        self.current += 2
                        continue
    
                    elif self.searchOfString(self.current + 1, 2, u"LI") and not self.__slavoGermanic():
                        self.__addLetter(u"KL", 1, 1)
                        #self.extraAdd(u"L")
                        self.current += 2
                        continue

                    elif ((self.current == self.indent and self.word[self.current + 1] == u"Y")
                          or self.searchOfString(self.current + 1, 2, u"ES", u"EP", u"EB", u"EL", u"EY", u"IB", u"IL", u"IN", u"IE", u"EI", u"ER")):
                        self.__addLetter(u"K")
                        #self.extraAdd(u"J")
                        self.current += 2
                        continue
    
                    elif (self.searchOfString(self.current + 1, 2, u"ER") or self.word[self.current + 1] == u"Y"
                        and not self.searchOfString(self.indent, 6, u"DANGER", u"RANGER", u"MANGER") and not self.word[self.current - 1] in u"EI"
                            and not self.searchOfString(self.current - 1, 3, u"RGY", u"OGY")):
                        self.__addLetter(u"K")
                        #self.extraAdd(u"J")
                        self.current += 2
                        continue
                    
                    elif (self.searchOfString(self.current + 1, 2, u"ER") or self.word[self.current + 1] == u"Y"
                          and not self.searchOfString(self.indent, 6, u"DANGER", u"RANGER", u"MANGER") and not self.word[self.current - 1] in u"EI"
                            and not self.searchOfString(self.current - 1, 3, u"RGY", u"OGY")):
                        self.__addLetter(u"K")
                        #self.extraAdd(u"J")
                        self.current += 2
                        continue
    
                    elif self.word[self.current + 1] in u"EIY" or self.searchOfString(self.current - 1, 4, u"AGGI", u"OGGI"):
                        if ((self.searchOfString(self.indent, 4, 'VAN ', 'VON ') or self.searchOfString(self.indent, 3, u"SCH"))
                            or self.searchOfString(self.current + 1, 2, u"ET")):
                            self.__addLetter(u"K")
                        else:
                            if self.searchOfString(self.current + 1, 4, u"IER"):
                                self.__addLetter(u"J")
                            else:
                                self.__addLetter(u"J")
                                #self.extraAdd(u"K")
                        self.current += 2
                        continue
                    
                    else:
                        self.__addLetter(u"K")
                        self.current += 1
                        while self.word[self.current] in u"GK":
                            self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                            self.current += 1
                    continue
                
                #Case u"H"
                elif self.word[self.current] == u"H":
                    if self.current == self.indent or isVowel(self.word[self.current - 1]):
                        tmp = 1
                        while self.word[self.current + tmp] == u"H":
                            tmp += 1
                        if isVowel(self.word[self.current + tmp]):
                            self.__addLetter(u"H", tmp)
                            self.current += tmp + 1
                        else:
                            self.current += tmp
                    else:
                        while self.word[self.current] == u"H":
                            self.current += 1
                    continue
    
                #Case u"J"
                elif self.word[self.current] == u"J":
                    if self.searchOfString(self.current, 4, u"JOSE") or self.searchOfString(self.indent, 4, 'SAN '):
                        if (self.current == self.indent and self.word[self.current + 4] == ' ') or self.searchOfString(self.indent, 4, 'SAN '):
                            self.__addLetter(u"H")
                        else:
                            self.__addLetter(u"J")
                            #self.extraAdd(u"H")
                        self.current += 1
                        continue
    
                    elif self.current == self.indent and not self.searchOfString(self.current, 4, u"JOSE"):
                        self.__addLetter(u"J")
                        #self.extraAdd(u"A")
                    elif (isVowel(self.word[self.current - 1]) and not self.__slavoGermanic() and
                          (self.word[self.current + 1] == u"A" or self.word[self.current + 1] == u"O")):
                        self.__addLetter(u"J")
                        #self.extraAdd(u"H")
                    elif self.current == self.length - 1:
                        self.__addLetter(u"J")
                        #self.extraAdd(' ')
                    elif (not self.word[self.current + 1] in u"LTKSNMBZ" and not self.word[self.current - 1] in u"SKL"):
                        self.__addLetter(u"J")
                    else:
                        while self.word[self.current] == u"J":
                            self.current += 1
                        continue
                    self.current += 1
                    while self.word[self.current] == u"J":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                        continue
    
                #Case u"K"
                elif self.word[self.current] == u"K":
                    if self.word[self.current + 1] == u"N" and self.current == self.indent:
                        self.__addLetter(u"N", 2)
                        self.current += 2
                        continue
                    self.__addLetter(u"K")
                    self.current += 1
                    while self.word[self.current] == u"K":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"L"
                elif self.word[self.current] == u"L":
                    if self.word[self.current + 1] == u"L":
                        if ((self.current == self.length - 3 and self.searchOfString(self.current - 1, 4, u"ILLO", u"ILLA", u"ALLE"))
                            or ((self.searchOfString(self.length - 2, 2, u"AS", u"OS") or self.word[self.length - 1] in u"AO") 
                                and self.searchOfString(self.current - 1, 4, u"ALLE"))):
                            self.__addLetter(u"L", 2)
                            #self.extraAdd(' ')
                            self.current += 2
                            continue

                    self.__addLetter(u"L")
                    self.current += 1
                    while self.word[self.current] == u"L":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"M"
                elif self.word[self.current] == u"M":
                    self.__addLetter(u"M")
                    self.current += 1
                    while self.word[self.current] == u"M":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    if (self.searchOfString(self.current - 2, 3, u"UMB") and ((self.current == self.length - 1) 
                        or self.searchOfString(self.current + 1, 2, u"ER"))):
                        self.current += 1
                    continue
    
                #Case u"N"
                elif self.word[self.current] == u"N":
                    if self.word[self.current - 1] == u"M" and self.current == self.length - 1:
                        if len(self.amountsOfReplacedSymbols) > 0:
                            self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1
                        self.current += 1
                        continue
                    self.__addLetter(u"N")
                    self.current += 1
                    while self.word[self.current] == u"N":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"P"
                elif self.word[self.current] == u"P":
                    if self.current == self.indent:
                        if self.word[self.current + 1] == u"N":
                            self.__addLetter(u"N")
                            self.current += 2
                            continue
                        elif self.word[self.current + 1] == u"S":
                            self.__addLetter(u"S")
                            self.current += 2
                            continue
                    if self.word[self.current + 1] == u"H":
                        tmp = 1
                        while self.word[self.current + tmp] == u"H":
                            tmp += 1
                        self.__addLetter(u"F", tmp)
                        self.current += tmp
                        continue
                    self.__addLetter(u"P")
                    self.current += 1
                    while self.word[self.current] in u"PB":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"Q"
                elif self.word[self.current] == u"Q":
                    self.__addLetter(u"K")
                    self.current += 1
                    while self.word[self.current] == u"Q":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"R"
                elif self.word[self.current] == u"R":
                    if (self.current == self.length - 1 and not self.__slavoGermanic()
                        and self.searchOfString(self.current - 2, 2, u"IE") and not self.searchOfString(self.current - 4, 2, u"ME", u"MA")):
                        #self.__addLetter('')
                        #self.extraAdd(u"R")
                        None
                    elif (self.current == self.length - 1 and self.word[self.current - 1] == u"E"):
                        #self.extraAdd(u"R")
                        #self.__addLetter('')
                        None
                    else:
                        self.__addLetter(u"R")
                    self.current += 1
                    while self.word[self.current] == u"R":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"S"
                elif self.word[self.current] == u"S":
                    if self.searchOfString(self.current + 1, 3, u"ISL", u"YSL"):
                        self.current += 1
                        continue
    
                    elif self.current == self.indent and self.searchOfString(self.current, 5, u"SUGAR"):
                        self.__addLetter(u"X")
                        #self.extraAdd(u"S")
                        self.current += 1
                        continue
        
                    elif self.word[self.current + 1] == u"H":
                        if self.searchOfString(self.current + 1, 4, u"HEIM", u"HOEK", u"HOLM", u"HOLZ"):
                            self.__addLetter(u"S", 2)
                        else:
                            self.__addLetter(u"X", 2)
                        self.current += 2
                        continue
    
                    elif (self.searchOfString(self.current + 1, 2, u"IO", u"IA") 
                          or self.searchOfString(self.current + 1, 3, u"IAN")):
                        if not self.__slavoGermanic():
                            self.__addLetter(u"S")
                            #self.extraAdd(u"X")
                        else:
                            self.__addLetter(u"S")
                        self.current += 3
                        continue
    
                    elif ((self.current == self.indent and self.word[self.current + 1] in u"MNLW")
                          or self.word[self.current + 1] == u"Z"):
                        tmp = 1
                        while self.word[self.current + tmp] in u"SZ":
                            self.current += 1
                        self.__addLetter(u"S", tmp)
                        #self.extraAdd(u"X")
                        self.current += tmp
                        continue

                    elif self.word[self.current + 1] == u"C":
                        if self.word[self.current + 2] == u"H":
                            if self.searchOfString(self.current + 3, 2, u"OO", u"ER", u"EN", u"UY", u"ED", u"EM"):
                                if self.searchOfString(self.current + 3, 2, u"ER", u"EN"):
                                    self.__addLetter(u"X", 3)
                                    #self.extraAdd(u"SK")
                                else:
                                    self.__addLetter(u"SK", 1, 2)
                                self.current += 3
                                continue
                            else:
                                if (self.current == self.indent and not isVowel(self.word[self.indent + 3]) and self.word[self.indent + 3] != u"W"):
                                    self.__addLetter(u"X", 3)
                                    #self.extraAdd(u"S")
                                else:
                                    self.__addLetter(u"X", 3)
                                self.current += 3
                                continue
                        elif self.word[self.current + 2] in u"IEY":
                            self.__addLetter(u"S", 2)
                            self.current += 3
                            continue
                        self.__addLetter(u"SK", 1, 1)
                        self.current += 2
                        continue
        
                    elif (self.current == self.length - 1 and self.searchOfString(self.current - 2, 2, u"AI", u"OI")):
                        #self.__addLetter('')
                        #self.extraAdd(u"S")
                        None
                    else:
                        self.__addLetter(u"S")
                        self.current += 1
        
                    while self.word[self.current] in u"SZ":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"T"
                elif self.word[self.current] == u"T":
                    if self.searchOfString(self.current + 1, 3, u"ION"):
                        self.__addLetter(u"X", 3)
                        self.current += 3
                        continue
        
                    elif self.searchOfString(self.current + 1, 2, u"IA"):
                        self.__addLetter(u"X")
                        self.current += 3
                        continue
                    elif self.searchOfString(self.current + 1, 2, u"CH"):
                        self.__addLetter(u"X", 3)
                        self.current += 3
                        continue
                    elif self.word[self.current + 1] == u"H" or self.searchOfString(self.current + 1, 2, u"TH"):
                        if (self.searchOfString(self.current + 2, 2, u"OM", u"AM") 
                            or self.searchOfString(self.indent, 4, 'VAN ', 'VON ') or self.searchOfString(self.indent, 3, u"SCH")):
                            if self.word[self.current + 1] == u"H":
                                self.__addLetter(u"T", 2)
                            else:
                                self.__addLetter(u"T", 3)
                        else:
                            if self.word[self.current + 1] == u"H":
                                self.__addLetter(u"S", 2)
                                #self.extraAdd(u"T")
                            else:
                                self.__addLetter(u"S", 3)
                                #self.extraAdd(u"T")
                        self.current += 2
                        continue
                    self.__addLetter(u"T")
                    self.current += 1
                    while self.word[self.current] in u"TD":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"V"
                elif self.word[self.current] == u"V":
                    self.__addLetter(u"F")
                    self.current += 1
                    while self.word[self.current] == u"V":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"W"
                elif self.word[self.current] == u"W":
                    if self.word[self.current + 1]  == u"R":
                        self.__addLetter(u"R", 2)
                        self.current += 2
                        continue

                    elif self.current == self.indent:
                        if isVowel(self.word[self.current + 1]):
                            self.__addLetter(u"F")
                            #self.extraAdd(u"A")
                            self.current += 2
                            continue
                        elif self.word[self.current + 1]  == u"H" and isVowel(self.word[self.current + 2]):
                            self.__addLetter(u"F", 2)
                            self.current += 3
                            continue

                    elif isVowel(self.word[self.current + 1]) and isVowel(self.word[self.current - 1]):
                        self.__addLetter(u"F")
                        self.current += 1
                        continue

                    elif ((self.current == self.length - 1 and isVowel(self.word[self.current - 1])) 
                          or self.searchOfString(self.current - 1, 5, u"EWSKI", u"EWSKY", u"OWSKI", u"OWSKY")):
                        #self.__addLetter('')
                        #self.extraAdd(u"F")
                        self.current += 1
                        continue

                    elif self.searchOfString(self.current, 4, u"WICZ", u"WITZ"):
                        self.__addLetter(u"TS", 4)
                        #self.extraAdd(u"FX")
                        self.current += 4
                        continue
        
                    while self.word[self.current] == u"W":
                        self.current += 1
                    continue

                #Case u"X"
                elif self.word[self.current] == u"X":
                    if self.current == self.indent:
                        self.__addLetter(u"S")
                        self.current += 1
                    elif (not (self.current == self.length - 1 and
                              self.searchOfString(self.current - 2, 2, u"AU", u"OU"))):
                        self.__addLetter(u"KS", 1, 0)
                        self.current += 1
                        while self.word[self.current] in u"CX":
                            self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 2] += 1 
                            self.current += 1
                        continue
                    while self.word[self.current] in u"CX":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue
    
                #Case u"Z"
                elif self.word[self.current] == u"Z":
                    if self.word[self.current + 1] == u"H":
                        self.__addLetter(u"J", 2)
                        self.current += 2
                        continue
                    elif (self.searchOfString(self.current + 1, 2, u"ZO", u"ZI", u"ZA") or (self.__slavoGermanic() 
                            and (self.current > self.indent and self.word[self.current - 1] != u"T"))):
                        self.__addLetter(u"S")
                        #self.extraAdd(u"TS")
                        self.current += 1
                    else:
                        self.__addLetter(u"S")
                        self.current += 1

                    while self.word[self.current] == u"Z":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case the other letters
                else:
                    self.current += 1

            #Russian language
            elif isRussian(self.word[self.current]):
                
                #Case Vowel
                if isVowel(self.word[self.current]):
                    if self.current == self.indent:
                        self.__addLetter(u"A")
                    self.current += 1
                    continue

                #Case u"Б"
                elif self.word[self.current] == u"Б":
                    self.__addLetter(u"P")
                    self.current += 1

                    while self.word[self.current] == u"БП":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"В"
                elif self.word[self.current] == u"В":
                    self.__addLetter(u"F")
                    self.current += 1

                    while self.word[self.current] == u"ВФ":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Г"
                elif self.word[self.current] == u"Г":
                    self.__addLetter(u"K")
                    self.current += 1

                    while self.word[self.current] == u"Г" or self.word[self.current] == u"К":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Д"
                elif self.word[self.current] == u"Д":
                    if self.word[self.current + 1] == u"С":
                        self.__addLetter(u"TS", 1, 0)
                        #self.extraAdd(u"X", 2)
                        self.current += 2
                        continue
                    else:
                        self.__addLetter(u"T")
                        self.current += 1

                    while self.word[self.current] in u"ДT":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Ж"
                elif self.word[self.current] == u"Ж":
                    self.__addLetter(u"J")
                    self.current += 1

                    while self.word[self.current] in u"ЖШ":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"З"
                elif self.word[self.current] == u"З":
                    self.__addLetter(u"S")
                    self.current += 1

                    while self.word[self.current] in u"ЗС":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"К"
                elif self.word[self.current] == u"К":
                    self.__addLetter(u"K")
                    self.current += 1

                    while self.word[self.current] in u"КГ":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Л"
                elif self.word[self.current] == u"Л":
                    self.__addLetter(u"L")
                    self.current += 1

                    while self.word[self.current] == u"Л":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"М"
                elif self.word[self.current] == u"М":
                    self.__addLetter(u"M")
                    self.current += 1

                    while self.word[self.current] == u"М":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Н"
                elif self.word[self.current] == u"Н":
                    self.__addLetter(u"N")
                    self.current += 1

                    while self.word[self.current] == u"Н":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"П"
                elif self.word[self.current] == u"П":
                    self.__addLetter(u"P")
                    self.current += 1

                    while self.word[self.current] in u"БП":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Р"
                elif self.word[self.current] == u"Р":
                    self.__addLetter(u"R")
                    self.current += 1

                    while self.word[self.current] == u"Р":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"С"
                elif self.word[self.current] == u"С":
                    self.__addLetter(u"S")
                    self.current += 1

                    while self.word[self.current] in u"СЗ":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Т"
                elif self.word[self.current] == u"Т":
                    self.__addLetter(u"T")
                    self.current += 1

                    while self.word[self.current] in u"ТД":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Ф"
                elif self.word[self.current] == u"Ф":
                    self.__addLetter(u"F")
                    self.current += 1

                    while self.word[self.current] in u"ФВ":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Х"
                elif self.word[self.current] == u"Х":
                    self.__addLetter(u"H")
                    self.current += 1

                    while self.word[self.current] == u"Х":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Ц"
                elif self.word[self.current] == u"Ц":
                    self.__addLetter(u"TS", 1, 0)
                    self.current += 1

                    while self.word[self.current] == u"Ц":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 2] += 1 
                        self.current += 1
                    continue

                #Case u"Ч"
                elif self.word[self.current] == u"Ч":
                    if self.word[self.current + 1] in u"ТН":
                        self.__addLetter(u"X", 2)
                        self.current += 2
                        continue

                    self.__addLetter(u"X")
                    self.current += 1
                    while self.word[self.current] == u"Ч":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case u"Ш" or u"Щ"
                elif self.word[self.current] in u"ШЩ":
                    self.__addLetter(u"X")
                    self.current += 1
                    
                    while self.word[self.current] in u"ШЩ":
                        self.amountsOfReplacedSymbols[len(self.amountsOfReplacedSymbols) - 1] += 1 
                        self.current += 1
                    continue

                #Case the other letters
                else:
                    self.current += 1

            #Case other symbols            
            else:
                self.current += 1

        return self.transcription


    def searchOfString(self, start, length, *strings):
        if self.word[start : start + length] in strings:
            return True
        else:
            return False
    
    def __addLetter(self, string, *numbersOfReplacedCharacters):
        if len(numbersOfReplacedCharacters) == 0:
            self.amountsOfReplacedSymbols.append(1)
            self.numbersOfTranscriptionSymbols.append(self.current - self.indent)
        else:
            currentDelta = 0
            for num in numbersOfReplacedCharacters:
                self.amountsOfReplacedSymbols.append(num)
                self.numbersOfTranscriptionSymbols.append(self.current - self.indent + currentDelta)
                currentDelta += num
        self.transcription += string

    #TODO?
    #def extraAdd(self, string):
    #   None

    def __slavoGermanic(self):
        if u"W" in self.word or u"K" in self.word or u"CZ" in self.word or u"WITZ" in self.word:
            return True
        else:
            return False

    '''def __str__(self):
        
        #answer = self.transcription[0]
        #if len(self.transcription) > 0:
        #    for i in range(1, len(self.transcription)):
        #        if self.transcription[i - 1] != self.transcription[i]:
        #            answer += self.transcription[i]
        #return answer
        return self.transcription'''

    def getNumbersOfSymbols(self):
        ''' 
            @attention: before this you should run self.getTranscription() with argument
            @return: list, the numbers of the first letters in the word that relate to each of the symbols of the transcription
        '''

        if self.numbersOfTranscriptionSymbols == []:
            return -1
        else:
            return self.numbersOfTranscriptionSymbols

    def getAmountsOfReplacedSymbols(self):
        ''' 
            @attention: before this you should run self.getTranscription() with argument
            @return: list, the amounts of the letters in the word that relate to each of the symbols of the transcription
        '''

        if self.amountsOfReplacedSymbols == []:
            return - 1
        else:
            return self.amountsOfReplacedSymbols



if __name__ == u"__main__":
    DM = DoubleMetaphon()
    print( DM.getTranscription(u"column") )
    print( DM.getNumbersOfSymbols(), DM.getAmountsOfReplacedSymbols())