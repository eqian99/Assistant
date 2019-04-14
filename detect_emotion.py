import requests
import json

class EmotionAzure:
    def __init__(self, image_url=None):
        # Subscription Key for Faces API
        subscription_key = '9193e2d12cb2422f8c17b8101e64a8f4'
        assert subscription_key

        # TODO: Change to send binary image data, instead of url of image (see caption_image.py for reference)
        if image_url == None:
            image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg'
        self.image_url = image_url

        self.face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

        self.headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

        self.params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        }

    def analyzeFace(self):
        def getAgeGender (age, gender):
            return "The subject pictured is a " + age + " year old " + gender + "."

        def getExposureDescription (exposure_state):
            if exposure_state == 'UnderExposure':
                return "The camera is under exposed. Please turn up the exposure."
            elif exposure_state == 'OverExposure':
                return "The camera is over exposed. Please turn up the exposure."
            else:
                return ""

        def getOcclusion (foreheadOcclusion):
            if foreheadOcclusion:
                return "The subject's forehead is occluded. Please angle the camera down."
            else:
                return ""

        response = requests.post(self.face_api_url, params=self.params, headers=self.headers, json={"url": self.image_url})
        for i in range(len(response.json())):
            age = str(int(response.json()[i]['faceAttributes']['age']))
            gender = response.json()[i]['faceAttributes']['gender']
            exposure_state = response.json()[i]['faceAttributes']['exposure']['exposureLevel']
            foreheadOcclusion = response.json()[i]['faceAttributes']['occlusion']['foreheadOccluded']

            age_gender = getAgeGender(age, gender)
            exposure_descr = print(getExposureDescription (exposure_state))
            occlusion_descr = print(getOcclusion (foreheadOcclusion))

            # TODO: Any other ideas? :)

            description = ' '.join([age_gender, exposure_descr, occlusion_descr])
            output = {'_result': description, 'confidence': confidence, 'response': response}
            # print(json.dumps(response.json()))

        return output
