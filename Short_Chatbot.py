from Helper import Helper, create_mp3_file, use_lev
from Algorithms import Algorithms
from Chatbot import Chatbot
import sys, time, random
import numpy as np
import pandas as pd


class Shorten_Chatbot():

    def __init__(self, area, price, food, dictionary, path) -> None:
        self.my_helper_obj = Helper(0,time.time(),'restaurant_info_upgrade.csv')
        self.a, self.p, self.t = area, price, food
        self.a_l, self.p_l, self.t_l = [], [], []
        self.dictionary = dictionary
        self.flag = True
        self.path = path

    def null_func_2(self,inp):
        algo  = Algorithms('keyword_rule_algorithm_classification',self.my_helper_obj.File3)
        cls = algo.keyword_rule_algorithm_classification_train(inp,self.dictionary)
        print("Classified as: ", cls)
        if(cls=='bye'):
            print('SYSTEM: Thanks for using the short version of chatbot. Goodbye!')
            create_mp3_file("Thanks for using the short version of chatbot. Goodbye!")
            print()
            t_finish = time.time()
            print('Total Runtime: %.2f s' %(t_finish-self.my_helper_obj.t_start))
            print('The total number of turns that needed were: ', self.my_helper_obj.turns)
            sys.exit()
        if(len(inp)<2):
            cls = 'null'
        while(cls=='null'):
            print("SYSTEM: Sorry, I cant understand you. Can you repeat please?")
            create_mp3_file("Sorry, I cant understand you. Can you repeat please?")
            response = self.my_helper_obj.Series_of_actions(use_lev)
            cls = algo.keyword_rule_algorithm_classification_train(response,self.dictionary)
            print("Classified as: ", cls)
            if (cls=='hello'):
                return(response,cls)
            if(cls=='bye'):
                print('SYSTEM: Thanks for using the short version of chatbot. Goodbye!')
                create_mp3_file("Thanks for using the short version of chatbot. Goodbye!")
                sys.exit()
            if(len(response)<2):
                cls = 'null'
            inp = response
        return(inp,cls)

    def reasoning_2(self, cand_rest, response):
        ek = set(response.split()).intersection(self.my_helper_obj.reasoning_list)
        if(len(ek)>0):
            wanted = ek.pop()
            if(wanted=='romantic'):
                final_df = cand_rest[cand_rest['longstay'] == 1]
            if(wanted=='children' or wanted=='child'):
                final_df = cand_rest[cand_rest['longstay'] == 0]
            if(wanted=='touristic'):
                final_df = cand_rest[(cand_rest['pricerange'] == 'cheap') & (cand_rest['quality'] == 1) & (cand_rest['food']!='romanian')]
            if(wanted=='assigned' or wanted=='seats' or wanted=='assigned seats'):
                final_df = cand_rest[cand_rest['crowdedness']==1]
        else: return(cand_rest, '')
        return(final_df, wanted)  
          
    def restaurant_lookup_2(self, a, p, t, flag=True):
        df_result = self.my_helper_obj.df3
        if a!='any' and a!='none':
            df_result = df_result[df_result['area'] == a]
        if p!='any' and p!='none':
            df_result = df_result[df_result['pricerange'] == p]
        if t!='any' and t!='none':
            df_result = df_result[df_result['food'] == t]  
        if(flag): return(df_result)

    def print_restaurants(self,chosen,w):
        print("The remaining restaurants with these preferences are: ", len(chosen))
        if(not chosen.empty):
            df_output = chosen.sample() 
            index = df_output.index.tolist()
            arr = np.array(df_output)
            if(len(w)>0):
                print("SYSTEM SUGGESTION: ", arr[0][0].capitalize(), 'is a', arr[0][1].capitalize(), 'priced and', w ,'restaurant in the', arr[0][2].capitalize(), 'that serves', arr[0][3].capitalize(), 'food.')
                create_mp3_file(arr[0][0].capitalize() + 'is a' + arr[0][1].capitalize() + 'priced and' + w + 'restaurant in the' + arr[0][2].capitalize() + 'that serves' + arr[0][3].capitalize() + 'food.')
                time.sleep(9)
            else:
                print("SYSTEM SUGGESTION: ",arr[0][0].capitalize(), 'is a', arr[0][1].capitalize(), 'priced restaurant in the', arr[0][2].capitalize(), 'that serves', arr[0][3].capitalize(), 'food.')
                create_mp3_file(arr[0][0].capitalize() + 'is a' + arr[0][1].capitalize() + 'priced restaurant in the' +  arr[0][2].capitalize() + 'that serves' + arr[0][3].capitalize() + 'food.')
                time.sleep(8)
            chosen.drop(index, axis=0, inplace=True)
        else: 
            print("SYSTEM: Sorry there are no restaurants that match your criteria.")
            create_mp3_file("Sorry there are no restaurants that match your criteria.")
            time.sleep(5)
            self.main()
            self.flag = False
            return(pd.DataFrame(),pd.DataFrame())
        return(chosen,df_output)
  
    def feature_extrector(self,inp):
        self.a_l, self.p_l, self.t_l = [], [], []
        self.a, self.p, self.t = 'none', 'none', 'none'
        tt = inp.split()    
        for i in self.my_helper_obj.area_list:
            if(i in inp):
                if('not'in inp):
                    self.a_l = [j for j in self.my_helper_obj.area_list if j!=i]
                else:
                    self.a_l.append(i)
        if(len(self.a_l)>0):
            self.a = random.choice(self.a_l)
            if (self.a=='center'):
                self.a = 'centre'
        for i in self.my_helper_obj.price_list:
            if(i in inp):
                if('not' in inp):
                    self.p_l = [j for j in self.my_helper_obj.price_list if j!=i]
                else:
                    self.p_l.append(i)
        if(len(self.p_l)>0):
            self.p = random.choice(self.p_l) 
        for i in self.my_helper_obj.type_food_list:
            if(i in inp):
                if('not' in inp):
                    self.t_l = [j for j in self.my_helper_obj.type_food_list if j!=i]
                else:
                    self.t_l.append(i)
        if(len(self.t_l)>0):
            self.t = random.choice(self.t_l) 
        for i,k in enumerate(self.my_helper_obj.dont_mind_list):
            if(k in tt and len(tt)>1):
                index = tt.index(k)
                if(tt[index+1]=='area' or tt[index+1]=='place', tt[index+1]=='part'):
                    self.a = 'any'
                if(tt[index+1]=='price'):
                    self.p = 'any'
                if(tt[index+1]=='type' or tt[index+1]=='food'):
                    self.t = 'any'

        print(self.a, self.p, self.t)
        chosen_rest = self.restaurant_lookup_2(self.a, self.p, self.t)
        chosen_rest,wanted = self.reasoning_2(chosen_rest,inp)
        if(self.a == 'none' and self.p == 'none' and self.t == 'none' and len(wanted)==0):
            print("SYSTEM: Okay, I assume that you dont have any preferences, so...")
            create_mp3_file("Okay, I assume that you dont have any preferences, so...")
            time.sleep(5)
        return (chosen_rest, self.a, self.p, self.t, wanted) 

    def extra_info(self,df_output):
        print('SYSTEM: You can ask for the phone number, address or post code of the restaurant')
        create_mp3_file("You can ask for the phone number, address or post code of the restaurant")
        response = self.my_helper_obj.Series_of_actions(use_lev)
        response,classified = self.null_func_2(response.lower())
        extra_info_match = set(response.split()).intersection(self.my_helper_obj.extra_information_list)
        if(classified!='bye' and classified!='negate' and classified!='deny' and len(extra_info_match)>0):
            if(len(extra_info_match)>0):
                initial_length = len(extra_info_match) 
                temp_list = []
                for i in range(initial_length):
                    temp = extra_info_match.pop()
                    temp_list.append(temp)
                Chatbot.print_extraInfo(None,temp_list,df_output) 
        else: 
            print('SYSTEM: Thanks for using the short version of chatbot. Goodbye!')
            create_mp3_file("Thanks for using the short version of chatbot. Goodbye!")

    def main(self):
        print("SYSTEM: Hello, welcome to the Cambridge restaurant system? You can ask for restaurants by area, price range or food type. How may I help you?")
        create_mp3_file("Hello, welcome to the Cambridge restaurant system. You can ask for restaurants by area, price range or food type. How may I help you?")
        response = self.my_helper_obj.Series_of_actions(use_lev) 
        response,classified = self.null_func_2(response.lower())
        initial_desire = response
        options,_,_,_, e = self.feature_extrector(response)
        options,proposed = self.print_restaurants(options,e)
        if (len(options)>=0 and self.flag==True):
            print("SYSTEM: Is that okay? Yes/No")
            create_mp3_file("Is that okay? Yes or No?")
            response = self.my_helper_obj.Series_of_actions(use_lev) 
            response,classified = self.null_func_2(response.lower())
            if(classified=='affirm'):
                pass
            if(classified=='restart'):
                self.main()
                sys.exit()
            while(classified=='negate'):
                if (len(options)>0):
                    options,proposed = self.print_restaurants(options,e)
                    print("SYSTEM: Is that okay? Yes/No")
                    create_mp3_file("Is that okay? Yes or No?")
                    response = self.my_helper_obj.Series_of_actions(use_lev) 
                    response,classified = self.null_func_2(response.lower())
                    if(classified=='restart'):
                        self.main()
                        break
                else:
                    print("SYSTEM: Sorry there are no other alternatives that match your criteria.")
                    create_mp3_file("Sorry there are no other alternatives that match your criteria.")
                    time.sleep(5)
                    self.main()
                    self.flag = False
                    break
            if(self.flag): 
                self.extra_info(proposed)
                print()
                t_finish = time.time()
                print('Total Runtime: %.2f s' %(t_finish-self.my_helper_obj.t_start))
                print('The total number of TURNS needed, were: ', self.my_helper_obj.turns)
                print()
                self.my_helper_obj.clear_mp3_files(self.path)