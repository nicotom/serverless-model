from os import getenv

from boto.s3.key import Key
from boto.s3.connection import S3Connection
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
    conn = S3Connection()
    bucket = conn.get_bucket(BUCKET_NAME)
    key_obj = Key(bucket)
    key_obj.key = MODEL_FILE_NAME

    contents = key_obj.get_contents_to_filename(MODEL_LOCAL_PATH)
    return joblib.load(MODEL_LOCAL_PATH)


def predict(data):
    # Process your data, create a dataframe/vector and make your predictions
    final_formatted_data = np.expand_dims(np.fromstring(data.strip('['), sep=','), axis=0)
    return load_model().predict(final_formatted_data).tolist()
