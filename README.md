#GoogleNews-vectors-negative300-SLIM

In several projects i've been using the [word2vec](https://code.google.com/archive/p/word2vec/) pre-trained Google News model [(GoogleNews-vectors-negative300)](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM)
with the [gensim](https://radimrehurek.com/gensim/) Python library. The model was trained over a 3 billion word corpus, and contains 3 million words (of which ~930k are phrases). The compressed file size is 1.6 GB, and it takes over 3 minutes to load in gensim on my laptop.

As many words are less useful for my use cases (e.g. Chinese names), I made a slimmer version which saves on disk space, loading time and memory.

I found several large English word lists at [github.com/dwyl/english-words](https://github.com/dwyl/english-words). I combined all the words found in the files: words.txt, words2.txt and words3.txt, and converted to lowercase.
This gave a total of 466,920 unique words. I then filtered the Google News words to retain only those which their lowercase version appear in my word list.
This leaves 260,217 words, saved to a 235 MB compressed word2vec format file, which loads in 0.3 minutes on my laptop.

Notes:
1. If you are filtering words by their vocab dictionary index, note that these indices have been updated according to the smaller container size.
2. You do lose the word "feminazi" and its inflictions.
3. You will need to install [git lfs](https://git-lfs.github.com/) to be able to clone this.