import urllib
import requests
import os
import json
from article import Article
from facts import Facts


class Query(object):
    def __init__(self, query):
        self.API_KEY = os.getenv('GOOGLE_API')
        self.SEARCH_ENGINE_ID = '015040051912301786117:ukzldfl328w'
        self.query = query.replace(' ','+')

        self.facts = []
        self.articles = []#{'title':[], 'url':[], 'sentiment':[], 'political':[], 'summary':[]}

        self.article_information()


    def create_fake(self):
        self.facts = ['Pip is a good man', 'Byron is a person', 'Keenan is Keenan', 'Patrick smells']
        for i in xrange(10):
            self.articles.append( {'title':str(i), 'url':'google.com', 'sentiment':str(i*4), 'political':str(i*8), 'summary':'Hello I am summary. This is summary. I will summarize you BITCH'})


    def generate_query(self, iteration):
        if iteration != 0:
            template = ['https://www.googleapis.com/customsearch/v1?highrange&start=', str(iteration), '&key=',self.API_KEY,'&cx=',self.SEARCH_ENGINE_ID,'&q=', self.query]
        else: 
            template = ['https://www.googleapis.com/customsearch/v1?highrange&key=',self.API_KEY,'&cx=',self.SEARCH_ENGINE_ID,'&q=', self.query]

        url = ''.join(template)
        return url
        

    def sort_urls(self, urls):
        ret = {'cnn':[], 'guardian':[], 'huffington':[], 'nytimes':[]}
        for i in urls:
            if 'cnn.com' in i:
                ret['cnn'].append(i)
            elif 'guardian.com' in i:
                ret['guardian'].append(i)
            elif 'huffingtonpost.com' in i:
                ret['huffington'].append(i)
            elif 'nytimes.com' in i:
                ret['nytimes'].append(i)
        
        return ret


    # TODO: Reimplement this over get_urls tmp
    def get_urls(self):
        # Returns a dictionary object with links as the values
        urls = []
        for i in xrange(5):
            url = self.generate_query( 10 * i )
            response = requests.get(url)
            response = json.loads(response.content)
            if 'error' in response.keys():
                raise Exception("Error")

            for i in response['items']:
                urls.append(i['link'])

        return self.sort_urls(urls)


    def get_urls_tmp(self):
        urls = []

        try:
            f = open('backup_urls.txt', 'r')
        except:
            f = open('models/backup_urls.txt','r')

        for line in f:
            urls.append(line.strip())

        f.close()
        return self.sort_urls(urls)


    def article_information(self):
        Articles = self.fetch_articles()
        self.articles = Articles

        self.choosing_quotes(Articles)
    

    def choosing_quotes(self, Articles):
        total_quotes = []
        total_length = 0
        count = 0
        for item in Articles:
            for i in item.quotes:
                tmp = len(''.join(item.quotes[i]))
                total_length += tmp
                count += 1

        average = total_length/float(count)

        for item in Articles:
            for i in item.quotes:
                tmp = len(''.join(item.quotes[i]))
                if tmp > average:
                    total_quotes.append(i)

        #print total_quotes
        self.facts = total_quotes[:8]

    def fetch_articles(self):
        # TODO: REIMPLEMENT get_urls & not tmp
        urls = self.get_urls_tmp()
        #urls = self.get_urls()
        firsts = []
        for i in urls:
            try:
                firsts.append(urls[i][0])
            except:
                pass

        Articles = []
        for link in firsts:
            Articles.append(Article(link))
            
        return Articles


if __name__ == '__main__':
    test = Query('ahmed mohamed')

    #print test.articles
    for i in test.facts:
        print i
        print

    #test.create_fake()

    #Articles = test.fetch_articles()
    #facts = Facts(Articles)
    #for i in Articles:
    #    print i.quotes
