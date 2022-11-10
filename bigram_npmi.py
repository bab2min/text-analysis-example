from collections import Counter

import numpy as np

def main(args):
    unicnt = Counter()
    bicnt = Counter()
    for i in args.inputs:
        for line in open(i, encoding='utf-8'):
            tokens = line.strip().split()
            unicnt.update(tokens)
            bicnt.update(zip(tokens[:-1], tokens[1:]))
    
    if args.mode == 'count':
        for w, c in bicnt.most_common():
            print(w, c, sep='\t')
    elif args.mode in ('pmi', 'npmi'):
        global_tot = sum(unicnt.values())
        keys = []
        scores = []
        cnts = []
        for (a, b), n in bicnt.items():
            if n < args.min_cnt: continue
            score = n * global_tot / unicnt[a] / unicnt[b]
            keys.append((a, b))
            scores.append(score)
            cnts.append(n)
        
        scores = np.array(scores)
        scores = np.log(scores)
        cnts = np.array(cnts)
        if args.mode == 'npmi':
            scores /= np.log(global_tot / np.array(cnts))

        idx = (-scores).argsort()
        for (a, b), s, c in zip(map(keys.__getitem__, idx), scores[idx], cnts[idx]):
            if s <= 0: break
            print(a, b, f'{s:.3f}', c, sep='\t')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('--mode', choices=['count', 'pmi', 'npmi'], default='npmi')
    parser.add_argument('--min_cnt', default=10, type=int)
    main(parser.parse_args())


