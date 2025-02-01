import matplotlib.pyplot as plt
import numpy as np
from random import randrange

class Algorithms():

    def __init__(self, algorithm_name, file_obj) -> None:
        self.al_name = algorithm_name
        self.file_obj = file_obj

    def zero_rule_algorithm_classification(self,all_data):
        print("Now you can test the zero rule algorithm by entering utterances (press 'exit' to exit)")
        output_values = [row[0] for row in all_data] 
        prediction = max(set(output_values), key=output_values.count) # calculate the max occuring label in the dataset
        x = input()
        while(x.lower()!='exit'):
            print("The most common label of the utterance entered is:", prediction)
            x = input()
        d_frame = self.file_obj.make_a_dataframe()[0]
        n_inform = d_frame[d_frame.Label == 'inform'] 
        print("The total number of correct classifications by the zero rule are:", n_inform.shape[0])
        print("The percentage accuracy of zero rule is %0.2f" % (n_inform.shape[0]/len(all_data)*100))
        return (n_inform.shape[0]/len(all_data)*100)
          
    def random_algorithm(self,all_data, flag):
        output_values = [row[0] for row in all_data] 
        unique = list(set(output_values)) #unique is a list with the 15 given labels of dialog acts 
        index = randrange(len(unique))
        prediction = unique[index]
        return prediction

    def keyword_rule_algorithm_classification(self,labels_keys_dict,all_data):
        print("Now you can test the keyword rule algorithm by entering utterances (press 'exit' to exit)")
        x = input()
        while(x.lower()!='exit'):
            flag = True 
            for i in labels_keys_dict.items(): 
                for j in i[1]: 
                    temp = x.lower().split(' ')
                    if(len(j.split())<2):
                        if(j.lower() in temp):
                            print("The most common label of the utterance entered is:", i[0])
                            flag = False
                            break
                    else:   
                        if(j.lower() in x.lower()):
                            print("This is a phrase keyword")
                            print("The most common label of the utterance entered is:", i[0])
                            flag = False
                            break
                if(flag==False):
                    break  
            if(flag==True): 
                print("random guess")
                prd = self.random_algorithm(all_data,True)
                print("The most common label of the utterance entered is:", prd)
            x = input()
        
    def keyword_rule_algorithm_classification_train(self,utterance,labels_keys_dict):
        flag = True
        for i in labels_keys_dict.items():
            for j in i[1]:
                temp = utterance.lower().split()
                if(len(j.split())<2):
                    if(j.lower() in temp):
                        flag = False
                        return i[0]
                else:
                    if(j.lower() in utterance.lower()):
                        flag = False
                        return i[0]
            if(flag==False):
                break   
        if(flag==True): 
            prd = 'inform'
            return prd

    def keyword_rule_algorithm_results(self,dialog_frame,labels_keys_dict):
        result_list = [] 
        for i in range(len(dialog_frame)): 
            result_list.append(self.keyword_rule_algorithm_classification_train(dialog_frame["Utterance"][i],labels_keys_dict)) 

        correct = 0
        label_column = list(dialog_frame['Label']) 
        for i in range(len(result_list)):
            if (label_column[i]==result_list[i]):
                correct += 1

        print("The total number of correct classifications by the keyword rule are:", correct)
        print("The percentage accuracy of keyword rule is %0.2f" % (correct/len(label_column)*100))
        numerical_column = self.file_obj.to_numerical(label_column)
        numerical_result = self.file_obj.to_numerical(result_list) 
        most_errors = self.file_obj.nonsimilarity(np.asarray(numerical_column), np.asarray(numerical_result))
        print("The label in which most errors are observed is: ", most_errors)
        return(correct/len(label_column)*100)
      
    def get_algorithm(self,data,dictionary):
        if (self.al_name == 'zero_rule_algorithm_classification'):
            n_info = self.zero_rule_algorithm_classification(data)
            return(n_info)
        elif(self.al_name == 'keyword_rule_algorithm_classification'):
            self.keyword_rule_algorithm_classification(dictionary,data)
            n_labels = self.keyword_rule_algorithm_results(self.file_obj.make_a_dataframe()[0],dictionary)
            return(n_labels)

    def Statistics(self,dialog_frame):  
        column0, column1 = dialog_frame["Label"], dialog_frame["Utterance"]
        len_list = []  
        for i in range(len(dialog_frame)):  
            len_list.append(len(column1[i].split()))

        unique = list(set(column0))
        all_indicies = [] 
        for t in unique:
            indices = [i for i, x in enumerate(list(column0)) if x == t]
            all_indicies.append(len(indices))

        d1 = np.arange(len(unique))
        fig = plt.figure(figsize=(16,6))
        ax = fig.add_axes([0,0,1,1])
        plt.title("Label distribution among the 15 classes", fontsize=18)
        plt.xlabel('Classes-Lables', fontsize=18)
        plt.ylabel('Number of instances', fontsize=18)
        plt.bar(d1,all_indicies, color='b',width=0.5)
        plt.xticks([r for r in range(len(unique))], unique,rotation=0)
        plt.grid(True)
        plt.show()
        print("The maximum utterance length in the dataset is: ", max(len_list))
        print("The minimum utterance length in the dataset is: ", min(len_list))
        print("The average utterance length in the dataset is:  %0.3f"  %np.mean(len_list))  
