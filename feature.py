import nltk.probability, nltk.metrics


class FeatureBuilder:
    def __init__(self):
        self.vocabulary = []
        self.top_words = []

    def build_vocabulary(self, data):
        self.vocabulary = [word for (lyric, category) in data for word in lyric]
        all_words = nltk.FreqDist(w for w in self.vocabulary)
        self.top_words = list(all_words.most_common())[:100]

    def feature_contains(self, lyrics):
        document_word = set(lyrics)
        features = {}
        for (w, freq) in self.top_words:
            features['contains({})'.format(w)] = (w in document_word)
        return features

    def feature_contains_num(self, lyrics):
        document_word = set(lyrics)
        features = []
        for (w, freq) in self.top_words:
            features.append(w in document_word)
        return features

    def feature_frequency(self, lyrics):
        features = {}
        for (w, freq) in self.top_words:
            count = lyrics.count(w)
            features['frequency_no({})'.format(w)] = count == 0
            features['frequency_single({})'.format(w)] = count == 1
            features['frequency_multipe({})'.format(w)] = count > 1 & count < 7
            features['frequency_many({})'.format(w)] = count >= 7
        return features

    def feature_frequency_num(self, lyrics):
        features = []
        for (w, freq) in self.top_words:
            count = lyrics.count(w)
            features.append(count)
        return features
