from collections import Counter
import itertools

import numpy as np
from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords

def main(args):
    kiwi = Kiwi(num_workers=12, typos='basic')
    kiwi.load_user_dictionary('user_words.txt')
    stopwords = Stopwords('stopwords.txt')
    stopwords = None
    for i in args.inputs:
        for tokens in kiwi.tokenize(open(i, encoding='utf-8'), stopwords=stopwords, normalize_coda=True):
            print(*(token.tagged_form for token in tokens))
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='*')
    main(parser.parse_args())


