import discord
import requests
from discord.ext.commands import Bot

bot_token = 'put your bot token inside this'

intents = discord.Intents.default()
bot = Bot(command_prefix='!', intents=intents)
intents.message_content = True


def poll_check(channel_id, message_id):

    url = f'https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}'

    headers = {'Authorization': f'Bot {bot_token}'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()

        poll = json_data.get('poll', '1')

        return True if len(poll) > 1 else False


@bot.event
async def on_message(message):
    roles = [1229267366207160402, 1170613705910784020]  # you can also add more roles...

    get_poll = poll_check(channel_id=message.channel.id, message_id=message.id)
    has_role = False

    if get_poll:
        for role in roles:
            user_role = discord.utils.get(message.author.guild.roles, id=role)

            if user_role in message.author.roles:
                has_role = True
                break

        if not has_role:
            await message.delete()


@bot.event
async def on_ready():
    print('Successfully logged in as:', bot.user.name)
bot.run(bot_token)
