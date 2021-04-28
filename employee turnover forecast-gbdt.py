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

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

X_train, X_valid, y_train, y_valid = train_test_split(train.drop('Attrition',axis=1), train['Attrition'], test_size=0.2, random_state=42)

# ���ûع��㷨�����Եõ����õ�AUC���
model = GradientBoostingRegressor(random_state=10)
model.fit(X_train, y_train)
predict = model.predict(test)
print(predict)
test['Attrition']=predict
#print(predict)
# ת��Ϊ���������
#test['Attrition']=test['Attrition'].map(lambda x:1 if x>=0.5 else 0)
test[['Attrition']].to_csv('submit_gbdt.csv')
print('submit_gbdt.csv saved')


