import pandas as pd
from playwright.sync_api import sync_playwright
from pathlib import Path

class Logger:
    def __init__(self):
        self.dataframe = pd.DataFrame(columns=['time', 'page', 'message_type', 'message'])

    def logVariables(self , url_list, browser_option, headless_option):
        totalUrls = len(url_list)
        currProgress = 0

        print("-------------------------------")
        print("Current progress:")
        print("\r0 of " + str(totalUrls) + " pages...", end='')

        with sync_playwright() as p:
            if browser_option == 'firefox':
                browser = p.firefox.launch(headless=headless_option)
            else:
                browser = p.chromium.launch(headless=headless_option)

            page = browser.new_page()

            for url in url_list:
                startTime = pd.Timestamp.now()
                page.goto(url)
                try:
                    page.wait_for_load_state('networkidle')
                except:
                    currTime = pd.Timestamp.now()
                    self.dataframe.loc[len(self.dataframe)] = [currTime, url, 'LOADING_TIMED_OUT', 'NOT A CONSOLE MESSAGE: Loading timed out, proceeding to the next page...']
                    #TODO: Add timeout CLI argument.

                currTime = pd.Timestamp.now()
                timeDelta = currTime - startTime
                self.dataframe.loc[len(self.dataframe)] = [currTime, url, 'PAGE_LOADING_TIME', str(timeDelta.total_seconds()) + ' seconds']
                
                for message in page.console_messages():
                    self.dataframe.loc[len(self.dataframe)] = [currTime, url, message.type, message.text]

                currProgress += 1
                if currProgress == totalUrls:
                    print ("\rDONE!", "                          ")

                else:
                    progress = str(currProgress) + " of " + str(totalUrls) + " pages..."
                    print ("\r" + progress, end='')

            browser.close()
            

    def saveCSV(self, output_path):
        file_path = (
            str(Path(output_path).absolute())
            + "/"
            + str(pd.Timestamp.now().date()) 
            + "-"
            + str(pd.Timestamp.now().time().replace(microsecond=0)).replace(":", "-")
            + ".csv"
        )

        print("-------------------------------")
        print("Report preview:")
        print(self.dataframe.head(5))
        print("...")
        print("")

        self.dataframe.to_csv(file_path, index=False)
        
        print("Report saved at: " + file_path)

print()