import numpy as np
import pandas as pd

class Files():

    def __init__(self, file_name) -> None:
        self.df = pd.read_csv(file_name)
        self.dialog_data = np.array(self.df)
                
    def separete_labels_utt(self,my_list):
        self.my_list = my_list
        for i in self.dialog_data:
            for j in i[0]:
                if(j == ' '):
                    label_utt = i[0].split(' ', 1)
                    self.my_list.append(label_utt)
                    break

    def make_a_dataframe(self):
        self.dialog_data = np.array(self.my_list)
        self.dialog_frame = pd.DataFrame(self.dialog_data, columns=['Label', 'Utterance'])
        for i in range(len(self.dialog_frame)):
            self.dialog_frame.loc[i, "Utterance"] = self.dialog_frame.loc[i, "Utterance"].replace(";", "")
        return(self.dialog_frame,self.dialog_data)

    def keywords_lists(self):
        inform_list = ['thai', 'french', 'gastropub', 'matter']
        confirm_list = ['correct', 'does it']
        affirm_list = ['yes', 'right']
        request_list = ['what', 'how', 'which', 'type', 'phone', 'address', 'post', 'postcode']
        thankyou_list = ['thank']
        null_list = ['noise', 'uhm', 'eh', 'sil','unintelligible']
        bye_list = ['goodbye', 'bye']
        reqalts_list = ['what about', 'how about', 'anything', 'else', 'another', 'other']
        negate_list = ['no', 'nah']
        hello_list = ['hi', 'hey', 'hello']
        repeat_list = ['repeat', 'again']
        ack_list = ['okay', 'kay', 'fine', 'good']
        restart_list = ['start', 'restart']
        deny_list = ['wrong', "don't", 'not']
        reqmore_list = ['more'] 
        #all the keys that were used for each label put in one dictionary
        self.all_keys_list = [inform_list,reqalts_list,affirm_list,request_list,thankyou_list,null_list,bye_list,confirm_list,negate_list,hello_list,repeat_list,ack_list,restart_list,deny_list,reqmore_list]

    def create_dicitionaries(self):
        list_lab = list(self.dialog_frame.Label.unique())
        a, b = list_lab.index('confirm'), list_lab.index('reqalts') 
        list_lab[b], list_lab[a] = list_lab[a], list_lab[b]
        numbers = [i+1 for i in range(15)]
        self.my_dictionary = dict(zip(list_lab, numbers)) 
        self.inv_dictionary = {v: k for k, v in self.my_dictionary.items()} 
        self.labels_keys_dict = dict(zip(list_lab, self.all_keys_list)) 
        return(self.my_dictionary, self.inv_dictionary, self.labels_keys_dict)

    def to_numerical(self,a_list):
        numerical = []
        for i in range(len(a_list)):
            numerical.append(self.my_dictionary[a_list[i]])
        return(numerical)

    def nonsimilarity (self,actual, fake):
        pos_counter = np.zeros(15)
        for i in range(len(actual)):
            if (actual[i]!=fake[i]):
                pos_counter[actual[i]-1] = pos_counter[actual[i]-1] + 1
        max_values = np.where(pos_counter == np.amax(pos_counter))
        if (len(max_values[0])>1):
            print("Multiple values: ",max_values[0])
        return(self.inv_dictionary[max_values[0][0]+1])

    def return_as_dataframe(self):
        return(self.df)