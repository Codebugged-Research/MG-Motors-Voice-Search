from tkinter import *
from tkinter.messagebox import showinfo
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize
import pandas as pd
import spacy
import spacy
from spacy.matcher import PhraseMatcher
import numpy as np
import os
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")
window= Tk()
window.title('Speech To Text Converter')
window.geometry('500x500')
window.resizable(0, 0)
window.configure(bg='Violet')
def speak(textwind):
        textwind.delete("1.0", "end")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak now")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_text = r.listen(source,timeout=3, phrase_time_limit=5)
        text = r.recognize_google(audio_text)
        print(text)
        words=preprocess(text)
        result=list(checking(words))
        textwind.delete("1.0", "end")
        try:
            df=pd.DataFrame(result,columns=["Part Name","Location","Quantity"])
            #df['Query text']=text
            print(df)
            #textwind.delete("1.0", "end")
            return  f"Query text : {text} \n\n {df}"

        except Exception as E:
            print(E)
            return f"Query text : {text} \n\n {result[0]}"

def preprocess(words):
    word_tokens_1 = word_tokenize(words)
    stop_words = set(stopwords.words('english'))
    new_sent_1 = [w for w in word_tokens_1 if not w.lower() in stop_words]
    new_sent_1= ' '.join([str(elem.lower()) for elem in new_sent_1])
    words=new_sent_1
    return words
    #return words

def checking(text):
    df=pd.read_excel("MG Data.xlsx")
    dict={}
    terms=df["Part Name"].to_list()
    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab)
    term_new=[]
    for term in terms:
        term=preprocess(term)
        term_new.append(term)
    patterns = [nlp.make_doc(text) for text in term_new]
    matcher.add("TerminologyList", patterns)
    for i in range(0, len(term_new)):       
        dict[term_new[i]]=[df.iloc[i,0],df.iloc[i,1],df.iloc[i,2]]
    text =preprocess(text)
    doc=nlp(text)
    output=[]
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        output.append(span.text)
    if len(output)>0:
        for i in output:
            yield dict[i]
    else:

        yield "Plase try again"


        
def SpeechToText():
    global text
    speechtotextwindow = Toplevel(window)
    speechtotextwindow.title('Speech to Text Converter')
    speechtotextwindow.geometry("500x500")
    speechtotextwindow.configure(bg='blue')
    Label(speechtotextwindow, text='Speech to Text Conversion', font=("BankGothic Lt BT", 15), bg="violet").place(x=50)
    text = Text(speechtotextwindow, font=12, height=5, width=50)
    text.place(x=25, y=100)
    recordbutton = Button(speechtotextwindow, text='Record', bg='sky blue', command=lambda: text.insert(INSERT, speak(text)))
    recordbutton.place(x=150, y=50)
speechtotextbutton = Button(window, text='Speech To Text Conversion', font=('BankGothic Lt BT', 15), bg='Purple', command=SpeechToText)
speechtotextbutton.place(x=100, y=250)
Label(window, text='Speech To Text Converter',font=('BankGothic Lt BT', 25), bg='blue', wrap=True, wraplength=450).place(x=25, y=0)
window.update()
window.mainloop()
