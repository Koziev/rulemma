# -*- coding: utf-8 -*-
"""
Лемматизатор для R&D прототипирования NLP задач в Питоне
"""

from __future__ import division
from __future__ import print_function

import os
import pickle
import pathlib
import gzip


def decode_pos(pos):
    if pos in [u'ДЕЕПРИЧАСТИЕ', u'ГЛАГОЛ', u'ИНФИНИТИВ']:
        return u'ГЛАГОЛ'
    else:
        return pos


class Lemmatizer(object):
    def __init__(self):
        pass

    def load(self, dict_path=None):
        """ Загружаем модель лемматизации, созданную отдельным скриптом builder.py """
        dict_filename = 'rulemma.dat'
        if dict_path is None:
            module_folder = str(pathlib.Path(__file__).resolve().parent)
            p = os.path.join(module_folder, '../tmp', dict_filename)
            if not os.path.exists(p):
                p = os.path.join(module_folder, dict_filename)
        else:
            p = dict_path

        with gzip.open(p, 'r') as f:
            self.forms, self.forms2, self.special_lemmas, self.key2transducer = pickle.load(f)

    def get_lemma(self, word):
        if word in self.forms:
            return self.forms[word]
        elif word in self.forms2:
            return self.forms2[word][0]
        elif word in self.special_lemmas:
            return self.special_lemmas[word]
        else:
            return word

    def decode_pos_tags(self, pos_tags):
        stags1 = []
        part_of_speech = u'unk'
        short_tag_index = -1
        for tag in pos_tags.split('|'):
            if tag == 'NOUN':
                part_of_speech = u'СУЩЕСТВИТЕЛЬНОЕ'
            elif tag == 'VERB':
                part_of_speech = u'ГЛАГОЛ'
            elif tag == 'ADJ':
                part_of_speech = u'ПРИЛАГАТЕЛЬНОЕ'
                stags1.append((u'КРАТКИЙ', u'0'))
                short_tag_index = 0
            elif tag == 'ADV':
                part_of_speech = u'НАРЕЧИЕ'
            elif tag == 'PRON':
                part_of_speech = u'МЕСТОИМЕНИЕ'
            elif tag == 'ADP':
                part_of_speech = u'ПРЕДЛОГ'
            elif '=' in tag:
                if part_of_speech == u'СУЩЕСТВИТЕЛЬНОЕ':
                    if tag == u'Case=Nom':
                        stags1.append((u'ПАДЕЖ', u'ИМ'))
                    elif tag == u'Case=Acc':
                        stags1.append((u'ПАДЕЖ', u'ВИН'))
                    elif tag == u'Case=Dat':
                        stags1.append((u'ПАДЕЖ', u'ДАТ'))
                    elif tag == u'Case=Ins':
                        stags1.append((u'ПАДЕЖ', u'ТВОР'))
                    elif tag == u'Case=Prep':
                        stags1.append((u'ПАДЕЖ', u'ПРЕДЛ'))
                    elif tag == u'Case=Loc':
                        stags1.append((u'ПАДЕЖ', u'МЕСТ'))
                    elif tag == u'Case=Gen':
                        stags1.append((u'ПАДЕЖ', u'РОД'))
                    elif tag == u'Case=Voc':
                        stags1.append((u'ПАДЕЖ', u'ЗВАТ'))
                    elif tag == u'Number=Sing':
                        stags1.append((u'ЧИСЛО', u'ЕД'))
                    elif tag == u'Number=Plur':
                        stags1.append((u'ЧИСЛО', u'МН'))
                    elif tag == u'Gender=Masc':
                        stags1.append((u'РОД', u'МУЖ'))
                    elif tag == u'Gender=Fem':
                        stags1.append((u'РОД', u'ЖЕН'))
                    elif tag == u'Gender=Neut':
                        stags1.append((u'РОД', u'СР'))
                    else:
                        print(u'неизвестный тэг "{}"'.format(tag))
                        raise NotImplementedError()
                elif part_of_speech == u'ПРИЛАГАТЕЛЬНОЕ':
                    if tag == u'Case=Nom':
                        stags1.append((u'ПАДЕЖ', u'ИМ'))
                    elif tag == u'Case=Acc':
                        stags1.append((u'ПАДЕЖ', u'ВИН'))
                    elif tag == u'Case=Dat':
                        stags1.append((u'ПАДЕЖ', u'ДАТ'))
                    elif tag == u'Case=Ins':
                        stags1.append((u'ПАДЕЖ', u'ТВОР'))
                    elif tag == u'Case=Prep':
                        stags1.append((u'ПАДЕЖ', u'ПРЕДЛ'))
                    elif tag == u'Case=Loc':
                        stags1.append((u'ПАДЕЖ', u'МЕСТ'))
                    elif tag == u'Case=Gen':
                        stags1.append((u'ПАДЕЖ', u'РОД'))
                    elif tag == u'Number=Sing':
                        stags1.append((u'ЧИСЛО', u'ЕД'))
                    elif tag == u'Number=Plur':
                        stags1.append((u'ЧИСЛО', u'МН'))
                    elif tag == u'Gender=Masc':
                        stags1.append((u'РОД', u'МУЖ'))
                    elif tag == u'Gender=Fem':
                        stags1.append((u'РОД', u'ЖЕН'))
                    elif tag == u'Gender=Neut':
                        stags1.append((u'РОД', u'СР'))
                    elif tag == u'Degree=Cmp':
                        stags1.append((u'СТЕПЕНЬ', u'СРАВН'))
                    elif tag == u'Degree=Pos':
                        stags1.append((u'СТЕПЕНЬ', u'АТРИБ'))
                    elif tag == u'Variant=Short':
                        stags1[short_tag_index] = (u'КРАТКИЙ', u'1')
                    else:
                        print(u'неизвестный тэг "{}"'.format(tag))
                        raise NotImplementedError()
                elif part_of_speech == u'ГЛАГОЛ':
                    if tag == u'Number=Sing':
                        stags1.append((u'ЧИСЛО', u'ЕД'))
                    elif tag == u'Number=Plur':
                        stags1.append((u'ЧИСЛО', u'МН'))
                    elif tag == u'Gender=Masc':
                        stags1.append((u'РОД', u'МУЖ'))
                    elif tag == u'Gender=Fem':
                        stags1.append((u'РОД', u'ЖЕН'))
                    elif tag == u'Gender=Neut':
                        stags1.append((u'РОД', u'СР'))
                    elif tag == u'Mood=Ind':
                        stags1.append((u'НАКЛОНЕНИЕ', u'ИЗЪЯВ'))
                    elif tag == u'Mood=Imp':
                        stags1.append((u'НАКЛОНЕНИЕ', u'ПОБУД'))
                    elif tag == u'Tense=Past':
                        stags1.append((u'ВРЕМЯ', u'ПРОШЕДШЕЕ'))
                    elif tag == u'Tense=Notpast':
                        stags1.append((u'ВРЕМЯ', u'НАСТОЯЩЕЕ'))
                    elif tag == u'Tense=Pres':
                        stags1.append((u'ВРЕМЯ', u'НАСТОЯЩЕЕ'))
                    elif tag == u'Person=1':
                        stags1.append((u'ЛИЦО', u'1'))
                    elif tag == u'Person=2':
                        stags1.append((u'ЛИЦО', u'2'))
                    elif tag == u'Person=3':
                        stags1.append((u'ЛИЦО', u'3'))
                    elif tag == u'VerbForm=Fin':
                        pass
                    elif tag == u'VerbForm=Inf':
                        pass
                    elif tag == u'VerbForm=Conv':
                        pass
                    else:
                        msg = u'неизвестный тэг "{}"'.format(tag)
                        raise RuntimeError(msg)
                elif part_of_speech == u'НАРЕЧИЕ':
                    raise NotImplementedError()
                else:
                    pass

        return part_of_speech, stags1

    def get_lemma2(self, word, pos_tags):
        part_of_speech, decoded_tags = self.decode_pos_tags(pos_tags)
        nword = word.lower()
        if nword in self.special_lemmas:
            return self.special_lemmas[nword], part_of_speech, decoded_tags
        elif nword in self.forms:
            lemma = self.forms[nword]
            return lemma, part_of_speech, decoded_tags
        elif nword in self.forms2:
            for lemma, lemma_part_of_speech in self.forms2[nword]:
                if lemma_part_of_speech == part_of_speech:
                    return lemma, part_of_speech, decoded_tags
        elif len(word) > 4:
            # используем модель лемматизации для OV-слов
            ending = word[-4:]
            key = ending + u'|' + part_of_speech
            if key in self.key2transducer:
                transducer = self.key2transducer[key]
                lemma = word[:-transducer[0]] + transducer[1]
                return lemma, part_of_speech, decoded_tags

        # fallback-вариант - возвращаем исходное слово в качестве леммы
        return word, part_of_speech, decoded_tags

    def lemmatize(self, tagged_words):
        """Для результата работы rupostagger'а добавляем часть лемму и извлеченный код части речи"""
        return [(word, tags,)+tuple(self.get_lemma2(word, tags)) for (word, tags) in tagged_words]
