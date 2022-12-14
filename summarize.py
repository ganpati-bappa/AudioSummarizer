import numpy as np
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import networkx as nx


stopWords = set(stopwords.words('english'))
ps = PorterStemmer()


def make_text(s):
    text = s
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = sumValues // len(sentenceValue)

    # print(average)
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.0 * average)):
            summary += " " + sentence

    return summary


embeding_ind = {}
with open('glove6b50d/glove.6B.50d.txt', encoding='utf-8') as f:
    for line in f:
        values = line.split()
        word = values[0]
        coef = [float(values[i]) for i in range(1, 51)]
        num = np.asarray(coef)
        embeding_ind[word] = num


def read_article(s):
    sentences = sent_tokenize(s)
    return sentences


def cosine_product(a, b):
    return np.dot(a, b)


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    review1 = sent1.lower()
    review1 = review1.split()
    review1 = [ps.stem(word) for word in review1 if not word in stopWords]
    review1 = ' '.join(review1)
    t1 = word_tokenize(sent1)
    review2 = sent2.lower()
    review2 = review2.split()
    review2 = [ps.stem(word) for word in review2 if not word in stopWords]
    review2 = ' '.join(review2)
    t2 = word_tokenize(sent2)

    maxlen = 50
    embeding_out1 = np.zeros((maxlen, 50))
    for j in range(maxlen):
        try:
            embeding_out1[j] = embeding_ind[sent1[j].lower()]
        except:
            embeding_out1[j] = np.zeros((50,))

    embeding_out2 = np.zeros((maxlen, 50))
    for j in range(maxlen):
        try:
            embeding_out2[j] = embeding_ind[sent2[j].lower()]
        except:
            embeding_out2[j] = np.zeros((50,))
    sum = 0
    for j in range(maxlen):
        sum = sum + cosine_product(embeding_out1[j], embeding_out2[j])
    return (50 - sum) / 50


def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=1):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_article(file_name)
    # print(sentences)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph, tol=1.0e-3, max_iter=1500)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], i, s) for i, s in enumerate(sentences)), reverse=True)
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)
    ranked_sentence = ranked_sentence[0:top_n]
    ranked_sentence.sort(key=lambda x: x[1])
    for i in range(top_n):
        summarize_text.append("".join(ranked_sentence[i][2]))

    # Step 5 - output the summarize text
    text = ""
    text = text.join(summarize_text)

    return text
