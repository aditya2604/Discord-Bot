import discord
from discord.ext import commands
import asyncio
import random
from media.drawings import *


class Hangman(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_word(self):
        lines = open("media/word_list").readlines()
        word = random.choice(lines)
        word = word[:-1]
        print(word)
        return word

    def instances(self, s, ch):
        return [i for i, letter in enumerate(s) if letter == ch]

    def check_finished(self, blanks, word, not_finished):
        blanks = blanks.replace(' ', '')
        if blanks == word:
            not_finished = False
        else:
            not_finished = True
        return not_finished

    def check_chances(self, num_chances_left):
        if num_chances_left == 0:
            chances_left = False
        else:
            chances_left = True
        return chances_left

    @commands.command(aliases=['hangmen', 'hangmn', 'hang', 'hngmn', 'men'], description="hangman game")
    async def hangman(self, ctx):
        word = self.get_word()
        not_finished = True
        chances_left = True
        num_chances_left = 9
        blanks = ''
        letters_guessed = []
        for i in range(len(word)):
            blanks += '_ '
        hangman_board = await ctx.send(f"```{hangmen[num_chances_left]}```")
        blanks_board = await ctx.send(f"```Word: {blanks}```")
        self.bot.loop.create_task(self.hangman_loop(ctx, letters_guessed, not_finished, chances_left, num_chances_left, word, blanks, hangman_board, blanks_board))

    async def hangman_loop(self, ctx, letters_guessed, not_finished, chances_left, num_chances_left, word, blanks, hangman_board, blanks_board):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        while not_finished and chances_left:
            try:
                letter = await self.bot.wait_for('message', timeout=20.0, check=check)
                msg = letter
                letter = letter.content.lower()
                try:
                    await msg.delete()
                except:
                    pass
            except asyncio.TimeoutError:
                return await ctx.send(f'letter not picked in time\nthe word was `{word}`')

            if letter not in word and letter not in letters_guessed:
                num_chances_left -= 1
                chances_left = self.check_chances(num_chances_left)
            elif letter in letters_guessed:
                previous_guesses = letters_guessed.count(letter)
                if previous_guesses == 1:
                    previous_guesses = f"{previous_guesses} time"
                else:
                    previous_guesses = f"{previous_guesses} times"
                await ctx.send(f"you've already attempted this letter {previous_guesses}...", delete_after=2.5)
            else:
                for i in word:
                    if letter == i:
                        pos = self.instances(word, letter)
                        for _ in pos:
                            blanks = blanks.replace(' ', '')
                            blanks = blanks[:_] + letter + blanks[_ + 1:]
                            blanks = " ".join(blanks)
                        not_finished = self.check_finished(blanks, word, not_finished)
            letters_guessed.append(letter)
            wrong_letters_guessed = [i for i in letters_guessed if i not in word]
            wrong_letters_guessed = list(dict.fromkeys(wrong_letters_guessed))
            await hangman_board.edit(content=f"```{hangmen[num_chances_left]} {'[%s]' % ', '.join(map(str, wrong_letters_guessed))}```")
            await blanks_board.edit(content=f"```Word: {blanks}```")
        if not chances_left:
            await hangman_board.edit(content=f"```{hangmen[num_chances_left]} {'[%s]' % ', '.join(map(str, wrong_letters_guessed))}\n\nWord: {blanks}```\nrip to the homie - had to die cuz of {ctx.author.mention}'s stupidity lol gg\nthe word was `{word}`")
            await blanks_board.delete()
        if not not_finished:
            await hangman_board.edit(content=f"```{hangmen[num_chances_left]}\n\nWord: {blanks}```\nggs {ctx.author.mention} - you found the word")
            await blanks_board.delete()
        return


def setup(bot):
    bot.add_cog(Hangman(bot))
