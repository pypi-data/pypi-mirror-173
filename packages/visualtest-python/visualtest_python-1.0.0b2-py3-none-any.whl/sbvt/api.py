import os
import logging
import json
import requests
import sbvt
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(f'vt.{os.path.basename(__file__)}')
host = os.environ["VT_API_HOST"] if "VT_API_HOST" in os.environ else 'https://api.visualtest.io'
api = requests.Session()
s3 = requests.Session()

# from https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 10  # seconds
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


# define retry strategy and timeout
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = TimeoutHTTPAdapter(timeout=10, max_retries=retries)

# Mount it for both http and https usage
api.mount("https://", adapter)
api.mount("http://", adapter)
s3.mount("https://", adapter)

s3.headers.update({"Content-Type": "application/octet-stream"})


class Api:

    def __init__(self, projectToken=None):
        self.baseUrl = f'{host}/api/v1'
        self.projectToken = None
        self.projectId = None
        if projectToken:
            self.projectToken = projectToken
            self.projectId = projectToken.split("/")[0]
            api.headers.update({'Authorization': f'Bearer {projectToken}'})
        self.testRun = None

    def getDeviceInfo(self, userAgentInfo, driverCapabilities):

        url = f'{self.baseUrl}/device-info/'
        log.info(f'calling API to get device info at: {url}')
        response = api.post(url, json={'userAgentInfo': userAgentInfo, 'driverCapabilities': driverCapabilities})
        if response.status_code in range(200, 300):

            return response.json()
        else:
            raise Exception(f'Failed to save image. HTTP Response: {response}')

    def findTestRunByName(self, name):
        query = {'testRunName': {'eq': name}}
        url = f'{self.baseUrl}/projects/{self.projectId}/testruns?q={requests.utils.quote(json.dumps(query))}'
        log.info(f'calling API to get testRun by name: {url}')
        response = api.get(url)
        log.info(f'findTestRunByName response: {response}')
        if response.status_code in range(200, 300):
            result = response.json()
            if type(result['items']) == 'list' and len(result['items']) == 1:
                log.info(f'Found existing testrun: {str(result)}')
                return result['testruns'][0]
            else:
                log.info(f"type of items: {type(result['items'])}")
                log.info(f"length of items: {len(result['items'])}")
                log.info(f'Did NOT find existing testrun')
                return None
        else:
            raise Exception(f'Failed to get test run by name: {name}. HTTP Response: {str(response)}')

    def createTestRun(self, testRunName):

        url = f'{self.baseUrl}/projects/{self.projectId}/testruns'
        log.info(f'calling API to create testRun by name: {url}')
        response = api.post(url, json={
            'testRunName': testRunName,
            'sdk': 'python',
            'sdkVersion': sbvt.__version__,
        })
        if response.status_code in range(200, 300):
            return response.json()
        else:
            raise Exception(f'Failed to create testRun. HTTP Response: {response}')

    def saveImage(self, testRunName, imageData, filePath):
        log.info(f'Saving image for testRunName: {testRunName}')
        # check if testRun already exists, if not create one
        if not self.testRun:
            result = self.findTestRunByName(testRunName)
            if result:
                self.testRun = result
            else:
                self.testRun = self.createTestRun(testRunName)

        url = f'{self.baseUrl}/projects/{self.projectId}/testruns/{self.testRun["testRunId"]}/images'
        log.info(f'calling API to save image: {url}')
        log.debug(f'imageData: {imageData}')

        response = api.post(url, json=imageData)
        log.info(f'create image response: {response}')

        if response.status_code in range(200, 300):
            result = response.json()
        else:
            raise Exception(f'Failed to create image. HTTP Response: {response.json()}')

        imageBinary = open(filePath, "rb")
        log.info(f'uploading image to: {result["uploadUrl"]}')

        response = s3.put(result['uploadUrl'], data=imageBinary)
        log.info(f'upload image response: {response}')
        imageBinary.close()

        if response.status_code in range(200, 300):
            return result
        else:
            raise Exception(f'Failed to upload image. HTTP Response: {response.json()}')
