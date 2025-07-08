# Fetch latest minutes and upload to wordpress account

# To load packages installed with pip when using a python version manager (asdf in my case),
# check that you are using the same python path in the interpreter of your IDE or code editor and on your system.
# For example, input [which python] in the terminal, and check python version/path for interpreter in VSCode
# by cmd+shift+p-> Python: Select interpreter -> select the same version as you see in your terminal.
# 

import os, pathlib, datetime, base64, requests, logging
from dotenv import load_dotenv

logging.getLogger('requests').setLevel(logging.WARNING)

load_dotenv()

# retrieve env variables
USERNAME = os.getenv('WORDPRESS_USERNAME')
PASSWORD = os.getenv('WORDPRESS_PASSWORD')
BASE_URL = os.getenv('WORDPRESS_SITE')
CONTENT_TYPE = {
   '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
   '.pdf': 'application/pdf'
}

# os pathway for minutes
# get year input
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")

RAW_DIRECTORY = f'~/Documents/Hager Park HOA/{year}/Minutes/to_upload/'
RAW_DESTINATION = f'~/Documents/Hager Park HOA/{year}/Minutes/uploaded/'
DIRECTORY = os.path.expanduser(RAW_DIRECTORY)
DESTINATION = os.path.expanduser(RAW_DESTINATION)
print(f'Retrieving documents from {DIRECTORY}')

FILES = pathlib.Path(DIRECTORY).iterdir()

def header(USERNAME, PASSWORD):
    credentials = USERNAME + ':' + PASSWORD
    token = base64.b64encode(credentials.encode())
    header_json = {'Authorization': 'Basic ' + token.decode('utf-8')}
    return header_json


def upload_to_wordpress(file_path, file_name, BASE_URL, header_json):
    url = BASE_URL + 'wp-json/wp/v2/media'
    media = {'file': open(file_path,'rb')}

    headers = header_json.copy()
    headers.update({
        'Content-Disposition': f'attachment; filename={file_name}',
        'Content-Type': f'{CONTENT_TYPE[file_path.suffix]}'
    })

    res = requests.post(url, headers = headers, files = media)
    return res.status_code


HEADER = header(USERNAME, PASSWORD)

for file in FILES:
  if os.path.isfile(file):
    file_name = os.path.basename(file)
    
    print(f'Attempting to upload {file_name}. . .')
    upload_status = upload_to_wordpress(file, file_name, BASE_URL, HEADER)

    if upload_status == 201:
      print(f'SUCCESS {upload_status}: Moving {file_name} to {DESTINATION}')
      os.rename(file, DESTINATION + file_name)
    else:
      print(f'ERROR {upload_status}: Failed to upload {file_name}')
