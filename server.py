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
    # Video location
    loc = "/Users/haoyuyun/Desktop/ATT/Assistant/{}".format(js['link'])
    print(loc)
    try:
        # os.system("python3 tf-pose/run.py --model=mobilenet_v2_small --resolution=432x368 --image={}".format(loc))
        os.system("python3 tf-pose/run_webcam.py --model=mobilenet_v2_small --resize=432x368 --camera=0")
    except:
        pass
    # TODO: Send POST request to IBM Watson depending on mode (given in header)
    # TODO: use enums
    if mode == "caption":
        return captionImage()
    elif mode == "faces":
        return describeFaces()
    return {"result": "Error"}

def describeFaces():
    """
    Input: Image
    Output: JSON, with info
    e.g. {"result": "two people: one is 80% happy, two is 72% sad"}
    """
    return {}


# Compare Azure and IBM Watson captioning
def captionImage():
    """
    Input: Image
    Output: JSON, with info
    e.g. {"result": "a red fox in a green field", "confidence": 88.5, "other stuff".....}
    """
    json = {}
    return json

if __name__ == "__main__":
    app.run(debug=True)