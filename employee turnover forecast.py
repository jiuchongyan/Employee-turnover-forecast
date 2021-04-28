__author__ = 'samsung'
import pandas as pd
train=pd.read_csv('train.csv',index_col=0)
test=pd.read_csv('test.csv',index_col=0)

#print(train['Attrition'].value_counts())
# ����Attrition�ֶ�
train['Attrition']=train['Attrition'].map(lambda x:1 if x=='Yes' else 0)
from sklearn.preprocessing import LabelEncoder
# �鿴�����Ƿ��п�ֵ
#print(train.isna().sum())

# ȥ��û�õ��� Ա�����룬��׼��ʱ��=80��
train = train.drop(['EmployeeNumber', 'StandardHours'], axis=1)
test = test.drop(['EmployeeNumber', 'StandardHours'], axis=1)

# ���ڷ���������������ֵ����
attr=['Age','BusinessTravel','Department','Education','EducationField','Gender','JobRole','MaritalStatus','Over18','OverTime']
lbe_list=[]
for feature in attr:
    lbe=LabelEncoder()
    train[feature]=lbe.fit_transform(train[feature])
    test[feature]=lbe.transform(test[feature])
    lbe_list.append(lbe)
#train.to_csv('temp.csv')
#print(train)

import xgboost as xgb
from sklearn.model_selection import train_test_split

param = {'boosting_type':'gbdt',
                         'objective' : 'binary:logistic', #
                         'eval_metric' : 'auc',
                         'eta' : 0.01,
                         'max_depth' : 15,
                         'colsample_bytree':0.8,
                         'subsample': 0.9,
                         'subsample_freq': 8,
                         'alpha': 0.6,
                         'lambda': 0,
        }
X_train, X_valid, y_train, y_valid = train_test_split(train.drop('Attrition',axis=1), train['Attrition'], test_size=0.2, random_state=42)

train_data = xgb.DMatrix(X_train, label=y_train)
valid_data = xgb.DMatrix(X_valid, label=y_valid)
test_data = xgb.DMatrix(test)

model = xgb.train(param, train_data, evals=[(train_data, 'train'), (valid_data, 'valid')], num_boost_round = 10000, early_stopping_rounds=200, verbose_eval=25)
predict = model.predict(test_data)
test['Attrition']=predict
print(predict)
# ת��Ϊ���������
#test['Attrition']=test['Attrition'].map(lambda x:1 if x>=0.5 else 0)
test[['Attrition']].to_csv('submit_xgb.csv')
