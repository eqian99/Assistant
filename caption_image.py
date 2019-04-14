import requests

class CaptionImage:
    def __init__(self, image):
        # Subscription Key for Computer Vision API
        subscription_key = '9a801624fab842b8867b963ecc5f151f'
        assert subscription_key

        self.image = image

        vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
        self.analyze_url = vision_base_url + "analyze"

        # https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python-disk
        self.headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key
        }

        self.params = {'visualFeatures': 'Categories,Description,Color'}


    def captionImage(self):

        # # Set image_path to the local path of an image that you want to analyze.
        # image_path = "/Users/haoyuyun/Downloads/IMG_0795.JPG"
        # # Read the image into a byte array
        # image_data = open(image_path, "rb").read()

        try:
            # if image is binary:
            response = requests.post(self.analyze_url, headers=self.headers, params=self.params, data=self.image)
            response.raise_for_status()
            analysis = response.json()
            print(analysis)
            image_caption = analysis["description"]["captions"][0]["text"].capitalize()
            print(image_caption)
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        output = {'result': image_caption}
        return output
