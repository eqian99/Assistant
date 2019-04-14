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
    FACE_CONFIDENCE_THRESHOLD = 0.8
    try:
        image = request.files.get('image')
        if request.args["test"] == 'true':
            return jsonify({"_result": "Test mode on. Server received your image!"})
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return jsonify({"result": "Error: request reading failed"})

    result = {'_result': ""}
    # Do something depending on mode
    if request.args["caption"] == 'true':
        captionData = captionImage(image)
        result['_result'] += captionData['_result']
    if request.args["faces"] == 'true':
        facesData = describeFaces(image)
        if facesData['confidence'] >= FACE_CONFIDENCE_THRESHOLD:
            result['_result'] += facesData['_result']
    if request.args["ocr"] == 'true':
        textData = extractText(image)
        result['_result'] += textData['_result']
    return jsonify(result)

    # TODO: if faces of a certain confidence, append to result


def detectEmotion(image):
    """
    Input: Image binary data
    Output: JSON, with info
    e.g. {"result": "two people: one is 80% happy, two is 72% sad", "confidence": 0.98}
    """
    json = EmotionAzure(image).analyzeFace()
    return json


def extractText(image):
    """
    Input: Image binary data, to perform OCR on
    Output: Dict with info
    e.g. {"result": "anclsaknlasfasf", "confidence": 0.42}
    """
    json = ExtractText(image).extractText()
    return json


# Compare Azure and IBM Watson captioning
def captionImage(image):
    """
    Input: Image
    Output: Dict with info
    e.g. {"result": "a red fox in a green field", "confidence": 88.5, "other stuff".....}
    """
    json = CaptionImage(image).captionImage()
    return json


if __name__ == "__main__":
    app.run(debug=True)