# -*- coding: utf-8 -*-
from TwitterAPI import TwitterAPI
import codecs
import sys
from pprint import pprint
from google_translator import translate
from .config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

SEARCH_TERM = 'Coronation Night'  # 'pizza'
MAX_COUNT = 100


api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)

r = api.request('search/tweets', {'q': SEARCH_TERM, 'count': MAX_COUNT, 'include_entities': True, })

print(u'\nQUOTA: %s' % r.get_rest_quota())

UTF8Writer = codecs.getwriter('utf-8')
sys.stdout = UTF8Writer(sys.stdout)

quota = u'QUOTA: %s\n\n' % r.get_rest_quota()
out = codecs.open('posted_posts.txt', 'w', 'utf-8')
out2 = codecs.open('posted_posts_short.txt', 'w', 'utf-8')


def merge_lines(s):
    arr = s.splitlines()
    arr2 = []
    for a in arr:
        if a:
            arr2.append(a)
    return u" ".join(arr2)

out.write(quota)
out2.write(quota)
for item in r:
    text = item['text']
    user = item['user']
    name = user['name'].strip()
    screen_name = user['screen_name'].strip()
    content = text
    
    out.write('\n')
    pprint(item, out)
    out2.write(u'|%s|\t' % (name) + merge_lines(text) + u'\n')
    # pprint(unicode(translate(text)), out2)
    #content = unicode(text, 'utf-8', errors='ignore')
    # print(u"\t" + text.decode('utf-8'))

    #out.write(content)
    #out.write("\n")

meta = r.get_search_metadata()
params = r.parse_query_string(meta['next_results'])
pprint(meta)
print('params:' + str(params))
