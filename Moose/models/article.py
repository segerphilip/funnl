from newspaper import Article as NewsArticle
import sys
import os
from tools.FrequencySummarizer import FrequencySummarizer
import indicoio

class Article(object):

    api_key = os.getenv("INDICO_KEY")
    indicoio.config.api_key = api_key

    def __init__(self, url):
        self.summarizer = FrequencySummarizer()
        
        self.url = url
        self.title = None
        self.text = self._get_source()
        self.quotes = self._get_quotes()
        self.sentiment = self._get_sentiment()
        self.political = self._get_political()
        self.summary = self._get_summary()

    def _get_source(self):
        article = NewsArticle(self.url)

        article.download()
        article.parse()

        self.title = article.title

        raw_text = article.text
        raw_text = raw_text.encode("ascii", 'backslashreplace')
        raw_text = raw_text.replace('\\u201d', '"')
        raw_text = raw_text.replace('\\u201c', '"')
        raw_text = raw_text.replace('\\u2014', '--')
        raw_text = raw_text.replace('\\u2019', '\'')
        raw_text = raw_text.replace('\\u2018', '\'')
        raw_text = raw_text.replace('\\u2026', '...')
        raw_text = raw_text.replace('\\u2013', '-')

        raw_text = raw_text.split('\n\n')

        filtered = self._filter(raw_text)

        return filtered

    def _filter(self, unfiltered_text):
        filtered_text = []
        filter_words = ['photo', 'image', 'related', 'copyright', 'photograph', 'watch', 'video', 'youtube', 'advertisement']
        for sentence in unfiltered_text:
            lowered = [word.lower() for word in sentence.split()]
            if not any(word in lowered for word in filter_words):
                filtered_text.append(sentence)

        return filtered_text


    def _get_sentiment(self):
        return indicoio.sentiment(" ".join(self.text))

    def _get_political(self):
        return indicoio.political(" ".join(self.text))

    def _get_summary(self):
        return " ".join(self.summarizer.summarize(" ".join(self.text), 5))

    def _check_for_quotes(self, line):
        count = line.count('"')

        if count == 0:
            return None
        elif count % 2 != 0: # TODO: This will be an edge case, ignore for now
            return None
        
        locations = [i for i, ltr in enumerate(line) if ltr == '"']
        quote_object = [ line[locations[i]:locations[i+1]+1] for i in xrange(0,count,2) ]
        return quote_object

    def _get_quotes(self):
        quotes = {}
        potential = []

        # Get potential quotes
        keywords = ['said', 'says', 'told', '"'] # Possibly only need " character
        for line in self.text:
            if [ True for i in keywords if i in line ]: 
                potential.append(line)

        # Extract only the sentence with the quote in it
        new = []
        for line in potential:
            tmp = 0
            while( line.find('.') < line.find('"') or line.find('.') == 0):
                tmp +=1 
                line = line[line.find('.')+1:].strip()
                new.append(line)
                if tmp == 50:
                    break
            else:
                line = line.strip()
                new.append(line)
        potential = new

        # Extract just the quoted section to check for redundancy later on
        for line in potential:
            tmp = self._check_for_quotes(line)
            if tmp != None:
                # TODO: Might switch tmp : line, so that quoted section can call full sentence
                quotes[line] = tmp 

        return quotes

if __name__ == "__main__":
    myArticle = Article("http://www.cnn.com/2015/09/19/politics/donald-trump-muslims-controversy/index.html")

    for i in myArticle.quotes:
        print i
        print
