import click
from .nagao import Nagao


@click.command()
@click.option('-c', '--corpus', help='Corpus file path.')
@click.option('-o', '--output', default='vocab.tsv', help='Output file path.')
@click.option('-l', '--lang', default='en', help='Corpus language.')
@click.option('-minn', '--min_ngram', default=2, help='Minimum n-gram size.')
@click.option('-maxn', '--max_ngram', default=6, help='Max n-gram size.')
@click.option('--min_freq', default=10, help='Minimum frequency of word.')
@click.option('--min_lrc', default=5, help='Minimum count between left and right neighbor.')
@click.option('--min_lre', default=0.5, help='Minimum entropy between left and right neighbor.')
@click.option('--min_pmi', default=1e-6, help='Minimum pmi(pointwise mutual information).')
@click.option('--min_eta', default=0.6, help='Minimum balanced value for left and right neighbor count.')
@click.option('--threshold', default=0.01, help='Minimum word probability.')
@click.option('--stopwords', default=None, help='Stopword file path.')
@click.option('--punctuations', default=None, help='Punctuation file path.')
@click.option('--lower', is_flag=True, help='If use lower option, keep lowered dictionary.')
@click.option('--clean', is_flag=True, help='If use clean option, the cache file will be cleaned at the end of the program.')
@click.option('--verbose', is_flag=True, help='If use verbose option, logs will be displayed on the terminal.')
def nagao(corpus, output, lang, min_ngram, max_ngram, min_freq, min_lrc,
          min_lre, min_pmi, min_eta, threshold, stopwords, punctuations, lower, clean, verbose):

    nagao = Nagao(lang=lang,
                  min_ngram=min_ngram,
                  max_ngram=max_ngram,
                  min_freq=min_freq,
                  min_lrc=min_lrc,
                  min_lre=min_lre,
                  min_pmi=min_pmi,
                  min_eta=min_eta,
                  threshold=threshold,
                  stopwords=stopwords,
                  punctuations=punctuations,
                  lower=lower,
                  clean=clean,
                  verbose=verbose
                  )
    nagao.process(corpus)
    nagao.save(output)


if __name__ == '__main__':
    nagao()
