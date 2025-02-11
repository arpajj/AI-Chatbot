#  AI-Chatbot project:

#### This is a small application that recommends restaurants to potential customers by using information retrieval from a standard-small database (type of cuisines, areas etc). For operation (understanding & generation), the AI-Chatbot is based on logic, machine learning and hard-coded rules while processing the input utterances.   

## How to use:

__STEP 1__: Start by cloning the present repository by running: `git clone https://github.com/arpajj/AI-Chatbot.git`.

__STEP 2__: Install all the required packages from the [requirements file](./requirements.txt) by using: `pip install -r requirements.txt`.

__STEP 3__: If you are only interested to test/talk to the AI-Chatbot you can run the file [chatting.py](./chatting.py), by executing `python chatting.py`. If you do so, you will be asked if you want to chat with the "normal Chatbot" ([Chatbot.py](./Chatbot.py)) or with a "shortened version of the Chatbot" ([Short_Chatbot.py](./Short_Chatbot.py)).  

__STEP 4__: If you are also interested on the statistical analysis on the data that the project used, you can run the notebook [Runner.ipynb](./Runner.ipynb). In the end of this notebook you will be able to start chatting with the two versions of the Chatbot (as in the [chatting.py](./chatting.py) file). There you can also see two examples, one for each version of the Chatbot, of how the conversation between the _User_ and the _System_ is unfolding.

#### __Important Notes__:  
1) ✅ It is _highly recommended_ that, before trying to talk to the Chatbot, you first read some general instuctions of how to use it in the file [instructions_form.pdf](./instructions_form.pdf). There, you can see specific examples of how you could interact with the Chatbot and other relevant information. For instance, there are only certain types of cuisines that are accepted, which can be found under the file [cuisine_types.txt](./cuisine_types.txt).
2) ✅ It is also _highly recommended_ that, before trying to talk to the Chatbot, you first explore the original notebok of the project [AI_Chatbot_Final.ipynb](./AI_Chatbot_Final.ipynb). This notebook, which essentially encompasses the whole implementation and the front-end of the project, includes several examples of conversations that will help you understand how a chat is carried out between a _User_ and the _System_.  
