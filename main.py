import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from youtube_transcript_api import YouTubeTranscriptApi
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import csv

video_ids = []
final_video_ids = []
all_text = []
all_starting_time = []
all_url = []



class VideoTranscription:
    def __init__(self):
        self.keyword = input("Enter your keyword: ")

    def get_first_ten_video_id(self):
        self.options = Options()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Desktop\Youtube Transcription\chromedriver.exe", chrome_options=self.options)
        self.driver.get(f"https://www.youtube.com/results?search_query={self.keyword}") 
        self.driver.maximize_window()
        time.sleep(3)

        # If cookie is arise:
        # click = self.driver.find_element("xpath", "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
        # click.click()
        
        for x in range(1, 11):
            try:
                youtube_url = self.driver.find_element("xpath", f"(//h3[@class='title-and-badge style-scope ytd-video-renderer']/a)[{x}]").get_attribute('href')
                video_id = youtube_url.split("=")[1]
                print(video_id)
                video_ids.append(video_id)
            except:
                pass
                print("Video ID is not avilable")
                
        print(f"Total Video id scraped {video_ids}")


    def check_if_transcription_avilable(self):
        for video_id in video_ids:
            self.driver.get(f"https://www.youtube.com/watch?v={video_id}")
            time.sleep(3)
            self.html = self.driver.page_source
            if "Show transcript" in self.html:
                final_video_ids.append(video_id)
        print(f"Transcript avilable video id {final_video_ids}")
        
        time.sleep(2)
        self.driver.quit()


    def getting_transcript_point(self):
        for video_id in final_video_ids:
            transcript = YouTubeTranscriptApi.get_transcript(video_id,  languages=['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu', 'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw'])
            for x in range(len(transcript)):
                if self.keyword in transcript[x]['text']:
                    data = transcript[x]
                    text = data['text']
                    all_text.append(text)
                    starting_time = str(data['start']).split(".")[0]
                    all_starting_time.append(starting_time)
                    url_point = f"https://youtu.be/{video_id}?t={starting_time}"
                    print(f"{text} = {url_point}")
                    all_url.append(url_point)

        print(len(all_url))
        df = pd.DataFrame(
                        {
                            "Text": all_text,
                            "Starting Time": all_starting_time,
                            "URL Point": all_url
                        }
                    )
        df.to_csv("all_url_point.csv", index=False)
        print("Data saved successfully")


# # Running the bot
bot = VideoTranscription()
bot.get_first_ten_video_id()
bot.check_if_transcription_avilable()
bot.getting_transcript_point()

