from preprocess import *
from feature import *
from download import *
from random import shuffle
from sklearn import linear_model, metrics, svm
import math, csv

# ----- PRE PROCESSING

try:
    lyrics = []
    with open('lyrics.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            lyrics.append(row)
except Exception:
    download_lyrics()
    pass

valid_genres = ['Pop', 'Hip Hop/Rap', 'Reggae']
clean_data = [(preprocess(lyrics), genre) for lyrics, genre in lyrics if genre in valid_genres]
print(len(clean_data))


# ----- FEATURE SELECTION

builder = FeatureBuilder()
builder.build_vocabulary(clean_data)

N = len(clean_data)

# Uncomment the feature set to use
# feature_sets = [(builder.feature_contains_num(lyric), category) for (lyric, category) in clean_data]
# feature_sets = [(builder.feature_frequency_num(lyric), category) for (lyric, category) in clean_data]
# feature_sets = [(builder.feature_contains(lyric), category) for (lyric, category) in clean_data]
feature_sets = [(builder.feature_frequency(lyric), category) for (lyric, category) in clean_data]

shuffle(feature_sets, lambda: 0.4)
test_set, train_set = feature_sets[math.floor(N*0.8):], feature_sets[:math.floor(N*0.8)]

train_lyrics = [lyrics for (lyrics, genre) in train_set]
train_genre = [genre for (lyrics, genre) in train_set]

test_lyrics = [lyrics for (lyrics, genre) in test_set]
test_genre = [genre for (lyrics, genre) in test_set]

# ----- NAIVE BAYES CLASSIFIER

classifier = nltk.NaiveBayesClassifier.train(train_set)

predictions = classifier.classify_many(test_lyrics)

# Measure accuracy
# classifier.show_most_informative_features(30)
accuracy = nltk.classify.accuracy(classifier, test_set)
confusion_matrix = nltk.ConfusionMatrix(test_genre, predictions)

print(confusion_matrix)
print(accuracy)

# ----- LOGISTIC REGRESSION

# logreg = linear_model.LogisticRegression(C=1e5)
# logreg.fit(train_lyrics, train_genre)
# predictions = logreg.predict(test_lyrics)
# print(metrics.accuracy_score(test_genre, predictions))

# ----- SUPPORT VECTOR MACHINE

# clf = svm.SVC()
# clf.fit(train_lyrics, train_genre)
# predictions = clf.predict(test_lyrics)
# print(metrics.accuracy_score(test_genre, predictions))




