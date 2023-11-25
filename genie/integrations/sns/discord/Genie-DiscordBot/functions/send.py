import os
import discord
from discord.ext import commands
from discord.ui import View
from component.button import TokenButton, NftButton
from utils.api_call import check_user_account, get_user_inbox_account, create_inbox_account, create_social_account, register_sns, get_user_tokens, get_user_nfts


class Send(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def send(self, ctx, *args) -> None:
        from_id = ctx.author.id
        from_name = ctx.author.name
        from_discriminator = ctx.author.discriminator
        from_avatar = ctx.author.avatar

        if ctx.guild:
            server_id = ctx.guild.id
            server_name = ctx.guild.name
        else:
            server_id = ""
            server_name = ""

        social_account_pub_key, is_inbox =check_user_account(from_id)
        
        if social_account_pub_key == "" or not is_inbox:
            await ctx.reply(
                f":genie:: Hey {from_name}! Please use !register command to create your genie wallet. This message will be deleted after 10 seconds.",
                delete_after=10.0,
            )

            return

        args = list(args)
        
        if len(args) == 2 and (args[0] == "token" or args[0] == "nft"):
            to_user = discord.utils.get(ctx.message.mentions, id=int(args[1].strip('<@!>')))

            receiver_social_account_pub_key, is_receiver_inbox = check_user_account(to_user.id)
            
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                to_user: discord.PermissionOverwrite(read_messages=True)
            }

            channel = [channel for channel in ctx.guild.channels if channel.name == f"genie-alert-{to_user.id}"][0]
            if not channel:
                channel = await ctx.guild.create_text_channel(f"Genie Alert-{to_user.id}", overwrites=overwrites)
            
            if receiver_social_account_pub_key != "" and is_receiver_inbox:
                receiver_inbox_address = get_user_inbox_account(to_user.id)
            
            else:
                await ctx.reply(
                    f":genie:: Please wait.",
                    delete_after=10.0,
                )

                if receiver_social_account_pub_key != "":
                    register_sns("Solana", receiver_social_account_pub_key, to_user.id, to_user.name + '#' + to_user.discriminator)
                    receiver_inbox_address = create_inbox_account(to_user.id, "Solana")
           
                    await channel.send(
                        f":genie::  Hey {to_user.name}! Your genie wallet is registered.\nInbox Address: {receiver_inbox_address}.\n",
                    )

                else:
                    receiver_social_account_pub_key = create_social_account(to_user.name + '#' + to_user.discriminator)
                    register_sns("Solana", receiver_social_account_pub_key, to_user.id, to_user.name + '#' + to_user.discriminator)
                    receiver_inbox_address = create_inbox_account(to_user.id, "Solana")

                    await channel.send(
                        f":genie::  Hey {to_user.name}! Your genie wallet is registered.\nInbox Address: {receiver_inbox_address}.\n",
                    )

            if args[0] == "token": 
                token_value_list, token_ticker_list, token_address_list = get_user_tokens(from_id, "Solana") 
                view = View()

                for i in range(len(token_value_list)):
                    token_button = TokenButton(
                        ticker=token_ticker_list[i], 
                        mint_address=token_address_list[i], 
                        to_address=receiver_inbox_address, 
                        server_id=server_id, 
                        max_amount=token_value_list[i],
                        channel=channel
                    )
                    view.add_item(token_button)

                if len(token_value_list) == 0:
                    await ctx.reply(":genie:: You don't have token to send.", delete_after=60)
                else:
                    await ctx.reply(":genie:: Choose token to send.", view=view, delete_after=60)
            elif args[0] == "nft": 
                nft_name_list, nft_address_list = get_user_nfts(from_id, "Solana") 
                view = View()

                for i in range(len(nft_name_list)):
                    nft_button = NftButton(
                        name=nft_name_list[i], 
                        mint_address=nft_address_list[i], 
                        to_address=receiver_inbox_address, 
                        server_id=server_id, 
                        max_amount=1,
                        channel=channel
                    )
                    view.add_item(nft_button)
                if len(nft_name_list) == 0:
                    await ctx.reply(":genie:: You don't have NFT to send.", delete_after=60)
                else:
                    await ctx.reply(":genie:: Choose NFT to send.", view=view, delete_after=60)

        else:
            await ctx.reply(
                "Please try again."
            )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Send(bot))
