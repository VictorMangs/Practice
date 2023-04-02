
import openai
import requests
import os
from PIL import Image

openai.api_key='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'

imageDir = os.getcwd()+'\\images'

if not os.path.isdir(imageDir):
    os.mkdir(imageDir)

#print(f"{imageDir=}")


prompt = "Superman saving the earth from an asteroid,digital art"


generation_response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024",
    response_format="url",)

#print(generation_response)

generated_image_name = "generated_image.png"
generated_image_filepath = os.path.join(imageDir, generated_image_name)
generated_image_url = generation_response["data"][0]["url"]
generated_image = requests.get(generated_image_url).content

with open(generated_image_filepath, "wb") as image_file:
    image_file.write(generated_image)  # write the image to the file

#print(generated_image_filepath)
#display(Image.open(generated_image_filepath))