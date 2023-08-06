from werkzeug import wrappers
import os
from io import BytesIO
from PIL import Image
from requests.models import Response
import json

def get_upload_image_preprocess_input(image_path: str, name: str):
    """Return a mock input for preprocess that simulates the input from proxy while it was invoked as follows:
    curl -F "filename=test.png" -F "name=@test.png" PROXY_API_URL

    Keyword arguments:
    image_path -- the path to the file
    name -- the name in input.files

    Usage:
        input = get_upload_image_preprocess_input('test.png', 'image')
        image = input.files["image"]
    """
    with open(image_path, "rb") as img:
        image_content = img.read()
        file_name = os.path.basename(image_path)
        data = (b"--boundary\r\n")
        data += (b'Content-Disposition: form-data; name="') + name.encode() + (b'"; filename="') + file_name.encode() + (b'"\r\n')
        image_info = Image.open(image_path)
        data += (b"Content-Type: ") + image_info.get_format_mimetype().encode() + (b"\r\n")
        data += (b"\r\n")
        data += image_content
        data += (b"\r\n")
        data += (b"--boundary--")
        request = wrappers.Request.from_values(
            input_stream = BytesIO(data),
            content_length = len(data),
            content_type = "multipart/form-data; boundary=boundary",
            method = "POST",
        )

        return request

def get_postprocess_input(inference_result):
    """Return a mock input for postprocess that inference_result simulates the result form model inferencing.

    Keyword arguments:
    inference_result -- the result that simulates the result form model inferencing
    """
    response = Response()
    response.code = "ok"
    response.status_code = 200
    if(isinstance(inference_result, dict)):
        inference_result = json.dumps(inference_result)
        response._content = inference_result.encode()
    elif(isinstance(inference_result, str)):
        response._content = inference_result.encode()

    return response
