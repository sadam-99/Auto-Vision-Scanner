from google.cloud import vision
from google.cloud.vision import types
import os

client = vision.ImageAnnotatorClient()

client = vision.ImageAnnotatorClient.from_service_account_file('/Users/ruchisingh/google_creds.json')

class Detect_Image:

	def detect_image(imagePath):


		if os.path.exists("images/.DS_Store"):
			os.remove("images/.DS_Store")

		image_to_open = imagePath


		with open(image_to_open, 'rb') as image_file:
			content = image_file.read()

		image = vision.types.Image(content=content)

		text_response = client.text_detection(image=image)

		texts = [text.description for text in text_response.text_annotations]

		print(texts)

		if len(texts) != 0:
			texts_to_show = texts[0]

			output = texts_to_show

			#show web response of the detected image

			web_response = client.web_detection(image=image)

			#web_response = client.web_detection(image=image)

			web_content = web_response.web_detection
			web_content.best_guess_labels

			predictions = [(entity.description, '{:.2%}'.format(entity.score)) for entity in web_content.web_entities]

			web_content.full_matching_images

			web_content.visually_similar_images[:3]

		else:
			#to detect facial emotion recognition

			# image_to_open = imagePath

			print(image_to_open)

			with open(image_to_open, 'rb') as image_file:
				content = image_file.read()
			image = vision.types.Image(content=content)

			face_response = client.face_detection(image=image)
			face_content = face_response.face_annotations
			print("face", face_content)

			conf = face_content[0].detection_confidence
			

			face_content_result = face_content[0]



			output = str(face_content_result)

		return output

		

		


