import sys
import json


def define_new_terms_score(tweet_file, sent_dict, limit=0):
    """ Returns a dictionary of terms not in sent_dict with their score.

    Limit is the number of tweets processed. If equal to 0, all tweets from
    the tweet file are will be processed.
    """
    new_terms = {}
    count = 0
    for line in tweet_file.readlines():
        tweet_infos = json.loads(line)
        try:

            if 'text' in tweet_infos.keys():
                text = tweet_infos['text']
                if text:
                    derive_new_sent(text, sent_dict, new_terms)
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

        # Limit check
        count += 1
        if limit > 0 and count > limit:
            break

    return new_terms


def derive_new_sent(text, sent_dict, new_terms):
    words = text.split()
    score = 0
    # Compute score for tweet
    for word in words:
        uni_word = word.encode('utf-8')
        score += sent_dict[word] if uni_word in sent_dict.keys() else 0

    # List of terms encountered to avoid overcounting.
    processed = []
    for word in words:
        uni_word = word.encode('utf-8')
        if not uni_word in sent_dict.keys() and not uni_word in processed:
            term_score = score + new_terms[uni_word] \
                if uni_word in new_terms.keys() else score
            new_terms[uni_word] = term_score
            processed.append(uni_word)


def extract_sent_dict(sent_file_path):
    afinnfile = open(sent_file_path)
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)  # Convert the score to an integer.

    return scores


def main():
    if len(sys.argv) >= 2:
        sent_file_path = sys.argv[1]
        tweet_file = open(sys.argv[2])
    else:
        sent_file_path = 'AFINN-111.txt'
        tweet_file = open('output.txt')
    sent_dict = extract_sent_dict(sent_file_path)
    new_terms = define_new_terms_score(tweet_file, sent_dict, limit=30)
    for (k, v) in new_terms.items():
        print k, v

if __name__ == '__main__':
    main()
