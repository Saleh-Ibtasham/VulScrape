import pandas as pd
from .classifier import get_result

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

    print(result_feature_df,classifier_df)
    if classifier_df.shape[0] != 0:
        result_probability, result_truth = get_result(classifier_df.iloc[:,1:])
        print(result_probability,result_truth)
        result_feature_df["Exploited"] = result_truth
        print(result_feature_df["Exploited"])
        result_feature_df["Exploited_score"] = result_probability * 100
        print(result_feature_df["Exploited_score"])


    result_feature_df["id"] = result_feature_df.index
    return result_feature_df


