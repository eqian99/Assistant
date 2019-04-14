#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template
import json
import os
import requests
from detect_emotion import EmotionAzure
from caption_image import CaptionImage
from extract_text import ExtractText
import http.client, urllib.request, urllib.parse, urllib.error, base64

app = Flask(__name__)


@app.route('/', methods=['POST'])
def start():
    """
    POST endpoint to receive from app
    """
    # js = json.loads(request.data.decode('utf-8'))
    # print(js)

    try:
        mode = request.args["mode"]
        image = request.files.get('image')
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
    elif mode == "ocr":
        return extractText(image)
    elif mode == "test":
        return jsonity({"result": "Success!"})
    else:
        return jsonify({"result": "Error: mode not recognized"})


def describeFaces(image):
    """
    Input: Image binary data
    Output: JSON, with info
    e.g. {"result": "two people: one is 80% happy, two is 72% sad", "confidence": 0.98}
    """
    json = EmotionAzure(image).analyzeFace()
    return jsonify(json)


def extractText(image):
    """
    Input: Image binary data, to perform OCR on
    Output: JSON, with info
    e.g. {"result": "anclsaknlasfasf", "confidence": 0.42}
    """
    json = ExtractText(image).extractText()
    return jsonify(json)


# Compare Azure and IBM Watson captioning
def captionImage(image):
    """
    Input: Image
    Output: JSON, with info
    e.g. {"result": "a red fox in a green field", "confidence": 88.5, "other stuff".....}
    """
    json = CaptionImage(image).captionImage()
    return jsonify(json)


if __name__ == "__main__":
    app.run(debug=True)