import discord
from discord.ext import commands
from discord import app_commands

BOT_TOKEN = ""
GUILD_ID = discord.Object(id=964685374716792862) # test server

intents = discord.Intents.default()
intents.message_content = True  # 🔥 THIS IS REQUIRED FOR COMMANDS
bot = commands.Bot(command_prefix="!", intents=intents)


# Create column headers (S M T W T F S)
day_labels = ["S", "M", "T", "W", "T", "F", "S"]

# Create 1hr intervals 
def generate_intervals():
    intervals = []
    for hour in range(24):
        intervals.append(f"{str(hour).zfill(2)}:00")
    return intervals

# Dummy schedule matrix: 58 rows × 7 columns (all ⬛️ for now)
def build_schedule_matrix():
    rows = []
    for _ in range(24):
        row = ["⬛️"] * 7
        rows.append(row)
    return rows

# @bot.command()
# @bot.tree.command(name="timetable", description="Display the weekly hourly timetable", guild=GUILD_ID)
async def timetable(interaction: discord.Interaction):
    intervals = generate_intervals()
    grid = build_schedule_matrix()

    # Build timetable text block
    timetable_text = ""

    # Header row
    timetable_text += "       " + "   ".join(day_labels) + "\n"

    # Each hour row
    for time_label, row in zip(intervals, grid):
        timetable_text += f"{time_label} " + "  ".join(row) + "\n"

    # Create embed with the timetable
    embed = discord.Embed(
        title="📅 Weekly Timetable",
        description=f"```\n{timetable_text}```",
        color=discord.Color.green()
    )

    # Optional footer or timestamp
    # embed.set_footer(text="Use commands to update your timetable.")
    # embed.set_thumbnail(url="https://i.imgur.com/Z6RQF7U.png")  # Optional icon

#     await ctx.send(embed=embed)
    await interaction.response.send_message(embed=embed)
    

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
    try:
        # Find and remove the command
        command = bot.tree.get_command("timetable")
        if command:
            bot.tree.remove_command("timetable", guild=GUILD_ID)
            print("Removed 'timetable' command.")
        
        # Sync changes
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# @bot.event
# async def on_message(message):
#     print(f"Message received: {message.content}")
#     await bot.process_commands(message)

# Run the bot
bot.run(BOT_TOKEN)
