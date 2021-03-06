import disnake
import requests
from disnake.ext import commands

from checks.check_license import check_license_lol


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="meme", description="Get a random meme")
    async def meme(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @meme.sub_command(
        name="reddit",
        description="Get a random meme from reddit",
    )
    async def meme_reddit(self, interaction: disnake.ApplicationCommandInteraction):
        if not check_license_lol(interaction.author):
            no_licesnse_embed = disnake.Embed(
                title="No license ⛔",
                description="You have not set a license for this server. Please use `/license activate <license>` to set a license.",
                color=disnake.Color.red()
            )
            no_licesnse_embed.set_footer(
                text="If you dont have a license, please contact the bot owner"
            )
            await interaction.response.send_message(
                embed=no_licesnse_embed,
                ephemeral=True
            )
        else:
            loading_embed = disnake.Embed(
                description="Getting memes from Reddit...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )

            URL = "https://some-random-api.ml/meme"
            response = requests.get(
                URL,
                params={},
                headers={}
            )
            if response.status_code == 200:
                data = response.json()

                meme_embed = disnake.Embed(
                    title=data["caption"],
                    description=f"Category: {data['category']}",
                    color=disnake.Color.green()
                )
                meme_embed.set_image(url=data["image"])

                await interaction.edit_original_message(
                    embed=meme_embed
                )
            else:
                await interaction.edit_original_message(f"Die API gibt den Status:{response.status_code}.")


def setup(bot):
    bot.add_cog(Meme(bot))
