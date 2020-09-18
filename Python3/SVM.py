#%%
from sklearn import svm
import numpy
All_Data = numpy.loadtxt('./DataMining/DML.csv',dtype=float,delimiter=',')
test_data = All_Data[0:2000,0:53]
test_rlt =  All_Data[0:2000,54:]
#%%
validate_data = All_Data[1000:2000,0:53]
validate_rlt =  All_Data[1000:2000,54:55]
#%%
print(test_data.shape,test_rlt.shape,validate_data.shape,validate_rlt.shape)
clf = svm.SVC(C=0.02, kernel='rbf', gamma=0.02,coef0=1,tol=1,verbose=True, decision_function_shape='ovr')
clf.fit(test_data, test_rlt.ravel())
#%%
print(clf.score(validate_data, validate_rlt))
y_hat = clf.predict(validate_data)
#print(y_hat)

import pandas