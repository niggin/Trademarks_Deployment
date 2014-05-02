# -*- coding: utf-8 -*-
import algorithm

def metricOfWords(pattern, word, vFine = 50.0, cFine = 5.0):
    u'''
        @version: Version 1.1 from 16.04.2014
        @author: Alex Kuzmin
        @return: double, the distance between input words
    u'''
    if pattern == u"" or word == "":
        return -1

    lenP = len(pattern)
    lenW = len(word)
    if lenW < lenP:
        lenP, lenW = lenW, lenP
        pattern, word = word.upper(), pattern.upper()
    else:
        word, pattern = word.upper(), pattern.upper()
    
    DM = algorithm.DoubleMetaphon()
    DMTrancriptionP = DM.getTranscription(pattern)
    lenTP = len(DMTrancriptionP)
    DMTrancriptionPinfo = (DM.getNumbersOfSymbols(), DM.getAmountsOfReplacedSymbols())
    DMTrancriptionW = DM.getTranscription(word)
    lenTW = len(DMTrancriptionW)
    DMTrancriptionWinfo = (DM.getNumbersOfSymbols(), DM.getAmountsOfReplacedSymbols())
    numbers = 0 # like define
    amounts = 1 # like define

    distance = 0
    fines = 0
    #TODO improve: find u'pattern' in 'word'
    if len(DMTrancriptionP) == len (DMTrancriptionW):
        indexP = 0 # pattern index
        indexW = 0 # word index
        idxP = 0 # pattern transcription index
        idxW = 0 # word transcription index
        while indexW < lenW or indexP < lenP:
            #print(indexW, indexP)
            if indexW < lenW and indexP < lenP:
                #Case 1: the current letters of u'pattern' form the current symbol of the transcription
                if idxP < lenTP and indexP == DMTrancriptionPinfo[numbers][idxP]:
                    #print(u"where: ", DMTrancriptionP[indexP], DMTrancriptionW[indexW])
                    #print(u"P", DMTrancriptionP[idxP])
                    while indexW < lenW and indexW != DMTrancriptionWinfo[numbers][idxW]:
                        #subcase: there are extra letters(vowels) in u'word'
                        #@fine for each extra-letter (vowel)
                        fines += vFine
                        #print(u"extra in W: ", word[indexW])
                        indexW += 1
                    if DMTrancriptionP[idxP] == DMTrancriptionW[idxW]:
                        #subcase: Coincidence of transcription symbols
                        distance += cFine * compareConsonants(word[indexW:indexW + DMTrancriptionWinfo[amounts][idxW]], 
                                                      pattern[indexP:indexP + DMTrancriptionPinfo[amounts][idxP]])
                        fines += cFine
                        #print(u"OkayP: ", word[indexW])
                        indexP += DMTrancriptionPinfo[amounts][idxP]
                        indexW += DMTrancriptionWinfo[amounts][idxW]
                        idxP += 1
                        idxW += 1
                        continue
                    elif indexW < lenW:
                        #subcase: different letters of trascriptions
                        #max-@fine for a different-letter (consonant)
                        fines += vFine
                        #print(u"differ")
                        indexP += DMTrancriptionPinfo[amounts][idxP]
                        indexW += DMTrancriptionWinfo[amounts][idxW]
                        idxP += 1
                        idxW += 1
                        continue
                    else:
                        #subcase: there are no any letters in u'word'
                        #max-@fine for extra-letter (consonant) in u'pattern'
                        fines += cFine
                        indexP += DMTrancriptionPinfo[amounts][idxP]
                        idxP += 1
                        #print (u"The End?")
                        continue

                #Case 2: the current letters of u'word' form the current symbol of the transcription
                if idxW < lenTW and indexW == DMTrancriptionWinfo[numbers][idxW]:
                    while indexP < lenP and indexP != DMTrancriptionPinfo[numbers][idxP]:
                        #subcase: there are extra letters(vowels) in u'pattern'
                        #@fine for each extra-letter (vowel)
                        fines += vFine
                        #print(u"extra in P: ", pattern[indexP])
                        indexP += 1
                    if DMTrancriptionW[idxW] == DMTrancriptionP[idxP]:
                        #subcase: Coincidence of transcription symbols
                        distance += cFine * compareConsonants(word[indexW:indexW + DMTrancriptionWinfo[amounts][idxW]], 
                                                      pattern[indexP:indexP + DMTrancriptionPinfo[amounts][idxP]])
                        fines += cFine
                        #print(u"OkayW: ", word[indexP])
                        indexP += DMTrancriptionPinfo[amounts][idxP] - 1
                        indexW += DMTrancriptionWinfo[amounts][idxW] - 1
                        idxP += 1
                        idxW += 1
                        continue
                    elif indexP < lenP:
                        #subcase: different letters of trascriptions
                        #max-@fine for a different-letter (consonant)
                        fines += cFine
                        #print(u"differ")
                        indexP += DMTrancriptionPinfo[amounts][idxP]
                        indexW += DMTrancriptionWinfo[amounts][idxW]
                        idxP += 1
                        idxW += 1
                        continue
                    else:
                        #subcase: there are no any letters in u'pattern'
                        #max-@fine for extra-letter (consonant) in u'word'
                        fines += cFine
                        indexW += DMTrancriptionWinfo[amounts][idxW]
                        idxW += 1
                        #print (u"The End?")
                        continue

                #Case 3: the current letters are not in transcriptions of u'word' and 'pattern'
                distance += vFine * compareVovels(word[indexW], pattern[indexP])
                fines += vFine
                indexW += 1
                indexP += 1
                #print(u"work with Vowels")
                continue

            #Case: the remaining part of u'pattern' is empty
            elif indexW < lenW:
                #@fine for extra-letter of u'word'
                fines += vFine
                indexW += 1
                #print(u"fine for extra-vowel of Pattern!")

            #Case: the remaining part of u'word' is empty
            else:
                #@fine for extra-letter of u'pattern'
                fines += vFine
                indexP += 1
                #print(u"fine for extra-vowel of Word!")
    else:
        return 1
    return 1 - distance / fines

def compareVovels(letters, oLetters):
    #return double in [0, 1]
    if letters == oLetters:
            return 1
    if len(letters) == 1 and len(oLetters) == 1:
        if algorithm.isEnglish(letters):
            if algorithm.isRussian(oLetters):
                return 0.75
            else:
                return 0.5
        else:
            if algorithm.isRussian(oLetters):
                return 0.5
            else:
                return 0.75
    return 0.75

def compareConsonants(letters, oLetters):
    #return double in [0, 1]
    #print(letters)
    #print(oLetters)
    if letters == oLetters:
            return 1
    if len(letters) == 1 and len(oLetters) == 1:
        if algorithm.isEnglish(letters):
            if algorithm.isRussian(oLetters):
                return 0.75
            else:
                return 0.5
        else:
            if algorithm.isRussian(oLetters):
                return 0.5
            else:
                return 0.75
    return 0.75


def metricOfTranscriptions(patternTr, wordTr, vFine=1.0, cFine=5.0, coef=3.0):
    u'''
        @version: Version 1.0 from 28.04.2014
        @author: Alex Kuzmin
        @return: double, the distance between input words
    u'''
    if patternTr == u"" or wordTr == "":
        return -1

    lenP = len(patternTr)
    lenW = len(wordTr)
    #TODO improve: find u'pattern' in 'word'
    distance = 0.0
    fines = 0.0
    indexP = 0 # patternTr index
    indexW = 0 # wordTr index
    while indexW < lenW or indexP < lenP:
        if indexW < lenW and indexP < lenP:
        
            #Case 1: the current symbol of u'wordTr' sounds like consonant one
            if not isVowelTr(wordTr[indexW]):
                while indexP < lenP and isVowelTr(patternTr[indexP]):
                    #subcase: there are extra letters(vowels) in u'patternTr'
                    #@fine for each extra-letter (vowel)
                    distance += coef * vFine
                    fines += coef * vFine
                    indexP += 1
                if indexP < lenP:
                    #subcase: sounds of u'wordTr' and 'patternTr' exists
                    distance += cFine * compareTr(wordTr[indexW], patternTr[indexP])
                    fines += cFine
                    if wordTr[indexW] == u'r' or patternTr[indexP] == u'r':
                        if wordTr[indexW] == u'r' and patternTr[indexP] != u'Р':
                            indexW += 1
                            continue
                        elif wordTr[indexW] == u'Р' and patternTr[indexP] != u'r':
                            indexP += 1
                            continue
                    indexP += 1
                    indexW += 1
                    continue
                else:
                    #subcase: there are no any letters in u'patternTr'
                    #max-@fine for extra-letter (consonant) in u'wordTr'
                    distance += coef * cFine
                    fines += coef * cFine
                    indexP += 1
                    continue

            #Case 2: the current symbol of u'patternTr' sounds like consonant one
            if not isVowelTr(patternTr[indexP]):
                while indexW < lenW and isVowelTr(wordTr[indexW]):
                    #subcase: there are extra letters(vowels) in u'wordTr'
                    #@fine for each extra-letter (vowel)
                    distance += coef * vFine
                    fines += coef * vFine
                    indexW += 1
                if indexW < lenW:
                    #subcase: sounds of u'wordTr' and 'patternTr' exists
                    distance += cFine * compareTr(wordTr[indexW], patternTr[indexP])
                    fines += cFine
                    if wordTr[indexW] == u'r' or patternTr[indexP] == u'r':
                        if wordTr[indexW] == u'r' and patternTr[indexP] != u'Р':
                            indexW += 1
                            continue
                        elif wordTr[indexW] == u'Р' and patternTr[indexP] != u'r':
                            indexP += 1
                            continue
                    indexP += 1
                    indexW += 1
                    continue
                else:
                    #subcase: there are no any letters in u'wordTr'
                    #max-@fine for extra-letter (consonant) in u'patternTr'
                    distance += coef * cFine
                    fines += coef * cFine
                    indexW += 1
                    continue

            #Case 3: the both current symbols u'wordTr' and 'patternTr' sound like vowels
            distance += vFine * compareTr(wordTr[indexW], patternTr[indexP], isVowels=True)
            fines += vFine
            indexW += 1
            indexP += 1
            continue

        #Case: the remaining part of u'patternTr' is empty
        elif indexW < lenW:
            #@fine for extra-letter of u'word'
            if isVowelTr(wordTr[indexW]):
                distance += coef * vFine
                fines += coef * vFine
            else:
                distance += coef * cFine
                fines += coef * cFine
            indexW += 1

        #Case: the remaining part of u'wordTr' is empty
        else:
            #@fine for extra-letter of u'patternTr'
            if isVowelTr(patternTr[indexP]):
                distance += coef * vFine
                fines += coef * vFine
            else:
                distance += coef * cFine
                fines += coef * cFine
            indexP += 1
    return distance / fines

def isVowelTr(letter):
    if letter in u'АОУЭИЙai':
        return True
    else:
        return False

def compareTr(symbol, oSymbol, isVowels=False):
    if symbol == oSymbol:
        return 0.0
    distance = 3.0
    if isVowels:
        if symbol == u'А':
            distance = 30.0
        elif symbol == u'О':
            distance = 40.0
        elif symbol == u'У':
            distance = 50.0
        elif symbol == u'Э':
            distance = 20.0
        elif symbol == u'И':
            distance = 10.0
        elif symbol == u'Й':
            distance = 5.0
        elif symbol == u'a':
            distance = 22.5
        elif symbol == u'i':
            distance = 7.5
        else:
            return 1.0
        if oSymbol == u'А':
            distance -= 30
        elif oSymbol == u'О':
            distance -= 40
        elif oSymbol == u'У':
            distance -= 50
        elif oSymbol == u'Э':
            distance -= 20
        elif oSymbol == u'И':
            distance -= 10
        elif oSymbol == u'Й':
            distance -= 5
        elif oSymbol == u'a':
            distance -= 22.5
        elif oSymbol == u'i':
            distance -= 7.5
        else:
            return 1
        distance /= 50
    else:
        if symbol in u"ВФwu":
            if oSymbol not in u"ВФwu":
                return 1.0
            if symbol == u'В':
                distance = 0.0
            elif symbol == u'Ф':
                distance = 1.0
            elif symbol == u'w':
                distance = 0.25
            elif symbol == u'u':
                distance = 0.35
            if oSymbol == u'В':
                distance -= 0
            elif oSymbol == u'Ф':
                distance -= 1
            elif oSymbol == u'w':
                distance -= 0.25
            elif oSymbol == u'u':
                distance -= 0.35
        elif symbol in u"ЗСzs":
            if oSymbol not in u"ЗСzs":
                return 1.0
            if symbol == u'З':
                distance = 0.0
            elif symbol == u'С':
                distance = 1.0
            elif symbol == u'z':
                distance = 0.25
            elif symbol == u's':
                distance = 1.25
            if oSymbol == u'З':
                distance -= 0
            elif oSymbol == u'С':
                distance -= 1
            elif oSymbol == u'z':
                distance -= 0.25
            elif oSymbol == u's':
                distance -= 1.25
        elif symbol in u"ШЩЧx":
            if oSymbol not in u"ШЩЧx":
                return 1.0
            elif symbol == u'x' or oSymbol == 'x':
                return 1.0 / 3
            if symbol == u'Ш':
                distance = 0.0
            elif symbol == u'Щ':
                distance = 1.0
            elif symbol == u'Ч':
                distance = 2.0
            if oSymbol == u'Ш':
                distance -= 0
            elif oSymbol == u'Щ':
                distance -= 1
            elif oSymbol == u'Ч':
                distance -= 2
        elif symbol in u"Нn":
            if oSymbol not in u"Нn":
                return 1.0
            distance = 0.35
        elif symbol in u"Рr":
            if oSymbol not in u"Рr":
                return 0.75
            distance = 0.5
        elif symbol in u"БП":
            if oSymbol not in u"БП":
                return 1.0
            else:
                return 1.0 / 3
        elif symbol in u"ДТ":
            if oSymbol not in u"ДТ":
                return 1.0
            else:
                return 1.0 / 3
        elif symbol in u"ГК":
            if oSymbol not in u"ГК":
                return 1.0
            else:
                return 1.0 / 3
        else:
            return 1.0
        distance /= 3
    return abs(distance)


if __name__ == u'__main__':
    word = u"тоти"
    pattern = u"totp"
    print (u"metric answer: ", metricOfWords(word, pattern) )
    DM = algorithm.DoubleMetaphon()
    print (u"DM of word: ", DM.getTranscription(word) )
    print (u"DM of pattern: ", DM.getTranscription(pattern) )
    print(word, pattern)
    word = u'СЛАНТЭС'
    pattern = u'СЛЭНrТЭС'
    print(u"metricTR answer: ", metricOfTranscriptions(word, pattern))