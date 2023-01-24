import openai
import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello there!')

    if message.content.startswith('!gpt'):
        input = message.content[5:]
        response = openai.Completion.create(engine="text-davinci-003", prompt=input, max_tokens=1024, n=1, stop=None, temperature=0.5).choices[0].text
        await message.channel.send(response)
        prompt = response
        while True:
            await message.channel.send('Do you have any follow-up questions? (y/n)')
            followup = (await client.wait_for('message', check=lambda message: message.author == message.author)).content
            if followup.lower() == 'y':
                await message.channel.send('Please enter your follow-up question:')
                followup_input = (await client.wait_for('message', check=lambda message: message.author == message.author)).content
                prompt += "\n" + followup_input
                followup_response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.5).choices[0].text
                await message.channel.send(followup_response)
                prompt += "\n" + followup_response
            elif followup.lower() == 'n':
                await message.channel.send('happy to help :)')
                break
            else:
                await message.channel.send('Invalid input. Please enter "y" or "n".')


openai.api_key = ""
client.run("")