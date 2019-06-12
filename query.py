from argparse import ArgumentParser
from base64 import b64encode
from requests import post

# Ask for the image
parser = ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="Image path")
parser.add_argument("-u", "--url",  default="http://127.0.0.1:5000/", help="Url to query")
args = parser.parse_args()

# Encode the image to Base64 in order to send it via request
with open(args.image, "rb") as image_file:
    encoded_image = b64encode(image_file.read())

# Send the Request
response = post(args.url, data='{"payload": "' + encoded_image.decode("utf-8") + '"}')
if response.status_code == 200:
    print(response.text)
else:
    print(response.status_code, response.text)
