from keras.models import Sequential, load_model
from keras.layers.core import Masking, Dense, Dropout, Activation
from keras.layers.recurrent import LSTM, GRU
from keras.layers.wrappers import Bidirectional
from keras import backend as K
from .vul_types import VULNERABILITY_TYPE, VULNERABILITY_FILE
import pickle
import os
import numpy as np
from .preprocess_dl_Input_version5 import *
from fastembed.predictor.lookup import *
import math

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def build_model(maxlen, vector_dim, layers, dropout):
    print('Build model...')
    model = Sequential()

    model.add(Masking(mask_value=0.0, input_shape=(maxlen, vector_dim)))

    for i in range(1, layers):
        model.add(Bidirectional(
            GRU(units=256, activation='tanh', recurrent_activation='hard_sigmoid', return_sequences=True)))
        model.add(Dropout(dropout))

    model.add(Bidirectional(GRU(units=256, activation='tanh', recurrent_activation='hard_sigmoid')))
    model.add(Dropout(dropout))

    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adamax', metrics=['accuracy'])

    model.summary()

    return model


def testrealdata(realtestpath, weightpath, maxlen, vector_dim, layers, dropout):
    K.clear_session()
    model = build_model(maxlen, vector_dim, layers, dropout)
    model.load_weights(weightpath)

    print("Loading data...")
    vulnerable_list = []
    df = pd.read_csv("./fastembed/ml_models/CVE_vector_list.csv", index_col=0)
    cve_vector_list = df.iloc[:,2:].to_numpy()

    for subdir in os.listdir(realtestpath):
        print(subdir)
        for filename in os.listdir(os.path.join(realtestpath, subdir)):
            print(filename)
            f = open(realtestpath + subdir + "/" + filename, "rb")
            dataset,labelsfile,funcsfiles,filenamesfile,testcasesfile = pickle.load(f)
            f.close()
            if len(dataset) == 0:
                continue
            # batch_size = 32
            test_generator = generator_of_data(dataset, labelsfile, len(dataset), maxlen, vector_dim)
            # all_test_samples = len(dataset)
            # steps_epoch = int(math.ceil(all_test_samples / batch_size))

            result_predict = model.predict_generator(test_generator, steps=1)
            result_predict = np.concatenate([np.array(i) for i in result_predict])
            max_result = np.amax(result_predict)
            max_result_index = np.array(np.argmax(result_predict, axis=0), ndmin=1)
            similar_cve = getCveSimilarity(cve_vector_list, dataset[max_result_index[0]])
            similar_cve_df = df.iloc[similar_cve[1],:]

            if max_result >= 0.5:
                vulnerable_list.append((subdir.split("%")[1], max_result * 100,
                                        VULNERABILITY_TYPE[VULNERABILITY_FILE.index(filename)], similar_cve_df["CVE_ID"]))


    K.clear_session()

    vulnerable_list = getSimilarCveList(vulnerable_list)

    return vulnerable_list


# classifier_data = np.reshape(realdata[0],(len(realdata[0]),1,vector_dim))
# f.close()
# test_generator = generator_of_data(realdata[0], realdata[1], 1, len(realdata[0])-1, vector_dim)
# # test_data = np.concatenate(realdata[0]).ravel()
# labels = model.predict_generator(test_generator, steps=len(realdata[0]))



def getDetectionsSys(working_directory):
    vectorDim = 30
    maxLen = 1
    layers = 2
    dropout = 0.2
    realtestdataSetPath = working_directory + "vector/"
    weightPath = './sysevr/ml_models/BRGU_full_fast_2'
    vulnerable_list = testrealdata(realtestdataSetPath, weightPath, maxLen, vectorDim, layers, dropout)
    return vulnerable_list