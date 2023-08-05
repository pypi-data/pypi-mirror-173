import re as re

def le_assinatura(wal, ttr, hlr, sal, sac, pal):
    return [wal, ttr, hlr, sal, sac, pal]



def le_textos(texto):
    i = 1
    textos = []
    while texto:
        textos.append(texto)
        i += 1
    return textos



def separa_sentencas(texto):
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas[-1] == '':
        del sentencas[-1]
    return sentencas



def separa_frases(sentenca):
    return re.split(r'[,:;]+', sentenca)



def separa_palavras(frase):
    return frase.split()



def n_palavras_unicas(lista_palavras):
    freq = dict()
    unicas = 0
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            if freq[p] == 1:
                unicas -= 1
            freq[p] += 1
        else:
            freq[p] = 1
            unicas += 1
    return unicas



def n_palavras_diferentes(lista_palavras):
    freq = dict()
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1
    return len(freq)



def compara_assinatura(as_a, as_b):
    similaridade = 0
    for i in range(0, 6):
        similaridade = similaridade + (abs(as_a[i] - as_b[i]))
    return similaridade / 6



def calcula_assinatura(texto):
    lista_sentencas = separa_sentencas(texto)
    soma_caracteres_sentencas = 0
    lista_frases = []
    soma_caracteres_frases = 0
    lista_palavras = []
    soma_caracteres_palavras = 0

    for sentenca in lista_sentencas:
        soma_caracteres_sentencas = soma_caracteres_sentencas + len(sentenca)
        frases = separa_sentencas(sentenca)

        for f in frases:
            lista_frases.append(f)
          
    for frase in lista_frases:
        soma_caracteres_frases = soma_caracteres_frases + len(frase)
        palavras = separa_palavras(frase)
        
        for palavra in palavras:
            lista_palavras.append(palavra)

    for palavra in lista_palavras:
        soma_caracteres_palavras = soma_caracteres_palavras + len(palavra)
    
    tamanhomedio_palavras = soma_caracteres_palavras / len(lista_palavras) 
    typetoken = n_palavras_diferentes(lista_palavras) / len(lista_palavras)
    hapax = n_palavras_unicas(lista_palavras) / len(lista_palavras)
    tamanhomedio_sentencas = soma_caracteres_sentencas / len(lista_sentencas)
    complexidade_sentenca = len(lista_frases) / len(lista_sentencas)
    tamanhomedio_frases = soma_caracteres_frases / len(lista_frases)

    return[tamanhomedio_palavras, typetoken, hapax, tamanhomedio_sentencas, complexidade_sentenca, tamanhomedio_frases]




def avalia_textos(textos, ass_cp):
    infectado = []

    for texto in textos:
        ass_texto = calcula_assinatura(texto)
        infectado.append(compara_assinatura(ass_texto, ass_cp))

    menor_similaridade = infectado[0]
    n = 1

    for i in range(1, len(infectado)):
        if menor_similaridade > infectado[i]:
            n = i

    return n



def main():
    assinatura_principal = le_assinatura()
    textos = le_textos()
    n = avalia_textos(textos, assinatura_principal)

main()
