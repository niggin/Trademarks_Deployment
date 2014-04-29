def parserEnglishTranscription(transcription , line, count):
    '''
        @version: Version 1.0 from 17.04.2014
        @author: Alex Kuzmin
        @return: My full transcription of the standard transcription of the word
        @note: [ər] -> [Эr], [ɛər] = [ЭИ(Й)Эr] -> [ЭiЭr], [ɜr] -> [ЙОr], [w] -> [w], [ʰw] -> [u], [ŋ] -> [n], [æ] -> [a], [ɔɪ] -> [Оi], [ð] -> [z], [θ] -> [s].
    '''

    lenTr = len(transcription)
    fullTranscription = ""
    if lenTr == 0:
        return -1

    idx = 0
    while idx < lenTr:
        if transcription[idx] == 'ˈ':
            idx += 1
            continue
        elif transcription[idx] == ' ':
            idx += 1
            continue
        elif transcription[idx] == 'ˌ':
            idx += 1
            continue
        elif transcription[idx] == 'r':
            fullTranscription += 'Р'
            idx += 1
            continue
        elif transcription[idx] == 'n':
            fullTranscription += 'Н'
            idx += 1
            continue
        elif transcription[idx] == 's':
            fullTranscription += 'С'
            idx += 1
            continue
        elif transcription[idx] == 'l':
            fullTranscription += 'Л'
            idx += 1
            continue
        elif transcription[idx] == 'k':
            fullTranscription += 'К'
            idx += 1
            continue
        elif transcription[idx] == 'p':
            fullTranscription += 'П'
            idx += 1
            continue
        elif transcription[idx] == 'ə':
            if idx + 1 < lenTr and transcription[idx + 1] == 'r':
                fullTranscription += 'Эr'
                idx += 2
                continue
            else:
                fullTranscription += 'Э'
                idx += 1
                continue
        elif transcription[idx] == 'm':
            fullTranscription += 'М'
            idx += 1
            continue
        elif transcription[idx] == 't':
            if idx + 1 < lenTr and transcription[idx + 1] == 'ʃ':
                fullTranscription += 'Ч'
                idx += 2
                continue
            else:
                fullTranscription += 'Т'
                idx += 1
                continue
        elif transcription[idx] == 'ɪ':
            if idx + 1 < lenTr and transcription[idx + 1] == '̃':
                fullTranscription += 'И'
                idx += 2
                continue
            else:
                fullTranscription += 'И'
                idx += 1
                continue
        elif transcription[idx] == 'æ':
            fullTranscription += 'a'
            idx += 1
            continue
        elif transcription[idx] == 'b':
            fullTranscription += 'Б'
            idx += 1
            continue
        elif idx + 1 < lenTr and transcription[idx : idx + 2] == 'eɪ':
            fullTranscription += 'ЭЙ'
            idx += 2
            continue
        elif transcription[idx] == 'f':
            fullTranscription += 'Ф'
            idx += 1
            continue
        elif transcription[idx] == 'ʊ':
            fullTranscription += 'У'
            idx += 1
            continue
        elif transcription[idx] == 'd':
            fullTranscription += 'Д'
            idx += 1
            continue
        elif transcription[idx] == 'ʃ':
            fullTranscription += 'Ш'
            idx += 1
            continue
        elif transcription[idx] == 'ɒ':
            fullTranscription += 'О'
            idx += 1
            continue
        elif idx + 1 < lenTr and transcription[idx : idx + 2] == 'oʊ':
            fullTranscription += 'ОУ'
            idx += 2
            continue
        elif transcription[idx] == 'v':
            fullTranscription += 'В'
            idx += 1
            continue
        elif transcription[idx] == 'ʌ':
            fullTranscription += 'А'
            idx += 1
            continue
        elif transcription[idx] == 'g':
            fullTranscription += 'Г'
            idx += 1
            continue
        elif transcription[idx] == 'w':
            fullTranscription += 'w'
            idx += 1
            continue
        elif transcription[idx] == 'i':
            if idx + 1 < lenTr and transcription[idx + 1] == '̃':
                fullTranscription += 'И'
                idx += 2
                continue
            else:
                fullTranscription += 'И'
                idx += 1
                continue
        elif transcription[idx] == 'ɛ':
            if idx + 2 < lenTr and transcription[idx + 1: idx + 3] == 'ər':
                fullTranscription += 'ЭiЭr'
                idx += 3
                continue
            elif idx + 1 < lenTr and transcription[idx + 1] == '̃':
                fullTranscription += 'Э'
                idx += 2
                continue
            else:
                fullTranscription += 'Э'
                idx += 1
                continue
        elif transcription[idx] == 'h':
            fullTranscription += 'Х' 
            idx += 1
            continue
        elif transcription[idx] == 'u':
            fullTranscription += 'У'
            idx += 1
            continue
        elif transcription[idx] == 'ʒ':
            fullTranscription += 'Ж' 
            idx += 1
            continue
        elif idx + 1 < lenTr and transcription[idx : idx + 2] == 'ɜr':
            fullTranscription += 'ЙОr'
            idx += 2
            continue
        elif transcription[idx] == 'z':
            fullTranscription += 'З'
            idx += 1
            continue
        elif transcription[idx] == 'y':
            fullTranscription += 'Й'
            idx += 1
            continue
        elif transcription[idx] == 'ŋ':
            fullTranscription += 'n'
            idx += 1
            continue
        elif transcription[idx] == 'ɔ':
            if idx + 1 < lenTr:
                if transcription[idx + 1] == 'ɪ':
                    fullTranscription += 'Оi' 
                    idx += 2
                    continue
                elif transcription[idx + 1] == '̃':
                    fullTranscription += 'О'
                    idx += 2
                    continue
            fullTranscription += 'О'
            idx += 1
            continue
        elif transcription[idx] == 'a':
            if idx + 3 < lenTr and transcription[idx + 1 : idx + 4] == 'ɪər':
                    fullTranscription += 'АИЭr' 
                    idx += 4
                    continue
            elif idx + 1 < lenTr and transcription[idx + 1] == 'ɪ':
                fullTranscription += 'АЙ' 
                idx += 2
                continue
            elif idx + 1 < lenTr and transcription[idx + 1] == '̃':
                fullTranscription += 'А' 
                idx += 2
                continue
            else:
                fullTranscription += 'А' 
                idx += 1
                continue
        elif transcription[idx] == 'ɑ':
            if idx + 1 < lenTr and transcription[idx + 1] == '̃':
                fullTranscription += 'А' 
                idx += 2
                continue
            else:
                fullTranscription += 'А' 
                idx += 1
                continue
        elif transcription[idx] == 'ð':
            fullTranscription += 'z' 
            idx += 1
            continue
        elif transcription[idx] == 'θ':
            fullTranscription += 's' 
            idx += 1
            continue
        elif idx + 1 < lenTr and transcription[idx : idx + 2] == 'ʰw':
            fullTranscription += 'u' 
            idx += 2
            continue
        elif transcription[idx] == 'x':
            fullTranscription += 'Х' 
            idx += 1
            continue
        elif transcription[idx] == 'œ':
            if idx + 1 < lenTr and transcription[idx + 1] == '̃':
                fullTranscription += 'Э' 
                idx += 2
                continue
            else:
                fullTranscription += 'Э' 
                idx += 1
                continue
        elif transcription[idx] == 'ü':
            fullTranscription += 'У' 
            idx += 1
            continue
        else:
            #unknown synbol
            with open("err.txt", mode = 'a', encoding = 'utf8') as writer:
                writer.write("unknown synbol: |" + transcription[idx] + "|")
                writer.write("in #" + str(count) + " " + line)
            idx += 1
    return fullTranscription



if __name__ == '__main__':
    with open("EN+ftr.txt", mode = 'w', encoding = 'utf8'):
        None
    with open("EN+tr.txt", mode = 'r', encoding = 'utf8') as reader: 
        line = reader.readline()
        count = 0
        while line != "":
            splitLine = line.split('#')
            with open("EN+ftr.txt", mode = 'a', encoding = 'utf8') as writer:
                writer.write(splitLine[0] + "#" + parserEnglishTranscription(splitLine[1], line, count) + "#" + splitLine[2])
                #writer.write(splitLine[1] + '\n')
                #print(splitLine[1])
            line = reader.readline()
            count += 1