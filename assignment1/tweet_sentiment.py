import sys
import json


def test_10_tweets(tweet_file, sent_dict):
    """Test on 10 first lines from tweet file

    """
    count = 0

    for line in tweet_file.readlines():
        tweet_infos = json.loads(line)
        try:

            if 'text' in tweet_infos.keys():
                text = tweet_infos['text']
                if text:
                    analyse_text(text, sent_dict)
                else:
                    print 'error'
                count += 1
                if count > 50:
                    break
        except Exception, e:
            print 'Error on tweet:'
            print tweet_infos
            print str(e)
            raise


def extract_sent_dict(sent_file_path):
    afinnfile = open(sent_file_path)
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)  # Convert the score to an integer.

    return scores


def analyse_text(text, sent_dict):
    words = text.split()
    score = 0
    for word in words:
        uni_word = word.encode('utf-8')
        score += sent_dict[word] if uni_word in sent_dict.keys() else 0
    print score


def main():
    sent_dict = extract_sent_dict('AFINN-111.txt')
    tweet_file = open('output.txt')
    test_10_tweets(tweet_file, sent_dict)

if __name__ == '__main__':
    main()
