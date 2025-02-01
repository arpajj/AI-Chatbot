from Files import Files
from Chatbot import Chatbot
from Short_Chatbot import Shorten_Chatbot

File1 = Files('dialog_acts.csv')
File1.separete_labels_utt([])
data_as_frame, data_as_array = File1.make_a_dataframe()
File1.keywords_lists()
my_dict, inv_dict, labels_keys = File1.create_dicitionaries()


x = input("Do you prefer the Short or Long version of the Chatbot? [S/L] \n ----> ")

if x == 'L' or x.lower() == 'l':
    chat_obj = Chatbot('none', 'none', 'none', 0, labels_keys, "C:/Users/yugio/Projects/MAIR/Chatbot/audio_files/")
    chat_obj.Main()
elif x == 'S' or x.lower() == 's':
    short_chat = Shorten_Chatbot('none','none','none', labels_keys, "C:/Users/yugio/Projects/MAIR/Chatbot/audio_files/")
    short_chat.main()
else: print("You have made a mistake. Please run again the python file")
