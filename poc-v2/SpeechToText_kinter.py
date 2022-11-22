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
try:
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


            
    def SpeechToText(window):
            #canvas.create_rectangle(0, 0, 400, 856, fill='#00203F')
            window.title('MG Motors Voice Inventory Search')
            #window.configure(bg='#1B98F5')
            Label(window, text='MG Motors Voice Inventory Search', font=("BankGothic Lt BT", 15), bg="#E1A2B8").place(x=640 , y=50)
            text = Text(window, font=12, height=10, width=40,padx=4,pady=4,bd=10)
            text.place(x=580, y=180)
            recordbutton = Button(window, text='Record', bg='#51E1ED', command=lambda: text.insert(END, speak(text)))
            recordbutton.place(x=760, y=120)
            window.update()
            window.mainloop()
except Exception as E:
    print("Exception raised",E)
    print("\n\n Try Again")