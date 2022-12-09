import json, discord, asyncio, functools, typing
from revChatGPT.revChatGPT import Chatbot


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        wrapped = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, wrapped)
    return wrapper

@to_thread
def get_answer(chatbot,query):
    response = chatbot.get_chat_response(query)
    return response

if __name__ == "__main__":
    with open("config.json", "r") as f: config = json.load(f)
    chatbot = Chatbot(config, conversation_id=None);chatbot.refresh_session()
    intents = discord.Intents.default();intents.message_content = True
    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client)

    @tree.command(name="chat",description="Chat with OpenAI")
    async def chat(inter : discord.Interaction, query : str):
        await inter.response.defer()
        response = await get_answer(chatbot,query)
        await inter.followup.send(response["message"].replace("OpenAI","Skynet"))

    @client.event
    async def on_ready():
        # await tree.sync()
        print(f'We have logged in as {client.user}')

    client.run(config["discord_bot_token"])
