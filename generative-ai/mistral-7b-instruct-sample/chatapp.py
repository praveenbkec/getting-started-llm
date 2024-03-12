"""
A simple web application to implement a chatbot. This app uses Streamlit 
for the UI and the Python requests package to talk to an API endpoint that
implements text generation and Retrieval Augmented Generation (RAG) using LLMs
and Amazon OpenSearch as the vector database.
"""
import boto3
import streamlit as st
import requests as req
from typing import List, Tuple, Dict

# utility functions
def get_cfn_outputs(stackname: str) -> List:
    cfn = boto3.client('cloudformation')
    outputs = {}
    for output in cfn.describe_stacks(StackName=stackname)['Stacks'][0]['Outputs']:
        outputs[output['OutputKey']] = output['OutputValue']
    return outputs


def format_instructions(instructions: List[Dict[str, str]]) -> List[str]:
    """Format instructions where conversation roles must alternate user/assistant/user/assistant/..."""
    prompt: List[str] = []
    for user, answer in zip(instructions[::2], instructions[1::2]):
        prompt.extend(["<s>", "[INST] ", (user["content"]).strip(), " [/INST] ", (answer["content"]).strip(), "</s>"])
    prompt.extend(["<s>", "[INST] ", (instructions[-1]["content"]).strip(), " [/INST] "])
    return "".join(prompt)

# global constants
STREAMLIT_SESSION_VARS: List[Tuple] = [("generated", []), ("past", []), ("input", ""), ("stored_session", [])]
HTTP_OK: int = 200

# two options for the chatbot, 1) get answer directly from the LLM
# 2) use RAG (find documents similar to the user query and then provide
# those as context to the LLM).
MODE_RAG: str = 'RAG'
MODE_TEXT2TEXT: str = 'Text Generation'
MODE_VALUES: List[str] = [MODE_TEXT2TEXT, MODE_RAG]

# Currently we use the flan-t5-xxl for text generation
# and gpt-j-6b for embeddings but in future we could support more
# TEXT2TEXT_MODEL_LIST: List[str] = ["flan-t5-xxl"]
TEXT2TEXT_MODEL_LIST: List[str] = ["huggingface-llm-mistral-7b-instruct"]
EMBEDDINGS_MODEL_LIST: List[str] = ["gpt-j-6b"]

# if running this app on a compute environment that has
# IAM cloudformation::DescribeStacks access read the 
# stack outputs to get the name of the LLM endpoint
CFN_ACCESS = False
if CFN_ACCESS is True:
    CFN_STACK_NAME: str = "llm-apps-blog-rag"
    outputs = get_cfn_outputs(CFN_STACK_NAME)
else:
    # create an outputs dictionary with keys of interest
    # the key value would need to be edited manually before
    # running this app
    outputs: Dict = {}
    # REPLACE __API_GW_ENDPOINT__ WITH ACTUAL API GW ENDPOINT URL
    outputs["LLMAppAPIEndpoint"] = "https://4lbtec2vmk.execute-api.us-west-2.amazonaws.com/default/sausgenai-text2text-invoker"

# API endpoint
# this is retrieved from the cloud formation template that was
# used to create this solution
api: str = outputs.get("LLMAppAPIEndpoint")
api_rag_ep: str = f"{api}/api/v1/llm/rag"
api_text2text_ep: str = f"{api}"
print(f"api_rag_ep={api_rag_ep}\napi_text2text_ep={api_text2text_ep}")

####################
# Streamlit code
####################

# Page title
st.set_page_config(page_title='Juniper Virtual assistant for knowledge base 👩‍💻', layout='wide')

# keep track of conversations by using streamlit_session
_ = [st.session_state.setdefault(k, v) for k,v in STREAMLIT_SESSION_VARS]

# Define function to get user input
def get_user_input() -> str:
    """
    Returns the text entered by the user
    """
    print(st.session_state)    
    input_text = st.text_input("You: ",
                               st.session_state["input"],
                               key="input",
                               placeholder="Ask me a question and I will consult the knowledge base to answer...", 
                               label_visibility='hidden')
    return input_text


# sidebar with options
with st.sidebar.expander("⚙️", expanded=True):
    text2text_model = st.selectbox(label='Text2Text Model', options=TEXT2TEXT_MODEL_LIST)
    embeddings_model = st.selectbox(label='Embeddings Model', options=EMBEDDINGS_MODEL_LIST)
    mode = st.selectbox(label='Mode', options=MODE_VALUES)
    

# streamlit app layout sidebar + main panel
# the main panel has a title, a sub header and user input textbox
# and a text area for response and history
st.title("👩‍💻 Juniper Virtual assistant for a knowledge base")
st.subheader(f" Powered by :blue[{TEXT2TEXT_MODEL_LIST[0]}] for text generation and :blue[{EMBEDDINGS_MODEL_LIST[0]}] for embeddings")

# get user input
user_input: str = get_user_input()

# based on the selected mode type call the appropriate API endpoint
if user_input:
    # headers for request and response encoding, same for both endpoints
    headers: Dict = {"accept": "application/json", "Content-Type": "application/json"}
    output: str = None
    if mode == MODE_TEXT2TEXT:
        print("=====user_input=====")
        print(user_input)
        # parameters = {
        #         "top_k": 10,
        #         "top_p": 0.9,
        #         "prompt": user_input,
        #         "temperature": 0.6,
        #         "max_new_tokens": 1024,
        #         "prompt_template": "<s>[INST] {prompt} [/INST] ",
        #         "presence_penalty": 0,
        #         "frequency_penalty": 0
        #     }
        # data = {'inputs': '[INST] Who is Shah Rukh Khan? [/INST]', 'parameters':{'max_new_tokens': 256, 'do_sample': True, 'temperature': 0.2}}
        # {'inputs': '<s>[INST] Who is Shah Rukh Khan? [/INST] ', 'parameters': {'max_new_tokens': 256, 'do_sample': True, 'temperature': 0.2}}

        # payload = {"inputs": user_input}
        instructions = [
            {
                "role": "user",
                "content": user_input,
            }
        ]
        prompt = format_instructions(instructions)
        # print(prompt)
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 256, "do_sample": True, "temperature": 0.2}
        }
        print("before post to endpoint====>>>")
        print(payload)
        resp = req.post(api_text2text_ep, headers=headers, json=payload)
        if resp.status_code != HTTP_OK:
            output = resp.text
        else:
            output = resp.json()[0]['generated_text']
    elif mode == MODE_RAG:        
        data = {"q": user_input, "verbose": True}
        resp = req.post(api_rag_ep, headers=headers, json=data)
        if resp.status_code != HTTP_OK:
            output = resp.text
        else:
            resp = resp.json()
            sources = [d['metadata']['source'] for d in resp['docs']]
            output = f"{resp['answer']} \n \n Sources: {sources}"
    else:
        print("error")
        output = f"unhandled mode value={mode}"
    st.session_state.past.append(user_input)  
    st.session_state.generated.append(output) 


# download the chat history
download_str: List = []
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="❓") 
        st.success(st.session_state["generated"][i], icon="👩‍💻")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])
    
    download_str = '\n'.join(download_str)
    if download_str:
        st.download_button('Download', download_str)
