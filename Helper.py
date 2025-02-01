from Files import Files
import os, sys, time, re
import string, random
from difflib import SequenceMatcher
from collections import Counter
from Algorithms import Algorithms
from spellchecker import SpellChecker
from pygame import mixer  # Load the popular external library
from gtts import gTTS # Import the required module for text-to-speech conversion
#from Chatbot import Chatbot


allow_restart = True # Allow the system to restart if an entered utterance is classified as 'restart'.
use_lev = True # Use the Levenshtein edit or not. It is also a configurability rule of the dialog system.
text_to_speech = True # Whether the chatbot speaks or not.
change_pref = True # Allow the user to change preferences after their first choice. If we dont allow it, we should definitely allow the system to restart, because in such cases we restart the chat. 

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return(result_str)

def create_mp3_file(mytext):   
    # Language in which you want to convert
    language = 'en'
    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)
    
    if(text_to_speech):
        # Saving the converted audio in a mp3 file named welcome
        path = "C:/Users/yugio/Projects/MAIR/Chatbot/audio_files/" 
        random_string = get_random_string(5)
        file = random_string + ".mp3"
        final_path = path + file 
        myobj.save(final_path)
        mixer.init()
        mixer.music.load(final_path)
        mixer.music.play()
    

class Helper():

    def __init__(self,turns,starting_time,name) -> None:
        self.File3 = Files(name)
        self.df3 = self.File3.return_as_dataframe()
        self.turns = turns
        self.t_start = starting_time
        self.area_list = ['west', 'east', 'south', 'north', 'centre', 'center']
        self.price_list = ['cheap', 'expensive', 'moderate']
        self.type_food_list = list(set(self.df3["food"]))
        self.dont_mind_list = ['any', 'dont', 'anywhere', 'doesnt', 'mind', 'matter', 'care', 'anything', 'whatever']
        self.extra_information_list = ['phone', 'number', 'address', 'post', 'code', 'postcode', 'all', 'three', 'everything']
        self.reasoning_list = ['romantic', 'children', 'child', 'touristic', 'assigned' ,'seats', 'assigned seats']
        self.negate_list = ['wouldnt', 'dont', 'couldnt', 'not']
        self.vrisies_list = ['fuck', 'fucks', 'bastard', 'bitch', 'moron', 'fucking', 'idiot', 'stupid', 'blowjob', 'pussy', 'cock', 'asshole', 'fucker']
        self.vrisies = 0
        
    def clear_mp3_files(self, path):
        for file in os.listdir(path):
            if(file[-4:]=='.mp3'):
                try:
                    os.remove(path+file)
                except IOError:
                    print("------->", file)
                    print("The above file cannot be deleted because it is already opened on another app.")
    
    def Exit(self,inp):
        if(inp.lower()=='exit'):  
            print("SYSTEM: Thanks for using the chatbot. Goodbye!")     
            sys.exit()

    def Series_of_actions(self,lev):
        # lev: whether to use the levenshtein edit or not (configurability rule)
        self.turns += 1
        response = input('USER: ')
        response = response.lower()
        self.Exit(response) # It checks if the user entered 'exit' in order to terminate the chat immediately
        response = response.translate(str.maketrans('', '', string.punctuation)) # It remooves all punctuation marks
        if(lev==True):
            response = self.levenshtein_check(response) # It checks if any word of the entered phrase is misspelled
        if('center' in response.split()): # If the user types 'center' its actually a correct value for area, but the CSV corresponding value is 'centre' so we change it 
            response = response.replace('center','centre') 
        splitted_utterance = response.split()
        vrisia = set(splitted_utterance).intersection(self.vrisies_list)
        if(len(vrisia)>0):
            self.vrisies += 1
            if self.vrisies >= 2: 
                print("SYSTEM: Okay... I will terminate the conversation now")
                create_mp3_file("Okay... I will terminate the conversation now")
                time.sleep(4)
                sys.exit()
            print("SYSTEM: Sorry, but I don't think that you are speaking properly. If you say something like this again, I will terminate the conversation")
            #create_mp3_file("Go to hell mother fucker, I will shut down the conversation...")
            create_mp3_file("Sorry, but I don't think that you are speaking properly. If you say something like this again, I will terminate the conversation")
            time.sleep(10)
        return(response)

    def levenshtein_check(self,inp):
        # inp: the incoming utterance 
        inp_splitted = inp.split()
        hlist = [] 
        for i in inp_splitted:
            if(i=='touristic'): 
                hlist.append(i)
                continue
            hlist.append(SpellChecker().correction(i)) 
        return(' '.join(hlist)) # join the list to make it a utterance once again

    def Restart(self,inp,classed,dictionary): 
        if(classed=='restart'): # Restart the program only if we classify the utterance as restart.
            #chat = Chatbot('none','none','none', 0, dictionary, "C:/Users/yugio/Projects/MAIR/Chatbot/")
            if(allow_restart==True):
                #chat.Main()
                return None
            else:
                sys.exit()
        else: return True

    def similar(self, a, splitted_phrase): # This function finds the most similar string to 'a' in the list 'splitted_phrase' and changes that string with 'a'
        # a: a random string
        # splitted_phrase: a list which has as elements the strings of a splitted phrase
        similarity_indices = []
        for b in splitted_phrase:
            similarity_indices.append(SequenceMatcher(None, a, b).ratio())
        ind = similarity_indices.index(max(similarity_indices))
        if([*splitted_phrase[ind]][0]!=[*a][0]): # this means we have something like 'inexpensive'
            splitted_phrase[ind] = a
            most_similar = random.choice([j for j in self.price_list if j!=a])
        else:
            most_similar = a
            splitted_phrase[ind] = a
        return (splitted_phrase,most_similar)

    def check_distance(self,split,negate,element,thresshold):
      # split: a splitted utterance in its words-components 
      # negate: a negate word like the 'not'
      # element: another word 
      # thresshold: how much in terms of word a negation will be from a target word. We use this func to extract denials in sentences.
        if((abs(split.index(element) - split.index(negate)))<=thresshold):
            return(True)
        else: 
            return(False)
  
    def check_existance(self,inp,checking_list): # a function that checks if a word co-exists in an utterance input and a random (global) list
      #inp: incoming utteracnce
      #checking list: the list from which we check if any element is in the incoming utterance
        for i in checking_list:
            if (i in inp):
                return(True)
        return(False)

    def negation_check(self,inp,rlist,element,choices_list):
        # inp: incoming utterance
        # rlist: a list that will be probably one of area, price or type food lists
        # element: a value that has been pointed that as 'concern' because a negation may refers to it
        # choices_list: a list that eventually will contain all the right values (or value) that needs to be retuned for the preference extraction
        splitted_utterance, most_smlr = inp.split(), element
        match = set(splitted_utterance).intersection(self.negate_list)
        if(len(match)>0):
            negation = match.pop()
            splitted_utterance,most_smlr = self.similar(element,splitted_utterance)
            if(splitted_utterance.index(element)>splitted_utterance.index(negation)): 
                thress = 6 if self.negate_list.index(negation) != self.negate_list.index(self.negate_list[-1]) else 4
                if(self.check_distance(splitted_utterance,negation,element,thress)): 
                    choices_list = [j for j in rlist if j!=element] 
                else:
                    choices_list.append(element)
            else:
                choices_list.append(element)
        else:
            _,most_smlr = self.similar(element,splitted_utterance)
            if (most_smlr==element):
                choices_list.append(element)
            else: choices_list.append(most_smlr)
        if('center' in choices_list):
            choices_list = list(map(lambda x: x.replace('center', 'centre'), choices_list))
            if(Counter(choices_list)['centre'] == 1): # from collections
                choices_list.remove('centre')
        return(choices_list)

    def mapping_price(self,inp,price,dictionary):
        temp1 = re.findall(r'\d+', inp) # find number of digits through regular expression
        res2 = list(map(int, temp1))
        if(len(res2)>0):
            Max = max(res2)
            if('per' not in inp):
                print("SYSTEM: Do you mean per person?")
                create_mp3_file("Do you mean per person?")
                response = self.Series_of_actions(use_lev)
                response,classified = self.null_func(response.lower(),dictionary)
                if(classified!='affirm'):
                    if(Max<=50):
                        price = 'cheap'
                    elif(Max>=50 and Max<150):
                        price = 'moderate'
                    else:
                        price = 'expensive'
                    return(price)
                else:
                    if(Max<=20):
                        price = 'cheap'
                    elif(Max>=20 and Max<50):
                        price = 'moderate'
                    else:
                        price = 'expensive'
                    return(price)
            else:
                if(Max<=20):
                    price = 'cheap'
                elif(Max>=20 and Max<50):
                    price = 'moderate'
                else:
                    price = 'expensive'
                return(price)        
        else:
            return(price)

    def null_func(self,inp,dictionary):
        # inp: The incoming utterance
        # dictionary: The dictionary with the keywords 
        name = 'keyword_rule_algorithm_classification'
        algo = Algorithms(name,self.File3)
        cls = algo.keyword_rule_algorithm_classification_train(inp,dictionary) # Call the keyword rule to classify the incoming utterance
        print("Classified as: ", cls)
        existance = self.Restart(inp,cls,dictionary)
        if existance: pass
        else: return(inp,cls,existance)
        if(cls=='bye'):
            print('SYSTEM: Thanks for using the chatbot. Goodbye!') 
            create_mp3_file("Thanks for using the chatbot. Goodbye!")
            print()
            t_finish = time.time()
            print('Total Runtime: %.2f s' %(t_finish-self.t_start))
            print('The total number of turns that needed were: ', self.turns)
            sys.exit()
        if(len(inp)<2):  #if the input is just 1 letter it is probably a user's mistake and will be classified as 'null'
            cls = 'null'
        while(cls=='null'): # a while loop that checks if the input is still 'null'
            print("SYSTEM: Sorry, I can't understand you. Can you repeat it please?")
            create_mp3_file("Sorry, I can't understand you. Can you repeat it please?")
            response = self.Series_of_actions(use_lev)
            cls = algo.keyword_rule_algorithm_classification_train(response,dictionary)
            print("Classified as: ", cls) 
            self.Restart(inp,cls,dictionary)
            if existance: pass
            else: return(inp,cls,existance)
            if (cls=='hello'): # gives info when the input is classified as hello
                return(response,cls,existance)
            if(cls=='bye'): # again exits when is classified as 'bye'
                print('SYSTEM: Thanks for using the chatbot. Goodbye!')
                create_mp3_file("Thanks for using the chatbot. Goodbye!")
                print()
                t_finish = time.time()
                print('Total Runtime: %.2f s' %(t_finish-self.t_start))
                print('The total number of turns that needed were: ', self.turns)
                sys.exit()
            if(len(response)<2): #  classifies it as 'null' when only 1 letter is given
                cls = 'null'
            inp = response
        return(inp,cls,existance)
