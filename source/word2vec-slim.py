# allow plural words which have a singular form in the dicts (use stem logic)

from gensim.models import word2vec
import time
import numpy as np
import gzip
import os

model_folder = 'd:/data'
model_filename = 'GoogleNews-vectors-negative300.bin.gz'
slim_filename = 'GoogleNews-vectors-negative300-SLIM.bin.gz'

max_suffix_len = 2
min_base_len = 8

words = set()
for dict_filename in os.listdir('dicts'):
    with gzip.open('dicts/'+dict_filename, 'rt', encoding='utf8') as f:
        temp = f.readlines()
        save_len = len(temp)
        for i in range(len(temp)):
            temp[i] = temp[i].strip().lower()
        temp = set(temp)
        print('%s: %d -> %d' % (dict_filename, save_len, len(temp)))
    words |= temp
print('combined: %d' % (len(words)))

start = time.time()
model = word2vec.Word2Vec.load_word2vec_format(model_folder + '/' + model_filename, binary=True)
print('Finished loading original model %.2f min' % ((time.time()-start)/60))
print('word2vec: %d' % len(model.vocab))
print('non-phrases: %d' % len([w for w in model.vocab.keys() if '_' not in w]))

indices_to_delete = []
j = 0
suffix_grace_words = 0
for i,w in enumerate(model.index2word):
    l = w.strip().lower()
    found = False
    if l in words:
        found = True
    else:
        for s in range(1, 1+max_suffix_len):
            if len(l)-s<min_base_len:
                break
            elif l[:-s] in words:
                suffix_grace_words += 1
                found = True
                break

    if found:
        model.vocab[w].index = j
        j += 1
    else:
        del model.vocab[w]
        indices_to_delete.append(i)

model.syn0 = np.delete(model.syn0, indices_to_delete, axis=0)
print('slim: %d' % len(model.vocab))
print('suffix grace words: %d' % (suffix_grace_words))

model.save_word2vec_format(model_folder + '/' + slim_filename, binary=True)
del model

start = time.time()
model = word2vec.Word2Vec.load_word2vec_format(model_folder + '/' + slim_filename, binary=True)
print('Finished loading slim model %.1f sec' % ((time.time()-start)))
