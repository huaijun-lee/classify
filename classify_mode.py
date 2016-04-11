from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
#from sklearn.naive_bayes import MultinomialNB
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
#from sklearn.externals import joblib
#from sklearn import metrics

class classifymode():
	"""docstring for classifymode"""
	def __init__(self,tuned_parameters):
		super(classifymode, self).__init__()
		self.tuned_para = tuned_parameters				
	def search_para(self,train_seg,train_label):
		print('支持向量机linear')
		print('开始训练模型')		
		scores = ['precision', 'recall']
		vect = TfidfVectorizer(ngram_range=(1,1), min_df=2, max_features=1000)
		xvec = vect.fit_transform(train_seg)
		X_train, X_test, y_train, y_test = train_test_split(xvec, train_label, train_size=0.7, random_state=0)
		for score in scores:
                    print("# Tuning hyper-parameters for %s" % score)
                    print()
                
                    clf = GridSearchCV(SVC(C=1), self.tuned_para, cv=5,
                                       scoring='%s_weighted' % score)
                    clf.fit(X_train, y_train)
                
                    print("Best parameters set found on development set:")
                    print()
                    print(clf.best_params_)
                    print()
                    print("Grid scores on development set:")
                    print()
                    for params, mean_score, scores in clf.grid_scores_:
                        print("%0.3f (+/-%0.03f) for %r"
                              % (mean_score, scores.std() * 2, params))
                    print()
                
                    print("Detailed classification report:")
                    print()
                    print("The model is trained on the full development set.")
                    print("The scores are computed on the full evaluation set.")
                    print()
                    y_true, y_pred = y_test, clf.predict(X_test)
                    print(classification_report(y_true, y_pred))
                    print()

class modeltest(object):
     """docstring for modeltest"""
     def __init__(self):
          super(modeltest, self).__init__()
     def test(self,train_seg,train_label):     
          vect = TfidfVectorizer(ngram_range=(1,1), min_df=1, max_features=1000)
          xvec = vect.fit_transform(train_seg)
          train_X, test_X, train_y, test_y = train_test_split(xvec, train_label, train_size=0.8, random_state=1)
          clf_lin = SVC(decision_function_shape='ovo')
          #clf_RFC = RandomForestClassifier(n_estimators=C)
          #clf_RFC.fit(train_X, train_y)
          #pre_result = clf_RFC.predict(test_X)
          clf_lin.fit(train_X, train_y)
          pre_result = clf_lin.predict(test_X)
          print(classification_report(test_y, pre_result))