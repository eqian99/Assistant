import requests
import json

class EmotionAzure:
    def __init__(self, image):
        # Subscription Key for Faces API
        subscription_key = '9193e2d12cb2422f8c17b8101e64a8f4'
        assert subscription_key

        self.image = image

        self.face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
        
        self.headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key
        }

        self.params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        }

    def analyzeFace(self):
        response = requests.post(self.face_api_url, headers=self.headers, params=self.params, data=self.image)
        response.raise_for_status()
        analysis = response.json()
        # TODO: Get confidence that there is a face
        confidence = 0
        description = ""

        try:
            age = str(int(response.json()[0]['faceAttributes']['age']))
            gender = response.json()[0]['faceAttributes']['gender']
            exposure_state = response.json()[0]['faceAttributes']['exposure']['exposureLevel']
            foreheadOcclusion = response.json()[0]['faceAttributes']['occlusion']['foreheadOccluded']

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

            age_gender = getAgeGender(age, gender)
            exposure_descr = print(getExposureDescription (exposure_state))
            occlusion_descr = print(getOcclusion (foreheadOcclusion))

            description = ' '.join([age_gender, exposure_descr, occlusion_descr])
        except:
            pass

        output = {'_result': description, 'confidence': confidence, 'response': analysis}
        # print(json.dumps(response.json()))

        return output