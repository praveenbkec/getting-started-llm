# Large Language Model Examples

## 1. Question and Answering using mistral-7b-instruct LLM Model
command run chat app: 

> streamlit run chatapp.py
        
        
## 2. Simple RAG using Google Gemini-Pro LLM Model
commands to run chat app:

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

> {
    "generated_text": "\n\nSachin Tendulkar, the cricket legend, was asked to write an autobiography. He replied, \"I'm not sure I want to reveal all my secrets.\" The interviewer asked, \"What do you mean?\" Sachin smiled and said, \"Well, for starters, how did I manage to hit so many boundaries without getting caught?\""
}