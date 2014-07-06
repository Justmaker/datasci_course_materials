import sys
import json


def compute_frequencies(tweet_file, limit=0):
    term_occ = {}
    total_occ = 0
    count = 0
    for line in tweet_file.readlines():
        tweet_infos = json.loads(line)
        try:

            if 'text' in tweet_infos.keys():
                text = tweet_infos['text']
                if text:
                    total_occ += count_occ_in_tweet(text, term_occ)
                else:
                    print 'error'
            else:
                # print 0
                pass

        except Exception, e:
            print 'Error on tweet:'
            print tweet_infos
            print str(e)
            raise

        count += 1
        if limit > 0 and count > limit:
            break

    # Now compute freqs which is:
    # (# occ of term in all tweets)/(# occ of all terms in all tweets)
    freqs = {key: value/float(total_occ) for (key, value) in term_occ.items()}
    return freqs


def count_occ_in_tweet(text, term_occ):
    words = text.split()
    tweet_total_occ = 0
    for word in words:
        tweet_total_occ += 1
        uni_word = word.encode('utf-8')
        term_occ[uni_word] = term_occ[uni_word] + 1 \
            if uni_word in term_occ.keys() else 1
    return tweet_total_occ


def main():
    if len(sys.argv) >= 1:
        tweet_file = open(sys.argv[1])
    else:
        tweet_file = open('output.txt')

    freqs = compute_frequencies(tweet_file)
    for (k, v) in freqs.items():
        print k + ' ' + str(v)

    # Define frequencies


if __name__ == '__main__':
    main()
