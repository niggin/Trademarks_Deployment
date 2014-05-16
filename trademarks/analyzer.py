# -*- coding: utf-8 -*-
import algorithm

def analyzer(word, transcription=u"", numbersOfSymbols=[], amountsOfReplacedSymbols=[]):
    '''
        @version: Version 1.0 from 28.04.2014
        @author: Alex Kuzmin
        @return: Full transcription of the word
        @note: DoubleMetaphon.transcription [u'X'] goes into ['x']
    '''
    if word == u"":
        return -1
    if transcription == u"" or numbersOfSymbols == [] or amountsOfReplacedSymbols == []:
        DM = algorithm.DoubleMetaphon()
        DMTranscription = DM.getTranscription(word)
        NOS = DM.getNumbersOfSymbols()
        ARS = DM.getAmountsOfReplacedSymbols()
    else:
        DMTranscription = transcription.upper()
        NOS = numbersOfSymbols
        ARS = amountsOfReplacedSymbols
    lenTr = len(DMTranscription)
    lenW = len(word)
    

    fullTranscription = u""
    current = 0
    indexTr = 0
    while current < lenW:
        #Current letter from DoubleMetaphon Transcription
        if indexTr < lenTr and current == NOS[indexTr]:
            if algorithm.isVowel(DMTranscription[indexTr]):
                indexTr += 1
                continue
            elif ARS[indexTr] == 1 and (indexTr + 1 >= lenTr or ARS[indexTr + 1] != 0):
                    fullTranscription += toTranscription(word[current].upper())
                    current += 1
                    indexTr += 1
                    continue
            else:
                #assumption, because I am not perfect ;)
                #TODO: improve - analyze voiced/voiceless letters in u'algorithm.py'
                fullTranscription += toTranscription(DMTranscription[indexTr], tr=True)
                current += ARS[indexTr]
                indexTr += 1
                continue

        #Current letter from Russian Language and is smth like vowel
        if algorithm.isRussian(word[current].upper()):
            if (current == 0 or algorithm.isVowel(word[current - 1].upper())) and word[current].upper() in u"ЕЁЮЯ":
                if word[current].upper() == u'Е':
                    fullTranscription += u'ЙЭ'
                elif word[current].upper() == u'Я':
                    fullTranscription += u'ЙА'
                elif word[current].upper() == u'Ю':
                    fullTranscription += u'ЙУ'
                elif word[current].upper() == u'Ё':
                    fullTranscription += u'ЙО'
                current += 1
                continue
            elif word[current].upper() == u'Ь' or word[current].upper() == u'Ъ':
                if current + 1 < lenW and word[current + 1].upper() in u"ЕЁЮЯ":
                    if word[current + 1].upper() == u'Е':
                        fullTranscription += u'ЙЭ'
                    elif word[current + 1].upper() == u'Я':
                        fullTranscription += u'ЙА'
                    elif word[current + 1].upper() == u'Ю':
                        fullTranscription += u'ЙУ'
                    elif word[current + 1].upper() == u'Ё':
                        fullTranscription += u'ЙО'
                    current += 2
                    continue
                else: 
                    current += 1
                    continue
            else:
                fullTranscription += toTranscription(word[current].upper())
                current += 1
                continue

        #Current letter from English Language and is smth like vowel
        elif algorithm.isEnglish(word[current].upper()):
            #the next letter is a vowel too
            if current + 1 < lenW and algorithm.isVowel(word[current + 1].upper()):
                if word[current].upper() == u'E':
                    if word[current + 1].upper() == u'A':
                        fullTranscription += u'И'
                        current += 2
                        continue
                    elif word[current + 1].upper() == u'E':
                        fullTranscription += u'И'
                        current += 2
                        continue
                    elif word[current + 1].upper() == u'Y':
                        fullTranscription += u'ЭЙ'
                        current += 2
                        continue
                    else:
                        #print(u'E?')
                        None
                elif word[current].upper() == u'O':
                    if word[current + 1].upper() == u'O':
                        fullTranscription += u'У'
                        current += 2
                        continue
                    else:
                        #print(u"O?")
                        None
                elif word[current].upper() == u'A':
                    if word[current + 1].upper() == u'U':
                        fullTranscription += u'ЭЙ'
                        current += 2
                        continue
                    else:
                        #print(u"A?")
                        None
                else:
                    #print(u"??")
                    None
            #the next letter is a consonant
            else:
                if word[current].upper() == u'E':
                    if current + 1 < lenW:
                        if word[current + 1].upper() == u'R':
                            if indexTr < lenTr and DMTranscription[indexTr] == u'R':
                                indexTr += 1
                            if current + 2 < lenW and word[current + 2].upper() == u'E':
                                fullTranscription += u'ИЭr'
                                current += 3
                                continue
                            else:
                                fullTranscription += u'Ёr'
                                current += 2
                                continue
                        else:
                            if current + 2 < lenW and algorithm.isVowel(word[current + 2].upper()):
                                fullTranscription += u'И'
                                current += 1
                                continue
                            else:
                                fullTranscription += u'Э'
                                current += 1
                                continue
                    else:
                        current += 1
                        continue
                elif word[current].upper() == u'A':
                    if current + 1 < lenW:
                        if word[current + 1].upper() == u'R':
                            if DMTranscription[indexTr] == u'R':
                                indexTr += 1
                            if current + 2 < lenW and word[current + 2].upper() == u'E':
                                fullTranscription += u'ЭiЭr'
                                current += 3
                                continue
                            else:
                                fullTranscription += u'A'
                                current += 2
                                continue
                        else:
                            if current + 2 < lenW and algorithm.isVowel(word[current + 2].upper()):
                                fullTranscription += u'ЭЙ'
                                current += 1
                                continue
                            else:
                                fullTranscription += u'a'
                                current += 1
                                continue
                    else:
                        fullTranscription += u'Э'
                        current += 1
                        continue
                elif word[current].upper() == u'I':
                    if current + 1 < lenW:
                        if word[current + 1].upper() == u'R':
                            if DMTranscription[indexTr] == u'R':
                                indexTr += 1
                            if current + 2 < lenW and word[current + 2].upper() == u'E':
                                fullTranscription += u'АИЭr'
                                current += 3
                                continue
                            else:
                                fullTranscription += u'ИЭr'
                                current += 2
                                continue
                        else:
                            if current + 2 < lenW and algorithm.isVowel(word[current + 2].upper()):
                                fullTranscription += u'АЙ'
                                current += 1
                                continue
                            else:
                                fullTranscription += u'И'
                                current += 1
                                continue
                    else:
                        fullTranscription += u'И'
                        current += 1
                        continue
                elif word[current].upper() == u'O':
                    if current + 1 < lenW:
                        if word[current + 1].upper() == u'R':
                            if DMTranscription[indexTr] == u'R':
                                indexTr += 1
                            if current + 2 < lenW and word[current + 2].upper() == u'E':
                                fullTranscription += u'ОР'
                                current += 3
                                continue
                            else:
                                fullTranscription += u'ОР'
                                current += 2
                                continue
                        else:
                            if current + 2 < lenW and algorithm.isVowel(word[current + 2].upper()):
                                fullTranscription += u'ОУ'
                                current += 1
                                continue
                            else:
                                fullTranscription += u'О'
                                current += 1
                                continue
                    else:
                        fullTranscription += u'ОУ'
                        current += 1
                        continue
                elif word[current].upper() == u'U':
                    if current + 1 < lenW:
                        if word[current + 1].upper() == u'R':
                            if DMTranscription[indexTr] == u'R':
                                indexTr += 1
                            if current + 2 < lenW and word[current + 2].upper() == u'E':
                                fullTranscription += u'УЭr'
                                current += 3
                                continue
                            else:
                                fullTranscription += u'Ёr'
                                current += 2
                                continue
                        else:
                            if current + 2 < lenW and algorithm.isVowel(word[current + 2].upper()):
                                fullTranscription += u'ЙУ'
                                current += 1
                                continue
                            else:
                                fullTranscription += u'А'
                                current += 1
                                continue
                    else:
                        fullTranscription += u'У'
                        current += 1
                        continue
                elif word[current].upper() == u'Y':
                    if current + 1 < lenW:
                        if word[current + 1].upper() == u'R':
                            if DMTranscription[indexTr] == u'R':
                                indexTr += 1
                            if current + 2 < lenW and word[current + 2].upper() == u'E':
                                fullTranscription += u'АИЭr'
                                current += 3
                                continue
                            else:
                                fullTranscription += u'Эr'
                                current += 2
                                continue
                        else:
                            if current + 2 < lenW and algorithm.isVowel(word[current + 2].upper()):
                                fullTranscription += u'АЙ'
                                current += 1
                                continue
                            else:
                                fullTranscription += u'И'
                                current += 1
                                continue
                    else:
                        fullTranscription += u'И'
                        current += 1
                        continue
                else:
                    fullTranscription += u'?'
                fullTranscription += toTranscription(word[current].upper())
        if word[current] == u' ':
            current += 1
            continue
        fullTranscription += u'?'
        current += 1
        continue

    while indexTr < lenTr and ARS[indexTr] == 0:
        fullTranscription += toTranscription(DMTranscription[indexTr], tr=True)
        indexTr += 1

    return fullTranscription

def toTranscription(letter, tr=False):
    u'''
        @param u'tr': if letter from the DoubleMetaphon Transcription set 'True', if letter from just a word set 'False'.
        @return: the transcriptional equivalent of the letter
    u'''

    if algorithm.isRussian(letter):
        return letter
    elif algorithm.isEnglish(letter):
        if letter == u'B':
            return u'Б'
        elif letter == u'P':
            return u'П'
        elif letter == u'V':
            return u'В'
        elif letter == u'F':
            return u'Ф'
        elif letter == u'D':
            return u'Д'
        elif letter == u'T':
            return u'Т'
        elif letter == u'G':
            return u'Г'
        elif letter == u'K':
            return u'К'
        elif letter == u'Z':
            return u'З'
        elif letter == u'S':
            return u'С'
        elif letter == u'N':
            return u'Н'
        elif letter == u'L':
            return u'Л'
        elif letter == u'M':
            return u'М'
        elif letter == u'H':
            return u'Х'
        elif not tr:
            if letter == u'C':
                return u'К'
            elif letter == u'R':
                return u'r'
            elif letter == u'J':
                return u'ДЖ'
            elif letter == u'Q':
                return u'К'
            elif letter == u'W':
                return u'w'
            elif letter == u'X':
                return u'КС'
            else:
                return u'?'
        elif tr:
            if letter == u'J':
                return u'Ж'
            elif letter == u'R':
                return u'Р'
            elif letter == u'X':
                return u'x'
            else:
                return u'?'

if __name__ == u'__main__':
    #print(analyzer(u"cause"))
    #print(analyzer(u"THEREFy"))
    #print(analyzer(u"царитьсяц"))
    #print(analyzer(u"щётка"))
    #print(analyzer(u"сланец"))
    #print(analyzer(u"солнце"))
    dm = algorithm.DoubleMetaphon()
    print(u"better")
    print(dm.getTranscription(u"better"))
    print(dm.getAmountsOfReplacedSymbols())
    print(dm.getNumbersOfSymbols())