# Large Language Model Examples

## 1. Question and Answering using mistral-7b-instruct LLM Model
commands to streamlit chat app: 

> streamlit run chatapp.py
        
        
## 2. Simple RAG using Google Gemini-Pro LLM Model
ommands to streamlit chat app:

> streamlit run chatpdf.py

## 3. Fetch SQL Data from database and Summarize/Plot using Gemini-Pro LLM Model
run the notebook examples

## 3. Approach to run LLM Locally/Cloud
build docker using command
> docker build -t sausalito/llama-2-7b-chat-llm-api .

Run docker using command
> docker run -p 80:80 sausalito/genai:llama-2-7b-chat-llm-api  

Access server using below command 
> curl --location 'http://127.0.0.1/ask' --header 'Content-Type: application/json' --data '{"category":"joke","input_text":"Sachin","no_words":"100"}'
