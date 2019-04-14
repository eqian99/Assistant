#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template
import json
import os
import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64

app = Flask(__name__)

# Azure Variables
_region = 'westcentralus' #Here you enter the region of your subscription
_url = 'https://{}.api.cognitive.microsoft.com/vision/v2.0/analyze'.format(_region)
_key = '9a801624fab842b8867b963ecc5f151f'
_maxNumRetries = 10

@app.route('/', methods=['POST'])
def start():
    # js = json.loads(request.data.decode('utf-8'))
    # print(js)

    try:
        mode = request.args["mode"]
        image = request.form.get("image_url") # request.form["image_url"]
        # image = request.files['image']
        # filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        # image.save(filename)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return jsonify({"result": "Error: request reading failed"})

    # Do something depending on mode
    if mode == "caption":
        return captionImage(image)
    elif mode == "faces":
        return describeFaces(image)
    elif mode == "test":
        return jsonity({"result": "Success!"})
    else:
        return jsonify({"result": "Error: mode not recognized"})

def describeFaces():
    """
    Input: Image
    Output: JSON, with info
    e.g. {"result": "two people: one is 80% happy, two is 72% sad"}
    """
    json = {}
    return jsonify(json)


# Compare Azure and IBM Watson captioning
def captionImage(image_url):
    """
    Input: Image
    Output: JSON, with info
    e.g. {"result": "a red fox in a green field", "confidence": 88.5, "other stuff".....}
    """
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

    describe_url = vision_base_url + "describe"

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': _key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'maxCandidates': '1',
        'language': 'en',
    })

    body = {"url": image_url}

    try:
        response = requests.post(describe_url, headers=headers, params=params, data=body)
        response.raise_for_status()
        data = response.read()
        print(data)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    json = {}
    return jsonify(json)

if __name__ == "__main__":
    app.run(debug=True)