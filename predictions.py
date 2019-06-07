from sklearn.externals import joblib
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from flask import Flask
from flask import request
from flask import json

BUCKET_NAME = 'your-s3-bucket-name'
MODEL_FILE_NAME = 'your-model-name.pkl'
MODEL_LOCAL_PATH = '/tmp/' + MODEL_FILE_NAME

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
  payload = json.loads(request.get_data().decode('utf-8'))
  prediction = predict(payload['payload'])
  data = {}
  data['data'] = prediction[-1]
  return json.dumps(data)

def load_model():
  print 'Loading model from S3'

def predict(data):
  print 'Making predictions'
