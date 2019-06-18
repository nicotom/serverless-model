from base64 import b64decode
from io import BytesIO
from PIL import Image
from os import getenv
from os.path import join
import boto3
from dotenv import load_dotenv
from flask import Flask
from flask import request
from flask import json
from pickle import load

# Load environmental variables
load_dotenv()

BUCKET_NAME = getenv('BUCKET_NAME')
MODEL_WRAPPER = getenv('MODEL_WRAPPER')
MODEL_WEIGHTS = getenv('MODEL_WEIGHTS')
TMP_PATH = getenv('TMP_PATH')


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    payload = json.loads(request.get_data().decode('utf-8'))
    prediction = predict(payload['payload'])
    data = {
        'class': f"{prediction[0]}",
        'probability': f"{prediction[1]:.6f}"
    }
    return json.dumps(data)


def load_model():
    s3 = boto3.client('s3')
    # Load model wrapper
    # s3.download_file(BUCKET_NAME, MODEL_WRAPPER, join(TMP_PATH, MODEL_WRAPPER))
    # s3.download_file(BUCKET_NAME, MODEL_WEIGHTS, join(TMP_PATH, MODEL_WEIGHTS))
    with open(join(TMP_PATH, MODEL_WRAPPER), 'rb') as filehandler:
        model = load(filehandler)
    model.load(join(TMP_PATH, MODEL_WEIGHTS))
    return model


def predict(data):
    # Load encoded image
    loaded_image = Image.open(BytesIO(b64decode(data))).convert('RGB')
    return load_model().predict(loaded_image)


if __name__ == "__main__":
    app.run()
