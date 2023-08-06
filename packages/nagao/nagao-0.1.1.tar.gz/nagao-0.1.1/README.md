# Nagao
An implementation of the paper: [A new method of n-gram statistics for large number of n and automatic extraction of words and phrases from large text data of Japanese](https://aclanthology.org/C94-1101.pdf)



## Install

Two ways to install Nagao:

**Install Nagao from Pypi:**

```
pip install nagao
```



**Install Nagao from the Github source:**

```
git clone https://github.com/Chiang97912/nagao.git
cd nagao
python setup.py install
```



## Usage

You can use Nagao in Python file:

```python
from nagao import Nagao

nagao = Nagao(lang='en', min_ngram=2, max_ngram=6, min_freq=5, min_lrc=2, min_lre=0.5, min_pmi=0, min_eta=0, threshold=0,\
              use_disk=True, use_db=True, lower=True, clean=True, verbose=True)
ts = time.time()
nagao.process('path/to/corpus/file')
nagao.save('path/to/output/file')
print('total spend:', time.time() - ts)

```

From the command line, you can run:

```shell
nagao -c "path/to/corpus/file" -o "path/to/output/file" -l zh --clean --verbose
```

You can use `nagao --help` to find the usage of nagao cli:

```
Options:
  -c, --corpus TEXT           Corpus file path.
  -o, --output TEXT           Output file path.
  -l, --lang TEXT             Corpus language.
  -minn, --min_ngram INTEGER  Minimum n-gram size.
  -maxn, --max_ngram INTEGER  Max n-gram size.
  --min_freq INTEGER          Minimum frequency of word.
  --min_lrc INTEGER           Minimum count between left and right neighbor.
  --min_lre FLOAT             Minimum entropy between left and right neighbor.
  --min_pmi FLOAT             Minimum pmi(pointwise mutual information).
  --min_eta FLOAT             Minimum balanced value for left and right
                              neighbor count.

  --threshold FLOAT           Minimum word probability.
  --stopwords TEXT            Stopword file path.
  --punctuations TEXT         Punctuation file path.
  --lower                     If use lower option, keep lowered dictionary.
  --clean                     If use clean option, the cache file will be
                              cleaned at the end of the program.
  --verbose                   If use verbose option, logs will be displayed on
                              the terminal.

  --help                      Show this message and exit.
```



## Dependencies

* `Python` version 3.6

* `nltk`  version 3.5



## References

* [@newword-py](https://github.com/atesop/newword-py)

