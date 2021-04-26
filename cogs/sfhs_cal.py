import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime


class Calendar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_cal_month(self, driver):
        month = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fsCalendarGridShowMonthPickerButton"))).text
        calendar_month = (month.split(' ')[0]).lower()
        return calendar_month

    def get_right_button(self, driver):
        right_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='fsCalendarNextMonth fsRightArrow']")))
        return right_button

    def get_left_button(self, driver):
        left_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='fsCalendarPrevMonth fsLeftArrow']")))
        return left_button

    def month_page_turner(self, driver, calendar_month, user_month, user_month_num, current_month_num):
        if user_month_num > current_month_num:
            while calendar_month not in user_month and user_month not in calendar_month:
                self.get_right_button(driver).click()
                time.sleep(.1)
                calendar_month = self.get_cal_month(driver)
        else:
            while calendar_month not in user_month and user_month not in calendar_month:
                self.get_left_button(driver).click()
                time.sleep(.1)
                calendar_month = self.get_cal_month(driver)

    @commands.command(aliases=['cal'], description="shows SFHS calendar for 2021 of the specified month")
    async def calendar(self, ctx, month: str):

        await ctx.send("Getting calendar - please wait patiently, est. wait time 5-10 seconds")

        user_month = month

        GOOGLE_CHROME_PATH = os.environ['GOOGLE_CHROME_BIN']
        CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
        # CHROMEDRIVER_PATH = "/Users/adityatomar/Downloads/chromedriver"

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.binary_location = GOOGLE_CHROME_PATH
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        driver.maximize_window()

        size = driver.get_window_size()
        print("Window size: width = {}px, height = {}px".format(size["width"], size["height"]))

        driver.get("https://www.sfhs.com/calendar")

        calendar_month = self.get_cal_month(driver)

        current_month_num = int(datetime.now().strftime("%m"))

        try:
            user_month_num = int(datetime.strptime(user_month, "%B").month)
        except:
            user_month_num = int(datetime.strptime(user_month, "%b").month)

        self.month_page_turner(driver, calendar_month, user_month, user_month_num, current_month_num)

        html = driver.find_element_by_tag_name("html")

        for i in range(8):
            html.send_keys(Keys.ARROW_DOWN)

        driver.save_screenshot("media/screenshot.png")

        await ctx.send(file=discord.File("media/screenshot.png"))

        try:
            os.remove("media/screenshot.png")
            print("file removed")
        except:
            print("file not found")
            pass

        driver.quit()

def setup(bot):
    bot.add_cog(Calendar(bot))
