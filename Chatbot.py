from Helper import Helper, create_mp3_file, use_lev, change_pref
import time, random, sys
import numpy as np
import pandas as pd
from Algorithms import Algorithms


class Chatbot():

    def __init__(self,area,price,food,state,dictionary,path) -> None:
        self.area = area
        self.price = price
        self.type_of_food = food
        self.state = state 
        self.dictionary = dictionary
        self.my_helper_obj = Helper(0,time.time(),'restaurant_info_upgrade.csv')
        self.path = path

    def Reasoning_rule(self, cand_rest, wanted):
        # cand_rest: a datafame with the candidate restuarants up to the point where the user has picked his/her preferences for area, price and type of food
        # wanted: the extra requirment that the user demands
        #This is a dictionary that takes the wanted consequent as a key and as a value a list containing two properties: the corresponding reasoning rule and a line of explanation.
        #A developer of the system can add or edit rules by just adding a new pair to this dictionary or edit one of the existing key-value pairs. 
        Reasoning_dict = { 'touristic': [(cand_rest['pricerange'] == 'cheap') & (cand_rest['quality'] == 1) & (cand_rest['food'] != 'romanian'), "And it is also touristic because it is a cheap restaurant with good quality of food"],
                        'children': [cand_rest['longstay'] == 0, "And it's also suitable for children because it has a fixed time of staying (short stay)"], 
                        'child' :  [cand_rest['longstay'] == 0, "And it's also suitable for children because it has a fixed time of staying (short stay)"], 
                      'romantic': [(cand_rest['longstay'] == 1) & (cand_rest['crowdedness'] == 0),"And it is also romantic because it allows you to stay for a long time"], 
                      'assigned': [cand_rest['crowdedness'] == 1, "And it also operates with assigned seats due to the high demand in reservations"],
                      'seats':  [cand_rest['crowdedness'] == 1, "And it also operates with assigned seats due to the high demand in reservations"], 
                      'assigned seats':  [cand_rest['crowdedness'] == 1, "And it also operates with assigned seats due to the high demand in reservations"] }

        final_df = cand_rest[Reasoning_dict[wanted][0]] # The wanted restaurants after the filtering with the reasoning rules
        mystr = Reasoning_dict[wanted][1] # A string which will justify why a possible restaurant has a respective attribute
        return(final_df, mystr)


    def check_restart(self, exist):
        if exist: 
            pass
        else: 
            chat = Chatbot('none','none','none', 0, self.dictionary, "C:/Users/yugio/Projects/MAIR/Chatbot/")
            chat.Main()
            sys.exit()


    def Reasoning(self, cand_rest):
        # cand_rest: all the candidate restaurants for a user preference up to the point where the user has picked his/her preferences for area, price and type of food
        print("SYSTEM: Do you have additional requirements?")
        create_mp3_file("Do you have additional requirements?")
        response = self.my_helper_obj.Series_of_actions(use_lev)
        response, classified, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
        self.check_restart(existance) 
        if((classified=='ack' or classified=='affirm') and len(response.split())<3): # if the user does not correspond positevely (with a 'yes' for example), continue
            print("SYSTEM: What would you like to have?")
            create_mp3_file(" What would you like to have?")
            response = self.my_helper_obj.Series_of_actions(use_lev)
            response, classified, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary) 
            self.check_restart(existance) 
        reasoning_match = set(response.split()).intersection(self.my_helper_obj.reasoning_list) # Intersection of the incoming utterance with the reasoning_list
        if(len(reasoning_match)>0): # Check if there is an intersection
            wanted = reasoning_match.pop()
            final_df,mystr = self.Reasoning_rule(cand_rest, wanted)
        else: # if there is no => return the same cand_rest and a void string.
            mystr = ""
            return(cand_rest,mystr)
        return(final_df,mystr)  

    def State_transition(self, inp, area, price, food_type, my_state):
        # inp: incoming utterance, area, price, food_type: obvious, my_state: the current state of the dialog
        multiple_areas_list, multiple_prices_list, multiple_foodtypes_list = [], [], [] # These lists are only used if the user enters a utterance with 2 preferences in the same category i.e. "spanish or italian restaurant"
        splitted_utterance = inp.split()
        for i in self.my_helper_obj.area_list:
            if(i in inp):
                multiple_areas_list = self.my_helper_obj.negation_check(inp,self.my_helper_obj.area_list,i,multiple_areas_list)
        if(len(multiple_areas_list)>0): # check the length because the input might not refer to area values at all
            id_random = random.randint(0,len(multiple_areas_list)-1) # if there are 2 or more preferances assign the final value at random
            area = multiple_areas_list[id_random] # possibly assign value to area
        price = self.my_helper_obj.mapping_price(inp,price,self.dictionary)
        for i in self.my_helper_obj.price_list:
            if(i in inp):
                multiple_prices_list = self.my_helper_obj.negation_check(inp,self.my_helper_obj.price_list,i,multiple_prices_list)  
        if(len(multiple_prices_list)>0):
            id_random = random.randint(0,len(multiple_prices_list)-1)
            price = multiple_prices_list[id_random]  # possibly assign value to price
        for i in self.my_helper_obj.type_food_list:
            if(i in inp):
                multiple_foodtypes_list = self.my_helper_obj.negation_check(inp,self.my_helper_obj.type_food_list,i,multiple_foodtypes_list)  
        if(len(multiple_foodtypes_list)>0):
            id_random = random.randint(0,len(multiple_foodtypes_list)-1)
            food_type = multiple_foodtypes_list[id_random]  # possibly assign value to type of food
        for i,k in enumerate(self.my_helper_obj.dont_mind_list):
            # Here we implement a pattern matching, but only to assign the 'any' category in the respective variables area,price,food_type. Also we nead a utterance of at least length 2
            if(k in splitted_utterance and len(splitted_utterance)>1): 
                index = splitted_utterance.index(k)
                if(len(splitted_utterance)-index) >= 2: # Check to see that the pattern happend at least in the peniultimate word of the incoming input => not to get out of indices
                    if(splitted_utterance[index+1]=='area' or splitted_utterance[index+1]=='place' or splitted_utterance[index+1]=='part'):
                        area = 'any'
                    if(splitted_utterance[index+1]=='price'):
                        price = 'any'
                    if(splitted_utterance[index+1]=='type' or splitted_utterance[index+1]=='food'):
                        food_type = 'any'
      
        #From now on the function will ask an extra question for each preference that still has the value 'none' after the initial stated preferences 
        #above, so that ultimately all of the preferences will have a value that is not 'none'. In this task we call also the 'reassign_var' function.
        while(area == 'none'or price == 'none'or food_type =='none'):
            if area == 'none':
                my_state = 2
                print("Current State: ", my_state)
                print('SYSTEM: What area?')
                create_mp3_file("What area?")
                response = self.my_helper_obj.Series_of_actions(use_lev)
                response,_,existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
                self.check_restart(existance) 
                match = set(response.split()).intersection(self.my_helper_obj.dont_mind_list) # Implementation of keyword matching for extraction of no preference ("any, dont care etc"). 
                #Ιf the user's input contains a "don't mind" utterance, we assign the 'any'variable
                match2 = set(response.split()).intersection(self.my_helper_obj.area_list)
                if (len(match)>0 and len(match2)==0): 
                    area = 'any'
                else: # otherwise we call the reassign function to update the values and the state
                    area = self.reassign_var(response,self.my_helper_obj.area_list,my_state)
            elif price == 'none':
                my_state = 3
                print("Current State: ", my_state)
                print('SYSTEM: What price?')
                create_mp3_file("What price?")
                response = self.my_helper_obj.Series_of_actions(use_lev)
                response, _, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
                self.check_restart(existance) 
                price = self.my_helper_obj.mapping_price(response, price,self.dictionary)
                if (price=='none'):
                    match = set(response.split()).intersection(self.my_helper_obj.dont_mind_list)  #If the user's input contains a "don't mind" utterance, we assign the 'any'variable
                    for i in self.my_helper_obj.price_list:
                        if i in response:
                            match2 = set(self.my_helper_obj.similar(i,response.split())[0]).intersection(self.my_helper_obj.price_list) 
                            break
                        else:
                            match2 = set(response.split()).intersection(self.my_helper_obj.price_list) 
                    if (len(match)>0 and len(match2)==0):
                        price = 'any'
                    else:
                        price = self.reassign_var(response,self.my_helper_obj.price_list,my_state)
            elif food_type == 'none':
                my_state = 4
                print("Current State: ", my_state)
                print('SYSTEM: What type of food?')
                create_mp3_file("What type of food?")
                response = self.my_helper_obj.Series_of_actions(use_lev)
                response, _, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
                self.check_restart(existance) 
                match = set(response.split()).intersection(self.my_helper_obj.dont_mind_list)  #If the user's input contains a "don't mind" utterance, we assign the 'any'variable
                macth2 = set(response.split()).intersection(self.my_helper_obj.type_food_list)
                if (len(match)>0 and len(macth2)==0):
                    food_type = 'any'
                else:
                    food_type = self.reassign_var(response,self.my_helper_obj.type_food_list,my_state)
        my_state = 5
        return(area,price,food_type,my_state) #return the final preferences (later they might change) of the user and the new state.


    def reassign_var(self,inp,rlist,my_st): 
        # inp: the incoming utterance
        # rlist: will be either type_of_food_list, price_list, or area_list, 
        # my_st: the current state that we are
        x = 'none' # Possibly will refer to area, price or food type. It depends on the rlist argument 
        splitted_input = inp.split()
        while(x=='none'): # loops so a not 'none' value is assigned to x => to 1 of the 3 desired categories
            for i in rlist:
                if(i in inp):
                    element_list = self.my_helper_obj.negation_check(inp,rlist,i,[]) 
                    x = random.choice(element_list)
            if(rlist==self.my_helper_obj.type_food_list and x=='none'): # if we refer to type of food then ask the user to enter a proper value for type of food 
                print("Current State: ", my_st)
                print("SYSTEM: There is no restaurant with such kind of food, ask for something else please")
                create_mp3_file("There is no restaurant with such kind of food, ask for something else please")
                response = self.my_helper_obj.Series_of_actions(use_lev)
                response, _, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary) 
                self.check_restart(existance) 
                dont_mind_match = set(response.split()).intersection(self.my_helper_obj.dont_mind_list) 
                foodtype_match = set(response.split()).intersection(self.my_helper_obj.type_food_list) # Implementation of keyword matching for extraction of preference that targets a food type preference
                if(len(dont_mind_match)>0):
                    x = 'any'
                if(len(foodtype_match)>0):
                    elm = foodtype_match.pop()
                    element_list = self.my_helper_obj.negation_check(response,rlist,elm,[]) 
                    x = random.choice(element_list)
            if(rlist==self.my_helper_obj.price_list and x=='none'): # if we refer to price then ask the user to enter a proper value for price 
                print("Current State: ", my_st)
                print("SYSTEM: This is not a category for price, please try again")
                create_mp3_file("This is not a category for price, please try again")
                response = self.my_helper_obj.Series_of_actions(use_lev)
                response, _, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
                self.check_restart(existance)
                x = self.my_helper_obj.mapping_price(response,x,self.dictionary)
                if(x=='none'):
                    dont_mind_match = set(response.split()).intersection(self.my_helper_obj.dont_mind_list)
                    price_match = set(response.split()).intersection(self.my_helper_obj.price_list) # Implementation of keyword matching for extraction of preference that targets a price preference
                    if(len(dont_mind_match)>0):
                        x = 'any'
                    if(len(price_match)>0 or (self.my_helper_obj.check_existance(response,rlist))):
                        if (len(price_match) > 0):
                            elm = price_match.pop() 
                        else:
                            for i in rlist: 
                                if i in response: 
                                    elm = set(self.my_helper_obj.similar(i,response.split())[0]).intersection(self.my_helper_obj.price_list).pop()
                        element_list = self.my_helper_obj.negation_check(response,rlist,elm,[])
                        x = random.choice(element_list)
            if(rlist==self.my_helper_obj.area_list and x=='none'): # if we refer to area then ask the user to enter a proper value for area 
                print("Current State: ", my_st)
                print("SYSTEM: There are no restaurants in this area, please choose a different area")
                create_mp3_file("There are no restaurants in this area, please choose a different area")
                response = self.my_helper_obj.Series_of_actions(use_lev)
                response, _, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
                self.check_restart(existance)
                dont_mind_match = set(response.split()).intersection(self.my_helper_obj.dont_mind_list)
                area_match = set(response.split()).intersection(self.my_helper_obj.area_list) # Implementation of keyword matching for extraction of preference that targets an area preference
                if(len(dont_mind_match)>0):
                    x = 'any'
                if(len(area_match)>0):
                    elm = area_match.pop()
                    element_list = self.my_helper_obj.negation_check(response,rlist,elm,[]) 
                    x = random.choice(element_list)

        return(x) 

    def restaurant_lookup(self, area, price, food_type, flag, print_fl):
        # area, price, food_type:  obvious
        # flag: a boolean variable that, in essence checks if there are options of the combination of the user's preference in the database-CSV and therefore if there is a recursive call
        # of the main function => chatbot. In such case we need to ensure that the first called functions (in recurssion) will terminate normally and that is what flag achieves. 
        # print_fl: Some times we dont need to print an option inside this function.
        df_result = self.my_helper_obj.df3 # df_result will be 3-4 times filtered (it depends on applyin reasoning rules) till we get the final options of restaurants.
        if area != 'any':
            df_result = df_result[df_result['area'] == area]
        if price != 'any':
            df_result = df_result[df_result['pricerange'] == price]
        if food_type != 'any':
            df_result = df_result[df_result['food'] == food_type]  
        if df_result.empty: # No options
            print("SYSTEM: No restaurants matching your criteria were found, please try something else!")
            create_mp3_file("No restaurants matching your criteria were found, please try something else!")
            time.sleep(7)
            flag = False
            self.Main() # If this occurs, transition back to input state so the user may try again
            return(df_result, None, pd.DataFrame(),"") # In case of recursion return the empty object so to terminate noramally 
        if(flag): # Only if we have at least 1 restaurant proposal for the user
            df_result, my_string = self.Reasoning(df_result) # After the final preferences regarding area, price and type of food and after the collateral that there is at least one option
            if not df_result.empty: 
                df_output = df_result.sample() 
                index = df_output.index.tolist()
                arr = np.array(df_output)
                if(print_fl==None):
                    print("SYSTEM SUGGESTION: ", arr[0][0].capitalize(), 'is a', arr[0][1].capitalize(), 'priced restaurant in the', arr[0][2].capitalize(), 'that serves', arr[0][3].capitalize(), 'food.', my_string)
                    create_mp3_file(arr[0][0].capitalize() + 'is a' + arr[0][1].capitalize() + 'priced restaurant in the' + arr[0][2].capitalize() + 'that serves' + arr[0][3].capitalize() + 'food.' + my_string)
                    time.sleep(12)
                return(df_result,index,df_output,my_string)
            else: # No options
                print("SYSTEM: No restaurants matching your criteria were found, please try something else!")
                create_mp3_file("No restaurants matching your criteria were found, please try something else!")
                time.sleep(6)
                flag = False
                self.Main() 
                return(df_result,None,pd.DataFrame(),"")

    def print_extraInfo(self,extra_info_asked,final_rest_choosed):
        # Applies some logic to print the demanded extra information from the user
        my_idx = list(final_rest_choosed.index) # taking the static index of the incoming dataframe
        f1, f2, f3 = False, False, False
        if (('phone' in extra_info_asked) or ('number' in extra_info_asked)):
            f1 = True
        if('address' in extra_info_asked):
            f2 = True
        if(('postcode' in extra_info_asked) or ('code' in extra_info_asked) or ('post' in extra_info_asked)):
            f3 = True
        if (('all' in extra_info_asked) or ('three' in extra_info_asked)):
            f1, f2, f3 = True, True, True
        if(f1 and not f2 and not f3):
            print("SYSTEM: Okay! The phone is: ", final_rest_choosed.at[my_idx[0],'phone'])
            create_mp3_file ('Okay! The phone is:' + final_rest_choosed.at[my_idx[0],'phone'])
        elif(not f1 and f2 and not f3):
            print("SYSTEM: Okay! The address is: ", final_rest_choosed.at[my_idx[0],'addr'])
            create_mp3_file ('Okay! The address is:' + final_rest_choosed.at[my_idx[0],'addr'])
        elif(not f1 and not f2 and f3):
            print("SYSTEM: Okay! The postcode is: ", final_rest_choosed.at[my_idx[0],'postcode'])
            create_mp3_file ('Okay! The postcode is:' + str(final_rest_choosed.at[my_idx[0],'postcode']))
        elif(f1 and f2 and not f3):
            print("SYSTEM: Okay! The phone is:", final_rest_choosed.at[my_idx[0],'phone'], "and the address is: ", final_rest_choosed.at[my_idx[0],'addr'])
            create_mp3_file("Okay! The phone is:" + final_rest_choosed.at[my_idx[0],'phone'] + "and the address is: " + final_rest_choosed.at[my_idx[0],'addr'])
        elif(f1 and not f2 and f3):
            print("SYSTEM: Okay! The phone is: ", final_rest_choosed.at[my_idx[0],'phone'], "and the postcode is: ", final_rest_choosed.at[my_idx[0],'postcode'])
            create_mp3_file("Okay! The phone is:" + final_rest_choosed.at[my_idx[0],'phone'] + "and the postcode is: " + str(final_rest_choosed.at[my_idx[0],'postcode']))
        elif(not f1 and f2 and f3):
            print("SYSTEM: Okay! The address", final_rest_choosed.at[my_idx[0],'addr'], "and postcode is: ",  final_rest_choosed.at[my_idx[0],'postcode'])
            create_mp3_file("Okay! The address is:" + final_rest_choosed.at[my_idx[0],'addr'] + "and the postcode is: " + str(final_rest_choosed.at[my_idx[0],'postcode']))
        else:
            print("SYSTEM: Okay! The phone is: ", final_rest_choosed.at[my_idx[0],'phone'], ", the address is: ", final_rest_choosed.at[my_idx[0],'addr'], "and the postcode is: ",  final_rest_choosed.at[my_idx[0],'postcode'])
            create_mp3_file("Okay! The phone is: " + final_rest_choosed.at[my_idx[0],'phone'] + ", " + "the address is: " + final_rest_choosed.at[my_idx[0],'addr'] + "and the postcode is: " + str(final_rest_choosed.at[my_idx[0],'postcode']))
            
    def AfterValues(self,inp,cand_rests,area,price,food_type,first,flg,strng,my_state):
        # inp: incoming utterance -- area,price,food_type: obvious
        # cand_rests: a dataframe of all candidate restaurnts that match the user preferances. It is actually passed by the look-up function to main and then here. We need in case the user request for alternatives
        # first: a dataframe of length 1 and the first proposal that the system gives. We need to handle some tough cases like: only one appropriate restaurant in the CSV or the calling of look-up function fails. 
        # flg: a boolean variable that also handles the difficult by itself case of recurssion
        # strng: Since we allow changes on preferences => we allow the changes of the reasoning rules applied so this string is the justification of the new reasoning rule
        # my_state: the current state of the dialog
        name = 'keyword_rule_algorithm_classification'
        algo = Algorithms(name,self.my_helper_obj.File3)
        df_output = first
        classified = algo.keyword_rule_algorithm_classification_train(inp,self.dictionary) # classify to see if an alternative is requested
        while(classified=='reqalts'):
            area_cross= set(inp.split()).intersection(self.my_helper_obj.area_list) # use intersections (keyword matching) to check if the user asked for a new preference in either of 3 categories
            price_cross = set(inp.split()).intersection(self.my_helper_obj.price_list)
            typefood_cross = set(inp.split()).intersection(self.my_helper_obj.type_food_list)
            if((len(typefood_cross)>0 or len(price_cross)>0 or len(area_cross)>0) and (change_pref==False)):
                print("SYSTEM: Sorry, you are not allowed to change preferences")
                create_mp3_file("Sorry, you are not allowed to change preferences")
                existance = self.my_helper_obj.Restart('restart','restart') # If the user tries to change preferances while it is not allowed, we restart the conversation
                self.check_restart(existance)
            if(len(cand_rests)==0 and len(typefood_cross)==0 and len(price_cross)==0 and len(area_cross)==0): 
                # If there are no altenatives (empty cand_rests) and we are sured that the user didnt changed his/her preferences we restart the conversation
                print("SYSTEM: Sorry there are no other alternatives that match your criteria.")
                create_mp3_file("Sorry there are no other alternatives that match your criteria.")
                time.sleep(6)
                flg = False
                self.Main()  # see below <----
                break
            print("Current State: ", my_state)
            print("SYSTEM: Okay, let's try again.")
            create_mp3_file("Okay, let's try again.")
            time.sleep(3)
            while(len(typefood_cross)>0 or len(price_cross)>0 or len(area_cross)>0): 
                # if the user changed at least 1 category pop the new preference out, update the respective variable and look-up again
                if(len(area_cross)>0):
                    area = area_cross.pop()
                if(len(price_cross)>0):
                    price = price_cross.pop()
                if(len(typefood_cross)>0):
                    food_type = typefood_cross.pop()
                print("Area:", area,"| ", "price:", price, "| ", "Type of food:", food_type)
                cand_rests,_,first,strng = self.restaurant_lookup(area, price, food_type, True, 0) # The 0 corresponds to the print_fl value. It doesnt matter what it is. We care only NOT to be None.
            if (first.empty): # if this holds it means that the look up failed on searching and we have a recurssive call from the look-up function, so we terminate this function => break
                break
            else: # else we print our new option of a restaurant
                df_output = cand_rests.sample()
                index = df_output.index.tolist()
                print("The remaining restaurants with these preferences are:", len(cand_rests)-1)
                cand_rests.drop(index, axis=0, inplace=True)
                arr = np.array(df_output)
                print("SYSTEM SUGGESTION: ", arr[0][0].capitalize(), 'is a', arr[0][1].capitalize(), 'priced restaurant in the', arr[0][2].capitalize(), 'that serves', arr[0][3].capitalize(), 'food.', strng)
                create_mp3_file(arr[0][0].capitalize() + 'is a' + arr[0][1].capitalize() + 'priced restaurant in the' + arr[0][2].capitalize() + 'that serves' + arr[0][3].capitalize() + 'food.' + strng)
                time.sleep(11)
                print("SYSTEM: Is that okay for you?")
                create_mp3_file("Is that okay for you?")
                response = self.my_helper_obj.Series_of_actions(use_lev) 
                inp = response.lower()
                inp, classified, existance = self.my_helper_obj.null_func(inp.lower(),self.dictionary)
                self.check_restart(existance)
                # Here we give to user the opportunity to change his mind wihtout using reqalts and we store the old values of area, price and type food so to detect the possible difference
                old_area, old_price, old_typefood = area, price, food_type
                area, price, food_type, my_state = self.State_transition(inp.lower(),area,price,food_type,my_state)
                if(old_area!=area or old_price!=price or old_typefood!=food_type):
                    if(change_pref==False): # again check if we are allowed to change preferences
                        print("SYSTEM: Sorry, you are not allowed to change preferences")
                        create_mp3_file("Sorry, you are not allowed to change preferences")
                        existance = self.my_helper_obj.Restart('restart','restart')
                        self.check_restart(existance)
                    print("Current State: ", my_state)
                    print("Area:", area,"| ", "price:", price, "| ", "Type of food:", food_type)
                    cand_rests,idx,first,strng = self.restaurant_lookup(area, price, food_type, True, None)
                    # Again we have an upcoming look-up for restaurants so we need to check if we succeded on finding any or if we recurssive called the main function
                    if(not first.empty):
                        response = self.my_helper_obj.Series_of_actions(use_lev)
                        inp = response.lower()
                        response, classified, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
                        self.check_restart(existance) 
                    else: # In case of recurssion => terminate normally
                        flg = False
                        break

        if classified == 'thankyou' or classified == 'negate' or classified == 'bye': # If the user does not ask for alternative or extra info, terminate the chat
            print('SYSTEM: Thanks for using the chatbot. Goodbye!')
            create_mp3_file("Thanks for using the chatbot. Goodbye!")
            return(df_output,7)

        else: # if the user stopped from changing his/her preferances and if we are not in a recurssive call, then give the extra information if requested 
            if(flg==True and classified!='reqalts'):
                my_state = 6
                print("Current State: ", my_state)
                extra_info_match = set(inp.split()).intersection(self.my_helper_obj.extra_information_list) # check if the user by himself/herself asked for something (by using keyword matching)
                if(len(extra_info_match)==0): # if not propose to him/her
                    print('SYSTEM: You can ask for the phone number, address or post code of the restaurant')
                    create_mp3_file("You can ask for the phone number, address or post code of the restaurant")
                    response = self.my_helper_obj.Series_of_actions(use_lev)
                    response, classified, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
                    self.check_restart(existance) 
                    extra_info_match = set(response.split()).intersection(self.my_helper_obj.extra_information_list) # make a new keyword matching for the new uttenrance
                    if classified == 'thankyou' or classified == 'negate' or len(extra_info_match)==0: # if not, terminate the chat
                        print('SYSTEM: Thanks for using the chatbot. Goodbye!')
                        create_mp3_file("Thanks for using the chatbot. Goodbye!")
                        return(df_output,7)
                if(len(extra_info_match)>0): # else find the extra info which is demanded
                    initial_length = len(extra_info_match) 
                    temp_list, extras_list = [],[]
                    for i in range(initial_length):
                        temp = extra_info_match.pop()
                        #extras_list = self.my_helper_obj.negation_check(response,self.my_helper_obj.extra_information_list,temp,extras_list)#NEW
                        #temp_list.append(extras_list[0]) #NEW 
                        temp_list.append(temp) # OLD
                    self.print_extraInfo(temp_list,df_output) # call the ExtraInfo with all the exra information asked to print
                my_state = 7
                return(df_output, my_state) # return the final dataframe (the user's choice) and the final state
            return(None,-1) # only for the case that we had a recurssive call of chatbot in <----- command line


    def Main(self):
        self.area, self.price, self.type_of_food, self.state = 'none', 'none', 'none', 0
        print("Current State: ", self.state) # The welcome state
        print("SYSTEM: Hello, welcome to the Cambridge restaurant system. You can ask for restaurants by area, price range or food type. How may I help you?")
        create_mp3_file("Hello, welcome to the Cambridge restaurant system. You can ask for restaurants by area, price range or food type. How may I help you?")
        response = self.my_helper_obj.Series_of_actions(use_lev) 
        response, classified, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
        self.check_restart(existance) 
        while (classified=='hello' or (classified!='inform' and classified!='request' and classified!='reqalts' and classified!='ack' and classified!='affirm' and classified!='deny')):
            # The Hello state, no preferences expressed. Loop here until we leave from the hello state
            self.state = 1 
            if(classified!='inform' and classified!='hello'):
                print("Current State: ", self.state)
                print("SYSTEM: Excuse me but I cannot understand you, can your repeat please?.")
                create_mp3_file("Excuse me but I cannot understand you, can you repeat please?")
            if(classified=='hello'):
                print("Current State: ", self.state)
                print("SYSTEM: Hi, please express your restaurant preferences regarding area, price and food type")
                create_mp3_file("Hi, please express your restaurant preferences regarding area, price and food type")
            response = self.my_helper_obj.Series_of_actions(use_lev)
            response, classified, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary) 
            self.check_restart(existance) 

        self.area, self.price, self.type_of_food, self.state = self.State_transition(response.lower(),self.area,self.price,self.type_of_food,self.state) 
        print("Current State: ", self.state)
        print("Area:", self.area,"| ", "price:", self.price, "| ", "Type of food:", self.type_of_food)

        chosen_rest,idx,fir_prop,mystr = self.restaurant_lookup(self.area, self.price, self.type_of_food, True, None) 
        if not chosen_rest.empty: # if there is at least 1 restaurant ask the user again for an input to verify if it is okay, if need extra info, or if he/she wants to request for something else  
            print("The remaining restaurants with these preferences are:", len(chosen_rest)-1)
            print("SYSTEM: Is that okay for you?")
            create_mp3_file("Is that okay for you?")
            response = self.my_helper_obj.Series_of_actions(use_lev)
            response, classified, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
            self.check_restart(existance) 
            if(classified!='reqalts'): 
                old_A, old_P, old_T = self.area, self.price, self.type_of_food
                self.area, self.price, self.type_of_food, self.state =  self.State_transition(response.lower(),self.area,self.price,self.type_of_food,self.state)
                while(old_A!=self.area or old_P!=self.price or old_T!=self.type_of_food): # if something is changed => look-up the CSV and make a new proposal if there are any options
                    old_A, old_P, old_T = self.area, self.price, self.type_of_food
                    if (change_pref==False): 
                        print("SYSTEM: Sorry, you are not allowed to change preferences")
                        create_mp3_file("Sorry, you are not allowed to change preferences")
                        existance = self.my_helper_obj.Restart('restart','restart') # If the user tries to change preferances while it is not allowed, we restart the conversation
                        self.check_restart(existance)
                    print("Current State: ", self.state)
                    print("Area:", self.area,"| ", "price:", self.price, "| ", "Type of food:", self.type_of_food)
                    chosen_rest,idx,fir_prop,mystr = self.restaurant_lookup(self.area,self.price,self.type_of_food, True, None)
                    if(not fir_prop.empty): 
                        response =  self.my_helper_obj.Series_of_actions(use_lev)
                        response, classified, existance = self.my_helper_obj.null_func(response.lower(),self.dictionary)
                        self.check_restart(existance) 
                    self.area,self.price,self.type_of_food,self.state = self.State_transition(response.lower(),self.area,self.price,self.type_of_food,self.state) # Make a new check for new values to exit or not the loop
            if(not chosen_rest.empty): # if indeed there are other options go to AfterValues and continue the convesation
                chosen_rest.drop(idx, axis=0, inplace=True)
                final_restaurant,self.state = self.AfterValues(response,chosen_rest,self.area,self.price,self.type_of_food,fir_prop,True,mystr,self.state)
            if(self.state==7): # The final state of the convesation
                print("Current (Final) State: ", self.state)
                print()
                t_finish = time.time()
                print('Total Runtime: %.2f s' %(t_finish-self.my_helper_obj.t_start))
                print('The total number of TURNS needed, were: ', self.my_helper_obj.turns)
                print()
                self.my_helper_obj.clear_mp3_files(self.path)