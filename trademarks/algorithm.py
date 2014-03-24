# coding: utf-8

class DoubleMetaphon:
    '''
        @version: Version 1.1 from 18.03.2014
        @author: Alex Kuzmin
        @return: Double Metaphon transcription of the word
    '''

    def __init__(self, word):
        self.length = len(word) + 4 #about extra '+4' see the first 4 symbols ('####') of the next line
        print (word)
        self.word = '####' + word.decode('utf-8').upper() + '########' #for safe indexing
        print (self.word)
        self.current = 4 # Attention! (because of 4 safe index in the begin of self.word)
        self.transcription = "" #the first answer
        self.extraTranscription = "" #the second answer

        if self.searchOfString(4, 2, 'GN', 'KN', 'PN', 'WR', 'PS'):
            self.current += 1

        if self.word[4] == 'X':
          self.addLetter('S');
          self.current += 1

        while self.current < self.length:
            
            #English language
            if 'A' <= self.word[self.current] <= 'Z':

                #Case Vowel
                if self.isVowel(self.word[self.current]):
                    if self.current == 4:
                        self.addLetter('A')   
                    self.current += 1
                    continue
                
                #Case 'B'
                elif self.word[self.current] == 'B':
                    self.addLetter('P')
                    while self.word[self.current] == 'B':
                        self.current += 1
                    continue
    
                #Case 'C'
                elif self.word[self.current] == 'C':
                    if (not self.isVowel(self.word[self.current - 2]) and self.searchOfString(self.current - 1, 3, 'ACH') 
                            and self.word[self.current + 2] not in 'IE'
                                or self.searchOfString(self.current - 2, 6, 'BACHER', 'MACHER')):
                        self.addLetter('K')
                        self.current += 2
                        continue
    
                    elif self.word[self.current + 1] == 'H':
                        if self.searchOfString(self.current + 2, 2, 'IA'):
                            self.addLetter('K')
                        elif self.current > 4 and self.searchOfString(self.current + 2, 2, 'AE'):
                            self.addLetter('K')
                            #self.extraAdd('X')
                        elif ((self.searchOfString(0, 4, 'VAN ', 'VON ') or self.searchOfString(0, 3, 'SCH'))
                            or self.searchOfString(self.current - 2, 6, 'ORCHES', 'ARCHIT', 'ORCHID')
                            or self.word[self.current - 2] in 'TS'
                            or (self.word[self.current - 1] in 'AOUE' or self.current == 4) 
                                and self.word[self.current + 2] in 'LRNMBHFVW '):
                            self.addLetter('K')
                        elif (self.current == 4 and 
                                (self.searchOfString(self.current + 2, 4, 'ARAC', 'ARIS') 
                                or self.searchOfString(self.current + 2, 4, 'OR', 'YM', 'IA', 'EM'))
                                    and not self.searchOfString(0, 5, 'CHORE')):
                            self.addLetter('K')
                        else:
                            if self.current > 4:
                                if self.searchOfString(0, 2, 'MC'):
                                    self.addLetter('K')
                                else:
                                    self.addLetter('X')
                                    #self.extraAdd('K')
                            else:
                                self.addLetter('X')
                        self.current += 2
                        continue
    
                    elif self.word[self.current + 1] == 'Z' and not self.searchOfString(self.current - 2, 4, 'WICZ'):
                        self.addLetter('S')
                        #self.extraAdd('X')
                        self.current += 2
                        continue
    
                    elif self.searchOfString(self.current + 1, 3, 'CIA'):
                        self.addLetter('X')
                        self.current += 3
                        continue
    
                    elif self.word[self.current + 1] == 'C' and not (self.current == 5 and self.word[4] == 'M'):
                        if self.word[self.current + 2] in 'IEH' and not self.searchOfString(self.current + 2, 2, 'HU'):
                            if (self.current == 5 and self.word[self.current - 1] == 'A' 
                                or self.searchOfString(self.current - 1, 5, 'UCCEE', 'UCCES')):
                                self.addLetter('KS')
                            else:
                                self.addLetter('X')
                            self.current += 3
                            continue
                        else:
                            self.addLetter('K')
                            self.current += 2
                            continue
    
                    elif self.word[self.current + 1] in 'KGQ':
                        self.addLetter('K')
                        self.current += 2
                        continue
    
                    elif self.word[self.current + 1] in 'IEY':
                        if self.searchOfString(self.current + 1, 2, 'IO', 'IE', 'IA'):
                            self.addLetter('S')
                            #self.extraAdd('X')
                        else:
                            self.addLetter('S')
                        self.current += 2
                        continue
    
                    elif self.current == 4 and self.searchOfString(self.current + 1, 5, 'AESAR'):
                        self.addLetter('S')
                        self.current += 2
                        continue
    
                    self.addLetter('K')
                    while self.word[self.current + 1] in 'CKQ':
                        self.current += 1
                    if not self.word[self.current] in 'EI':
                        self.current += 1
                    continue
                
                #Case 'D'
                elif self.word[self.current] == 'D':
                    if self.word[self.current + 1] == 'G':
                        if self.word[self.current + 2] in 'IEY':
                            self.addLetter('J')
                            self.current += 3
                            continue
                        else:
                            self.addLetter('TK')
                            self.current += 2
                    else:
                        self.addLetter('T')
                    while self.word[self.current] in 'DT':
                        self.current += 1
                    continue
    
                #Case 'F'
                elif self.word[self.current] == 'F':
                    self.addLetter('F')
                    while self.word[self.current] == 'F':
                        self.current += 1
                    continue
                
                #Case 'G'
                elif self.word[self.current] == 'G':
                    if self.word[self.current + 1] == 'H':
                        if not self.isVowel(self.word[self.current - 1]):
                            self.addLetter('K')
                            self.current += 2
                            continue
        
                        elif self.current == 4:
                            if self.word[self.current + 2] == 'I':
                                self.addLetter('J')
                                self.current += 3
                            else:
                                self.addLetter('K')
                                self.current += 2
                            continue

                        if (self.word[self.current - 2] in 'BHD' or self.word[self.current - 3] in 'BHD' 
                            or self.word[self.current - 4] in 'BHD'):
                            self.current += 2
                            continue
                        else:
                            if self.word[self.current - 1] == 'U' and self.word[self.current - 3] in 'CGLRT':
                                self.addLetter('F')
                            else:
                                if self.word[self.current - 1] != 'I':
                                    self.addLetter('K')
                            self.current += 2
                            continue

                    elif self.word[self.current + 1] == 'N':
                        if self.current == 5 and self.isVowel(self.word[4]) and not self.slavoGermanic():
                            self.addLetter('KN')
                            #self.extraAdd('N')
                        else:
                            if not self.searchOfString(self.current + 2, 2, 'EY') and not self.slavoGermanic():
                                self.addLetter('N')
                                #self.extraAdd('KN')
                            else:
                                self.addLetter('KN')
                        self.current += 2
                        continue
    
                    elif self.searchOfString(self.current + 1, 2, 'LI') and not self.slavoGermanic():
                        self.addLetter('KL')
                        #self.extraAdd('L')
                        self.current += 2
                        continue
    
                    elif ((self.current == 4 and self.word[self.current + 1] == 'Y')
                          or self.searchOfString(self.current + 1, 2, 'ES', 'EP', 'EB', 'EL', 'EY', 'IB', 'IL', 'IN', 'IE', 'EI', 'ER')):
                        self.addLetter('K')
                        #self.extraAdd('J')
                        self.current += 2
                        continue
    
                    elif (self.searchOfString(self.current + 1, 2, 'ER') or self.word[self.current + 1] == 'Y'
                        and not self.searchOfString(0, 6, 'DANGER', 'RANGER', 'MANGER') and not self.word[self.current - 1] in 'EI'
                            and not self.searchOfString(self.current - 1, 3, 'RGY', 'OGY')):
                        self.addLetter('K')
                        #self.extraAdd('J')
                        self.current += 2
                        continue
                    
                    elif (self.searchOfString(self.current + 1, 2, 'ER') or self.word[self.current + 1] == 'Y'
                          and not self.searchOfString(0, 6, 'DANGER', 'RANGER', 'MANGER') and not self.word[self.current - 1] in 'EI'
                            and not self.searchOfString(self.current - 1, 3, 'RGY', 'OGY')):
                        self.addLetter('K')
                        #self.extraAdd('J')
                        self.current += 2
                        continue
    
                    elif self.word[self.current + 1] in 'EIY' or self.searchOfString(self.current - 1, 4, 'AGGI', 'OGGI'):
                        if ((self.searchOfString(0, 4, 'VAN ', 'VON ') or self.searchOfString(0, 3, 'SCH'))
                            or self.searchOfString(self.current + 1, 2, 'ET')):
                            self.addLetter('K')
                        else:
                            if self.searchOfString(self.current + 1, 4, 'IER'):
                                self.addLetter('J')
                            else:
                                self.addLetter('J')
                                #self.extraAdd('K')
                        self.current += 2
                        continue
                    
                    else:
                        while self.word[self.current] in 'GK':
                            self.current += 1
                    self.addLetter('K')
                    continue
                
                #Case 'H'
                elif self.word[self.current] == 'H':
                    if self.current == 4 or self.isVowel(self.word[self.current - 1]):
                        while self.word[self.current] == 'H':
                            self.current += 1
                        if self.isVowel(self.word[self.current]):
                            self.addLetter('H')
                            self.current += 1
                    else:
                        while self.word[self.current] == 'H':
                            self.current += 1
                    continue
    
                #Case 'J'
                elif self.word[self.current] == 'J':
                    if self.searchOfString(self.current, 4, 'JOSE') or self.searchOfString(0, 4, 'SAN '):
                        if (self.current == 4 and self.word[self.current + 4] == ' ') or self.searchOfString(0, 4, 'SAN '):
                            self.addLetter('H')
                        else:
                            self.addLetter('J')
                            #self.extraAdd('H')
                        self.current += 1
                        continue
    
                    elif self.current == 4 and not self.searchOfString(self.current, 4, 'JOSE'):
                        self.addLetter('J')
                        #self.extraAdd('A')
                    elif (self.isVowel(self.word[self.current - 1]) and not self.slavoGermanic() and
                          (self.word[self.current + 1] == 'A' or self.word[self.current + 1] == 'O')):
                        self.addLetter('J')
                        #self.extraAdd('H')
                    elif self.current == self.length - 1:
                        self.addLetter('J')
                        #self.extraAdd(' ')
                    elif (not self.word[self.current + 1] in 'LTKSNMBZ' and not self.word[self.current - 1] in 'SKL'):
                        self.addLetter('J')
    
                    while self.word[self.current] == 'J':
                        self.current += 1
                    continue
    
                #Case 'K'
                elif self.word[self.current] == 'K':
                    self.addLetter('K')
                    while self.word[self.current] == 'K':
                        self.current += 1
                    continue

                #Case 'L'
                elif self.word[self.current] == 'L':
                    if self.word[self.current + 1] == 'L':
                        if ((self.current == self.length - 3 and self.searchOfString(self.current - 1, 4, 'ILLO', 'ILLA', 'ALLE'))
                            or ((self.searchOfString(self.length - 2, 2, 'AS', 'OS') or self.word[self.length - 1] in 'AO') 
                                and self.searchOfString(self.current - 1, 4, 'ALLE'))):
                            self.addLetter('L')
                            #self.extraAdd(' ')
                            self.current += 2
                            continue
                        while self.word[self.current] == 'L':
                            self.current += 1
                    else:
                        self.current += 1
                    self.addLetter('L')
                    continue
    
                #Case 'M'
                elif self.word[self.current] == 'M':
                    while self.word[self.current] == 'M':
                        self.current += 1
                    if (self.searchOfString(self.current - 2, 3, 'UMB') and ((self.current == self.length - 1) 
                        or self.searchOfString(self.current + 1, 2, 'ER'))):
                        self.current += 1
                    self.addLetter('M')
                    continue
    
                #Case 'N'
                elif self.word[self.current] == 'N':
                    while self.word[self.current] == 'N':
                        self.current += 1
                    self.addLetter('N')
                    continue
    
                #Case 'P'
                elif self.word[self.current] == 'P':
                    if self.word[self.current + 1] == 'H':
                        while self.word[self.current + 1] == 'H':
                            self.current += 1
                        self.addLetter('F')
                        self.current += 1
                        continue
                    while self.word[self.current] in 'PB':
                        self.current += 1
                    self.addLetter('P')
                    continue
    
                #Case 'Q'
                elif self.word[self.current] == 'Q':
                    while self.word[self.current] == 'Q':
                        self.current += 1
                    self.addLetter('K')
                    continue
    
                #Case 'R'
                elif self.word[self.current] == 'R':
                    if (self.current == self.length - 1 and not self.slavoGermanic()
                        and self.searchOfString(self.current - 2, 2, 'IE') and not self.searchOfString(self.current - 4, 2, 'ME', 'MA')):
                        self.addLetter('')
                        #self.extraAdd('R')
                    else:
                        self.addLetter('R')
                    while self.word[self.current] == 'R':
                        self.current += 1
                    continue
    
                #Case 'S'
                elif self.word[self.current] == 'S':
                    if self.searchOfString(self.current + 1, 3, 'ISL', 'YSL'):
                        self.current += 1
                        continue
    
                    elif self.current == 4 and self.searchOfString(self.current, 5, 'SUGAR'):
                        self.addLetter('X')
                        #self.extraAdd('S')
                        self.current += 1
                        continue
        
                    elif self.searchOfString(self.current, 2, 'SH'):
                        if self.searchOfString(self.current + 1, 4, 'HEIM', 'HOEK', 'HOLM', 'HOLZ'):
                            self.addLetter('S')
                        else:
                            self.addLetter('X')
                        self.current += 2
                        continue
    
                    elif (self.searchOfString(self.current, 3, 'SIO', 'SIA') 
                          or self.searchOfString(self.current, 4, 'SIAN')):
                        if not self.slavoGermanic():
                            self.addLetter('S')
                            #self.extraAdd('X')
                        else:
                            self.addLetter('S')
                        self.current += 3
                        continue
    
                    elif ((self.current == 4 and self.word[self.current + 1] in 'MNLW')
                          or self.word[self.current + 1] == 'Z'):
                        self.addLetter('S')
                        #self.extraAdd('X')
                        while self.word[self.current + 1] == 'Z':
                            self.current += 1
                        self.current += 1
                        continue
        
                    elif self.word[self.current + 1] == 'C':
                        if self.word[self.current + 2] == 'H':
                            if self.searchOfString(self.current + 3, 2, 'OO', 'ER', 'EN', 'UY', 'ED', 'EM'):
                                if self.searchOfString(self.current + 3, 2, 'ER', 'EN'):
                                    self.addLetter('X')
                                    #self.extraAdd('SK')
                                else:
                                    self.addLetter('SK')
                                self.current += 3
                                continue
                            else:
                                if (self.current == 4 and not self.isVowel(self.word[7]) and self.word[7] != 'W'):
                                    self.addLetter('X')
                                    #self.extraAdd('S')
                                else:
                                    self.addLetter('X')
                                self.current += 3
                                continue
                        elif self.word[self.current + 2] in 'IEY':
                            self.addLetter('S')
                            self.current += 3
                            continue
                        self.addLetter('SK')
                        self.current += 3
                        continue
        
                    elif (self.current == self.length - 1 and self.searchOfString(self.current - 2, 2, 'AI', 'OI')):
                        self.addLetter('')
                        #self.extraAdd('S')
                    else:
                        self.addLetter('S')
        
                    while self.word[self.current] in 'SZ':
                        self.current += 1
                    continue
    
                #Case 'T'
                elif self.word[self.current] == 'T':
                    if self.searchOfString(self.current, 4, 'TION'):
                        self.addLetter('X')
                        self.current += 3
                        continue
        
                    elif self.searchOfString(self.current, 3, 'TIA', 'TCH'):
                        self.addLetter('X')
                        self.current += 3
                        continue
        
                    elif self.searchOfString(self.current, 2, 'TH') or self.searchOfString(self.current, 3, 'TTH'):
                        if (self.searchOfString(self.current + 2, 2, 'OM', 'AM') 
                            or self.searchOfString(0, 4, 'VAN ', 'VON ') or self.searchOfString(0, 3, 'SCH')):
                            self.addLetter('T')
                        else:
                            self.addLetter('S')
                            #self.extraAdd('T')
                        self.current += 2
                        continue
        
                    while self.word[self.current] in 'TD':
                        self.current += 1
                    self.addLetter('T')
                    continue
    
                #Case 'V'
                elif self.word[self.current] == 'V':
                    while self.word[self.current] == 'V':
                        self.current += 1
                    self.addLetter('F')
                    continue
    
                #Case 'W'
                elif self.word[self.current] == 'W':
                    if self.word[self.current + 1]  == 'R':
                        self.addLetter('R')
                        self.current += 2
                        continue

                    elif self.current == 4:
                        if self.isVowel(self.word[self.current + 1]):
                            self.addLetter('F')
                            #self.extraAdd('A')
                            self.current += 2
                            continue
                        elif self.word[self.current + 1]  == 'H' and self.isVowel(self.word[self.current + 2]):
                            self.addLetter('F')
                            self.current += 3
                            continue

                    elif self.isVowel(self.word[self.current + 1]) and self.isVowel(self.word[self.current - 1]):
                        self.addLetter('F')
                        self.current += 1
                        continue

                    elif ((self.current == self.length - 1 and self.isVowel(self.word[self.current - 1])) 
                          or self.searchOfString(self.current - 1, 5, 'EWSKI', 'EWSKY', 'OWSKI', 'OWSKY')):
                        self.addLetter('')
                        #self.extraAdd('F')
                        self.current += 1
                        continue
        
                    elif self.searchOfString(self.current, 4, 'WICZ', 'WITZ'):
                        self.addLetter('TS')
                        #self.extraAdd('FX')
                        self.current += 4
                        continue
        
                    while self.word[self.current] == 'W':
                        self.current += 1
                    continue


                #Case 'X'
                elif self.word[self.current] == 'X':
                    if (not (self.current == self.length - 1 and
                             (self.searchOfString(self.current - 3, 3, 'IAU', 'EAU') 
                              or self.searchOfString(self.current - 2, 2, 'AU', 'OU')))):
                        self.addLetter('KS')

                    while self.word[self.current] in 'CX':
                        self.current += 1
                    continue
    
                #Case 'Z'
                elif self.word[self.current] == 'Z':
                    if self.word[self.current + 1] == 'H':
                        self.addLetter('J')
                        self.current += 2
                        continue
                    elif (self.searchOfString(self.current + 1, 2, 'ZO', 'ZI', 'ZA') or (self.slavoGermanic() 
                            and (self.current > 4 and self.word[self.current - 1] != 'T'))):
                        self.addLetter('S')
                        #self.extraAdd('TS')
                    else:
                        self.addLetter('S')
    
                    while self.word[self.current] == 'Z':
                        self.current += 1
                    continue

                #Case the other letters
                else:
                    self.current += 1

            #Russian language
            elif u'А' <= self.word[self.current] <= u'Я':
                
                #Case Vowel
                if self.isVowel(self.word[self.current]):
                    if self.current == 4:
                        self.addLetter('A')   
                    self.current += 1
                    continue

                #Case 'Б'
                elif self.word[self.current] == u'Б':
                    self.addLetter('P')
                    
                    while self.word[self.current] == u'Б' or self.word[self.current] == u'П':
                        self.current += 1
                    continue

                #Case 'В'
                elif self.word[self.current] == u'В':
                    self.addLetter('F')
                    
                    while self.word[self.current] == u'В' or self.word[self.current] == u'Ф':
                        self.current += 1
                    continue

                #Case 'Г'
                elif self.word[self.current] == u'Г':
                    self.addLetter('K')
                    
                    while self.word[self.current] == u'Г' or self.word[self.current] == u'К':
                        self.current += 1
                    continue

                #Case 'Д'
                elif self.word[self.current] == u'Д':
                    if self.word[self.current + 1] == u'C':
                        self.addLetter('X')
                        self.current += 2
                        continue
                    else:
                        self.addLetter('T')
                    
                    while self.word[self.current] == u'Д' or self.word[self.current] == u'Т':
                        self.current += 1
                    continue

                #Case 'Ж'
                elif self.word[self.current] == u'Ж':
                    self.addLetter('J')
                    
                    while self.word[self.current] == u'Ж':
                        self.current += 1
                    continue

                #Case 'З'
                elif self.word[self.current] == u'З':
                    self.addLetter('S')
                    
                    while self.word[self.current] == u'З' or self.word[self.current] == u'С':
                        self.current += 1
                    continue

                #Case 'К'
                elif self.word[self.current] == u'К':
                    self.addLetter('K')
                    
                    while self.word[self.current] == u'К' or self.word[self.current] == u'Г':
                        self.current += 1
                    continue

                #Case 'Л'
                elif self.word[self.current] == u'Л':
                    self.addLetter('L')
                    
                    while self.word[self.current] == u'Л':
                        self.current += 1
                    continue

                #Case 'М'
                elif self.word[self.current] == u'М':
                    self.addLetter('M')
                    
                    while self.word[self.current] == u'М':
                        self.current += 1
                    continue

                #Case 'Н'
                elif self.word[self.current] == u'Н':
                    self.addLetter('N')
                    
                    while self.word[self.current] == u'Н':
                        self.current += 1
                    continue

                #Case 'П'
                elif self.word[self.current] == u'П':
                    self.addLetter('P')
                    
                    while self.word[self.current] == u'Б' or self.word[self.current] == u'П':
                        self.current += 1
                    continue

                #Case 'Р'
                elif self.word[self.current] == u'Р':
                    self.addLetter('R')
                    
                    while self.word[self.current] == u'Р':
                        self.current += 1
                    continue

                #Case 'С'
                elif self.word[self.current] == u'С':
                    self.addLetter('S')
                    
                    while self.word[self.current] == u'С' or self.word[self.current] == u'З':
                        self.current += 1
                    continue

                #Case 'Т'
                elif self.word[self.current] == u'Т':
                    self.addLetter('T')
                    
                    while self.word[self.current] == u'Т' or self.word[self.current] == u'Д':
                        self.current += 1
                    continue

                #Case 'Ф'
                elif self.word[self.current] == u'Ф':
                    self.addLetter('F')
                    
                    while self.word[self.current] == u'Ф' or self.word[self.current] == u'В':
                        self.current += 1
                    continue

                #Case 'Х'
                elif self.word[self.current] == u'Х':
                    self.addLetter('H')
                    
                    while self.word[self.current] == u'Х':
                        self.current += 1
                    continue

                #Case 'Ц'
                elif self.word[self.current] == u'Ц':
                    self.addLetter('TS')
                    while self.word[self.current] == u'Ц':
                        self.current += 1
                    continue

                #Case 'Ч'
                elif self.word[self.current] == u'Ч':
                    if self.word[self.current + 1] == u'Т' and self.word[self.current + 1] == u'Н':
                        self.addLetter('X')
                        self.current += 2
                        continue

                    self.addLetter('X')
                    while self.word[self.current] == u'Ч':
                        self.current += 1
                    continue

                #Case 'Ш' or 'Щ'
                elif self.word[self.current] == u'Ш' or self.word[self.current] == u'Щ':
                    self.addLetter('X')
                    
                    while self.word[self.current] == u'Ш' or self.word[self.current] == u'Щ':
                        self.current += 1
                    continue

                #Case the other letters
                else:
                    self.current += 1

            #Case other symbols            
            else:
                self.current += 1


    def searchOfString(self, start, length, *strings):
        if self.word[start : start + length] in strings:
            return True
        else:
            return False
    
    def addLetter(self, string):    
        self.transcription += string

    #TODO?        
    def extraAdd(self, string):
        None

    def isVowel(self, letter):
        if letter in "AEIOUY" or letter in u"АУОЫИЭЯЮЕЁ":
            return True
        else:
            return False

    def slavoGermanic(self):
        if 'W' in self.word or 'K' in self.word or 'CZ' in self.word or 'WITZ' in self.word:
            return True
        else:
            return False

    def __str__(self):
        '''
        answer = self.transcription[0]
        if len(self.transcription) > 0:
            for i in range(1, len(self.transcription)):
                if self.transcription[i - 1] != self.transcription[i]:
                    answer += self.transcription[i]
        return answer
        '''
        return self.transcription

if __name__ == '__main__':
    print( DoubleMetaphon("thought") )