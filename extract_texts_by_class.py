from collections import defaultdict
import json

def extract_texts(args, data):
    all_texts = defaultdict(list)
    for datum in data:
        split_by = tuple(args.split_by) if args.split_by else ()
        p_info = datum['header']['participantsInfo']
        p_info = {p['participantID']: tuple(p[t] for t in split_by) for p in p_info}
        texts = defaultdict(list)
        for body in datum['body']:
            texts[p_info[body['participantID']]].append(body['utterance'].replace('\n', ' '))
        
        for k, v in texts.items():
            all_texts[k].append(args.turn_separator.join(v))
    return all_texts

def main(args):
    opened_files = {}
    for i in args.inputs:
        obj = json.load(open(i, encoding='utf-8'))
        for k, v in extract_texts(args, obj['data']).items():
            try:
                opened_files[k].write('\n'.join(v) + '\n')
            except KeyError:
                f = open(args.output_path + '/' + '.'.join(k) + '.txt', 'w', encoding='utf-8')
                f.write('\n'.join(v) + '\n')
                opened_files[k] = f
    for v in opened_files.values():
        v.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path')
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('--split_by', nargs='*')
    parser.add_argument('--turn_separator', default=' // ')
    main(parser.parse_args())
