import sys
import json


def get_hashtag_count(tweet_file, limit=0):
    """ Return dictionary of hashtag counts

    """
    hashtag_dict = {}
    count = 0
    for line in tweet_file.readlines():
        tweet_infos = json.loads(line)
        try:
            if 'entities' in tweet_infos.keys():
                entities = tweet_infos['entities']
                if 'hashtags' in entities.keys():
                    get_tweet_hashtag_count(entities['hashtags'], hashtag_dict)

        except Exception, e:
            print 'Error on tweet:'
            print tweet_infos
            print str(e)
            raise

        count += 1
        if limit > 0 and count - 1 > limit:
            break

    return hashtag_dict


def get_tweet_hashtag_count(hashtag_list, hashtag_dict):

    for hashtag_infos in hashtag_list:
        hashtag = hashtag_infos['text'].encode('utf-8')
        if hashtag in hashtag_dict.keys():
            hashtag_dict[hashtag] = hashtag_dict[hashtag] + 1
        else:
            hashtag_dict[hashtag] = 1


def sort_by_count(hashtag_dict):
    """ Returns a List sorted by count

    """
    unsorted_scores = [(v, k) for (k, v) in hashtag_dict.items()]
    unsorted_scores.sort()
    unsorted_scores.reverse()
    return unsorted_scores


def main():
    if len(sys.argv) > 1:
        tweet_file = open(sys.argv[1])
    else:
        tweet_file = open('output.txt')

    hashtag_count = get_hashtag_count(tweet_file)
    list_hashtag = sort_by_count(hashtag_count)
    if len(list_hashtag) > 9:
        for x in range(0, 10):
            item = list_hashtag[x]
            print item[1] + ' ' + str(item[0])
    else:
        raise Exception('List hastag size = ' + len(list_hashtag))


if __name__ == '__main__':
    main()
