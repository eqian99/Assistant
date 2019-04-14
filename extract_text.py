import requests
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
# from PIL import Image
# from io import BytesIO

class ExtractText:
    def __init__(self, image):
        # Subscription Key for Computer Vision API
        subscription_key = '9a801624fab842b8867b963ecc5f151f'
        assert subscription_key

        self.image = image

        vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
        self.ocr_url = vision_base_url + "ocr"

        # https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python-print-text
        self.headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key
        }

        self.params  = {'language': 'unk', 'detectOrientation': 'true'}


    def extractText(self):
        """
        Takes binary image and returns extracted text via OCR
        Currently only returns text if 'language' detected as 'en'
        """
        extracted_text = ''
        analysis = {}
        try:
            response = requests.post(self.ocr_url, headers=self.headers, params=self.params, data=self.image)
            response.raise_for_status()
            analysis = response.json()

            print(analysis)
            if analysis["language"] == "en":
                # Extract the word bounding boxes and text.
                line_infos = [region["lines"] for region in analysis["regions"]]
                word_infos = []
                for line in line_infos:
                    for word_metadata in line:
                        for word_info in word_metadata["words"]:
                            word_infos.append(word_info)
                extracted_text = ' '.join(wi['text'] for wi in word_infos)
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        output = {'_result': extracted_text, 'response': analysis}
        return output
        

    def displayImage(self, word_infos):
        # Display the image and overlay it with the extracted text.
        plt.figure(figsize=(5, 5))
        ax = plt.imshow(self.image, alpha=0.5)
        for word in word_infos:
            bbox = [int(num) for num in word["boundingBox"].split(",")]
            text = word["text"]
            origin = (bbox[0], bbox[1])
            patch  = Rectangle(origin, bbox[2], bbox[3], fill=False, linewidth=2, color='y')
            ax.axes.add_patch(patch)
            plt.text(origin[0], origin[1], text, fontsize=20, weight="bold", va="top")
        plt.axis("off")
