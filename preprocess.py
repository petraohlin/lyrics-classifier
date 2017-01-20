from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re, nltk


def preprocess(text):
    st = PorterStemmer()
    stop = stopwords.words('english')
    stop.append('')

    # Tokenize
    temp_tokens = (nltk.word_tokenize(text))

    # Remove non alpha-numeric characters and lowercase words
    temp_tokens = [re.sub(r'\W+', '', str(token)).lower() for token in temp_tokens]

    # Remove stopwords and stem tokens
    temp_tokens = [st.stem(str(token)) for token in temp_tokens if token not in stop]

    return temp_tokens
