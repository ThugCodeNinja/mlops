from scipy.stats import randint,uniform

LIGHTGM_PARAMETERS = {
    'n_estimators': randint(100,500),
    'max_depth': randint(5,50),
    'learning_rate': uniform(0.01,0.2),
    'num_leaves': randint(20,100),
    'boosting_type': ['dart','gbdt','goss']
}

RANDOM_SEARCH_PARAMETERS = {
    'n_iter': 4,
    'cv': 5,
    'verbose': 2,
    'scoring': "accuracy",
    'n_jobs': -1,
    'random_state': 42
}