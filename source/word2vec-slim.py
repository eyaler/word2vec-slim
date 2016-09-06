from gensim.models import word2vec
import time
import numpy as np

model_folder = 'd:/data'
model_filename = 'GoogleNews-vectors-negative300.bin.gz'
slim_filename = 'GoogleNews-vectors-negative300-SLIM.bin.gz'
dict_filenames = ['words.txt.gz', 'words2.txt.gz', 'words3.txt.gz']

words = set()
for dict_filename in dict_filenames:
    with open('dicts/'+dict_filename) as f:
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
print('phrases: %d' % len([w for w in model.vocab.keys() if '_' not in w]))

indices_to_delete = []
j = 0
for i,w in enumerate(model.index2word):
    if w.strip().lower() not in words:
        del model.vocab[w]
        indices_to_delete.append(i)
    else:
        model.vocab[w].index = j
        j += 1
model.syn0 = np.delete(model.syn0, indices_to_delete, axis=0)
print('slim: %d' % len(model.vocab))

model.save_word2vec_format(model_folder + '/' + slim_filename, binary=True)
del model

start = time.time()
model = word2vec.Word2Vec.load_word2vec_format(model_folder + '/' + slim_filename, binary=True)
print('Finished loading slim model %.2f min' % ((time.time()-start)/60))
