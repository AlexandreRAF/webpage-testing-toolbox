import requests
import xml.etree.ElementTree as ET
from pathlib import Path

class Validators:
    def validateUrlList(self, url):
        invalidUrls = []
        validUrls = []
        for i in url:
            if i.startswith('http://') or i.startswith('https://'):
                validUrls.append(i)
            else:
                invalidUrls.append(i)

        if len(invalidUrls) > 0:
            print("ERROR: Invalid URL(s) detected, they will be ignored:")
            for i in invalidUrls:
                print(i)
            print('')    

        return validUrls

    def validateUrlFile(self, filePath):
        if filePath.endswith('.xml'):
            return self.validateXML(filePath)
        return self.validateTXT(filePath)

    def validateTXT(self, path):
        try:
            if path.startswith('https://') or path.startswith('http://'):
                response = requests.get(path)
                #print (response.status_code)
                #print("CONTENT TYPE:", response.headers.get("Content-Type"))
                print(response.text)
                text = response.text.split()
            else:
                with open(path, "r") as file:
                    text = file.read().split()

            invalidUrls = []
            validUrls = []

            for i in text:
                if not (i.startswith('https://') or i.startswith('http://')):
                    invalidUrls.append(i)
                else:
                    validUrls.append(i)

            if len(invalidUrls) > 0:
                print('ERROR: Invalid URL(s) found on text file, they will be ignored:')
                for i in invalidUrls:
                    print(i)

            return validUrls

        except Exception as e:
            print("ERROR VALIDATING REMOTE TEXT FILE: " + str(e))
            return []            

    def validateXML(self, path):
        try:
            if path.startswith('https://') or path.startswith('http://'):
                response = requests.get(path)
                #print (response.status_code)
                #print("CONTENT TYPE:", response.headers.get("Content-Type"))
                root = ET.fromstring(response.text)
            else:
                root = ET.parse(path)

            invalidUrls = []
            validUrls = []

            for elem in root.iter():
                if elem.tag.split("}")[-1] == "loc":
                    if not (elem.text.startswith('https://') or elem.text.startswith('http://')):
                        invalidUrls.append(elem.text)
                    else:
                        validUrls.append(elem.text)

            if len(invalidUrls) > 0:
                print('ERROR: Invalid URL(s) found on XML file, they will be ignored:')
                for i in invalidUrls:
                    print(i)

            return validUrls

        except Exception as e:
            print("ERROR VALIDATING REMOTE XML: " + str(e))
            return []

    def validateOutputPath(self, path):
        directory = Path(path)
        if (directory.exists() == True and directory.is_dir() == True):
            print(directory.absolute())
            return True
        return False 