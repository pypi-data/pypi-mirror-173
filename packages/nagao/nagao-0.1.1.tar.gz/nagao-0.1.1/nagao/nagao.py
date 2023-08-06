# -*- coding:utf-8 -*-
from . import utils
from collections import defaultdict
from math import sqrt
from nltk.tokenize import word_tokenize
from sqlite_utils import Database
import ext_sort as es
import gc
import logging
import math
import os
import re
import sqlite_utils
import sys
import time


logging.getLogger('ext_sort').setLevel(logging.ERROR)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('nagao')

sqlite_utils.db.SQLITE_MAX_VARS = sys.maxsize
base_dir = os.path.dirname(os.path.abspath(__file__))


class Nagao:
    def __init__(self,
                 lang='zh',
                 min_ngram=3,
                 max_ngram=8,
                 min_freq=10,
                 min_lrc=5,
                 min_lre=0.5,
                 min_pmi=1e-6,
                 min_eta=0.6,
                 threshold=0.01,
                 stopwords=None,
                 punctuations=None,
                 lower=True,
                 use_db=True,
                 use_disk=True,
                 clean=False,
                 verbose=False,
                 db_filename='temp.db',
                 temp_filename='temp.txt',
                 sorted_temp_filename='sorted_temp.txt',
                 ):
        """

        Counting word frequency based on Nagao algorithm

        Keyword Arguments:
            lang {str} -- Corpus language (default: {'zh'})
            min_ngram {number} -- Minimum n-gram size (default: {3})
            max_ngram {number} -- Maximum n-gram size (default: {8})
            min_freq {number} -- Minimum frequency of word (default: {10})
            min_lrc {number} -- Minimum count between left and right neighbor (default: {5})
            min_lre {number} -- Minimum entropy between left and right neighbor (default: {0.5})
            min_pmi {number} -- Minimum pmi(pointwise mutual information) (default: {1e-6})
            min_eta {number} -- Minimum balanced value for left and right neighbor count (default: {0.6})
            threshold {number} -- Minimum word probability (default: {0.01})
            stopwords {iterator/str} -- Stopword list or file path (default: {None})
            punctuations {iterator/str} -- Punctuation list or file path (default: {None})
            lower {bool} -- Lower case the string (default: {True})
            use_db {bool} -- Using database to cache word statistics (default: {True})
            use_disk {bool} -- Using disk to cache pointer table (default: {True})
            clean {bool} -- If clean equals True, temp file will be cleaned at the end of the program (default: {False})
            verbose {bool} -- If use verbose equals True, logs will be displayed on the terminal (default: {False})
            db_filename {str} -- SQLite3 Database file (default: {'temp.db'})
            temp_filename {str} -- temp file name (default: {'temp.txt'})
            sorted_temp_filename {str} -- sorted temp file name (default: {'sorted_temp.txt'})
        """

        self.lang = lang
        self.min_ngram = min_ngram
        self.max_ngram = max_ngram
        self.min_freq = min_freq
        self.min_lrc = min_lrc
        self.min_lre = min_lre
        self.min_pmi = min_pmi
        self.min_eta = min_eta  # 2ab/(a^2+b^2)
        self.threshold = threshold
        self.lower = lower
        self.use_db = use_db
        self.use_disk = use_disk
        self.clean = clean
        self.verbose = verbose
        self.db_filename = db_filename
        self.temp_filename = temp_filename
        self.sorted_temp_filename = sorted_temp_filename

        if self.verbose is True:
            logger.setLevel(logging.INFO)

        if punctuations is None:
            self.punct_set = set(w.rstrip() for w in open(os.path.join(base_dir, 'data/punct.txt'), 'r', encoding='utf-8'))
        elif isinstance(punctuations, str):
            self.punct_set = set(w.rstrip() for w in open(os.path.join(base_dir, punctuations), 'r', encoding='utf-8'))
        elif isinstance(stopwords, list):
            self.punct_set = set(punctuations)
        if stopwords is None:
            self.punct_set.update([w.rstrip() for w in open(os.path.join(base_dir, 'data/stopwords_%s.txt' % self.lang), 'r', encoding='utf-8')])
        elif isinstance(stopwords, str):
            self.punct_set.update([w.rstrip() for w in open(os.path.join(base_dir, stopwords), 'r', encoding='utf-8')])
        elif isinstance(stopwords, list):
            self.punct_set.update(stopwords)
        self.punct_set.add(' ')
        self.punct_set.add('\t')
        self.punct_set.remove('\'')
        self.punct_set.remove('-')

        self.statistics = dict()
        self.alnum_dict = defaultdict(int)

        self.keys = ['count', 'size', 'lcount', 'rcount', 'lentropy', 'rentropy', 'pmi', 'eta_mean', 'threshold']
        self.key2idx = {k: i for i, k in enumerate(self.keys)}
        self.db = Database(self.db_filename, recreate=True)
        self.table = self.db['statistics']
        self.table.create({
            'word': str,
            'size': int,
            'count': int,
            'lcount': int,
            'rcount': int,
            'lentropy': float,
            'rentropy': float,
            },
            pk='word',
            defaults={'lcount': 0, 'rcount': 0, 'lentropy': 0, 'rentropy': 0}
        )
        self.table.create_index(['word'])

    def count_word_freq(self, ptable, ltable, min_ngram, max_ngram, reverse=False, use_disk=True, use_db=True, batch_size=1e6):
        temp = []
        if use_disk is True:
            self.sorted_temp_file = open(self.sorted_temp_filename, 'r', encoding='utf-8')
        size = len(ltable) + 1
        for i in range(min_ngram, max_ngram):
            j = 0
            if use_disk is True:
                self.sorted_temp_file.seek(0)
                line = self.sorted_temp_file.readline().rstrip('\n')
                if self.lang == 'en':
                    line = line.split()
                while j < size and len(line) < i:
                    line = self.sorted_temp_file.readline().rstrip('\n')
                    if self.lang == 'en':
                        line = line.split()
                    j += 1
            else:
                line = ptable[j]
                if self.lang == 'en':
                    line = line.split()
                while j < size and len(line) < i:
                    line = ptable[j]
                    if self.lang == 'en':
                        line = line.split()
                    j += 1

            if j == size:
                continue
            word = line[:i]
            if reverse is True:
                word = word[::-1]
            count = 1
            if len(line) == i:
                variety = 0
                neighbor = 0
                neighbors = []
            else:
                variety = 1
                neighbor = 1
                neighbors = []
            for k in range(j, len(ltable)):
                if use_disk is True:
                    line = self.sorted_temp_file.readline().rstrip('\n')
                else:
                    line = ptable[k+1]
                if self.lang == 'en':
                    line = line.split()
                if ltable[k] >= i:
                    count += 1
                    if ltable[k] == i:  # deduplicate
                        if len(line) <= i:  # no prefix or suffix
                            continue
                        if neighbor > 0:
                            neighbors.append(neighbor)
                        neighbor = 1

                        variety += 1
                    else:
                        neighbor += 1
                else:
                    if len(word) == i:
                        if neighbor > 0:
                            neighbors.append(neighbor)
                        entropy = 0
                        if len(neighbors) > 0:
                            s = sum(neighbors)
                            for x in neighbors:
                                p = x / s
                                entropy += -p * math.log(p) / math.log(math.e, 2)
                        entropy = round(entropy, 3)

                        if reverse is False:
                            variety_key = 'rcount'
                            entropy_key = 'rentropy'
                        else:
                            variety_key = 'lcount'
                            entropy_key = 'lentropy'

                        if self.lang == 'en':
                            word = ' '.join(word)

                        if use_db is False:
                            self.statistics.setdefault(word, [0] * len(self.keys))
                            self.statistics[word][self.key2idx['count']] = count
                            self.statistics[word][self.key2idx['size']] = i
                            self.statistics[word][self.key2idx[variety_key]] = variety
                            self.statistics[word][self.key2idx[entropy_key]] = entropy
                        else:
                            if reverse is True:
                                row = {'word': word, variety_key: variety, entropy_key: entropy}
                            else:
                                row = {'word': word, 'count': count, 'size': i, variety_key: variety, entropy_key: entropy}
                            temp.append(row)
                            if len(temp) % batch_size == 0:
                                ts = time.time()
                                self.table.upsert_all(temp, pk='word', batch_size=int(batch_size))
                                logger.debug('insert spend: %s' % (time.time() - ts))
                                temp.clear()
                    count = 1
                    if len(line) == i:
                        variety = 0
                        neighbor = 0
                        neighbors = []
                    else:
                        variety = 1
                        neighbor = 1
                        neighbors = []
                    word = line[:i]
                    if reverse is True:
                        word = word[::-1]
            if len(word) == i:  # count remaining strings in ptable
                if neighbor > 0:
                    neighbors.append(neighbor)
                entropy = 0
                if len(neighbors) > 0:
                    s = sum(neighbors)
                    for x in neighbors:
                        p = x / s
                        entropy += -p * math.log(p) / math.log(math.e, 2)
                entropy = round(entropy, 3)

                if reverse is False:
                    variety_key = 'rcount'
                    entropy_key = 'rentropy'
                else:
                    variety_key = 'lcount'
                    entropy_key = 'lentropy'

                if self.lang == 'en':
                    word = ' '.join(word)

                if use_db is False:
                    self.statistics.setdefault(word, [0] * len(self.keys))
                    self.statistics[word][self.key2idx['count']] = count
                    self.statistics[word][self.key2idx['size']] = i
                    self.statistics[word][self.key2idx[variety_key]] = variety
                    self.statistics[word][self.key2idx[entropy_key]] = entropy
                else:
                    if reverse is True:
                        row = {'word': word, variety_key: variety, entropy_key: entropy}
                    else:
                        row = {'word': word, 'count': count, 'size': i, variety_key: variety, entropy_key: entropy}
                    temp.append(row)
                    if len(temp) % batch_size == 0:
                        self.table.upsert_all(temp, pk='word', batch_size=int(batch_size))
                        temp.clear()
        if use_disk is True and len(temp) > 0:
            self.table.upsert_all(temp, pk='word', batch_size=int(batch_size))
            temp.clear()
            self.sorted_temp_file.close()

    def generate_semiinfinite_string(self, line, ptable, use_disk=True, save_every=1e4):
        for i in range(0, len(line)):
            word = line[i:]
            if not word:
                continue
            if self.lang == 'en':
                word = ' '.join(word)
            ptable.append(word)
            if use_disk and len(ptable) % save_every == 0:
                item = '\n'.join(ptable) + '\n'
                self.temp_file.write(item.encode('utf-8'))
                ptable.clear()

    def split_line(self, line, ptable, alnum_dict, reverse, use_disk):
        p = 0
        for i in range(0, len(line)):
            if line[i] in self.punct_set or re.search('[^\u4E00-\u9FA5a-zA-Z0-9]', line[i]):
                strng = line[p:i]
                self.generate_semiinfinite_string(strng, ptable, use_disk)
                p = i+1
        if p < len(line):
            strng = line[p:]
            self.generate_semiinfinite_string(strng, ptable, use_disk)

    def read_corpus(self, filename, ptable, reverse=False, use_disk=True):
        if self.use_disk is True:
            self.temp_file = open(self.temp_filename, 'wb')
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            for i, line in enumerate(file):
                line = line.rstrip()
                if not line:
                    continue
                line = line.replace('\r\n', '').replace('\n', '')
                line = utils.remove_html(line)
                if self.lower is True:
                    line = line.lower()
                if self.lang == 'en':
                    line = word_tokenize(line)
                if reverse:
                    line = line[::-1]
                self.split_line(line, ptable, self.alnum_dict, reverse, use_disk)

        if use_disk is True:
            item = '\n'.join(ptable) + '\n'
            self.temp_file.write(item.encode('utf-8'))
            ptable.clear()
            self.temp_file.close()

    def make_ptable(self, filename, reverse=False, use_disk=True):
        ptable = list()
        self.read_corpus(filename, ptable, reverse=reverse, use_disk=use_disk)
        if use_disk is False:
            ptable = list(sorted(ptable))
        else:
            self.temp_file = open(self.temp_filename, 'rb')
            self.sorted_temp_file = open(self.sorted_temp_filename, 'wb')
            es.sort(
                reader=self.temp_file,
                writer=self.sorted_temp_file,
                chunk_size=1_000_000,
                workers_cnt=4,
            )
            self.temp_file.close()
            self.sorted_temp_file.close()
        return ptable

    def get_common_prefix_length(self, str1, str2):
        if self.lang == 'en':
            str1 = str1.split()
            str2 = str2.split()
        i = 0
        while i < len(str1) and i < len(str2):
            if(str1[i] == str2[i]):
                i = i+1
            else:
                return i
        return i

    def make_ltable(self, ptable, use_disk=True):
        if use_disk is False:
            ltable = []
            for i in range(0, len(ptable)-1):
                ltable.append(self.get_common_prefix_length(ptable[i], ptable[i+1]))
            return ltable
        else:
            self.sorted_temp_file = open(self.sorted_temp_filename, 'r', encoding='utf-8')
            ltable = []
            last_line = self.sorted_temp_file.readline()
            for line in self.sorted_temp_file:
                ltable.append(self.get_common_prefix_length(last_line.rstrip('\n'), line.rstrip('\n')))
                last_line = line
            self.sorted_temp_file.close()
            return ltable

    def calc_eta_mean(self, a, b):
        if a == 0 and b == 0:
            return 0
        else:
            return 2.0 * a * b / (a*a + b*b)

    def calc_threshold_mean(self, f, r, l, p):
        if l == 0 or r == 0:
            return 0
        return sqrt(f)/(1.0/r + 1.0/l) * p

    def iterrows(self, use_disk=True):
        ts = time.time()
        if use_disk is True:
            rows = self.table.pks_and_rows_where()
            self.key2idx = {k: k for k, v in self.key2idx.items()}
        else:
            rows = self.statistics.items()
        for word, word_dict in rows:
            if self.lang == 'en':
                word = word.split()
            word_eta_mean = self.calc_eta_mean(word_dict[self.key2idx['lcount']], word_dict[self.key2idx['rcount']])
            if word_dict[self.key2idx['size']] < self.min_ngram or word_dict[self.key2idx['count']] < self.min_freq or \
                min(word_dict[self.key2idx['lentropy']], word_dict[self.key2idx['rentropy']]) < self.min_lre or \
                min(word_dict[self.key2idx['lcount']], word_dict[self.key2idx['rcount']]) < self.min_lrc or word_eta_mean < self.min_eta:
                continue
            tmp_mi = 0
            min_pmi = 999

            if use_disk is True:
                words = []
                self.statistics.clear()
                for j in range(1, word_dict[self.key2idx['size']]):
                    part1 = word[:j]
                    part2 = word[j:]
                    if self.lang == 'en':
                        part1 = ' '.join(part1)
                        part2 = ' '.join(part2)
                    words.extend([part1, part2])
                for row in self.table.rows_where('word in %s' % str(tuple(words))):
                    self.statistics[row['word']] = row

            for j in range(1, word_dict[self.key2idx['size']]):
                part1 = word[:j]
                part2 = word[j:]
                if self.lang == 'en':
                    part1 = ' '.join(part1)
                    part2 = ' '.join(part2)
                tmp_mi = word_dict[self.key2idx['count']]/(self.statistics[part1]
                         [self.key2idx['count']]*self.statistics[part2][self.key2idx['count']])
                if min_pmi > tmp_mi:
                    min_pmi = tmp_mi
            word_threshold = self.calc_threshold_mean(
                word_dict[self.key2idx['count']], word_dict[self.key2idx['rcount']], word_dict[self.key2idx['lcount']], min_pmi)
            if self.lang == 'en':
                word = ' '.join(word)
            if min_pmi < self.min_pmi or word_threshold < self.threshold:
                continue
            yield word, word_dict[self.key2idx['count']], word_dict[self.key2idx['lcount']], word_dict[self.key2idx['rcount']], word_dict[self.key2idx['lentropy']], word_dict[self.key2idx['rentropy']], min_pmi, word_eta_mean, word_threshold
        logger.debug('spend: %s' % (time.time() - ts))

    def process(self, filename):
        logger.info('First stage(1.1): making ptable and ltable')
        ptable = self.make_ptable(filename, reverse=False, use_disk=self.use_disk)
        ltable = self.make_ltable(ptable, use_disk=self.use_disk)
        logger.info('Second stage(2.1): counting word frequency')
        ts = time.time()
        self.count_word_freq(ptable, ltable, 1, self.max_ngram, reverse=False, use_disk=self.use_disk, use_db=self.use_db)
        logger.debug('spend: %s' % (time.time() - ts))
        del ptable, ltable
        gc.collect()

        logger.info('First stage(1.2): making reversed ptable and ltable')
        ptable = self.make_ptable(filename, reverse=True, use_disk=self.use_disk)
        ltable = self.make_ltable(ptable, use_disk=self.use_disk)
        logger.info('Second stage(2.2): counting reversed word frequency')
        ts = time.time()
        self.count_word_freq(ptable, ltable, 1, self.max_ngram, reverse=True, use_disk=self.use_disk, use_db=self.use_db)
        logger.debug('spend: %s' % (time.time() - ts))
        del ptable, ltable
        gc.collect()
        logger.info('Third stage(3.): writing result')

    def save(self, filename='vocab.tsv', sep='\t', header=True):
        with open(filename, 'w', encoding='utf-8') as f:
            if header is True:
                f.write(sep.join(['word', 'count', 'left-count', 'right-count', 'left-entropy', 'right-entropy', 'pmi', 'eta-mean', 'threshold']) + '\n')
            for word, freq, l, r, l_e, r_e, pmi, eta, thres in self.iterrows(use_disk=self.use_disk):
                line = sep.join(str(x) for x in [word, freq, l, r, l_e, r_e, pmi, eta, thres]) + '\n'
                f.write(line)
        if self.clean is True:
            if os.path.exists(self.temp_filename):
                os.remove(self.temp_filename)
            if os.path.exists(self.sorted_temp_filename):
                os.remove(self.sorted_temp_filename)
            if os.path.exists(self.db_filename):
                os.remove(self.db_filename)
