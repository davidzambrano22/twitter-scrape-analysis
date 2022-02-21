import re
import sklearn

class tokenizer:
    def __init__(self):
        self.pattern = re.compile(r'\w+')

    def get_tokens(self, line):
        line = line.lower()
        line = re.sub('@\w+', '_mention_', line)
        line = re.sub('#\w+', '_hashtag_', line)
        line = re.sub('\d+', '_number_', line)
        line = re.sub('([a-zA-Z]+[0-9]+[\w]*|[0-9]+[a-zA-Z]+[\w]*)', '', line)
        line = re.sub('[u"\U0001F600-\U0001F64F"]', '', line)
        line = re.sub('http[s]?//w+', '_url_', line)
        return self.pattern.findall(line)

