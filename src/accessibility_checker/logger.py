import pandas as pd
from playwright.sync_api import sync_playwright, Error, TimeoutError
from pathlib import Path

from checkers import CHECKERS

class Logger:
    def __init__(self):
        self.dataframe = pd.DataFrame(columns=[
            'time', 'page', 'criterion', 'message_type', 'tag', 'message', 'code'
        ])

    def checkHTML(self, html, url):
        for checkerClass in CHECKERS:
            checker = checkerClass()
            for result in checker.validate(html):
                self.dataframe.loc[len(self.dataframe)] = [
                    pd.Timestamp.now(), url, checker.criterion, 'REVIEW_REQUIRED',
                    result['tag'], result['message'], result['code']
                ]

    def checkPages(self, url_list, browser_option, headless_option):
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

            try:
                for url in url_list:
                    page = browser.new_page()
                    try:
                        page.goto(url)
                        try:
                            page.wait_for_load_state('networkidle')
                        except TimeoutError:
                            self.dataframe.loc[len(self.dataframe)] = [
                                pd.Timestamp.now(), url, '', 'LOADING_TIMED_OUT', '',
                                'Network idle timed out; checking the currently loaded HTML.', ''
                            ]
                        self.checkHTML(page.content(), url)
                    except Error as error:
                        self.dataframe.loc[len(self.dataframe)] = [
                            pd.Timestamp.now(), url, '', 'PAGE_ERROR', '', str(error), ''
                        ]
                    finally:
                        page.close()

                    currProgress += 1
                    if currProgress == totalUrls:
                        print("\rDONE!", "                          ")
                    else:
                        progress = str(currProgress) + " of " + str(totalUrls) + " pages..."
                        print("\r" + progress, end='')
            finally:
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
