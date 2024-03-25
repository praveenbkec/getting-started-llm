FROM python:3.9-slim
COPY app.py /deploy/
COPY requirements.txt /deploy/
COPY model/BasgitAli-llama-2-7b-chat/pytorch_model.bin /deploy/
WORKDIR /deploy/
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]