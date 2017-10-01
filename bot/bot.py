import discord
import asyncio
import logging
from horsebase import HorseBase
from dynamic import Dynamic
import os

client = discord.Client()
hb = HorseBase()
dynamic = Dynamic()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@client.event
async def on_ready():
    logging.info('------')
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)
    logging.info('------')

@client.event
async def on_message(message):
    if message.author == client.user:
            return
    elif message.content.startswith('!totalhorses'):
        logging.info('Found !totalhorses')
        await client.send_message(message.server, 'Total amount of ' +
        str(hb.getTotalHorses(message.server.name)) + ' :horse: posted in this channel')
        logging.info('Finished !totalhorses')
    elif message.content.startswith('!myhorses'):
        logging.info('Found !myhorses')
        author = (message.author.nick if message.author.nick else message.author.name)
        myhorses = hb.getMyHorses(message.server.name, author)
        await client.send_message(message.server, author + ', you have posted ' +
        str(myhorses['month']) + ' :horse: this month and ' + str(myhorses['total']) +
        ' :horse: since the beginning of time.')
        logging.info('Finished !myhorses')
    elif message.content.startswith('!tophorses'):
        logging.info('Found !tophorses')
        tophorses = hb.getTopHorses(message.server.name, 3)
        if len(tophorses['month']) == 0 and len(tophorses['alltime']) == 0:
            return
        msg = ""
        if len(tophorses['month']) > 0:
            msg += "Top posters of this month are: \n"
            for m in tophorses['month']:
                msg += "• " + m[0] + " with " + str(m[1]) + " :horse: \n"
        if len(tophorses['alltime']) > 0:
            msg += "\n\nAll time top posters are: \n"
        for m in tophorses['alltime']:
                msg += "• " + m[0] + " with " + str(m[1]) + " :horse: \n"
        await client.send_message(message.server, msg)
        logging.info('Finished !tophorses')

    # special case for data collectiong
    if '🐴' in message.content:
        hb.addHorseToDB(message.server.name, message.timestamp, message.author.nick if message.author.nick else message.author.name)
    
    # adding dynamically loaded reactions
    reactions = dynamic.determineReactions(message.content.lower())
    if reactions:
        for reaction in reactions:
            logging.info('Found ' + reaction + ' in a message')
            await client.add_reaction(message, reaction)
            logging.info('Finished ' + reaction)
    else:
        logging.info('No reactions found in message')

    # STATIC RESPONSES
    response = dynamic.determineResponses(message.content.lower())
    if response:
        logging.info('Found response')
        await client.send_message(message.server, response)
        logging.info('Finished response')
    else:
        logging.info('nothing to respond to')

client.run(os.environ.get('DISCORD_TOKEN'))
