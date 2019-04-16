# -*- coding: utf-8 -*-
"""
Код для построения модели лемматизации
"""

from __future__ import division
from __future__ import print_function

import os
import pickle
import logging
import pathlib
import gzip
import io


def decode_pos(pos):
    if pos in [u'ДЕЕПРИЧАСТИЕ', u'ГЛАГОЛ', u'ИНФИНИТИВ']:
        return u'ГЛАГОЛ'
    else:
        return pos


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

    data_folder = '../data'
    tmp_folder = '../tmp'

    gren_path = os.path.join(data_folder, 'word2lemma.dat')
    thesaurus_path = os.path.join(data_folder, 'links.csv')
    output_path = os.path.join(tmp_folder, 'rulemma.dat')

    logging.info(u'Loading thesaurus from "{}"'.format(thesaurus_path))
    part2inf = dict()
    with io.open(thesaurus_path, 'r', encoding='utf-8') as rdr:
        for line in rdr:
            tx = line.strip().split('|')
            if len(tx) == 5:
                word1 = tx[0].replace(u' - ', u'-').lower()
                pos1 = tx[1]
                word2 = tx[2].replace(u' - ', u'-').lower()
                pos2 = tx[3]
                relat = tx[4]

                if pos1 == u'ДЕЕПРИЧАСТИЕ' and pos2 == u'ИНФИНИТИВ':
                    part2inf[word1] = word2

    logging.info(u'Loading lexicon from {}'.format(gren_path))
    forms = dict()
    forms2 = dict()
    with open(gren_path, 'rb') as rdr:
        for line in rdr:
            tx = line.strip().decode('utf8').split('\t')
            if len(tx) == 3:
                form = tx[0].replace(u' - ', u'-').lower()
                lemma = tx[1].replace(u' - ', u'-').lower()
                if tx[2] == u'ДЕЕПРИЧАСТИЕ' and form in part2inf:
                    # Для деепричастий в качестве леммы используем инфинитив соответствующего глагола
                    lemma = part2inf[form]

                pos = decode_pos(tx[2])

                if form not in forms:
                    forms[form] = lemma
                else:
                    if forms[form] != lemma:
                        if form not in forms2:
                            lemma_data = (lemma, pos)
                            forms2[form] = [lemma_data]
                        elif lemma_data not in forms2[form]:
                            forms2[form].append(lemma_data)

    special_lemmas = {u'мы': u'я',
                      u'вы': u'ты',
                      u'она': u'он',
                      u'оно': u'он',
                      u'оно': u'оно',
                      u'они': u'они'}

    logging.info('Lexicon loaded')
    with gzip.open(output_path, 'wb') as f:
        pickle.dump((forms, forms2, special_lemmas), f)
