import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage , AIMessage 
from langchain_core.prompts import ChatPromptTemplate
import os


## Page config 
st.set_page_config(page_title="Langchain based chatbot" , page_icon="💻")

st.title("Chat with Groq 💻")
st.markdown("Learn Lanchain basics with Groq")

with st.sidebar:
    st.header("Settings")
    ## API KEY
    api_key=st.text_input("Groq API Key" , type="password", help="Get free API Key at console.groq.com" )


    model_name = st.selectbox(
        "Model",
        ["llama-3.1-8b-instant"],
        index=0 
    )

    #Clear button
    if st.button("Clear Chat"):
        st.session_state.messages= []
        st.rerun()

#initialise the session
if "messages" not in st.session_state:
    st.session_state.messages = []

# initialise llm
@st.cache_resource
def get_chain(api_key , model_name):
    if not api_key:
        return None
    #initialise groq model
    llm = ChatGroq(groq_api_key= api_key,
                   model_name = model_name,
                   temperature=0.7,
                   streaming=True)
    
    #prompt template
    prompt= ChatPromptTemplate.from_messages([
        ("system","You are a helpful AI assistant powered by Groq. Answer all questions clearly and concisely."),
        ("user","{question}")
    ])

    #chain initialise
    chain = prompt| llm| StrOutputParser()
    
    return chain

## get chain 
chain = get_chain( api_key , model_name)

if not chain:
    st.warning("Please enter the API key to start chatting")
    st.markdown("[Get a free API Key at](https://console.groq.com)")

else:
    #display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    ## chat input
    if question:= st.chat_input("Ask me anything"):
        #add user message to session state
        st.session_state.messages.append({"role":"user", "content":question})

        with st.chat_message("user"):
            st.write(question)

        #generate response
        with st.chat_message("assistant"):
            message_palceholder = st.empty()
            full_response = ""

            try:
                #streaming output
                for chunk in chain.stream({"question":question}):
                        full_response += chunk
                        message_palceholder.markdown(full_response + " ")
                
                message_palceholder.markdown(full_response)

                #add to history
                st.session_state.messages.append({"role":"assistant" , "content" : full_response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                







