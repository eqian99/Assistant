import requests
import json
import operator

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
        def getAgeGender (age, gender):
            return "The subject looks like a " + age + " year old " + gender + "."

        def getExposureDescription (exposure_state):
            if exposure_state == 'UnderExposure':
                return "The camera is under exposed."
            elif exposure_state == 'OverExposure':
                return "The camera is over exposed."
            else:
                return ""

        def getOcclusion (foreheadOcclusion):
            if foreheadOcclusion:
                return "Their forehead is occluded. Please angle the camera down."
            else:
                return ""

        def getEmotion(emotion):
            return "They are {}.".format(emotion)
                
        response = requests.post(self.face_api_url, headers=self.headers, params=self.params, data=self.image)
        # response.raise_for_status()
        analysis = response.json()
        description = ""
        confidence = 1

        for i in range(len(analysis)):
            age = str(int(analysis[i]['faceAttributes']['age']))
            gender = analysis[i]['faceAttributes']['gender']
            emotions = analysis[i]['faceAttributes']['emotion']
            emotion = max(emotions.items(), key=operator.itemgetter(1))[0]
            exposure_state = analysis[i]['faceAttributes']['exposure']['exposureLevel']
            foreheadOcclusion = analysis[i]['faceAttributes']['occlusion']['foreheadOccluded']

            age_gender = getAgeGender(age, gender)
            exposure_descr = getExposureDescription(exposure_state)
            occlusion_descr = getOcclusion(foreheadOcclusion)
            emotion_descr = getEmotion(emotion)

            description += ' '.join([age_gender, emotion_descr, exposure_descr, occlusion_descr])

        output = {'_result': description, 'response': analysis, 'confidence': confidence}
        # print(json.dumps(analysis))

        return output
