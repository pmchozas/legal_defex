import requests


def ixa(txt):
    #print(txt)
    url = 'https://ixasrl.linkeddata.es/pos?'
    response = requests.get('https://ixasrl.linkeddata.es/pos?txt='+txt)
    response2 = response.json()
    lemma = list()
    pos = list()
    tokens = list()
    sp = txt.split(' ')
    # print(response2)
    for i in response2['annotations']:
        lemma.append(i['pos'])
        pos.append(i['lemma'])
        tokens.append(i['word'])

    # print(response2['annotations']['word'])
    # print(sp)

    # print(response2)
    return(lemma, pos, tokens)


postag = [
    ['A', 'adjetivo'],
    ['N', 'nombre'],
    ['R', 'adverbio'],
    ['T', 'artículo'],
    ['D', 'determinante'],
    ['v', 'verbo'],
    ['P', 'pronombre'],
    ['C', 'conjunción'],
    ['M', 'numeral'],
    ['I', 'interjección'],
    ['Y', 'abreviatura'],
    ['S', 'preposición'],
    ['F', 'signo']

]
copulas = [
    'considerar',
    'consideración',
    'haber',
    'existir',
    'definir',
    'entender',
    'comprender',
    'ser'
]


def withterms(document, terms):
    termis = list()
    for t in terms:
        termis.append(t[:-1])
    # print(termis)

    sentence = document.replace('\n', '').split('.')
    filewithterms = open('withterms_copula+term_sobrantes.txt', 'w')
    #pos_tagger = CoreNLPParser('http://localhost:9003', tagtype='pos')
    words = list()
    sizes = list()
    # print(len(sentence))
    # print(sentence)
    sents = list()
    for term in termis:
        #print(term)
        i = 0
        band = int()
        while(i < len(sentence) and band < 1):
            sent = sentence[i].replace('<def>', '').replace('</def>', '').replace('<term>', '').replace('</term>', '')

            if(term in sent and sent not in sents):
                defiendum=str()
                definien=str()
                tokterm = term.split(' ')
                post = sent.index(term)
                back = sent[:post].split(' ')
                front = sent[post+len(term)+1:]
                frontlist = front.split(' ')
                back2 = ' '.join(back[-5:-1])
                # back
                resixa = ixa(back2)
                # print(resixa)
                lemma = resixa[1]
                pos = resixa[0]
                tokens = resixa[2]
                # front
                resixa_f = ixa(frontlist[0])
                lemmaf = resixa_f[1]
                posf = resixa_f[0]
                tokensf = resixa_f[2]

                lem = str()
                pos0 = str()
                pos1 = str()
                l = 0
                # for l in range(len(lemma)):
                poslem = -1
                while(l < len(lemma) and poslem < 0):
                    if(lemma[l] in copulas ):
                        lem = lemma[l]
                        poslem = l 
                        #print(poslem, pos, lemma,len(lemma))
                        if(l == 0):
                            pos0 = str()
                            pos1 = pos[l+1]
                        elif(l == len(lemma)):
                            pos0 = pos[l-1]
                            pos1 = str()
                    else:
                        pos0 = pos[-1]
                    l = l+1

                #print(term,'-',lem,'-', pos0,'-', pos1)
                # print(lem1)
                pattern = str()
                if(lem in copulas):
                    print('1-',term)
                    #print(term, '-' ,lemma, '-' ,pos,'-' , tokens,'-', poslem)
                    tok = tokens[poslem]

                    word_after_cop = str()
                    afterword = str()
                    #print(poslem, len(tokens) )
                    if(poslem > 0 and poslem+2 == len(tokens)):
                        #print(pos[poslem+1])
                        word_after_cop = tokens[poslem+1]
                        pattern = tokens[poslem-1].lower()+' '+tok.lower() + \
                            ' '+word_after_cop.lower()+' '+term.lower()
                    elif(poslem > 0 and poslem+1 < len(tokens)):
                        if(tokterm[0] in tokens[poslem+1]):
                            pattern = tokens[poslem-1].lower() + \
                                ' '+tok.lower()+' '+term.lower()
                        else:
                            pattern = tokens[poslem-1].lower()+' '+tok.lower()+' '+' '.join(
                                tokens[poslem+1:]).lower()+' '+term.lower()

                    elif(poslem > 0 and poslem == len(tokens)):
                        pass
                    else:
                        pattern = tok.lower()+' ' + \
                            ' '.join(tokens[poslem+1:]).lower() + \
                            ' '+term.lower()
                    #print(pattern,tok, tokens[poslem+1:] )

                    patterns = [
                        'se '+tok+' '+term,
                        'se '+tok+' '+word_after_cop+' '+term,
                        'se '+tok+' '+' '.join(tokens[poslem+1:])+' '+term,
                        'se '+tok+' '+afterword+' '+word_after_cop+' '+term,
                        'se '+tok+' '+term+' como',
                        'se '+tok+' como ' + term,
                        tok+' como '+term,
                        tok+' '+term,
                        tok+' '+' '.join(tokens[poslem+1:])+' '+term,
                        tok+' '+term+' cuando',
                        tok+' '+term+' siempre',
                        tok+' '+term+' si',
                    ]

                    if(term in front):
                        #print('FRONT', front.count(term))
                        times = front.count(term)
                        v = 0
                        while(v < times):
                            band = 1
                            post = sent.index(term)
                            front = sent[post+len(term)+1:]
                            frontlist = front.split(' ')
                            if(term in frontlist):
                                ind1 = frontlist.index(term)
                                resixa_f = ixa(frontlist[0])
                                lemmaf = resixa_f[1]
                                posf = resixa_f[0]
                                tokensf = resixa_f[2]
                                sents.append(sent)
                                #print(post, tokensf[0], posf[0][0])
                                if('A' in posf[0][0] or 'N' in posf[0][0]):
                                    defiendum = term+' '+tokensf[0]
                                else:
                                    defiendum = term
                                    definien = sent

                                p1 = front.index(term)
                                definien = front[:p1]

                                print('1->', defiendum, '-->',
                                      pattern, '--->', definien)
                                front = sent[p1:]
                                sent = front
                                # print(sent)

                            v = v+1

                    elif(pattern in patterns):
                        band = 1
                        sents.append(sent)
                        #print(tokensf[0], posf[0][0], pos, tokens, pos[len(pos)-2][0], pos[len(pos)-1][0])
                        if(len(posf) > 1):
                            if('A' in posf[0][0] or 'N' in posf[0][0]):
                                defiendum = term+' '+tokensf[0]
                        elif('A' in pos[len(pos)-2][0] or 'D' in pos[len(pos)-1][0]):
                            defiendum = tokens[len(
                                tokens)-2]+' '+tokens[len(tokens)-1]+' '+term
                            print('---------', defiendum)
                        else:
                            defiendum = term
                        definien = sent
                        print('1.1->', defiendum, '-->', pattern, '--->', sent)
                elif(len(pos0)>0):
                    if('D' in pos0[0]):
                        #print('2-',term, pos0[0])

                        nextt = front.split(' ')
                        resixaD = ixa(front)
                        lemmaD = resixaD[1]
                        posD = resixaD[0]
                        tokensD = resixaD[2]

                        # p=tokens[0]+' '+
                        #print(posD[0][0],len(tokens),tokterm, tokensD, lemmaD, posD)

                        if('comprender' in lemmaD):
                            band = 1
                            sents.append(sent)
                            defiendum = term
                            definien = sent
                            print('2->', defiendum, '-->', pattern, '--->', sent)
                        elif(term+' ' in front):
                            tokterm = term.split(' ')
                            lentt = len(tokterm)
                            #print(tokensD, front, tokterm[0])
                            #print(term, tokterm)
                            if(tokterm[0] in tokensD):
                                postt = tokensD.index(tokterm[0])
                                #print(tokensD[postt+lentt:], lemmaD[postt+lentt:])
                                lemmaD2 = lemmaD[postt+lentt:]
                                k = 0
                                readyk = 0
                                while(k < len(lemmaD2) and readyk < 1):
                                    lem = lemmaD2[k]
                                    if(lem in copulas):
                                        readyk = 1
                                        band = 1
                                        sents.append(sent)
                                        #print(lem)
                                        #print(term, posD, tokensD)
                                        pattern = [posD[0][0],
                                                posD[1][0], posD[2][0]]
                                        # print(pattern)
                                        patterns = [
                                            ['S', 'N', 'A']
                                        ]
                                        if(pattern in patterns):
                                            term = term+' ' + \
                                                ' '.join(tokensD[:len(pattern)])
                                            band = 1
                                            sents.append(sent)
                                            defiendum = term
                                            definien = sent
                                            print('6->', defiendum, '-->',
                                                pattern, '--->', sent)
                                        else:
                                            band = 1
                                            sents.append(sent)
                                            defiendum = term
                                            definien = sent
                                            print('6.1->', defiendum, '-->',
                                                pattern, '--->', sent)

                                    k = k+1
                        elif(len(posD) > 3):
                            if('S' in posD[0][0]):
                                pattern = [posD[1][0], posD[2][0], posD[3][0]]
                                # print(pattern)
                                patterns = [
                                    ['N', 'A', 'C']
                                ]
                                if(pattern in patterns):
                                    term = term+' ' + \
                                        ' '.join(tokensD[:len(pattern)])
                                    # print(pattern,'-',term)
                                    band = 1
                                    sents.append(sent)
                                    defiendum = term
                                    definien = sent
                                    print('2.1->', defiendum, '-->',
                                        pattern, '--->', sent)

                        elif(len(tokens) < 3):
                            if(term+' ' in front):
                                tokterm = term.split(' ')
                                lentt = len(tokterm)
                                #print(tokensD, front, tokterm[0])
                                #print(term, tokterm)
                                postt = tokensD.index(tokterm[0])
                                #print(tokensD[postt+lentt:], lemmaD[postt+lentt:])
                                lemmaD2 = lemmaD[postt+lentt:]
                                k = 0
                                readyk = 0
                                while(k < len(lemmaD2) and readyk < 1):
                                    lem = lemmaD2[k]
                                    if(lem in copulas):
                                        readyk = 1
                                        band = 1
                                        sents.append(sent)
                                        # print(term)
                                        defiendum = term
                                        print('7->', defiendum, '-->',
                                            pattern, '--->', sent)
                                    k = k+1
                            # elif()
                            else:
                                k = 0
                                readyk = 0
                                while(k < len(lemmaD) and readyk < 1):
                                    lem = lemmaD[k]
                                    if(lem in copulas):
                                        readyk = 1
                                        # termcomplement=tokens[k+1]
                                        #print(k, tokensD[k:], posD[k:])
                                        if('CS' in posD):
                                            band = 1
                                            ind = posD.index('CS')
                                            termcomplement = ' '.join(
                                                tokensD[k+1:k+ind])
                                            defiendum = term
                                            sents.append(sent)
                                            print(
                                                '5->', defiendum, '-', termcomplement, '-->', pattern, '--->', sent)
                                    k = k+1

                else:
                    #print('3-',term)

                    pos = sent.index(term)
                    back = sent[:pos].split(' ')
                    back3 = ' '.join(back)

                    resixa = ixa(back3)
                    lemma = resixa[1]
                    pos = resixa[0]
                    tokens = resixa[2]

                    # for i in range(len(lemma)):
                    #print(lemma, pos, tokens)
                    j = 0
                    ready = 0
                    while(j < len(lemma) and ready < 1):
                        lem = lemma[j]
                        if(lem in copulas and len(pos) > 1):
                            pattern = tokens[i-1:i+1]
                            if('D' in pos[1][0]):
                                ready = 1
                                pattern = tokens[i-1:i+2]
                                band = 1
                                sents.append(sent)
                                defiendum = ' '.join(tokens[j+2:])+' '+term
                                definien = sent
                                print('3->', defiendum, '-->',
                                      pattern, '--->', sent)
                        j = j+1

            i = i+1

    for s in range(len(sizes)):
        if(len(sizes[s]) > 0):
            max_item = max(sizes[s], key=int)
            ind = sizes[s].index(max_item)
            #print(term, '-->',pattern,'--->', sent.strip() )
            filewithterms.write(words[s][ind] + '\n')

            # print(w)
file = open('estatuto_es.txt', 'r', encoding='utf-8')
document = file.read()

filet = open('definiciones.txt', 'r', encoding='utf-8')
terms = filet.readlines()
withterms(document, terms)
#ixa('ella como patatas')
