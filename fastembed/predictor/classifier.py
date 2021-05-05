import lightgbm as lgb

def get_result(X_test):
    clf = lgb.Booster(model_file = "./fastembed/ml_models/lgb_classifier.txt")

    Y_pred = clf.predict(X_test)

    return ((Y_pred * 100 * 5) % 100), (((Y_pred * 100 * 5) % 100) > 50.00)