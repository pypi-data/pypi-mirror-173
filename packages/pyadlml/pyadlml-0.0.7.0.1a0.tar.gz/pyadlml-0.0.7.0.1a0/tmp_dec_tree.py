import sys

from torch.autograd import Variable

from pyadlml.feature_extraction import TimeDiffExtractor

sys.path.append("../")
from pyadlml.dataset import set_data_home, fetch_amsterdam
set_data_home('/tmp/pyadlml_data_home2')
data = fetch_amsterdam(cache=True, retain_corrections=False)



from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV
from pyadlml.pipeline import Pipeline, TrainOrEvalOnlyWrapper, TrainOnlyWrapper, EvalOnlyWrapper
from sklearn.model_selection import cross_validate


from pyadlml.model_selection import train_test_split

print('splitting data in train and test set...')
X_train, X_test, y_train, y_test = train_test_split(
    data.df_devices,
    data.df_activities,
    split='leave_one_day_out')


from sklearn.tree import DecisionTreeClassifier
from pyadlml.preprocessing import CVSubset, StateVectorEncoder, LabelEncoder, DropTimeIndex, DfCaster, \
    RandomUnderSampler, DropNanRows
from pyadlml.model_selection import KFold, GridSearchCV
import numpy as np

steps = [
    ('encode_devices', StateVectorEncoder(encode='changepoint')),
    ('fit_labels', TrainOrEvalOnlyWrapper(LabelEncoder(idle=False))),
    #('train_split', TrainOnlyWrapper(CVSubset(np.arange(len(X_train))))),
    ('train_split', TrainOnlyWrapper(CVSubset())),
    #('test_split', EvalOnlyWrapper(CVSubset(np.arange(len(X_test))))),
    ('test_split', EvalOnlyWrapper(CVSubset())),
    ('drop_nans', TrainOrEvalOnlyWrapper(DropNanRows())),
    ('drop_time', DropTimeIndex()),
    ('df->np', DfCaster('df->np', 'df->np')),
    ('undersample', TrainOnlyWrapper(RandomUnderSampler(sampling_strategy='not minority'))),
    ('classifier', DecisionTreeClassifier())
]

pipe = Pipeline(steps).train()

# evaluate pipeline
n = 10
scoring_fcts = ['f1_macro', 'accuracy', 'recall']
param_grid = {
    #'undersample__sampling_strategy' : ['not majority', 'not minority'],
    'classifier__max_depth': [3, 4],
    #'classifier__min_samples_leaf': [1,2,3]
}


ts = KFold()

gscv = GridSearchCV(
    online_train_val_split=True,
    estimator=pipe,
    param_grid=param_grid,
    scoring=['accuracy'],
    verbose=2,
    refit='accuracy',
    n_jobs=-1,
    cv=ts
)

gscv = gscv.fit(X_train, y_train)
print('report: ', gscv.cv_results_)
print('best params: ', gscv.best_params_)
print('best score: ', gscv.best_score_)
