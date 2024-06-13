FROM python:3.11.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./download_model.py /code/download_model.py
RUN python /code/download_model.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
