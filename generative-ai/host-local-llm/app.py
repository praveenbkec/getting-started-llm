from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
from flask import Flask, request, Response
import json

app = Flask(__name__)

def load_model():
    global llm_model
    print("=== load model is initialised ===")
    llm_model = CTransformers(model = "/deploy/pytorch_model.bin",
                        model_type = 'llama',
                        config={'max_new_tokens': 256,
                                'temperature': 0.01})

@app.route('/')
def home_endpoint():
    return 'Hello Welcome to play with llama-2-7b-chat llm APIS!'

@app.route('/ask', methods=['POST'])
def ask_model():
    print("==== inside ask_model ====")
    if request.method == 'POST':
        data = request.get_json()  # Get data posted as a json
        print(data)
    input_text = data["input_text"]
    category = data["category"]
    no_words = data["no_words"]

    ## PromptTemplate
    template = """Write a  {category} on {input_text} in less than {no_words} words"""

    prompt = PromptTemplate(input_variables = ["input_text", "no_words", "category"],
                            template = template)
    
    ## Generate the reponse from the LLama 2 Model
    llm_respone = llm_model(prompt.format(category=category,input_text=input_text,no_words=no_words))
    json_resp = json.dumps({'generated_text': llm_respone})
    return Response(json_resp, status=400, mimetype='application/json')


if __name__ == '__main__':
    load_model()  # load model at the beginning once only
    app.run(host='0.0.0.0', port=80)