#GoogleNews-vectors-negative300-SLIM

tl;dr: Filter down Google News word2vec model from 3 million words to 300k, by crossing it with English dictionaries.

In several projects i've been using the [word2vec](https://code.google.com/archive/p/word2vec/) pre-trained Google News model [(GoogleNews-vectors-negative300)](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM)
with the [gensim](https://radimrehurek.com/gensim/) Python library.
The model was trained over a 3 billion word corpus, and contains 3 million words (of which ~930k are NOT phrases, i.e. do not contain underscores).
The compressed file size is 1.6 GB, and it takes over 3 minutes to load in gensim on my laptop.

As many words are less useful for my use cases (e.g. Chinese names), I made a slimmer version which saves on disk space, loading time and memory.

I found several large English word lists at [github.com/dwyl/english-words](https://github.com/dwyl/english-words).
I combined all the words found in the files: words.txt, words2.txt and words3.txt, and converted to lowercase.
This gave a total of 466,920 unique words.

We could use the above to filter word2vec, however we would lose some contemporary words of the zeitgeist, absent from the outdated dictionaries, e.g. "feminazi", "douchebag", "bukkake", "hashtag", "meme", "transgender", "metrosexual", "polyamory", as well as "google" and "facebook".
 
Such words can be found in the [Urban Dictionary](http://www.urbandictionary.com/), and fortunately the complete word list from March 2016 can be found at [github.com/mattbierner/urban-dictionary-entry-collector](https://github.com/mattbierner/urban-dictionary-entry-collector).
It contains ~2 million entries, of which ~1.5 million are lowercase unique (of which ~800k are NOT phrases, i.e. do not contain spaces). 
This is quite noisy, and we can filter it down on `max(thumbs up vote)>=50`, leaving 86,724 spaceless words (of which 55k are not contained in our previous word list, comparing by lowercase).
Combining with the previous word list, we get a total of 521,924 unique words.

I then filtered the Google News words to retain only those which their lowercase version appear in my combined word list.
This leaves 288,751 words (28,534 due to Urban Dictionary).

I was still missing some inflections which are in the word2vec model but which only have their base form in the word list, e.g. 'antisemites' or 'feminazis'. 
This can be dealt with by considering also the base form of long words (`min_base_len = 8`), after truncating a short suffix (`max_suffix_len = 2`).
The above parameter choice added 10,816 words.
 
The final slim model has 299,567 words, saved in a 270 MB compressed word2vec format file, and loads in 20 seconds on my laptop. 

Notes:

1. If you are filtering words by their vocab dictionary index, note that these indices have been updated according to the smaller container size.
2. You can find the filtered down Urban Dictionary word list (sorted by decreasing max up vote) [here](https://github.com/eyaler/word2vec-slim/blob/master/source/dicts/urban50.txt.gz).
3. You will need to install [git lfs](https://git-lfs.github.com/) to be able to clone this.