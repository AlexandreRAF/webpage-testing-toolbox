import sys
import argparse

from pandas import Timestamp

from validators import Validators
from logger import Logger

class Initialize:
    def __init__(self):

        self.validators = Validators()
        self.logger = Logger()
        self.initializeArguments()

        print("Arguments:")

        self.printArgs()

        print("-------------------------------")

        if self.checkConditions():
            print("-------------------------------")
            print("Pre-flight verification passed!")
            variables = self.setVariables()
            self.logger.checkPages(variables['url_list'], variables['browser'], variables['headless'])
            self.logger.saveCSV(variables['output_path'])
        else:
            print("Pre-flight verification failed!")


    def initializeArguments(self):
        # Set and parse the arguments 
        parser = argparse.ArgumentParser(description='Check webpages for potential WCAG accessibility issues.')
        
        parser.add_argument("--url-file", nargs=1, help="Provide an URL map file or an sitemap URL", required=False)
        parser.add_argument("--urls", nargs='+', help="Provide the urls for scan separated by spaces", required=False)
        parser.add_argument("--browser", choices=["firefox", "chromium"], help="Browser to run", required=False, default='chromium')
        parser.add_argument("-o", "--output-path", nargs=1, help="Path to output the CSV report", required=False)
        parser.add_argument("-hl", "--headless", help="Run in headless mode", action='store_true', required=False)

        args = parser.parse_args()

        self.urlFile = args.url_file if not type(args.url_file) == list else args.url_file[0]
        self.urls = args.urls
        self.browser = args.browser if not type(args.browser) == list else args.browser[0]
        self.outputPath = args.output_path if not type(args.output_path) == list else args.output_path[0]
        self.headlessEnabled = args.headless

    def printArgs(self):
        print("URL file: " + str(self.urlFile))
        print("URL list: " + str(self.urls))
        print("browser: " + str(self.browser))
        print("Output path: " + str(self.outputPath))
        print("Headless: " + str(self.headlessEnabled))

    def checkConditions(self):
        valid = True
        self.urlList = []

        if not (self.urlFile or self.urls):
            print("ERROR: --url-file or --urls must be provided") 
            valid = False

        elif self.urlFile and self.urls:
            print("ERROR: multiple url sources provided")
            valid = False

        elif self.urls:
            self.urlList = self.validators.validateUrlList(self.urls)
            if len(self.urlList) > 0:
                print("selected urls count: ", len(self.urlList))
            else:
                print("ERROR: URL list rejected")
                valid = False

        elif self.urlFile:
            self.urlList = self.validators.validateUrlFile(str(self.urlFile))
            if len(self.urlList) > 0:
                print("Selected urls count: ", len(self.urlList))
            else:
                print("ERROR: URL File rejected")
                valid = False 


        if self.outputPath:
            if self.validators.validateOutputPath(str(self.outputPath)):
                print("Output path:", str(self.outputPath))
            else:
                print("ERROR: Output path rejected")
                valid = False

        else:
            print("ERROR: no output file path provided.")
            valid = False

        return valid

    def setVariables(self):
        # The URL list is already set by checkConditions().

        print("Parameter variables set")
        return {'browser': self.browser, 'headless': self.headlessEnabled, 'output_path': self.outputPath, 'url_list': self.urlList}

def main():
    startTime = Timestamp.now()
    Initialize()
    timeDelta = Timestamp.now() - startTime
    print("-------------------------------")
    print("Program finished in " + str(timeDelta.total_seconds()) + " seconds")

if __name__ == "__main__":
    sys.exit(main())
