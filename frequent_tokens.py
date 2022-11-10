from collections import Counter
import re

import numpy as np


def main(args):
    cnt = Counter()
    local_cnts = []

    if args.regex_filter:
        pat = re.compile(args.regex_filter).search
    else:
        pat = None
    
    if args.stopwords:
        stopwords = set(line.strip() for line in open(args.stopwords))
    else:
        stopwords = None

    for i in args.inputs:
        local_cnt = Counter()
        for line in open(i, encoding='utf-8'):
            tokens = line.strip().split()
            if pat is not None:
                tokens = filter(pat, tokens)
            if stopwords is not None:
                tokens = [t for t in tokens if t not in stopwords]
            local_cnt.update(tokens)
            
        if args.mode != 'all_count':
            local_cnts.append(local_cnt)
        cnt.update(local_cnt)
    
    if args.mode == 'all_count':
        for w, c in cnt.most_common():
            print(w, c, sep='\t')
    elif args.mode == 'count':
        for i, local_cnt in zip(args.inputs, local_cnts):
            print(f'<<<< Top words of {i} >>>>')
            for m, c in local_cnt.most_common(args.topn):
                print(m, c, sep='\t')
            print()
    else:
        global_tot = sum(cnt.values())
        for i, local_cnt in zip(args.inputs, local_cnts):
            print(f'<<<< Top PMI words of {i} >>>>')
            local_tot = sum(local_cnt.values())
            ks = list(local_cnt)
            local_vs = np.array(list(local_cnt.values()))
            idx = np.where(local_vs >= args.min_cnt)[0]
            local_vs = local_vs[idx]
            ks = list(map(ks.__getitem__, idx))
            global_vs = np.array(list(map(cnt.__getitem__, ks)))

            pa = global_vs / global_tot
            pb = local_tot / global_tot
            pab = local_vs / global_tot
            pmi = np.log(pab / (pa * pb))
            if args.mode == 'npmi':
                pmi /= -np.log(pab)

            idx = (-pmi).argsort()[:args.topn]
            for m, s, c in zip(map(ks.__getitem__, idx), pmi[idx], local_vs[idx]):
                if s <= 0: break
                print(m, f'{s:.3f}', c, sep='\t')
            print()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('-r', '--regex_filter')
    parser.add_argument('--stopwords')
    parser.add_argument('--mode', choices=['all_count', 'count', 'pmi', 'npmi'], default='all_count')
    parser.add_argument('--min_cnt', default=10, type=int)
    parser.add_argument('--topn', type=int)
    main(parser.parse_args())


