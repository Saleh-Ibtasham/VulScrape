import pandas as pd
from .classifier import get_result
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def getCveList(cve_list):
    df_feature = pd.read_csv("./fastembed/ml_models/CVE_data_with_features.csv")
    df_classifier = pd.read_csv("./fastembed/ml_models/CVE_classifier_data_with_features.csv")

    cve_list = cve_list.split(",")
    result_cve_list = []
    for index, value in enumerate(cve_list):
        result_cve_list.append("CVE-" + value.strip())

    result_feature_df = df_feature.loc[df_feature['ID'].isin(result_cve_list)]
    classifier_df = df_classifier.loc[df_classifier['ID'].isin(result_cve_list)]

    print(result_cve_list)

    if classifier_df.shape[0] != 0:
        result_probability, result_truth = get_result(classifier_df.iloc[:,1:])
        print(result_probability,result_truth)
        result_feature_df["Exploited"] = result_truth
        print(result_feature_df["Exploited"])
        result_feature_df["Exploited_score"] = result_probability
        print(result_feature_df["Exploited_score"])


    result_feature_df["id"] = result_feature_df.index
    return result_feature_df


def getCveSimilarity(df, data):
    result_feature_df = []
    data = np.reshape(data,(1,30))
    result_similarities = cosine_similarity(data, df)
    max_similarity = np.amax(result_similarities[0])
    max_similarity_index = np.array(np.argmax(result_similarities[0], axis=0), ndmin=1)
    # print(max_similarity, max_similarity_index[0])
    result_feature_df.append(max_similarity)
    result_feature_df.append(max_similarity_index[0])

    return result_feature_df

def getSimilarCveList(cve_list):
    df_feature = pd.read_csv("./fastembed/ml_models/CVE_data_with_features.csv")

    result_cve_list = [cve[3] for cve in cve_list]

    result_feature_df = df_feature.loc[df_feature['ID'].isin(result_cve_list)]

    if result_feature_df.shape[0] == 0:
        return

    print(result_cve_list)

    result_df = None
    id = 0
    for cve in cve_list:
        temp_df = result_feature_df.loc[result_feature_df["ID"] == cve[3]]
        temp_df["VULNERABILITY_KIND"] = cve[2]
        temp_df["VULNERABILITY_RISK"] = cve[1]
        temp_df["Source_code"] = cve[0]
        temp_df["id"] = id
        result_df = pd.concat([result_df,temp_df])
        id += 1

    return result_df


