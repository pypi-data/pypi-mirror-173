import requests
import traceback
import sys
import json

class Logger():
    _apiKey = ""
    _clientSecret = ""
    _applicationName = ""
    def __init__(self, apiKey, clientSecret, applicationName):
        self._apiKey = apiKey
        self._clientSecret = clientSecret
        self._applicationName = applicationName

    def LogError(self, error_type, error_message, error_traceback):
        stack = traceback.extract_tb(error_traceback)
        (filename, line, procname, text) = stack[-1]
        error = {}
        error['type'] = 'Error'
        error['message'] = str(error_message)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        error['traceback'] = traceback.format_tb(error_traceback)
        self.LogMessage(error)

    def LogError(self, err):
        stack = traceback.extract_tb(err.__traceback__)
        (filename, line, procname, text) = stack[-1]
        error = {}
        error['type'] = 'Error'
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        error['traceback'] = traceback.format_tb(err.__traceback__)
        self.LogMessage(error)

    def LogCritical(self, err):
        stack = traceback.extract_tb(err.__traceback__)
        (filename, line, procname, text) = stack[-1]
        error = {}
        error['type'] = 'Critical'
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        error['traceback'] = traceback.format_tb(err.__traceback__)
        self.LogMessage(error)

    def LogInformation(self, err):
        stack = traceback.extract_tb(err.__traceback__)
        (filename, line, procname, text) = stack[-1]
        error = {}
        error['type'] = 'Information'
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        error['traceback'] = traceback.format_tb(err.__traceback__)
        self.LogMessage(error)

    def LogDebug(self, err):
        stack = traceback.extract_tb(err.__traceback__)
        (filename, line, procname, text) = stack[-1]
        error = {}
        error['type'] = 'Debug'
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        error['traceback'] = traceback.format_tb(err.__traceback__)
        self.LogMessage(error)

    def LogTrace(self, err):
        stack = traceback.extract_tb(err.__traceback__)
        (filename, line, procname, text) = stack[-1]
        error = {}
        error['type'] = 'Trace'
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        error['traceback'] = traceback.format_tb(err.__traceback__)
        self.LogMessage(error)

    def LogWarning(self, err):
        stack = traceback.extract_tb(err.__traceback__)
        (filename, line, procname, text) = stack[-1]
        error = {}
        error['type'] = 'Warning'
        error['message'] = str(err)
        error['file'] = filename
        error['line'] = line
        error['procname'] = procname
        error['traceback'] = traceback.format_tb(err.__traceback__)
        self.LogMessage(error)

    def LogMessage(self, message):
        URL = "https://log.clearinsights.io/log/preprocesslog"  
        applicationName = self._applicationName

        framework = "Python " + ".".join([str(sys.version_info.major),str(sys.version_info.minor),str(sys.version_info.micro)])

        HEADERS  = {'apikey':self._apiKey, 'clientsecret':self._clientSecret, 'framework':framework, 'applicationName':applicationName, 'logType':message['type'], 'isPython':"true", }
  
        r = requests.post(url = URL, headers = HEADERS, json= message)

class DynamicMetric:
    _apiKey = ""
    _clientSecret = ""
    _applicationName = ""
    def __init__(self, apiKey, clientSecret, applicationName):
        self._apiKey = apiKey
        self._clientSecret = clientSecret
        self._applicationName = applicationName

    def SendPayload(self, payload):
        URL = "https://monitor.clearinsights.io/monitor/savedynamicmetric"  
        applicationName = self._applicationName
        _payload = {}
        _payload["Payload"] = json.dumps(payload)
        HEADERS  = {'apikey':self._apiKey, 'clientsecret':self._clientSecret, 'applicationName':applicationName, 'isPython':"true", }
  
        r = requests.post(url = URL, headers = HEADERS, json= _payload)






   

