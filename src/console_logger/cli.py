import sys
import argparse

from validators import Validators

from logger import Logger

from pandas import Timestamp

URL_LIST = BROWSER = OUTPUT_PATH = HEADLESS = None

#TODO: Implement paralel workers feature
#WORKERS = None 

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
            self.setVariables()
            self.logger.setVariables(URL_LIST, BROWSER, OUTPUT_PATH, HEADLESS)
            self.logger.logVariables()
            self.logger.saveCSV()
        else:
            print("Pre-flight verification failed!")


    def initializeArguments(self):
        parser = argparse.ArgumentParser()
        
        parser.add_argument("--url-file", nargs=1, help="Provide an URL map file or an sitemap URL", required=False)
        parser.add_argument("--urls", nargs='+', help="Provide the urls for scan separated by spaces", required=False)
        #parser.add_argument("--workers", nargs=1, help="Number of paralel browser sessions", required=False, default=1)
        parser.add_argument("--browser", choices=["firefox", "chromium"], help="Browser to run", required=False, default='chromium')
        parser.add_argument("-o", "--output-path", nargs=1, help="Path to output the CSV report", required=False)
        parser.add_argument("-hl", "--headless", help="Run in headless mode", action='store_true', required=False)
        #parser.add_argument("-v", "--verbose", help="Enable higher verbosity", action='store_true', required=False)
        #parser.add_argument("-l", "--log", help="Enable logging", action='store_true', required=False)

        args = parser.parse_args()

        self.urlFile = args.url_file if not type(args.url_file) == list else args.url_file[0]
        self.urls = args.urls
        #self.workers = args.workers if not type(args.workers) == list else args.workers[0]
        self.browser = args.browser if not type(args.browser) == list else args.browser[0]
        self.outputPath = args.output_path if not type(args.output_path) == list else args.output_path[0]
        self.headlessEnabled = args.headless
        #self.verboseEnabled = args.verbose
        #self.logEnabled = args.log

    def printArgs(self):
        print("URL file: " + str(self.urlFile))
        print("URL list: " + str(self.urls))
        #print("Workers: " + str(self.workers))
        print("browser: " + str(self.browser))
        print("Output path: " + str(self.outputPath))
        print("Headless: " + str(self.headlessEnabled))
        #print("Verbose: " + str(self.verboseEnabled))
        #print("Logs: " + str(self.logEnabled))

    def checkConditions(self):
        global URL_LIST
        valid = True

        if not (self.urlFile or self.urls):
            print("ERROR: --url-file or --urls must be provided") 
            valid = False

        elif self.urlFile and self.urls:
            print("ERROR: multiple url sources provided")
            valid = False

        elif self.urls:
            URL_LIST = self.validators.validateUrlList(self.urls)
            if len(URL_LIST) > 0:
                print("selected urls count: ", len(URL_LIST))
            else:
                print("ERROR: URL list rejected")
                valid = False

        elif self.urlFile:
            URL_LIST = self.validators.validateUrlFile(str(self.urlFile))
            if len(URL_LIST) > 0:
                print("Selected urls count: ", len(URL_LIST))    
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

        #try:
        #    self.workers = int(self.workers)
        #except:
        #    print("ERROR: failed converting workers parameter to integer")
        #    valid = False

        #if not type(self.workers) == int:
        #    print("ERROR: workers ammount must be an integer")
        #    valid = False

        return valid

    def setVariables(self):
        # The URL_LIST variable is already set on the checkConditions() function.
        global BROWSER, OUTPUT_PATH, HEADLESS#, WORKERS
        #WORKERS = self.workers
        BROWSER = self.browser
        HEADLESS = self.headlessEnabled
        OUTPUT_PATH = self.outputPath

        print("Parameter variables set")

def main():
    startTime = Timestamp.now()
    Initialize()
    timeDelta = Timestamp.now() - startTime
    print("-------------------------------")
    print("Program finished in " + str(timeDelta.total_seconds()) + " seconds")

if __name__ == "__main__":
    sys.exit(main())