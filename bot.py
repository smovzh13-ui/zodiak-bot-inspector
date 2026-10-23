import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

VIOLATORS_CHANNEL_ID = 1562904069570297926 


@bot.event
async def on_ready():
  print(f"Бот {bot.user} успішно запущений і готовий до роботи!")
  try:
    
    GUILD_ID = discord.Object(id=1253224429400625172)

    bot.tree.copy_global_to(guild=GUILD_ID)
    synced = await bot.tree.sync(guild=GUILD_ID)
    print(f"Синхронізовано слеш-команд для сервера: {len(synced)}")
  except Exception as e:
    print(e)


@bot.tree.command(
    name="порушення", description="Зафіксувати порушення гравця та опублікувати в чат"
)
@app_commands.describe(
    гравець="Оберіть порушника зі списку",
    причина="Що саме порушив гравець",
    покарання="Яке покарання застосовано",
)
@app_commands.checks.has_permissions(administrator=True)
async def punish(
    interaction: discord.Interaction,
    гравець: discord.Member,
    причина: str,
    покарання: str,
):
  channel = bot.get_channel(VIOLATORS_CHANNEL_ID)
  if not channel:
    await interaction.response.send_message(
        "❌ Помилка: Канал для порушників не знайдено!", ephemeral=True
    )
    return

  embed = discord.Embed(
      title="🚨 Виявлено порушника!",
      color=discord.Color.from_rgb(
          231, 76, 60
      ), 
  )

  embed.add_field(
      name="👤 Порушник", value=f"{гравець.mention} (`{гравець.id}`)", inline=False
  )
  embed.add_field(name="⚠️ Причина", value=причина, inline=False)
  embed.add_field(name="⚖️ Покарання", value=покарання, inline=False)

  embed.set_footer(
      text=f"Зафіксував: {interaction.user.name}",
      icon_url=interaction.user.display_avatar.url,
  )
  embed.timestamp = discord.utils.utcnow()

  await channel.send(embed=embed)

  await interaction.response.send_message(
      f"✅ Порушення успішно опубліковано в {channel.mention}!", ephemeral=True
  )

@punish.error
async def punish_error(interaction: discord.Interaction, error):
  if isinstance(error, app_commands.errors.MissingPermissions):
    await interaction.response.send_message(
        "❌ У вас немає прав адміністратора для використання цієї команди.",
        ephemeral=True,
    )
  else:
    await interaction.response.send_message(
        f"❌ Сталася помилка: {error}", ephemeral=True
    )

import os
bot.run(os.getenv("DISCORD_TOKEN"))