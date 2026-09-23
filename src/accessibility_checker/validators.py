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
                response = requests.get(path, timeout=30)
                response.raise_for_status()
                text = response.text.split()
            else:
                with open(path, "r", encoding='utf-8') as file:
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
            print("ERROR VALIDATING TEXT FILE: " + str(e))
            return []            

    def validateXML(self, path):
        try:
            if path.startswith('https://') or path.startswith('http://'):
                response = requests.get(path, timeout=30)
                response.raise_for_status()
                root = ET.fromstring(response.text)
            else:
                root = ET.parse(path)

            invalidUrls = []
            validUrls = []

            for elem in root.iter():
                if elem.tag.split("}")[-1] == "loc":
                    url = (elem.text or '').strip()
                    if not (url.startswith('https://') or url.startswith('http://')):
                        invalidUrls.append(url)
                    else:
                        validUrls.append(url)

            if len(invalidUrls) > 0:
                print('ERROR: Invalid URL(s) found on XML file, they will be ignored:')
                for i in invalidUrls:
                    print(i)

            return validUrls

        except Exception as e:
            print("ERROR VALIDATING XML: " + str(e))
            return []

    def validateOutputPath(self, path):
        directory = Path(path)
        if (directory.exists() == True and directory.is_dir() == True):
            print(directory.absolute())
            return True
        return False 
