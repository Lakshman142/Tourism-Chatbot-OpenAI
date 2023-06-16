from flask import Flask, render_template, request,redirect,url_for
from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import pyttsx3
import re
import openai
import pygame
import requests
import calendar

app = Flask(__name__)

openai.api_key = "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"
model_id = 'gpt-3.5-turbo'
def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation,
        temperature=0,
        max_tokens=3800
    )

    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation

# Set up Google Translate API
translator = Translator()

# Set up speech recognition
r = sr.Recognizer()

# Set up requests session with longer timeout
session = requests.Session()
session.timeout = 30

# Set up Google Translate API
translator = Translator()

# Set up speech recognition
r = sr.Recognizer()

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

def openaicall(prompt):
        conversation=[]
        conversation.append({'role': 'user', 'content': prompt})
        conversation = ChatGPT_conversation(conversation)
        response=conversation[-1]['content'].strip()
        return response

@app.route('/process', methods=['POST'])
def process():
    def source_text(source_lang,to_lang):
        # Listen to user's speech input
        while 1:
            with sr.Microphone() as source:
                print("Speak now:")
                audio = r.listen(source)

            # Convert speech to text
            try:
                user_input = r.recognize_google(audio, language=source_lang)
                print("You said: ", user_input)
                return user_input
            except sr.UnknownValueError:
                print("Sorry, could not understand your speech")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    source_lang = request.form['source_lang']
    to_lang = 'english'
    # invoking Translator
    user_input = source_text(source_lang,to_lang)
    translator = Translator()

    # Translating from src to dest
    text_to_translate = translator.translate(user_input, dest=to_lang)
    text = text_to_translate.text
    print(text)
    prompt0=text+"is that statement belong to tourism or travel domain. if it is not belonging to that domain say  \
    'no' only without any description. otherwise give 'yes'"
    response=openaicall(prompt0)
    neg=['no','not',"don't","can't","cannot","nope"]
    f=0
    for i in neg:
        if i in response:
            f=1
    if f==1:
        response="I am an AI chatbot.Ask about travel plan!"            
    else:
    # Translate response text to user's language
        translated_response = translator.translate(response, dest=source_lang)
        # Print translated response
        response_text = translated_response.text

        # Generate speech from response text
        speak = gTTS(text=response_text, lang=source_lang, slow=False)
        # Save speech to file
        speak.save("captured_voice.mp3")
            # Send user input to OpenAI API    
        prompt = "act like a tourism chatbot and answer" +text+"summarize the output"
        response=openaicall(prompt)

        print(response)        

# Translate response text to user's language
    translated_response = translator.translate(response, dest=source_lang)
            # Print translated response
    response_text = translated_response.text

            # Generate speech from response text
    speak = gTTS(text=response_text, lang=source_lang, slow=False)
            # Save speech to file
    speak.save("captured_voice.mp3")            
    return render_template('speech.html', response_text=response_text)
            

@app.route('/play_audio', methods=['POST'])
def play_audio():
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load sound file
    pygame.mixer.music.load('captured_voice.mp3')

    # Play sound file
    pygame.mixer.music.play()

    # Wait for sound to finish playing
    while pygame.mixer.music.get_busy():
        continue

    # Clean up pygame mixer
    pygame.mixer.quit()

    # Delete sound file
    os.remove('captured_voice.mp3')

    return render_template('speech.html')

@app.route("/")
def index():
    return render_template("interface.html")

@app.route('/speech')
def speech():
    return render_template('speech.html')

# define a route for the button that triggers the redirect
@app.route('/redirect')
def redirect_page():
    return redirect(url_for('speech'))

@app.route("/get")
def get_bot_response():
    months_abbr = list(calendar.month_abbr)[1:]
    months_full = list(calendar.month_name)[1:]
    all_months=months_full +[month.lower() for month in months_full]+months_abbr+[month.upper() for month in months_abbr]+[month.lower() for month in months_abbr]
    requirements=['type of trip','cuisine','budget','language','age','no of days']
    global responses
    if 'responses' not in globals():
        responses = []  # initialize the list of responses
    user_input = request.args.get("msg")
    responses.append(user_input)
    print(responses)
    if len(responses) == 1:
        global response
        response=""
        prompt=responses[0]+ "if the above text is a demographic location or real place return True" 
        conversation=[]
        conversation.append({'role': 'user', 'content': prompt})
        conversation = ChatGPT_conversation(conversation)
        response=conversation[-1]['content'].strip()
        neg1=['no','not','sorry','nope','cannot',"can't"]
        for i in neg1:
            if i in response.lower():
                responses.pop()
                return "Enter a valid place"
            else:
                return "In Which month do you want to visit?"
    
    elif len(responses)==2:  
        if responses[1] in all_months:
            return "Requirements:\n1.Type of Trip\n2.Cusine\n3.Budget\n4.Language\n5.Age\n6.No Of Days\nEnter number of requirements according to your preference."
        else:
            responses.pop()
            return "Enter a valid month"
        #return "Requirements:\n1.Type of Trip\n2.Cusine\n3.Budget\n4.Language\n5.Age\n6.No Of Days\nEnter number of requirements according to your preference."
    elif len(responses)==3 :
        if int(responses[2])>0 and int(responses[2])<7:
            global c
            global p_clist_req
            global p_list_add_nreq
            p_list_add_nreq=""
            p_clist_req=""
            global p_vlist_req
            p_vlist_req=""
            global c_add
            c_add=0
            global add_nreq
            add_nreq=0
            global nreq
            global cnreq
            global list_req
            global vlist_req
            vlist_req=[]
            list_req=[]
            global list_add_nreq
            list_add_nreq=[]
            nreq=int(user_input)
            print(nreq)
            cnreq=nreq
            c=nreq
            print(c)
            return "enter your requirement:"
        else:
            responses.pop()
            return "Enter a number between 1 and 6"
    elif c>1:
        list_req.append(user_input)
        print(list_req)
        c-=1
        return "enter your requirement:"
    elif len(responses)==3+cnreq:
        list_req.append(user_input)
        print(list_req)
        global clist_req
        clist_req=list_req.copy()
        for i in range(len(clist_req)):
            clist_req[i]=clist_req[i].lower()
        e=list_req.pop(0)
        return "Enter "+e
    elif len(list_req)>0:
        vlist_req.append(user_input)
        e=list_req.pop(0)
        return "Enter "+e
    elif len(responses)==3+(2*cnreq):
        if (len(list_req))==0:
            vlist_req.append(user_input)
        return "Do you want to add any additional requirements(y/n)?"
    elif len(responses)==3+(2*cnreq)+1:
        global choice
        choice=user_input
        if user_input.lower()=="y":
            return "Enter No Of Additional Reqirements You Want To Add:"
        if user_input.lower()=="n":
            print(add_nreq)
            return "do you want us to help with schedule a trip or best places to visit based on your requirements?\n(enter schedule trip/best places)"

    elif len(responses)==3+(2*cnreq)+2 and choice.lower()=='y':  
        add_nreq=int(user_input)
        print(add_nreq)
        c_add=add_nreq
        return "enter your requirement:"
    elif c_add>1:
        list_add_nreq.append(user_input)
        c_add-=1
        return "enter your requirement:"
    elif len(responses)==3+(2*cnreq)+2+add_nreq and choice.lower()=='y' :
        list_add_nreq.append(user_input)
        return "do you want us to help with schedule a trip or best places to visit based on your requirements?\n(enter schedule trip/best places)"
    elif (len(responses)==3+(2*cnreq)+2+add_nreq and user_input.lower()=="schedule trip")or (len(responses)==3+(2*cnreq)+2+add_nreq+1 and user_input.lower()=="schedule trip"):
        if "No Of Days".lower() not in clist_req:
            #print(clist_req)
            return "enter No Of Days:"
        else:
           
            for i in range(len(clist_req)):
                p_clist_req+=clist_req[i]+','
                p_vlist_req+=vlist_req[i]+","
            for j in range(len(list_add_nreq)):
                p_list_add_nreq+=list_add_nreq[j]+","
            prompt = "i would like to visit " + responses[0] +" in the month "+responses[1]+ "give a schedule trip for"+vlist_req[clist_req.index("no of days")]+"days"+"which includes"+p_clist_req[:-1]+"as"+p_vlist_req[:-1]+"and also include additional requirments like"+p_list_add_nreq[:-1]+"and aslo tell in which hotel to stay based on the above requirement which is include in the schedule of trip"
        response = openaicall(prompt)
        return response+"\n\n\n Are You Satisfied With The Response? say yes/no"
    elif (len(responses)==3+(2*cnreq)+2+add_nreq and user_input.lower()=="best places") :
        print(responses)
        prompt = "give response as if you are a tourist chatbot for this statement, i would like to visit " + responses[0] +" in the month "+responses[1]+ "give the best places to visit."
        response = openaicall(prompt)
        return response+"\n\n\n Are You Satisfied With The Response? say absolutely/never"
    elif (len(responses)==3+(2*cnreq)+2+add_nreq+1 and user_input.lower()=="best places")or(len(responses)==3+(2*cnreq)+2+add_nreq and user_input.lower()=="best places") :
        #print(responses)
        prompt = "i would like to visit " + responses[0] +" in the month "+responses[1]+ "give the best places to visit."
        response = openaicall(prompt)
        return response+"\n\n\n Are You Satisfied With The Response? say absolutely/never"

    elif (len(responses)==3+(2*cnreq)+2+add_nreq+1 and user_input.isdigit()):
        clist_req.append("no of days")
        vlist_req.append(user_input)
        prompt = "i would like to visit " + responses[0] +" in the month "+responses[1]+ "give a schedule trip for"+vlist_req[clist_req.index("no of days")]+"days"+"which includes"+p_clist_req[:-1]+"as"+p_vlist_req[:-1]+"and also include additional requirments like"+p_list_add_nreq[:-1]+"and aslo tell in which hotel to stay based on the above requirement which is include in the schedule of trip"
        response = openaicall(prompt)
        return response+"\n\n\n Are You Satisfied With The Response? say yes/no"
    elif (len(responses)==3+(2*cnreq)+2+add_nreq+2 and user_input.isdigit()):
        clist_req.append("no of days")
        vlist_req.append(user_input)
        prompt = "i would like to visit " + responses[0] +" in the month "+responses[1]+ "give a schedule trip for"+vlist_req[clist_req.index("no of days")]+"days"+"which includes"+p_clist_req[:-1]+"as"+p_vlist_req[:-1]+"and also include additional requirments like"+p_list_add_nreq[:-1]+"and aslo tell in which hotel to stay based on the above requirement which is include in the schedule of trip"
        response = openaicall(prompt)
        return response+"\n\n\n Are You Satisfied With The Response? say yeah/nope"
    elif user_input.lower()=="yes" or user_input.lower()=="yeah" or user_input.lower()=="absolutely":
        responses=[]
        return "Thank you for using our chatbot,visit again"
    
    elif user_input.lower()=="never":
        prompt = "i would like to visit " + responses[0] +" in the month "+responses[1]+ "give the best places to visit."
        response = openaicall(prompt)
        return response+"\n\n\n Are You Satisfied With The Response? say absolutely/never"
    elif user_input.lower()=="no":
        prompt = "i would like to visit " + responses[0] +" in the month "+responses[1]+ "give a schedule trip for"+vlist_req[clist_req.index("no of days")]+"days"+"which includes"+p_clist_req[:-1]+"as"+p_vlist_req[:-1]+"and also include additional requirments like"+p_list_add_nreq[:-1]+"and aslo tell in which hotel to stay based on the above requirement which is include in the schedule of trip"
        response = openaicall(prompt)
        return response+"\n\n\n Are You Satisfied With The Response? say yes/no"
    elif user_input.lower()=="nope":
        prompt = "i would like to visit " + responses[0] +" in the month "+responses[1]+ "give a schedule trip for"+vlist_req[clist_req.index("no of days")]+"days"+"which includes"+p_clist_req[:-1]+"as"+p_vlist_req[:-1]+"and also include additional requirments like"+p_list_add_nreq[:-1]+"and aslo tell in which hotel to stay based on the above requirement which is include in the schedule of trip"
        response = openaicall(prompt)

        return response+"\n\n\n Are You Satisfied With The Response? say yeah/nope"
            
    return response+"\n\n\n Are You Satisfied With The Response? say yes/no"

if __name__ =="__main__" :
    app.run(debug=True)