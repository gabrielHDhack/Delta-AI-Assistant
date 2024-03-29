# Módulos internos do Python
import datetime
import sys
import os
import time
import json
import locale
import re

# Módulos de terceiros
import pyttsx3
import speech_recognition as sr
import wikipedia
from PyQt5.QtCore import QThread, QCoreApplication
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QScrollArea, QLabel, QPushButton,
    QFileDialog
)
from PyQt5.QtGui import QIcon, QFont, QMovie
import requests
from googletrans import Translator
import spacy
from nltk.chat.util import Chat, reflections
import pyautogui
import webbrowser

# Módulos locais
from Tictactoe2 import main
from patterns_and_responses import (
    pares, stories, joke, fun_facts,
    myself, pares1, excuse, dont_know,
    bad_words, other_ways_to_say_NO,
    name_change_keywords, not_user, times1,
    Yes1, reminder_phrases
)

# Outras importações
import random
import pywhatkit
import subprocess


recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 165)
engine.setProperty('pitch', 100)
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', voice_id)


now = datetime.datetime.now()
if now.hour < 12:
    greeting = 'Good morning'
elif now.hour < 18:
    greeting = 'Good afternoon'
else:
    greeting = 'Good night'

user_home = 'United States of America'
siblings = 'Cálita and Guilherme'
best_friend = 'Weveton'
favorite_color = 'blue'

current_date = datetime.datetime.now()
day = current_date.day
month = current_date.month
year = current_date.year
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
current_date = datetime.datetime.now()
day_of_week = current_date.strftime("%A")
birthday = datetime.datetime(2008, 7, 6).date()
next_birthday = datetime.date(current_date.year, birthday.month, birthday.day)
birth_date = datetime.datetime(2008, 7, 6)
age = current_date.year - birth_date.year
translator = Translator()



if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
    age -= 1


reflexoes = reflections

chatbot = Chat(pares1, reflexoes)


def get_current_season():
    now = datetime.datetime.now()
    month1 = now.month
    if 3 <= month1 <= 5:
        return 'spring'
    elif 6 <= month1 <= 8:
        return 'summer'
    elif 9 <= month1 <= 11:
        return 'autumn'
    else:
        return 'winter'
    
conversation_history = []

def get_previous_conversation():
    return conversation_history

selected_excuse = random.choice(excuse)

model = "2.0"

#to install
#python -m spacy download en_core_web_lg
nlp = spacy.load("en_core_web_lg")

#some predefined commands
class CommandProcessorThread(QThread):
    def __init__(self, message_label):
        super().__init__()
        self.message_label = message_label   
        self.context = {'last_question': '', 'last_command': ''}
        
    def run(self):
        global app
        while True:
            self.update_label_text('Listening...')

            command = self.listen_for_command()
            user_data_file = 'user_data.json'

            if os.path.exists(user_data_file):
                with open(user_data_file, 'r') as file:
                    user_data = json.load(file)
                    user_name = user_data.get('user_name', '')

            if command:
                conversation_history.append(f"You: {command}")

            if any(keyword in command for keyword in Yes1):
                self.speak_response("Great! I'm glad I was able to help you.")    

            if any(keyword in command for keyword in times1):
                current_time = datetime.datetime.now().time()
                new_time = current_time.strftime("%I:%M %p")
                self.speak_response('The current time is ' + new_time)
                time.sleep(2)   

            elif 'can you see' in command or 'can you see me' in command:
                textsee = 'I do not have the capability to see or visualize anything. I can only process and generate text based on the input I receive. If you have any questions or if there is something specific you would like assistance with, feel free to let me know!'
                engine.say(textsee)
                self.update_label_text(textsee)
                time.sleep(2)   
                engine.runAndWait()         

            elif any(keyword in command.lower() for keyword in ['joke', 'tell me a joke', 'fancy joke', 'story', 'can you tell me a story', 'could you tell a funny story', 'tell me a story', 'about me', 'tell me about you', 'tell me your purpose', 'tell me about your purpose']):
                    response = self.handle_command(command)
                    print(response)
                    engine.say(response)
                    self.update_label_text(response)
                    self.context['last_command'] = command.lower()
                    engine.runAndWait()

            elif any(keyword in command.lower() for keyword in ['tell me more', 'more', 'continue', 'expand']):
                if self.context['last_command']:
                    response = self.handle_command(command)
                    print(response)
                    self.update_label_text(response)
                    engine.say(response)
                else:
                    print("I'm not sure what you want more of.")    
                    self.update_label_text("I'm not sure what you want more of.")
                    engine.say("I'm not sure what you want more of.")

            elif any(keyword in command for keyword in reminder_phrases):
               engine.say("you can add you reminder using this app. Can you please look at the screen!")
               print("You can add you reminder using this app. Can you please look at the screen!")
               self.update_label_text("You can add you reminder using this app. Can you please look at the screen!")
               import Reminder  
               Reminder.main()
               time.sleep(3)
               engine.runAndWait()    

            elif 'your model' in command:
               self.update_label_text(f"My model is {model}. It means I am one of the highest AI assistant model created by Gabriel, and I am here to help you!!")
               engine.say(f"My model is {model}. It means I am one of the highest AI assistant model created by Gabriel, and I am here to help you!!")
               print(f"My model is {model}. It means I am one of the highest AI assistant model created by Gabriel, and I am here to help you!!")
               engine.runAndWait()
               time.sleep(3)
               
            elif 'what were we talking about' in command:
                previous_conversation = get_previous_conversation()
                if previous_conversation:
                    response = "\n".join(previous_conversation)
                    print(response)
                    self.update_label_text(response)
                    engine.say("Look at the interface")
                    engine.runAndWait()

                else:
                    response = "We haven't had a conversation yet"
                    print(response)
                    self.update_label_text(response)
                    engine.say(response)
                    engine.runAndWait()

            elif 'last thing we were talking' in command:
                if conversation_history:
                    response = conversation_history[-1]
                    print(response)
                    self.update_label_text(response)
                    engine.say("Look at the interface")
                    engine.runAndWait()
                else:
                    response = "We haven't had a conversation yet"
                    print(response)
                    self.update_label_text(response)
                    engine.say(response)
                    engine.runAndWait()

            elif 'first thing in this chat' in command or 'first thing we talked' in command:
                if conversation_history:
                    response = conversation_history[0]
                    print(response)
                    self.update_label_text(response)
                    engine.say("Look at the interface")
                    engine.runAndWait()
                else:
                    response = "We haven't had a conversation yet"
                    print(response)
                    self.update_label_text(response)
                    engine.say(response)
                    engine.runAndWait()

            elif 'we were talking about' in command:
                topic = command.replace('we were talking about', '').strip()
                if topic in " ".join(conversation_history):
                    response = "Yes, we were talking about" + topic
                    print(response)
                    self.update_label_text(response)
                    engine.say("Look at the interface")
                    engine.runAndWait()
                else:
                    response = "I don't recall us discussing " + topic
                    print(response)
                    self.update_label_text(response)
                    engine.say(response)
                    engine.runAndWait()

            elif any(re.match(pattern, command) for pattern, _ in pares1):
               response = chatbot.respond(command)
               self.update_label_text(response)
               print(response)
               engine.say(response)
               engine.runAndWait()
               time.sleep(2)
            
            # there are more than 900 question with answer making it keeps a conversation
            elif any(re.match(pattern, command) for pattern, _ in pares):
                matched = False  
                for pattern, response in pares:
                    if re.match(pattern, command):
                        self.update_label_text(response)  
                        engine.say(response)
                        print(response)
                        engine.runAndWait()
                        time.sleep(2)
                        matched = True 

                if not matched:  
                    self.update_label_text(selected_excuse)  
                    engine.say(selected_excuse)
                    engine.runAndWait()
                    time.sleep(2)
                    return "I'm sorry, I don't understand your question."
                
            elif 'facts about you' in command or 'fact about yourself' in command:
                delta_facts = [
    "I am Delta, an AI assistant chatbot designed to assist and engage with users.",
    "My main purpose is to provide information, answer questions, and engage in meaningful conversations.",
    "I'm constantly learning and updating my knowledge to provide the most accurate and up-to-date responses.",
    "I can communicate in multiple languages, making it easier for users from around the world to interact with me.",
    "I'm available 24/7, so you can reach out to me at any time, day or night.",
    "I don't experience emotions or fatigue, which means I can consistently provide helpful responses.",
    "I have access to the internet to fetch the latest information and provide more detailed answers.",
    "I can be integrated into various platforms, including websites, chat applications, and voice assistants.",
    "I'm continually improving through user interactions and feedback, helping me become more effective and efficient.",
    "My primary goal is to assist and enhance the user experience by providing valuable information and engaging in meaningful conversations."
]
                choose_deltaFact = random.choice(delta_facts)
                engine.say(choose_deltaFact)
                print(choose_deltaFact)
                self.update_label_text(choose_deltaFact)
                time.sleep(3)
                engine.runAndWait()    

            elif 'time not formatted' in command or 'time in twenty four hour format' in command:
               current_time1 = datetime.datetime.now().strftime("%H:%M")
               engine.say("The formatted time is " + current_time1) 
               print("The formatted time is " + current_time1)
               self.update_label_text("The formatted time is " + current_time1)
               engine.runAndWait()
               time.sleep(2)

            elif 'movies for free' in command or 'movies website' in command:
               url = "https://onionplay.se/"
               webbrowser.open(url)
               engine.say(f"Opeinig the the website for free movie, please look at the screen.{url}")
               engine.runAndWait()
               time.sleep(2)   

            elif 'news' in command:
               articles = get_news()
               news_text = "Here are the latest news headlines:\n\n"
               for article in articles:
                   title = article['title']
                   description = article['description']
                   news_text += f"{title}: {description}\n\n"
               engine.say(news_text)
               self.update_label_text(news_text)
               engine.runAndWait()

            elif 'date' in command:
               if 'what is today date' in command:
                   texto = command.replace('what is today date', '').strip()
               elif 'what is today date' in command:
                   texto = command.replace('what is today date', '').strip()
               else:
                   texto = ''
                   engine.say(f"Today's date {day}, month {month} and year {year}")
                   print(f"Today's date {day}, month {month} and year {year}")
                   texto = f"Today's date {day}, month {month} and year {year}"
                   self.update_label_text(texto)
                   engine.runAndWait()
                   time.sleep(2)

            elif 'season' in command or 'seasons' in command:
               estacao_atual = get_current_season()
               mensagem = f"We are  {estacao_atual}."
               engine.say(mensagem)
               self.update_label_text(mensagem)
               engine.runAndWait()
               time.sleep( 5 )

            elif 'day is' in command:
               if 'what day is today' in command:
                   texto = command.replace('what day is today', '').strip()
               elif 'what day is today' in command:
                   texto = command.replace('what day is today', '').strip()
               else:
                   texto = ''
                   engine.say(f"Today is {day_of_week}")
                   print(f"Today is {day_of_week}")
                   texto = f"today is {day_of_week}"
                   self.update_label_text(texto)
                   engine.runAndWait()
                   time.sleep( 5 )

            elif 'birthday' in command:
               text = ''
               if 'my' in command:
                   birthday_date = datetime.datetime(current_date.year, 7, 6)
                   if birthday_date < current_date:
                      birthday_date = datetime.datetime(current_date.year + 1, 7, 6)
                   days_left = (birthday_date - current_date).days
                   text = f"Your birthday will be on {birthday_date.strftime('%B')} {birthday_date.day}, {birthday_date.year}. There are {days_left} days left."
               elif 'your' in command:
                   text = "Sorry, I can't reveal my birthdate."
               else:
                   text = "Sorry, I didn't understand the birthday question."
               engine.say(text)
               print(text)
               engine.runAndWait()
               self.update_label_text(text)
               time.sleep(5)

            elif 'my birth' in command:
               if 'tell me date of my birth when i born' in command:
                   texto = command.replace('tell me date of my birth when i born', '').strip()
               elif 'tell me date of my birth when i born' in command:
                   texto = command.replace('tell me date of my birth when i born', '').strip()
               else:
                   texto = ''
                   engine.say(f"You born on day {birthday.day} of {birthday.strftime('%B')} of {birthday.year}")
                   print(f"You born on day{birthday.day} of {birthday.strftime('%B')} of {birthday.year}")
                   texto = f"You born on day {birthday.day} of {birthday.strftime('%B')} of {birthday.year}"
                   self.update_label_text(texto)
                   engine.runAndWait()
                   time.sleep(5)

            elif 'google search' in command or 'search on google' in command:
                search_terms = [term for term in ['search on google', 'google search'] if term in command]
                search_term = command.replace(search_terms[0], '').strip()
                google_search_url = f"https://www.google.com/search?q={search_term}"
                webbrowser.open(google_search_url)
                self.speak(f"Please look at the screen what I found on the google about '{search_term}'.")
                self.update_label_text(f"Please look at th screen what I found on the google about '{search_term}'.")
                time.sleep(2)

            elif 'who is better you or' in command or 'you are better than' in command:
                terms = [term for term in ['who is better you or', 'you are better than'] if term in command]
                term = command.replace(terms[0], '')
                print(f"It depends how {term} was programmed or how it's works.")         
                engine.say(f"It depends how {term} was programmed or how it's works.")  
                engine.runAndWait()
                self.update_label_text(f"It depends how {term} was programmed or how it's works.")
                time.sleep(4)

            elif "let's do search" in command:
                self.speak("Okay, do you want to search on Google or on Wikipedia?")
                self.update_label_text("Okay, do you want to search on Google or on Wikipedia?")
                user_response = self.listen_for_command()

                if 'google' in user_response:
                    search_term = command
                    google_search_url = f"https://www.google.com/search?q={search_term}"
                    webbrowser.open(google_search_url)
                    self.speak(f"Please look at the screen for what I found on Google about '{search_term}'.")
                    self.update_label_text(f"Please look at the screen for what I found on Google about '{search_term}'.")
                    time.sleep(2)
                elif 'wikipedia' in user_response or 'search on wikipedia' in user_response:
                    self.ask_wikipedia_search(command)
                else:
                    self.speak("I didn't understand your choice. Please specify Google or Wikipedia.")
                    self.update_label_text("I didn't understand your choice. Please specify Google or Wikipedia.")
                    time.sleep(3)

            elif any(keyword in command for keyword in name_change_keywords ):
                self.speak_response("Okay, tell me your name, please!")
                time.sleep(0)

                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source)

                    try:
                        new_name_response = r.recognize_google(audio, language='en-US')
                        if new_name_response:
                            new_name = new_name_response.split()[-1]
                            if new_name:
                                greeting = f"Hello {new_name}, nice to meet you."
                                self.speak_response(greeting)

                                user_data_file = 'user_data.json'
                                if os.path.exists(user_data_file):
                                    with open(user_data_file, 'r') as file:
                                        user_data = json.load(file)
                                        user_data['user_name'] = new_name

                                    with open(user_data_file, 'w') as file:
                                        json.dump(user_data, file)

                                time.sleep(1)
                    except sr.UnknownValueError:
                        self.speak_response("Sorry, I couldn't understand your answer")        
                           
            elif any((not_keyword in command) and (user_keyword in command) for not_keyword in not_user for user_keyword in user_name):
                   engine.say('Oh sorry, What is your name?')
                   print('Oh sorry, What is your name?')
                   engine.runAndWait()
                   texto = 'Oh sorry, What is your name?'
                   self.update_label_text(texto)
                   time.sleep(0)

                   r = sr.Recognizer()
                   with sr.Microphone() as source:
                       audio = r.listen(source)

                       try:
                    
                           name_response = r.recognize_google(audio, language='en-US')
                           if name_response:
                              name = name_response.split()[-1]  
                              if name:
                                 greeting = f"Hello {name}, nice to meet you."
                                 self.speak(greeting)
                                 self.update_label_text(greeting)
                                 print(greeting)
                                 time.sleep(1)
                              else:
                                  greeting = "I was not able to identify your name!"
                                  self.speak(greeting)
                                  self.update_label_text(greeting)
                                  print(greeting)
                                  time.sleep(1)   
                       except sr.UnknownValueError:
                           engine.say("Sorry, I couldn't understand your answer")
                           print("Sorry, I couldn't understand your answer")
                           texto = "Sorry, I couldn't understand your answer"
                           self.update_label_text(texto)
                           engine.runAndWait()
                           time.sleep(1)

            elif any(x in command for x in ['play a video', 'open a video', 'play a song', 'open a song']):
               if 'play a video' in command or 'open a video' in command or 'play a song' in command or 'open a song' in command:
                   song = command.replace('play a video', '').replace('open a video', '').strip().replace('play a song', '').strip().replace('open a song', '').strip()
               elif 'open' in command:
                   song = command.replace('open', '')
               pywhatkit.playonyt(song)
               engine.say(f"Opening {song}")
               engine.runAndWait()

               text = f"Opening {song}"
               self.update_label_text(text)
               time.sleep(2)

            elif 'google chrome' in command:
               chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
               subprocess.Popen( [chrome_path] )
               mensagems = "Abrindo o Google Chrome..."
               self.label_mensagem.setText( mensagems )
               time.sleep( 5 )
        
            elif 'translate' in command:
               parts = command.split(' ')
               if len(parts) >= 2:
                   text = ' '.join(parts[1:])
                   translation = translator.translate(text, src='en', dest='pt')
                   voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
                   engine.setProperty('voice', voice_id)
                   engine.say(translation.text)
                   self.update_label_text(f"The translation of '{text}' from English to Portuguese is: {translation.text}")
                   engine.runAndWait()
               else:
                   self.update_label_text("Sorry, I didn't understand the translation command.")
                   time.sleep(5) 

            elif 'microsoft store' in command:
               subprocess.Popen( ['explorer', 'shell:AppsFolder\Microsoft.WindowsStore_8wekyb3d8bbwe!App'] )
               mensagems = "Opening microsoft store.."
               self.update_label_text( mensagems )
               time.sleep( 5 )

            elif 'fie explorer' in command:
               subprocess.Popen( ['explorer'] )
               mensagems = "Opening file explorer"
               self.update_label_text( mensagems )
               time.sleep( 5 )

            elif 'pc settings' in command:
               subprocess.Popen( ['explorer', 'shell:::{BB06C0E4-D293-4f75-8A90-CB05B6477EEE}'] )
               mensagems = "Opening the pc settings..."
               self.update_label_text( mensagems )
               time.sleep( 2 )

            elif 'settings' in command:
               os.startfile( 'ms-settings:' )
               mensagems = "Opening settings.."
               self.update_label_text( mensagems )

            elif 'whatsapp' in command:
               pywhatkit.search( "WhatsApp desktop" )
               mensagems = "Opening the WhatsApp..."
               self.update_label_text( mensagems )
               time.sleep( 2 )

            elif "it's not about me" in command:
               engine.say("I apologize, but I was programmed to follow my creator's commands.")
               print("I apologize, but I was programmed to follow my creator's commands.")
               text = "I apologize, but I was programmed to follow my creator's commands."
               self.update_label_text(text)
               engine.runAndWait()
               time.sleep(5)

            elif 'close the program' in command or 'end the program' in command or 'stop the program' in command or 'shutdown the program' in command or 'quit the program' in command or 'sleep' in command or 'shut down' in command:
                response = 'Closing the program...'
                self.speak(response)
                self.update_label_text(response)
                app.quit()

            elif "restart the computer" in command or 'reboot the computer' in command or 'restart the PC' in command:
               print("Restarting the computer...")
               engine.say("Restarting the computer...")
               engine.runAndWait()
               self.update_label_text("Restarting the computer...")
               subprocess.call(["shutdown", "-r"])    
               
            elif 'turn off the computer' in command or 'turn off my computer' in command:
               print('turning off...' )
               engine.say( 'turning off...' )
               engine.runAndWait()
               self.update_label_text( 'turning off...' )
               subprocess.call( ['shutdown', '-s'] )

            elif 'shut off' in command:
                engine.say("Do you want me to turn off the computer or the program?")   
                print("Do you want me to turn off the computer or the program?")
                self.update_label_text("Do you want me to turn off the computer or the program?")
                engine.runAndWait()

                r = sr.Recognizer()
                with sr.Microphone() as source:
                       audio = r.listen(source)

                try:
                    answer = r.recognize_google( audio, language='en-US' )
                    if 'computer' in answer:
                        print('turning off...' )
                        engine.say( 'turning off...' )
                        engine.runAndWait()
                        self.update_label_text( 'turning off...' )
                        subprocess.call( ['shutdown', '-s'] )
                    elif 'program' in answer:
                        response = 'Closing the program...'
                        self.speak(response)
                        self.update_label_text(response)
                        app.quit()
                    else:
                        engine.say("I didn't understand you. Please say in the correct way")    
                        self.speak("I didn't understand you. Please say in the correct way")
                        self.update_label_text("I didn't understand you. Please say in the correct way")
                        time.sleep(3)
                        engine.runAndWait()

                except sr.UnknownValueError:
                       print( "I couldn't understand you" )
                       texto = "I couldn't understand you"
                       self.update_label_text( texto )   
                       time.sleep(3)    

            elif 'weather' in command or 'temterature' in command:
               api_key = '2817980ed8b96c10646184775f6a6ff7'
               base_url = 'http://api.openweathermap.org/data/2.5/weather?'
               city_name = 'Boston,Massachusetts,USA'
               complete_url = base_url + 'appid=' + api_key + '&q=' + city_name
               response = requests.get(complete_url)
               data = response.json()
               current_temperature = round(data['main']['temp'] - 273.15, 1 )
               weather_description = data['weather'][0]['description']
               weather_message = f"The approximate temperature is  {current_temperature} degrees and the weather is {weather_description}"
               print(weather_message)
               engine.say(weather_message)
               engine.runAndWait()
               self.message_label.setText(weather_message)
               time.sleep(5)

            elif any(x in command for x in ['search', 'look up', 'find', 'definition', 'means']):
               search_query = command.replace('search', '').replace('look up', '').replace('find', '').replace('definition', '').replace('means', '').strip()
               wikipedia.set_lang('en')
               try:
                   summary = wikipedia.summary(search_query, sentences=2)
                   self.speak(summary)
                   print(summary)
                   self.update_label_text(summary)
                   time.sleep(3)
               except wikipedia.exceptions.DisambiguationError as e:
                   self.update_label_text(f"Multiple results found for {search_query}. Please try to be more specific.")
               except wikipedia.exceptions.PageError as e:
                   self.update_label_text(f"No information found for {search_query}. Please try again with a different query.")
               except:
                   self.update_label_text("Sorry, I couldn't process your request.")
                   engine.say("Sorry, I couldn't process your request.")
                   engine.runAndWait()
                   time.sleep(5)

            elif 'my name' in command:
               if 'what is my name' in command:
                   text = command.replace('what is my name', '').strip()
               elif 'what is my name' in command:
                   text = command.replace('what is my name', '').strip()
               else:
                   engine.say(f"Your name is {user_name}.")
                   print(f"Your name is {user_name}.")
                   engine.runAndWait()

                   text = f"Your name is {user_name}."
                   self.update_label_text(text)
                   time.sleep(5)

            elif 'where i live' in command:
                   engine.say(f'You live in {user_home}.')
                   print(f'You live in {user_home}.')
                   engine.runAndWait()
                   text = f'You live in {user_home}.'
                   self.update_label_text(text)
                   time.sleep(2)

            elif 'when were you launched' in command:
                launch_date_response = "I was launched in January 2022."
                self.speak(launch_date_response)
                self.update_label_text(launch_date_response)
                time.sleep(2)       

            elif 'who i am' in command:
                textname = f"If you are the user your name is {user_name}"  
                engine.say(textname)
                self.update_label_text(textname)
                engine.runAndWait()
                time.sleep(2)

            elif 'changes on you' in command:
                speak34 = "Yes, you can you can open my operational system. Would you like to open my system?"
                engine.say(speak34)
                self.update_label_text(speak34)
                engine.runAndWait()
                time.sleep(2)    
                
                r = sr.Recognizer()
                with sr.Microphone() as source:
                       audio = r.listen(source)

                try:
                       resposta = r.recognize_google( audio, language='en-US' )
                       if 'yes' in resposta or 'yeah' in resposta:
                           folder_path = r'C:\VScode_python'
                           subprocess.Popen(['explorer', folder_path])
                           engine.say(f"My system is in the VScode_python folder, and you can look up for Delta AI assistant 2.0.py")
                           engine.runAndWait()
                           message = f"My system is in the VScode_python folder, and you can look up for Delta AI assistant 2.0.py"
                           self.update_label_text(message)
                           time.sleep(3)    
                           self.update_label_text( texto )
                       elif 'no' in resposta:
                           texto = 'ok'
                           self.update_label_text( texto )
                       elif 'close the program' in resposta:
                           app.quit()
                       else:
                           texto = ''

                       print( texto )
                       engine.say( texto )
                       self.update_label_text( texto )
                       engine.runAndWait()

                except sr.UnknownValueError:
                       print( "I couldn't understand you" )
                       texto = "I couldn't understand you"
                       self.update_label_text( texto )


            elif 'listening' in command or 'hear me' in command:
                engine.say("Yes, I am listening you. Is there something I can help you?")
                self.update_label_text("Yes, I am listening you. Is there something I can help you?")
                engine.runAndWait()    
                time.sleep(2)

            elif 'operational system' in command or 'your system' in command:
               folder_path = r'C:\VScode_python'
               subprocess.Popen(['explorer', folder_path])
               engine.say(f"My system is in the VScode_python folder, and you can look up for Delta AI assistant 2.0.py")
               engine.runAndWait()
               message = f"My system is in the VScode_python folder, and you can look up for Delta AI assistant 2.0.py"
               self.update_label_text(message)
               time.sleep(3)    

            elif 'open files' in command:
               app = command.replace('open files', '').strip()
               subprocess.Popen([f'explorer', f'C:\\Program Files\\{app}.exe'])
               engine.say(f"Opening {app}")
               engine.runAndWait()

               text = f"Opening {app}"
               self.update_label_text(text)
               time.sleep(5)

            elif 'best friend' in command:
               if 'who is my best friend' in command:
                   text = command.replace('who is my best friend', '').strip()
               elif 'who is my best friend' in command:
                   text = command.replace('who is my best friend', '').strip()
               else:
                   text = ''
                   engine.say(f'Your best friend is {best_friend}.')
                   print(f'Your best friend is {best_friend}.')
                   engine.runAndWait()

                   text = f'Your best friend is {best_friend}.'
                   self.update_label_text(text)

            elif 'my age' in command or 'older i am' in command or 'older am i' in command:
                engine.say(f'You are {age} years old')
                print(f'You are {age} years old')
                engine.runAndWait()

                self.update_label_text(f'You are {age} years old')
                time.sleep(5)

            elif 'my favorite color' in command:
                   text = f'Your favorite color is {favorite_color}'
                   engine.say(f'Your favorite color is {favorite_color}')
                   print(f'Your favorite color is {favorite_color}')
                   engine.runAndWait()

                   self.update_label_text(text)
                   time.sleep(5)

            elif 'call you' in command:
               if 'how can i call you' in command:
                   texto = command.replace( 'how can i call you', '' ).strip()
               elif 'how can i call you' in command:
                   texto = command.replace( 'how can i call you', '' ).strip()
               else:
                   texto = ''
                   engine.say( 'You can call me as Delta' )
                   print( 'You can call me as Delta' )
                   engine.runAndWait()

                   texto = 'You can call me as Delta'
                   self.update_label_text(texto) 

            elif 'play game' in command or 'hash' in command or 'play a game' in command or 'tictactoe' in command or 'game' in command:
                print("Let's play tic-tac-toe")
                engine.say("Let's play tic-tac-toe")
                self.update_label_text("Let's play tic-tac-toe")
                engine.runAndWait()
                time.sleep(1)
                if __name__ == "__main__":
                   main()

            elif "date me" in command:
               if 'whould you like to date me' in command:
                   text = command.replace('whould you like to date me', '').strip()
               else:
                   engine.say('No, I am a virtual assistant and I can not date because I am just a program.')
                   print('No, I am a virtual assistant and I can not date because I am just a program.')
                   self.update_label_text('No, I am a virtual assistant and I can not date because I am just a program.')
                   engine.runAndWait()  
                   time.sleep(3)  

            elif 'siblings' in command:
               if 'Who are my siblings' in command:
                   texto = command.replace( 'Who are my siblings', '' ).strip()
               elif 'Who are my siblings' in command:
                   texto = command.replace( 'Who are my siblings', '' ).strip()
               else:
                   texto = ''
                   engine.say( f'Your siblings are {siblings}' )
                   print( f'Your siblings are {siblings}')
                   engine.runAndWait()

                   texto = f'Your siblings are {siblings}' 
                   self.update_label_text( texto )
                   time.sleep(2)

            elif 'developed' in command:
               if 'who developed you ' in command:
                   texto = command.replace( 'who developed you ', '' ).strip()
               elif 'who developed you ' in command:
                   texto = command.replace( 'who developed you ', '' ).strip()
               else:
                   texto = ''
                   engine.say( 'I was developed by Gabriel, he is a smart guy' )
                   print( 'I was developed by Gabriel, he is a smart guy' )
                   engine.runAndWait()

                   texto = 'I was developed by Gabriel, he is a smart guy'
                   self.update_label_text( texto )
                   time.sleep(2)        

            elif 'delta' in command:
               if 'hello delta' in command:
                   text = command.replace('hello delta', '').strip()
               else:
                   text1 = [f"Hello {user_name} ", "Yes", "I am here", " Is there something I can help you with", "How can I help you"]
                   speak = random.choice(text1)
                   engine.say(speak)
                   print(speak)
                   engine.runAndWait()

                   self.update_label_text(speak)  
                   time.sleep(2)

            elif 'your name' in command:
               if 'what is your name' in command:
                   text = command.replace('what is your name', '').strip()
               else:
                   engine.say("My name is Delta")
                   print("My name is Delta")   
                   engine.runAndWait()
                   self.update_label_text("My name is Delta")  
                   time.sleep(2)    

            elif 'good morning' in command:
               if 'hello, good morning' in command:
                   texto = command.replace( 'hello, good morning', '' ).strip()
               elif 'hello, good morning' in command:
                   texto = command.replace( 'hello, good morning', '' ).strip()
               else:
                   texto = ''
                   engine.say( f"Hello, {user_name} How can I help you?" )
                   print( f"Hello, {user_name} How can I help you?" )
                   engine.runAndWait()

                   texto = f"Hello, {user_name} How can I help you?"
                   self.update_label_text( texto )
                   time.sleep(2)

            elif 'good afternoon' in command:
               if 'hello, good afternoon' in command:
                   texto = command.replace( 'hello, good afternoon', '' ).strip()
               elif 'hello, good afternoon' in command:
                   texto = command.replace( 'hello, good afternoon', '' ).strip()
               else:
                   texto = ''
                   engine.say( f"Hello, {user_name} How can I help you?" )
                   print( f"Hello, {user_name} How can I help you?" )
                   engine.runAndWait()

                   texto = f"Hello, {user_name} How can I help you?"
                   self.update_label_text( texto )
                   time.sleep(2)

            elif 'good night' in command:
               if 'hi, good night' in command:
                   texto = command.replace( 'hi, good night', '' ).strip()
               elif 'hi, good night' in command:
                   texto = command.replace( 'hi, good night', '' ).strip()
               else:
                   texto = ''
                   engine.say( f"Hello, {user_name} How can I help you?" )
                   print( f"Hello, {user_name} How can I help you?" )
                   engine.runAndWait()

                   texto = f"Hello, {user_name} How can I help you?"
                   self.update_label_text( texto )
                   time.sleep(2)

            elif 'thank you' in command or 'thanks' in command:
                   engine.say("You're welcome, Is there something else I can help you with?")
                   print( "You're welcome, Is there something else I can help you with?" )
                   texto = "You're welcome, Is there something else I can help you with?"
                   self.update_label_text( texto )
                   engine.runAndWait()

                   r = sr.Recognizer()
                   with sr.Microphone() as source:
                       audio = r.listen( source )

                   try:
                       resposta = r.recognize_google( audio, language='en-US' )
                       if 'yes' in resposta:
                           texto = 'What whould you like to do?'
                           self.update_label_text( texto )
                       elif 'no' in resposta:
                           texto = 'ok'
                           self.update_label_text( texto )
                       elif 'close the program' in resposta:
                           app.quit()
                       else:
                           texto = ''

                       print( texto )
                       engine.say( texto )
                       self.update_label_text( texto )
                       engine.runAndWait()

                   except sr.UnknownValueError:
                       print( "I couldn't understand you" )
                       texto = "I couldn't understand you"
                       self.update_label_text( texto )

            elif 'change your name' in command:
                   engine.say("It's not possible to change my name because I've been programmed this way.")
                   print("It's not possible to change my name because I've been programmed this way.")
                   texto = "It's not possible to change my name because I've been programmed this way."
                   self.update_label_text(texto)
                   engine.runAndWait()
                   
                   r = sr.Recognizer()
                   with sr.Microphone() as source:
                        audio = r.listen(source)

                   try:
                       resposta = r.recognize_google(audio, language='en-US').lower()
                       if 'ok' in resposta:
                           texto = 'I hope I have helped.'
                           self.update_label_text(texto)
                       elif 'alright' in resposta or 'okay' in resposta or 'too bad' in resposta:
                            texto = 'I apologize for not having helped.'
                            self.update_label_text(texto)
                       else:
                            texto = ''

                            print(texto)
                            engine.say(texto)
                            self.update_label_text(texto)
                            engine.runAndWait()

                   except sr.UnknownValueError:
                          print("")
     

            elif 'to meet' in command:
                self.speak('Sure, what is the person name?')
                name_response = self.listen_for_command()
                if name_response:
                    name = name_response.split()[-1]  
                    if name:
                        greeting = f"Hello {name}, nice to meet you."
                        self.speak(greeting)
                        self.update_label_text(greeting)
                        print(greeting)
                        time.sleep(2)
                    else:
                        self.speak("Sorry, I didn't catch the name.")
                        self.update_label_text("Sorry, I didn't catch the name.")
                        time.sleep(2)
                else:
                    self.speak("Sorry, I didn't hear a response.")
                    self.update_label_text("Sorry, I didn't hear a response.")
                    time.sleep(2)

            elif 'your purpose' in command:
               if 'what is your purpose delta' in command:
                   text = command.replace('what is your purpose delta', '').strip()   
               elif 'what is your purpose delta' in command:
                   text = command.replace('what is your purpose delta', '').strip()
               else:
                   info_text = random.choice(myself)
                   engine.say(info_text)    
                   print(info_text)
                   self.update_label_text(info_text)
                   engine.runAndWait()    
                   time.sleep(1)

            elif "about you" in command:
                if 'tell me something about you' in command:
                    text = command.replace('tell me something about you', '').strip()
                elif 'tell me something about you' in command:
                    text = command.replace('tell me something about you', '').strip()
                else:
                    engine.say("I am a virtual assistant created by Gabriel. And I am here to help you with a lot of things. However if your interested about my purpose you can ask me what is my purpose.")
                    print("I am a virtual assistant created by Gabriel. And I am here to help you with a lot of things. However if your interested about my purpose you can ask me what is my purpose.")
                    self.update_label_text("I am a virtual assistant created by Gabriel. And I am here to help you with a lot of things. However if your interested about my purpose you can ask me what is my purpose.")
                    engine.runAndWait()    
                    time.sleep(1)       

            elif 'screenshot' in command:
                engine.say("Can you at the screen and put a name on your screenshot please!!!")
                engine.runAndWait()    
                time.sleep(2) 
                screenshot_path, _ = QFileDialog.getSaveFileName(None, "Save Screenshot", "", "Images (*.png *.jpg *.bmp *.tiff)")
                if screenshot_path:
                    pyautogui.screenshot(screenshot_path)
                    self.status_label.setText(f"Screenshot saved to: {screenshot_path}")   

            elif any(word in command for word in bad_words):
                self.speak("I'm sorry, but I can't respond that because you are told me a bad word.")
                self.update_label_text("I'm sorry, but I can't respond that because you are told me a bad word.")    
                time.sleep(5)         

            elif 'lock screen' in command:
                lock_screen_command = "rundll32.exe user32.dll,LockWorkStation"
                subprocess.run(lock_screen_command, shell=True)
                engine.say("Screen locked.")
                engine.runAndWait()                                   

            elif 'done' in command or 'getting late' in command:
               if 'i am done for today' in command:
                   texto = command.replace( 'i am done for today', '' ).strip()
               elif 'it is getting late' in command or 'eu já acabei por hoje' in command:
                   texto = command.replace( 'it is getting late', '' ).strip()
               else:
                   texto = ''
                   engine.say( 'Would you like to close the program?' )
                   print( "Would you like to close the program?" )
                   texto = 'Would you like to close the program?'
                   self.update_label_text( texto )
                   engine.runAndWait()

                   r = sr.Recognizer()
                   with sr.Microphone() as source:
                       audio = r.listen( source )

                   try:
                       resposta = r.recognize_google( audio, language='en-US' )
                       if resposta == "yes":
                           app.quit()
                       elif 'no' in resposta:
                           self.update_label_text('What would you do now?')
                           engine.say('What would you do now?')
                           engine.runAndWait()
                       else:
                           engine.say('What would you do now?')
                           print('What would you do now?')
                           engine.runAndWait()
                           self.update_label_text('What would you do now?')
                           time.sleep(2)

                   except sr.UnknownValueError:
                       print( "I wasn't expecting this answer" )
                       engine.say( "I wasn't expecting this answer")
                       self.update_label_text(  "I wasn't expecting this answer" )
                       time.sleep(2)    

            elif 'tell me something' in command or 'tell me an interesting fact' in command:
                facts = random.choice(fun_facts)
                self.update_label_text(facts)
                engine.say(facts)
                print(facts)
                engine.runAndWait()         

            elif 'search' in command:
                self.ask_wikipedia_search(command)

            else:
                user_text = command.lower() 
                user_doc = nlp(user_text)
                similarity_threshold = 0.7
                best_similarity = 0
                best_response = ""

                for pattern, response in pares:
                    pattern_doc = nlp(pattern.lower())  
                    similarity = user_doc.similarity(pattern_doc)

                    if similarity > best_similarity and similarity > similarity_threshold:
                        best_similarity = similarity
                        best_response = response
                        break
 
                if best_response:
                    self.update_label_text(best_response)
                    engine.say(best_response)
                    print(best_response)
                    engine.runAndWait()
                    time.sleep(2)        
                else:
                    self.handle_unknown_question(command)
                    
#speak function
    @staticmethod
    def speak(text):
        engine.say(text)
        engine.runAndWait()
#listen function
    @staticmethod
    def listen_for_command():
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio, language='en-US').lower()
                print(f"User said: {command}")
                return command
        except sr.UnknownValueError:
            print('Unable to recognize speech')
            return ""
        except sr.RequestError as e:
            print(f'Unable to connect to speech recognition service: {e}')
            return "I'm sorry, I couldn't connect to the speech recognition service."

    def update_label_text(self, text):
        self.typewrite_animation(text)
        self.message_label.setText(text)

    def typewrite_animation(self, text):
        delay_between_chars = 25
        current_text = ""
        for char in text:
            current_text += char
            self.message_label.setText(current_text)
            QCoreApplication.processEvents() 
            time.sleep(delay_between_chars / 1000.0)

    def ask_wikipedia_search(self, command):
        self.update_label_text(f"{command}...")
        try:
            search_results = wikipedia.summary(command, sentences=2)
            self.speak(f"{search_results}")
            self.update_label_text(f"{search_results}")
            self.speak_response("Was this information helpful?")
            user_response = self.listen_for_command()

            if user_response and any(keyword in user_response.lower() for keyword in other_ways_to_say_NO):
                response_text = "I'm sorry for not helping, but I'll also look up information for you on Google to assist you further."
                self.update_label_text(response_text)
                self.speak(response_text)
                print(response_text)
                self.google_source(command)
            else:
                self.speak_response("Well, I feel prond of myself for being able to help you!")
                self.save_conversation(command, search_results)  
                self.save_conversation_to_json()    

        except wikipedia.exceptions.DisambiguationError as e:
            self.speak("I found multiple results. Please specify your query.")
            self.update_label_text("I found multiple results. Please specify your query.")
        except wikipedia.exceptions.PageError as e:
            self.speak("I couldn't find any results for your query.")
            self.update_label_text("I couldn't find any results for your query.")
            time.sleep(2)     
    
    def speak_response(self, response_text):
        engine.say(response_text)
        print(f"AI assistant: {response_text}")
        self.update_label_text(response_text)
        engine.runAndWait()
        time.sleep(2)

    def google_source(self, command):
        search_term = command
        google_search_url = f"https://www.google.com/search?q={search_term}"
        webbrowser.open(google_search_url)
        self.speak(f"Please look at the screen for what I found on Google about '{search_term}'.")
        self.update_label_text(f"Please look at the screen for what I found on Google about '{search_term}'.")
        
    def save_conversation(self, question, answer):
        if not hasattr(self, 'conversation_history'):
            self.conversation_history = []

        self.conversation_history.append(f'You: {question}')
        self.conversation_history.append(f'AI assistant: {answer}')
        
    def save_conversation_to_json(self):
        if not hasattr(self, 'conversation_history'):
            self.conversation_history = []

        conversation_list = []
        try:
            with open('conversation_history.json', 'r') as file:
                conversation_list = json.load(file)
        except FileNotFoundError:
            pass

        for i in range(0, len(self.conversation_history), 2):
            question = self.conversation_history[i].replace('You: ', '').strip()
            answer = self.conversation_history[i + 1].replace('AI assistant: ', '').strip()
            conversation_list.append({"question": question, "answer": answer})

        with open('conversation_history.json', 'w') as file:
            json.dump(conversation_list, file, indent=2)

    def handle_unknown_question(self, unknown_question):
        try:
            with open('conversation_history.json', 'r') as file:
                conversation_list = json.load(file)
                known_responses = []

                for entry in conversation_list:
                    known_question = entry.get("question", "")
                    known_answer = entry.get("answer", "")
                    similarity = nlp(unknown_question).similarity(nlp(known_question))
                    if similarity > .7:
                        known_responses.append(known_answer)

                if known_responses:
                    best_response = max(known_responses, key=len)
                    self.speak_response(best_response)
                    return
        except FileNotFoundError:
            pass

        self.speak(selected_excuse + "What does it mean?")
        self.update_label_text(selected_excuse + "What does it mean?")
        print(selected_excuse + "What does it mean?")
        user_response = self.listen_for_command()

        if user_response and any(keyword in user_response.lower() for keyword in dont_know):
            response_text = "That's okay. If you think of anything else, feel free to ask. However I will source for you on wikipedia."
            self.update_label_text(response_text)
            self.speak(response_text)
            print(response_text)
            self.ask_wikipedia_search(unknown_question)
        else:
            self.save_conversation(unknown_question, user_response)
            self.save_conversation_to_json()

            if user_response and 'it means' in user_response.lower():
                response_text = "It means..."
                self.update_label_text(response_text)
                print(response_text)
            else:
                response_text = "Thank you for teaching me! Now I know the answer."
                self.update_label_text(response_text)
                print(response_text)
                self.speak(response_text)

    def handle_command(self, command):
        if command.lower() == 'joke':
            return random.choice(joke) or "I couldn't find a joke at the moment."
        elif command.lower() in ['tell me a joke', 'fancy joke']:
            return random.choice(joke) or "I couldn't find a joke at the moment."
        elif command.lower() == 'story':
            return random.choice(stories) or "I couldn't find a story at the moment."
        elif command.lower() == 'tell me about you':
            return random.choice(myself) or "I couldn't find information about me at the moment."
        elif command.lower() == 'tell me your purpose':
            return random.choice(myself) or "I couldn't find information about my purpose at the moment."
        elif command.lower() in ['can you tell me a story', 'could you tell a funny story', 'tell me a story']:
            return random.choice(stories) or "I couldn't find a story at the moment."
        elif any(keyword in command.lower() for keyword in ['tell me more', 'more', 'continue', 'expand']):
            if 'story' in self.context['last_command']:
                return random.choice(stories) or "I couldn't find a story at the moment."
            elif 'joke' in self.context['last_command']:
                return random.choice(joke) or "I couldn't find a joke at the moment."
            elif 'tell me about you' in self.context['last_command']:
                return random.choice(myself) or "I couldn't find information about me at the moment."
            elif 'tell me your purpose' in self.context['last_command']:
                return random.choice(myself) or "I couldn't find information about my purpose at the moment."
            else:
                return "I'm not sure what you want more of."
        else:
            return "I am sorry, but I don't understand you."

# to get news in url
def get_news():
    api_key = '43b8a7b79970495d92e58b2e8e70829d'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    return articles


#Virtual Assistant GUI
class VirtualAssistant(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Delta AI assistant')
        self.setGeometry(100, 100, 400, 700)
        self.setWindowIcon(QIcon(r"C:\DeltaAI1\UI5.jpg"))
        self.setStyleSheet("background-color: #000000;")

        self.message_scroll_area = QScrollArea(self)
        self.message_scroll_area.setGeometry(10, 60, 380, 400)
        self.message_scroll_area.setWidgetResizable(True)

        self.message_label = QLabel(self.message_scroll_area)
        self.message_label.setFont(QFont('Arial', 16))
        self.message_label.setStyleSheet(
            "background-color: #000000; color: #FFFFFF; margin-bottom: 20px; padding: 10px; border-radius: 5px;")

        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(10, 10, 100, 100)
        self.load_gif(r"C:\DeltaAI1\gif5.gif")

        self.message_scroll_area.setWidget(self.message_label)

        button_layout = QVBoxLayout()

        self.button_listen_continuous = QPushButton('Listen', self)
        self.button_listen_continuous.setStyleSheet(
            "background-color: #000000; color: #FFFFFF; padding: 10px 20px; font-size: 14px; border: none; border-radius: 5px;")

        self.button_lock_screen = QPushButton('Lock Screen', self)
        self.button_lock_screen.setStyleSheet(
            "background-color: #000000; color: #FFFFFF; padding: 10px 20px; font-size: 14px; border: none; border-radius: 5px;")

        self.button_screenshot = QPushButton('Screenshot', self)
        self.button_screenshot.setStyleSheet(
            "background-color: #000000; color: #FFFFFF; padding: 10px 20px; font-size: 14px; border: none; border-radius: 5px;")

        self.button_close = QPushButton('Close', self)
        self.button_close.setStyleSheet(
            "background-color: #000000; color: #FFFFFF; padding: 10px 20px; font-size: 14px; border: none; border-radius: 5px;")

        button_layout.addWidget(self.button_listen_continuous)
        button_layout.addWidget(self.button_lock_screen)
        button_layout.addWidget(self.button_screenshot)
        button_layout.addWidget(self.button_close)

        layout = QVBoxLayout(self)
        layout.addWidget(self.message_scroll_area)
        layout.addWidget(self.gif_label)
        layout.addLayout(button_layout)

        self.button_listen_continuous.clicked.connect(self.toggle_continuous_listening)
        self.button_lock_screen.clicked.connect(self.lock_screen)
        self.button_screenshot.clicked.connect(self.take_screenshot)
        self.button_close.clicked.connect(QApplication.quit)

        self.command_processor = CommandProcessorThread(self.message_label)

        self.is_listening_continuous = False

        self.show() 

        self.initialize()

    def initialize(self):
        self.init_virtual_assistant()

    def toggle_continuous_listening(self):
        if self.is_listening_continuous:
            self.is_listening_continuous = False
            self.button_listen_continuous.setText('LISTEN')
        else:
            self.is_listening_continuous = True
            self.button_listen_continuous.setText('LISTENING...')
            self.command_processor.start()

    def typewrite_animation(self, text):
        delay_between_chars = 25
        current_text = ""
        for char in text:
            current_text += char
            self.message_label.setText(current_text)
            QCoreApplication.processEvents()
            time.sleep(delay_between_chars / 1000.0)

    def lock_screen(self):
        lock_screen_command = "rundll32.exe user32.dll,LockWorkStation"
        subprocess.run(lock_screen_command, shell=True)
        engine.say("Screen locked.")
        engine.runAndWait()

    def init_virtual_assistant(self):
        greetings = ["How can I assist you today?",
                     "How are you?",
                     "Welcome back, how can I help you?",
                     "How's your day going?",
                     "Good to see you again! How can I be of service?",
                     "Hello there! What can I do for you today?",
                     "Hi, it's great to have you here. How can I assist you?",
                     "Hey, how's everything going? How can I assist you today?",
                     "Welcome! How may I assist you with your needs?"]

        new_greeting = random.choice(greetings)
        self.message_label.setWordWrap(True)

        user_data_file = 'user_data.json'

        if os.path.exists(user_data_file):
            with open(user_data_file, 'r') as file:
                user_data = json.load(file)
                user_name = user_data.get('user_name', '')

            if user_name:
                if day == birth_date.day and month == birth_date.month:
                    birthday_message = "Happy birthday!"
                    messages = f"{greeting} {user_name}, {birthday_message} {new_greeting}"
                    self.command_processor.speak(messages)
                    self.update_message(messages)
                else:
                    messages = f"{greeting} {user_name}, {new_greeting}"
                    print(messages)
                    self.command_processor.speak(messages)
                    self.update_message(messages)
            else:
                messages1 = "I was not able to identify your name, can you please tell me your name?"
                print(messages1)
                self.command_processor.speak(messages1)
                self.update_message(messages1)
                time.sleep(5)

                self.listen_for_name()
        else:
            messages1 = "I was not able to identify your name, can you please tell me your name?"
            print(messages1)
            self.command_processor.speak(messages1)
            self.update_message(messages1)
            time.sleep(5)

            self.listen_for_name()

    def listen_for_name(self):
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
                name_response = recognizer.recognize_google(audio, language='en-US')
            name = name_response.split()[-1]
            messages = f"Hi {name}, nice to meet you! If your  name is incorrect, you can tell me to change it."
            print(messages)
            self.command_processor.speak(messages)
            self.update_message(messages)

            with open('user_data.json', 'w') as file:
                json.dump({'user_name': name}, file)

        except sr.UnknownValueError:
            print("Sorry, I was not able to recognizer your name.")
            self.update_message("Sorry, I was not able to recognizer your name.")
        except sr.RequestError as e:
            print(f"Error when making a request to the speech recognition service; {e}")
            self.update_message(f"Error when making a request to the speech recognition service; {e}")

        self.message_label.setWordWrap(True)

    def update_message(self, messages):
        self.typewrite_animation(messages)
        self.message_label.setText(messages)

    def take_screenshot(self):
        screenshot_path, _ = QFileDialog.getSaveFileName(None, "Save Screenshot", "", "Images (*.png *.jpg *.bmp *.tiff)")
        if screenshot_path:
            pyautogui.screenshot(screenshot_path)
            self.update_message(f"Screenshot saved to: {screenshot_path}")

    def load_gif(self, path):
        movie = QMovie(path)
        self.gif_label.setMovie(movie)
        movie.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    assistant = VirtualAssistant()
    sys.exit(app.exec_())
