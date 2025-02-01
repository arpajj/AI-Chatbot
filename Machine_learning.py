from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
import warnings
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
import numpy as np
import matplotlib.pyplot as plt


class Machine_learning():

    def __init__(self, all_data, file_obj) -> None:
        self.y = all_data[:,0] 
        self.X = all_data[:,1] 
        self.count_vect = CountVectorizer()
        self.le = preprocessing.LabelEncoder()
        self.file_obj = file_obj

    def pre_processing (self):
        X_count = (self.count_vect).fit_transform(self.X) 
        print("X_encoded shape: ",X_count.shape)
        y_count = (self.le).fit_transform(self.y)
        print("y_encoded shape: ",y_count.shape)
        self.X_train_count, self.X_test_count, self.y_train_count, self.y_test_count = train_test_split(X_count, y_count, test_size=0.15, random_state=42) 
        print("X_train shape:", self.X_train_count.shape ,'|', "X_test shape:",self.X_test_count.shape, '|', "y_train shape:", self.y_train_count.shape, '|', "y_test shape:", self.y_test_count.shape)

    def ml_model_train_test(self,clf,mlname):
        warnings.simplefilter('ignore')
        clf.fit(self.X_train_count.astype(int), self.y_train_count.astype(int))
        scores = cross_val_score(clf, self.X_train_count.astype(int), self.y_train_count.astype(int), cv=5)
        print("The", mlname, "model on train set had %0.3f accuracy with a standard deviation of %0.2f" % (100*scores.mean(), 100*scores.std()))
        test_score = clf.score(self.X_test_count.astype(int), self.y_test_count.astype(int)) 
        results = clf.predict(self.X_test_count.astype(int))
        most_errors = self.file_obj.nonsimilarity(self.y_test_count.astype(int),results) 
        print("Accuracy on Test set for the", mlname, "model is: %0.3f"  %(100*test_score))
        print("The label on which the most errors are observed is: ", most_errors)
        warnings.filterwarnings('module') # or 'once', or 'always'
        return(100*test_score)

    def manual_input(self,clf,utterances_manual,inverse_dict):
        X_new_counts = (self.count_vect).transform(utterances_manual) 
        predicted = clf.predict(X_new_counts)
        for utt, category in zip(utterances_manual, predicted):
            print('%r => %s' % (utt, inverse_dict[category]))

    def pipeline_system(self,in_classifier,in_name):
        warnings.simplefilter('ignore')
        text_clf = Pipeline([('vect', self.count_vect),('clf', in_classifier)])
        text_clf.fit(self.X[0:int(0.85*len(self.X))], self.y[0:int(0.85*len(self.y))])
        predicted = text_clf.predict(self.X[int(0.85*len(self.X)):])
        warnings.filterwarnings('module')
        print("The accuracy of the", in_name, "pipeline system in test set is: %0.3f" %(100*np.mean(predicted == self.y[int(0.85*len(self.y)):])))
    
    def predict(self,inp, clf, inverse_dict): # a function that is used to predict manual inputs for machine learning models
        # inp: The incoming utterance, clf: One 1 of the 4 classifiers constructed to be used 
        X_new = self.count_vect.transform([inp])
        predicted = clf.predict(X_new)
        print(inverse_dict[predicted[0]])
        return(inverse_dict[predicted[0]]) 


class Machine_learning_model(Machine_learning):
    
    def decision_tree(self):
        self.classifier = DecisionTreeClassifier(random_state=0)
        return(self.classifier)

    def logistic_regression(self):
        self.classifier = LogisticRegression(random_state=0, max_iter=250)
        return(self.classifier)

    def support_vector_machine(self):
        self.classifier = svm.SVC(kernel='linear', C=1, random_state=42)
        return(self.classifier)

    def multi_layer_perceptron(self):
        self.classifier = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(7, ), max_iter=400, learning_rate_init=0.002, random_state=1)
        return(self.classifier)
    

def plot_results(all_results):
    models = ['Zero Rule','Keyword Rule','Decision Trees','LogisticRegression','SVM','MLP']
    d1 = np.arange(len(models))
    fig = plt.figure(figsize=(16,6))
    ax = fig.add_axes([0,0,1,1])
    plt.title("Algorithms Evaluation on Absolute Accuracy on Test set", fontsize=18)
    plt.xlabel('Algorithms', fontsize=18)
    plt.ylabel('Percentage (%)', fontsize=18)
    plt.ylim(0,110)
    plt.bar(d1,all_results, color='b',width=0.5)
    plt.xticks([r for r in range(len(models))], models,rotation=0)
    plt.yticks(np.arange(0,110,10))
    plt.grid(True)
    plt.show()