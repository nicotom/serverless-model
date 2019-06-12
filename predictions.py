from os import getenv
import boto3
from dotenv import load_dotenv
from flask import Flask
from flask import request
from flask import json
import numpy as np
from sklearn.externals import joblib


# Load environmental variables
load_dotenv()

BUCKET_NAME = getenv('BUCKET_NAME')
MODEL_FILE_NAME = getenv('MODEL_FILE_NAME')
MODEL_LOCAL_PATH = getenv('MODEL_LOCAL_PATH')


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    payload = json.loads(request.get_data().decode('utf-8'))
    prediction = predict(payload['payload'])
    data = dict()
    data['data'] = prediction[-1]
    return json.dumps(data)


def load_model():
    s3 = boto3.client('s3')
    s3.download_file(BUCKET_NAME, MODEL_FILE_NAME, MODEL_LOCAL_PATH)
    return joblib.load(MODEL_LOCAL_PATH)


def predict(data):
    # Process your data, create a dataframe/vector and make your predictions
    final_formatted_data = np.expand_dims(np.fromstring(data.strip('['), sep=','), axis=0)
    return load_model().predict(final_formatted_data).tolist()


if __name__ == "__main__":
    app.run()
