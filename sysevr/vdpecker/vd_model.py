from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional, LeakyReLU
from keras.optimizers import Adamax
import pickle,os


def build_model(vector_length):
    model = Sequential()
    model.add(Bidirectional(LSTM(300), input_shape=(vector_length, vector_length)))
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
    weightPath = './sysevr/ml_models/complete_cgd_binary_model.h5'
    vector_length = 50
    model = build_model(vector_length)
    model.load_weights(weightPath)
    model_input_path = working_directory + "model_input/"

    vulnerable_list = []
    for filename in os.listdir(model_input_path):
        print(filename)
        f = open(model_input_path + filename, "rb")
        realdata = pickle.load(f)
        f.close()

        labels = model.predict(x=realdata[0], batch_size=64)
        for i in range(len(labels)):
            if labels[i][0] >= 0.5:
                print(realdata[1][i])
                vulnerable_list.append((filename, realdata[4][i]))

    return vulnerable_list

