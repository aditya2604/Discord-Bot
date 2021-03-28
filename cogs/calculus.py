import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class Calculus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['derive', 'der', 'drv', 'differentiate', 'derivative'], description="calculates the derivative of the entered equation")
    async def deriv(self, ctx, *, problem:str):

        await ctx.send("Calculating derivative - please wait patiently, est. wait time 5-10 seconds")

        GOOGLE_CHROME_PATH = os.environ['GOOGLE_CHROME_BIN']
        CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.binary_location = GOOGLE_CHROME_PATH

        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

        driver.get("https://www.wolframalpha.com/calculators/derivative-calculator/")

        search = driver.find_element_by_id("_1jqx4")
        search.send_keys(f"derivative {problem}")
        search.send_keys(Keys.RETURN)

        try:
            main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_8J16o"))
            )

            img = main.find_element_by_tag_name("img").get_attribute("src")

            link = driver.current_url
            embed = discord.Embed(title="", description=f"[derivative of {problem}]({link})", color=discord.Color.green())
            embed.set_image(url=str(img))
            embed.set_footer(text=f"Derivative requested by {ctx.author.display_name} | Answer from WolframAlpha")
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(title="", description=f"derivative of {problem} not found", color=discord.Color.green())
            await ctx.send(embed=embed)
            driver.quit()

        driver.quit()

    @commands.command(description="calculates entered integral")
    async def integrate(self, ctx, *, problem:str):

        await ctx.send("Calculating integral - please wait patiently, est. wait time 5-10 seconds")

        GOOGLE_CHROME_PATH = os.environ['GOOGLE_CHROME_BIN']
        CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.binary_location = GOOGLE_CHROME_PATH

        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

        driver.get("https://www.wolframalpha.com/calculators/integral-calculator/")

        search = driver.find_element_by_id("_1jqx4")
        search.send_keys(f"integrate {problem}")
        search.send_keys(Keys.RETURN)

        try:
            main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_8J16o"))
            )

            img = main.find_element_by_tag_name("img").get_attribute("src")

            link = driver.current_url
            embed = discord.Embed(title="", description=f"[integral of {problem}]({link})", color=discord.Color.green())
            embed.set_image(url=str(img))
            embed.set_footer(text=f"Integral requested by {ctx.author.display_name} | Answer from WolframAlpha")
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(title="", description=f"integral of {problem} not found", color=discord.Color.green())
            await ctx.send(embed=embed)
            driver.quit()

        driver.quit()


def setup(bot):
    bot.add_cog(Calculus(bot))