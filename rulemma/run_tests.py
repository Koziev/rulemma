import operator
import rutokenizer
import rupostagger

import rulemma

if __name__ == '__main__':
    print('Loading dictionaries and models...')
    lemmatizer = rulemma.Lemmatizer()
    lemmatizer.load('../tmp/rulemma.dat')

    tokenizer = rutokenizer.Tokenizer()
    tokenizer.load()

    tagger = rupostagger.RuPosTagger()
    tagger.load()
    print('Loading finished')


    #sent = u'во сне я мимо школы проходил'
    #tokens = tokenizer.tokenize(sent)
    #tags = tagger.tag(tokens)
    #lemmas = lemmatizer.lemmatize(tags)
    #for word, tags, lemma, *_ in lemmas:
    #    print(u'{:15}\t{:15}\t{}'.format(word, lemma, tags))

    sent = u'Мяукая, голодные кошки ловят жирненьких хрюнделей'
    tokens = tokenizer.tokenize(sent)
    tags = tagger.tag(tokens)
    lemmas = lemmatizer.lemmatize(tags)
    for word, tags, lemma, *_ in lemmas:
        print(u'{:15}\t{:15}\t{}'.format(word, lemma, tags))

    tests = [(u'во сне я мимо школы проходил', u'в сон я мимо школа проходить'),
             (u'рой яму', u'рыть яма'),
             (u'мой окна', u'мыть окно'),
             (u'я тебя вижу', u'я ты видеть'),
             (u'я вижу хрюнделя', u'я видеть хрюндель'),
             (u'ты смотрел на хрюнделей', u'ты смотреть на хрюндель'),
             (u'Мяукая, голодные кошки ловят жирненьких мышек', u'мяукать , голодный кошка ловить жирненький мышка'),
             (u'Мы спрашивали про уроки и оценки', u'мы спрашивать про урок и оценка'),
             (u'Куда же улетели облачка?', u'куда же улететь облачко ?')
    ]

    print('Start testing...')
    for sent, required_lemmas in tests:
        tokens = tokenizer.tokenize(sent)
        tags = tagger.tag(tokens)
        lemmas = lemmatizer.lemmatize(tags)
        predicted_lemmas = u' '.join(map(operator.itemgetter(2), lemmas))
        if predicted_lemmas != required_lemmas:
            print(u'Test failed for "{}": required_lemmas="{}", predicted_lemmas="{}"'.format(sent, required_lemmas, predicted_lemmas))
    print('All tests OK.')
