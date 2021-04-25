from gensim.models.word2vec import Word2Vec
from gensim.models.fasttext import FastText
import pickle
import os
import gc

def generate_corpus(w2vModelPath, samples): 
    model = Word2Vec.load(w2vModelPath)
    print("begin generate input...")
    dl_corpus = []
    for sample in samples:
        word = (" ").join(sample)
        vectorized = model.wv[word]
        dl_corpus.append(vectorized)
    # for sample in samples:
    #     for word in sample:
    #         try:
    #             dl_corpus.append(model[word])
    #         except:
    #             continue
    # dl_corpus = [[model[word] for word in sample] for sample in samples]
    print("generate input success...")

    return dl_corpus

def get_dldata(filepath, dlTrainCorpusPath):
    folders = os.listdir(filepath)

    folders_train = folders
      
    for mode in ["api", "arraysuse", "pointersuse", "expr"]:
        train_set = [[], [], [], [], [], []]
        ids = []
        for folder_train in folders_train[:]:
            for filename in os.listdir(filepath + folder_train + '/'):
                if mode in filename:
                    f = open(filepath + folder_train + '/' + filename, 'rb')
                    data = pickle.load(f)
                    id_length = len(data[1])
                    for j in range(id_length):
                        ids.append(folder_train)
                        for n in range(5):
                            train_set[n] = train_set[n] + data[n]
                            train_set[-1] = ids
        if train_set[0] == []:
            continue
        f_train = open(dlTrainCorpusPath + mode + "_.pkl", 'wb')
        pickle.dump(train_set, f_train, protocol=pickle.HIGHEST_PROTOCOL)
        f_train.close()
        del train_set
        gc.collect()

def deliverVectors(working_directory):
    
    CORPUSPATH = working_directory + "corpus/"
    VECTORPATH = working_directory + "vector/"
    W2VPATH = "./sysevr/ml_models/fastText_full"
    print("turn the corpus into vectors...")
    for corpusfiles in os.listdir(CORPUSPATH):
        print(corpusfiles)
        if corpusfiles not in os.listdir(VECTORPATH):
            folder_path = os.path.join(VECTORPATH, corpusfiles)
            os.makedirs(folder_path)
        for corpusfile in os.listdir(CORPUSPATH + corpusfiles):
            corpus_path = os.path.join(CORPUSPATH, corpusfiles, corpusfile)
            f_corpus = open(corpus_path, 'rb')
            data = pickle.load(f_corpus)
            f_corpus.close()
            data[0] = generate_corpus(W2VPATH, data[0])
            vector_path = os.path.join(VECTORPATH, corpusfiles, corpusfile)
            f_vector = open(vector_path, 'wb')
            pickle.dump(data, f_vector, protocol=pickle.HIGHEST_PROTOCOL)
            f_vector.close()
    print("w2v over...")

    # print("spliting the train set and test set...")
    # dlTrainCorpusPath = working_directory + "model_input/"
    # get_dldata(VECTORPATH, dlTrainCorpusPath)
    
    print("success!")
