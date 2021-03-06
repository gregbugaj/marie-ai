import base64
import os
import requests

api_base_url = 'http://127.0.0.1:5000/api'
default_queue_id = '0000-0000-0000-0000'
api_key = 'MY_API_KEY'

auth_headers = {
    'Authorization': f'Bearer {api_key}'
}

def online(api_ulr) -> bool:
    import requests
    r = requests.head(api_ulr)
    return r.status_code == 200

def process_extract(queue_id: str, file_location: str) -> str:
    if not os.path.exists(file_location):
        raise Exception(f'File not found : {file_location}')
    upload_url = f'{api_base_url}/extract/{queue_id}'

    # if not online(api_base_url):
    #     raise Exception(f"API server is not online : {api_base_url}")

    # Prepare file for upload
    with open(file_location, 'rb') as file:
        encoded_bytes = base64.b64encode(file.read())
        base64_str = encoded_bytes.decode('utf-8')

        json_payload = {
            "data": base64_str,
            "mode": "word"
        }

        print(json_payload)
        # Upload file to api
        print(f'Uploading to marie-icr for processing : {file}')
        json_result = requests.post(
            upload_url,
            headers=auth_headers,
            json=json_payload
        ).json()

        print(json_result)
        return json_result

if __name__ == '__main__':
    # Specify the path to the file you would like to process
    # file_location = './set-001/test/fragment-003.png'
    src = '/home/gbugaj/dev/sk-snippet-dump/hashed/AARON_JANES/38585416cc1f22103336f3419390c9ce.tif'
    process_extract(queue_id=default_queue_id, file_location=src)
