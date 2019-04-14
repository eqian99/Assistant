#!/usr/bin/env python3

from flask import Flask, request
import json
import os
import matplotlib
matplotlib.use('PS')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def start():
    js = json.loads(request.data.decode('utf-8'))
    print(js)

    try:
        mode = request.mode
        image = request.files['image']
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filename)
    except:
        return jsonify({"result": "Error"})

    # Do something depending on mode
    if mode == "caption":
        return captionImage(image)
    elif mode == "faces":
        return describeFaces(image)
    elif mode == "test":
        return jsonity({"result": "Success!"})
    else:
        return jsonify({"result": "Error"})

def describeFaces():
    """
    Input: Image
    Output: JSON, with info
    e.g. {"result": "two people: one is 80% happy, two is 72% sad"}
    """
    json = {}
    return jsonify(json)


# Compare Azure and IBM Watson captioning
def captionImage():
    """
    Input: Image
    Output: JSON, with info
    e.g. {"result": "a red fox in a green field", "confidence": 88.5, "other stuff".....}
    """
    json = {}
    return jsonify(json)

if __name__ == "__main__":
    app.run(debug=True)