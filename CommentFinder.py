import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import math
import time, pickle, math, warnings, os, operator
import string
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate import bleu_score
import time
from difflib import SequenceMatcher
import statistics
from tqdm import tqdm
from CFprocessData import CFProcessTestDataset, CFProcessTrainDataset
from myProcessData import myProcessTestDataset, myProcessTrainDataset

base = './dataset/'
path_train = base + 'train.tsv'
path_test_source = base + 'source.txt'
path_test_target = base + 'target.txt'


train_dataset = [line.strip() for line in open(path_train)]
# for testing (16к ноут уже не тянет :( )
source_test = [line.strip() for counter, line in enumerate(open(path_test_source)) if counter < 10000]
target_test = [line.strip() for counter, line in enumerate(open(path_test_target)) if counter < 10000]

source_train, target_train = myProcessTrainDataset(train_dataset)
source_test = myProcessTestDataset(source_test)

data_count_vect = CountVectorizer(max_df=0.5, tokenizer=lambda x: x, preprocessor=lambda x: x)
train_data_vect = data_count_vect.fit_transform(source_train)
test_data_vect = data_count_vect.transform(source_test)

print(f'Vector Length: {train_data_vect.shape[1]}\n')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def predictionTopk(topk, similarity, similarity_time):
    print("processing:", topk)
    prediction = []
    start_time = time.time()
    for index in range(len(similarity)):
        if index % 1000 == 0:
            print("processing-instance ", index, "/", len(target_test))
        #       find top-10 instances based on cosine distance
        index_nn = np.argpartition(similarity[index], -10)[-10:]
        similar_nn = []
        for idx in index_nn:
            #       find best 10 candidates from top-10 instances based on text similarity score
            similar_score = similar(source_test[index], source_train[idx])
            similar_nn.append((idx, similar_score))
        similar_nn.sort(key=lambda x: x[1], reverse=True)
        similar_topk = similar_nn[:topk]
        current_prediction = []
        for element in similar_topk:
            current_prediction.append(target_train[element[0]])
        prediction.append(current_prediction)
    print(topk, " time cost:", time.time() - start_time + similarity_time, "s")
    #   write the recommendation comments to the file named as "our_predictions_k.txt"
    with open(base + 'our_predictions_' + str(topk) + '.txt', 'w') as f:
        for data in prediction:
            for element in data:
                f.write(element + '\n')


# Compute the cosine distance and its computational time
similarity_start_time = time.time()
similarity = cosine_similarity(test_data_vect, train_data_vect)
similarity_time = time.time() - similarity_start_time

# Compute the text similarity (GPM) and results
predictionTopk(1, similarity, similarity_time)
predictionTopk(3, similarity, similarity_time)
predictionTopk(5, similarity, similarity_time)
predictionTopk(10, similarity, similarity_time)

chencherry = bleu_score.SmoothingFunction()

# Evaluate perfect prediction & BLEU score of our approach
for k in [1, 3, 5, 10]:

    print('k candidates: ', k)
    path_targets = base + 'target.txt'
    path_predictions = base + 'our_predictions_' + str(k) + '.txt'

    pred = [line.strip() for line in open(path_predictions)]

    count_perfect = 0
    BLEUscore = []
    for i in tqdm(range(len(target_test))):
        best_BLEU = 0
        target = target_test[i]
        for prediction in pred[i * k:i * k + k]:
            if " ".join(prediction.split()) == " ".join(target.split()):
                count_perfect += 1
                best_BLEU = bleu_score.sentence_bleu([target], prediction, smoothing_function=chencherry.method1)
                break
            current_BLEU = bleu_score.sentence_bleu([target], prediction, smoothing_function=chencherry.method1)
            if current_BLEU > best_BLEU:
                best_BLEU = current_BLEU
        BLEUscore.append(best_BLEU)

    print(f'\nPP    : %d/%d (%s%.2f)' % (count_perfect, len(target_test), '%', (count_perfect * 100) / len(target_test)))
    print(f'BLEU mean              : ', statistics.mean(BLEUscore))

    with open(base + "bleu_" + str(k) + '.txt', 'w') as fs:
        for bleu in BLEUscore:
            fs.write(str(bleu) + '\n')
