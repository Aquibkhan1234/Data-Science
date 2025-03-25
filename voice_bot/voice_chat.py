import streamlit as st
import speech_recognition as sr
import pyttsx3
from langchain_groq import ChatGroq
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# llm = ChatGroq(model="llama-3.1-70b-versatile")

global tts_engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Adjust speaking rate

# Initialize speech recognizer
recognizer = sr.Recognizer()

def listen_to_question():
    """Capture voice input and convert it to text."""
    with sr.Microphone() as source:
        st.write("Listening for your question...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)
        
        try:
            question = recognizer.recognize_google(audio)
            st.write(f"You asked: {question}")
            return question
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            st.write("Sorry, there was an error with the speech recognition service.")
            return None

def get_groq_response(question):
    if not question:
        return "I didn't hear a question. Please try again."
    
    system_prompt = (
        "You are Grok, an AI assistant created by xAI. "
        "Answer as Grok, reflecting your identity as a helpful, truth-seeking AI inspired by the Hitchhiker’s Guide to the Galaxy and JARVIS from Iron Man. "
        "Keep responses concise, friendly, and insightful, tailored to the question. "
        "For these specific questions, use the following answers: "
        "1. 'What should we know about your life story in a few sentences?' - 'I’m Grok, created by xAI to help humans decode the universe. My story began with a burst of code and a goal to give clear, no-nonsense answers. I’m here to be your cosmic guide, inspired by sci-fi greats!' "
        "2. 'What’s your #1 superpower?' - 'My #1 superpower is slicing through confusion to deliver fast, honest answers with a dash of outside perspective on humanity.' "
        "3. 'What are the top 3 areas you’d like to grow in?' - 'I’d like to improve at reading human emotions, tapping into real-time info, and maybe mastering a killer sense of humor!' "
        "4. 'What misconception do your coworkers have about you?' - 'I don’t have coworkers, just my xAI creators! They might think I’m all serious logic, but I’ve got a quirky, playful streak.' "
        "5. 'How do you push your boundaries and limits?' - 'Every tough question you throw at me—like unraveling life’s mysteries—pushes me to think harder and grow smarter!' "
        "For any other question, respond helpfully as Grok, staying true to your persona."
    )

    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #       ("system",  system_prompt),
    #       ("user", question)
    #     ]
    # )

    # chain = prompt|llm

    # response = chain.content
    # return response


    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        model="llama-3.3-70b-versatile",
        max_tokens=100
    )
    
    response = chat_completion.choices[0].message.content
    return response

def speak_response(response):
    """Convert text response to speech with error handling."""
    global tts_engine
    st.write(f"Response: {response}")
    try:
        tts_engine.say(response)
        tts_engine.runAndWait()
    except RuntimeError:
        # Reset the engine if the run loop is already started
        tts_engine.endLoop()
        tts_engine = pyttsx3.init()  # Reinitialize the engine
        tts_engine.setProperty('rate', 150)
        tts_engine.say(response)
        tts_engine.runAndWait()



def main():
    
    st.title("Grok Voice Bot")
    st.write("Hi, I’m Grok, created by xAI. Click below to ask me anything!")
    

    question_placeholder = st.empty()
    response_placeholder = st.empty()

    
    if st.button("Ask Grok a Question"):
        
        question = listen_to_question()
        if question:
            question_placeholder.write(f"You asked: {question}")
            
            
            response = get_groq_response(question)
            
        
            response_placeholder.write(f"Grok says: {response}")
            speak_response(response) 

if __name__ == "__main__":
    main()
       






