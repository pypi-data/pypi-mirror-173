from werkzeug import wrappers
import os
from PIL import Image
from requests.models import Response

def get_upload_image_mock_request(image_path):
    with open(image_path, "rb") as img:
        image_content = img.read()
        file_name = os.path.basename(image_path)
        data = (b"--boundary\r\n")
        data += (b'Content-Disposition: form-data; name="image"; filename="') + file_name.encode() + (b'"\r\n')
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

def get_inference_mock_response(inference_result):
    response = Response()
    response.code = "ok"
    response.status_code = 200
    if(isinstance(inference_result, dict)):
        inference_result = json.dumps(inference_result)
        response._content = inference_result.encode()
    elif(isinstance(inference_result, str)):
        response._content = inference_result.encode()

    return response
