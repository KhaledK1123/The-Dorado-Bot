import discord
from selenium import webdriver
from datetime import datetime
from discord.ext import commands
import time



intentions = discord.Intents.all()
client = commands.Bot(command_prefix = '+', intents = intentions, help_command = None)
TOKEN = "MTExMjk2NTgzMTc3MzY2MzI4Mg.G8ehA2.JxcG_VYxUI6cjkWG2bxqn-Nx4yDOKwq5WQ2bgQ"

@client.event
async def on_ready():
    print("It's pronounced Dorito".format(client))

@client.event
async def on_message(message):
    admin_commands = ["Text Channels", "Admin", "Owner"]
    is_admin = False
    for role in message.author.roles:
        if role.name in admin_commands:
            is_admin = True
            break
    if message.author == client.user:
        return
    if message.content.startswith("+DoG logo"):
        await message.channel.send(file = discord.File("logo.png"))
    if message.content.startswith("+Chelsea"):
        await message.channel.send("https://docs.google.com/presentation/d/1f3cx11oEXtvMnQYaKgSTh0ATh2gwr470FynijboGd5s/edit#slide=id.p")
    if message.content.startswith("+W2M"):
        if  is_admin:
            await message.channel.send(await generate_when2meet(message.channel, str(message.channel.category)))
            # Set Server
            guild = discord.utils.get(client.guilds, id=1067283612698955796)
            # Channel name is same name as Role name
            role_name = message.channel.category.name
            team_role = discord.utils.get(guild.roles, name=role_name)
            try:
                await ping_role(message.channel, role = team_role)
            except:
                await message.channel.send("Channel and Role are not Equal")
        else:
            await message.channel.send("Admin Command.")
    if message.content.startswith("easy set"):
        await message.channel.send("""-
━━━━-╮
╰┃ ┣▇━▇
 ┃ ┃  ╰━▅╮
 ╰┳╯ ╰━━┳╯ANOTHER
  ╰╮ ┳━━╯ EASY set
 ▕▔▋ ╰╮╭━╮ FOR Dorado Gaming
╱▔╲▋╰━┻┻╮╲╱▔▔▔╲
▏  ▔▔▔▔▔▔▔  O O┃
╲╱▔╲▂▂▂▂╱▔╲▂▂▂╱
 ▏╳▕▇▇▕ ▏╳▕▇▇▕
 ╲▂╱╲▂╱ ╲▂╱╲▂╱
""")

@client.listen()
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("S"):
        await message.channel.send(await generate_when2meet(message.channel, str(message.channel.category)))
        # Set Server
        guild = discord.utils.get(client.guilds, id=1067283612698955796)
        # Channel name is same name as Role name
        role_name = message.channel.category.name
        team_role = discord.utils.get(guild.roles, name=role_name)
        try:
            await ping_role(message.channel, role = team_role)
        except:
            await message.channel.send("Channel and Role are not Equal")

@client.event
async def generate_when2meet(channel, team_name):
    try:
        driver = webdriver.Firefox()
        driver.get('https://www.when2meet.com/')
    except:
        await channel.send("Could not connect to Webpage")
    try:
        # Title
        input_element = driver.find_element(by = 'name', value = 'NewEventName').clear()
        input_element = driver.find_element(by = 'name', value = 'NewEventName')
        input_element.send_keys(team_name)
    except:
        await channel.send("Could not set title")
    try:
        # Time Zone
        input_element = driver.find_element(by = 'name', value = 'TimeZone')
        input_element.send_keys('America/Los_Angeles')
        # Time Slot #1
        input_element = driver.find_element(by = 'name', value = 'NoEarlierThan')
        input_element.send_keys('12')
        # Time Slot #2
        late_element = driver.find_element(by = 'name', value = 'NoLaterThan')
        late_element.send_keys('17')
    except:
        await channel.send("Could not set Time/TimeZone")
    # Date Selection
    current_date = datetime.now().strftime("%Y-%m-%d")
    i = 1
    k = 1
    selections = 0
    isSelected = False
    try:
        while(i < 8):
            date_element = driver.find_element(by = 'css selector', value = 'input#DateOf-1-' + str(i))
            date_value_element = date_element.get_attribute('value')
            if(date_value_element == current_date):
                isSelected = True
            if(isSelected == True):
                date_element = driver.find_element(by = 'css selector', value = 'div#Day-1-' + str(i))
                date_element.click()
                selections += 1
            i += 1
    except:
        await channel.send("Error setting the first row")
    selections = 8 - selections
    try:
        for k in range(1, selections + 1):
            date_element = driver.find_element(by = 'css selector', value = 'div#Day-2-' + str(k))
            date_element.click()
    except:
        await channel.send("Error setting the second row")
    # Click Create Event
    input_element = driver.find_element(by = 'css selector', value = 'input[value="Create Event"]')
    input_element.click()
    # Paste URL
    time.sleep(2)
    current_url = driver.current_url
    print(current_url)
    driver.close()
    return current_url

@client.command()
async def ping_role(ctx, role: discord.Role):
    await ctx.send(role.mention)

@client.command()
@commands.has_any_role("Text Channels", "Owner", "Admin")
async def admin_only(ctx):
    # Code for the admin-only command
    await ctx.send("This command can only be used by administrators.")

client.run(TOKEN)