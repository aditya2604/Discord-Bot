import discord
from discord.ext import commands
import random
import asyncio
from media.drawings import *


class Scramble(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_word(self):
        lines = open("media/word_list").readlines()
        word = random.choice(lines)
        word = word[:-1]
        print(word)
        return word

    @commands.command(aliases=['scrmble', 'scrm', 'scrim', 'scram', 'scramb', 'scrambl', 'scr'], description="scramble game")
    async def scramble(self, ctx):
        word = self.get_word()
        shuffled = ''.join(random.sample(word, len(word)))
        blanks = ''
        for i in range(len(shuffled)):
            blanks += '_ '
        board = await ctx.send(f"```Letters left: {' '.join(shuffled)}\n{blanks}```")
        message_reactions = []
        reaction_to_word = ""
        for i in shuffled:
            await board.add_reaction(DICT_ALPHABET[i])
            message_reactions.append(DICT_ALPHABET[i])
        await board.add_reaction(BACK_EMOJI)
        await board.add_reaction(STOP_EMOJI)
        message_reactions.append(BACK_EMOJI)
        message_reactions.append(STOP_EMOJI)
        not_finished = True
        not_wrong_guess = True
        self.bot.loop.create_task(self.scramble_loop(ctx, word, not_finished, message_reactions, reaction_to_word, blanks, board, shuffled, not_wrong_guess))

    def check_word(self, word, blanks, not_wrong_guess):
        blanks = blanks.replace(' ', '')
        if blanks != word:
            not_wrong_guess = False
        else:
            not_wrong_guess = True
        return not_wrong_guess

    async def scramble_loop(self, ctx, word, not_finished, message_reactions, reaction_to_word, blanks, board, shuffled, not_wrong_guess):
        while not_finished and not_wrong_guess:
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in message_reactions
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                message = reaction.message
            except asyncio.TimeoutError:
                return await ctx.send(f'word not guessed in time\nthe word was `{word}`')
            else:
                await message.remove_reaction(reaction, user)
                if reaction.emoji == STOP_EMOJI:
                    not_finished = False
                    return await board.edit(content = f"```Game ended...\nThe word was {word}```")
                for char, emote in DICT_ALPHABET.items():
                    if char in shuffled:
                        if reaction.emoji == emote:
                            reaction_to_word += f"{char}"
                            blanks = blanks.replace(' ', '')
                            blanks = blanks[:len(reaction_to_word)-1] + char + blanks[len(reaction_to_word):]
                            blanks = " ".join(blanks)
                            shuffled = shuffled.replace(char, '', 1)
                if reaction.emoji == BACK_EMOJI:
                    char = reaction_to_word[-1]
                    reaction_to_word = reaction_to_word[:-1]
                    blanks = blanks.replace(' ', '')
                    blanks = blanks[:len(reaction_to_word)] + '_' + blanks[len(reaction_to_word)+1:]
                    blanks = " ".join(blanks)
                    shuffled += char
                if blanks.replace(' ', '') == word:
                    not_finished = False
                if '_' not in blanks:
                    not_wrong_guess = self.check_word(word, blanks, not_wrong_guess)
            await board.edit(content=f"```Letters left: {' '.join(shuffled)}\n{blanks}```")
        if not not_wrong_guess:
            await board.edit(
                content=f'Wrong word foo lmao'
                        f'\n{user.mention} The word was "{word}"```\n{blanks}```')
        if not not_finished:
            await board.edit(content=f'{user.mention} has used the totality of their intellectual prowess and unscrambled the scrambled word'
                                     f'\nThe word was "{word}"```\n{blanks}```')
        return


def setup(bot):
    bot.add_cog(Scramble(bot))