import sys
import json

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


def rank_state_tweets(tweet_file, sent_dict, limit=0):
    """

    """
    count = 0
    # Structure is state: (score, nb_tweets_in_state)
    state_scores = {}
    for line in tweet_file.readlines():
        tweet_infos = json.loads(line)
        try:
            state = get_state(tweet_infos)
            if state:
                tweet_score = get_tweet_score(tweet_infos, sent_dict)
                if state in state_scores.keys():
                    (score, nb_tweets) = state_scores[state]
                    score = score + tweet_score
                    nb_tweets += 1
                    state_scores[state] = (score, nb_tweets)
                else:
                    state_scores[state] = (tweet_score, 1)

        except Exception, e:
            print 'Error on tweet:'
            print tweet_infos
            print str(e)
            raise

        count += 1
        if limit > 0 and count > limit:
            break

    return state_scores


def get_state(tweet_infos):
    """Return state if tweet is from USA, None otherwise

    Since offline solution, based on place and user-profile location
    """
    key_country_code = 'country_code'
    key_full_name = 'full_name'
    country_code_US = 'US'
    is_USA = False
    state = None
    place_key = 'place'

    if place_key in tweet_infos.keys() and tweet_infos[place_key]:
        place_dict = tweet_infos[place_key]

        if key_country_code in place_dict.keys() \
                and place_dict[key_country_code]:

            is_USA = place_dict[key_country_code] == country_code_US
        if is_USA:
            # print "place: "+str(tweet_infos[place_key])
            # Take the full name
            if key_full_name in place_dict.keys() \
                    and place_dict[key_full_name]:

                parsed = place_dict[key_full_name].split(',')
                if len(parsed) > 1:
                    possible_state = parsed[1].strip()
                    state = possible_state if possible_state in states.keys() \
                        else None

    user = 'user'
    location = 'location'
    if not state:
        if user in tweet_infos.keys() and tweet_infos[user]:
            if location in tweet_infos[user].keys() \
                    and tweet_infos[user][location]:

                user_location = tweet_infos[user][location]

                # First, see if the whole thing is a state name
                for (k, v) in states.items():
                    if v.lower() == user_location.lower():
                        state = k
                if state:
                    return state

                # Now, let's try parsing
                split = user_location.split(',')
                first_part = split[0]
                second_part = None
                if len(split) > 1:
                    second_part = split[1]
                for (k, v) in states.items():
                    if first_part.lower == k or first_part.lower == v:
                        state = k
                        return state

                    if second_part:
                        sec_part_low = second_part.lower()
                        if sec_part_low == k or sec_part_low == v:
                            state = k
                            return state

    return state


def extract_sent_dict(sent_file_path):
    afinnfile = open(sent_file_path)
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)  # Convert the score to an integer.

    return scores


def get_tweet_score(tweet, sent_dict):
    if 'text' in tweet.keys():
        text = tweet['text']
        if text:
            words = text.split()
            score = 0
            for word in words:
                uni_word = word.encode('utf-8')
                score += sent_dict[word] if uni_word in sent_dict.keys() else 0
            return score

    else:
        return 0


def sort_by_avg_score(state_score_dict):
    """ Returns a List sorted by average score

    """
    unsorted_scores = [(float(v[0])/float(v[1]), k) for (k, v) in state_score_dict.items()]
    unsorted_scores.sort()
    unsorted_scores.reverse()
    return unsorted_scores


def main():
    if len(sys.argv) >= 2:
        sent_file_path = sys.argv[1]
        tweet_file = open(sys.argv[2])
    else:
        sent_file_path = 'AFINN-111.txt'
        tweet_file = open('output.txt')
    sent_dict = extract_sent_dict(sent_file_path)
    state_scores = rank_state_tweets(tweet_file, sent_dict)
    sorted_by_scores = sort_by_avg_score(state_scores)

    # Print only the first
    print sorted_by_scores[0][1]


if __name__ == '__main__':
    main()
