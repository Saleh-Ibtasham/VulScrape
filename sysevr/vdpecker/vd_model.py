from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional, LeakyReLU
from keras.optimizers import Adamax
import pickle,os
from keras import backend as K
from ..slicer.preprocess_dl_Input_version5 import *
from ..slicer.vul_types import VULNERABILITY_TYPE, VULNERABILITY_FILE
from fastembed.predictor.lookup import *

def build_model(vector_length):
    model = Sequential()
    model.add(Bidirectional(LSTM(300), input_shape=(1, vector_length)))
    model.add(Dense(300))
    model.add(LeakyReLU())
    model.add(Dropout(0.5))
    model.add(Dense(300))
    model.add(LeakyReLU())
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))
    # Lower learning rate to prevent divergence
    adamax = Adamax(lr=0.002)
    model.compile(adamax, 'categorical_crossentropy', metrics=['accuracy'])
    return model

def getDetectionsVd(working_directory):
    weightPath = './sysevr/ml_models/complete_cgd_binary_small_model.h5'
    vector_length = 30
    maxlen = 1
    K.clear_session()
    model = build_model(vector_length)
    model.load_weights(weightPath)
    model_input_path = working_directory + "vector/"

    print("Loading data...")
    vulnerable_list = []
    df = pd.read_csv("./fastembed/ml_models/CVE_vector_list.csv", index_col=0)
    cve_vector_list = df.iloc[:,2:].to_numpy()

    for subdir in os.listdir(model_input_path):
        print(subdir)
        for filename in os.listdir(os.path.join(model_input_path, subdir)):
            if filename != VULNERABILITY_FILE[0]:
                continue
            print(filename)
            f = open(model_input_path + subdir + "/" + filename, "rb")
            dataset, labelsfile, funcsfiles, filenamesfile, testcasesfile = pickle.load(f)
            f.close()
            if len(dataset) == 0:
                continue

            test_generator = generator_of_data_vd(dataset, labelsfile, len(dataset), maxlen, vector_length)

            binary_predict = model.predict_generator(test_generator, steps=1)
            result_predict = []
            for result in binary_predict:
                result_predict.append(result[1])
            max_result = np.amax(result_predict)
            max_result_index = np.array(np.argmax(result_predict, axis=0), ndmin=1)
            similar_cve = getCveSimilarity(cve_vector_list, dataset[max_result_index[0]])
            similar_cve_df = df.iloc[similar_cve[1], :]

            # if max_result >= 0.45:
            vulnerable_list.append((subdir.split("%")[1], max_result * 100,
                                    VULNERABILITY_TYPE[VULNERABILITY_FILE.index(filename)], similar_cve_df["CVE_ID"]))

    K.clear_session()

    vulnerable_list = getSimilarCveList(vulnerable_list)

    return vulnerable_list

