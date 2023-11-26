import os
import discord
from discord.ext import commands
from discord.ui import View
from component.button import WithdrawTokenButton, WithdrawNftButton
from utils.api_call import check_user_account, get_user_inbox_account, create_inbox_account, create_social_account, register_sns, get_user_tokens, get_user_nfts


class Withdraw(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def withdraw(self, ctx, *args) -> None:
        from_id = ctx.author.id
        from_name = ctx.author.name
        from_discriminator = ctx.author.discriminator
        from_avatar = ctx.author.avatar

        social_account_pub_key, is_inbox =check_user_account(from_id)
        
        if social_account_pub_key == "" or not is_inbox:
            await ctx.reply(
                f":genie:: Hey {from_name}! Please use !register command to create your genie wallet. This message will be deleted after 10 seconds.",
                delete_after=10.0,
            )

            return

        args = list(args)
        
        if len(args) == 2 and (args[0] == "token" or args[0] == "nft"):
            receiver_inbox_address = args[1]

            if args[0] == "token": 
                token_value_list, token_ticker_list, token_address_list = get_user_tokens(from_id, "Solana") 
                view = View()

                for i in range(len(token_value_list)):
                    token_button = WithdrawTokenButton(
                        ticker=token_ticker_list[i], 
                        mint_address=token_address_list[i], 
                        to_address=receiver_inbox_address, 
                        max_amount=token_value_list[i],
                    )
                    view.add_item(token_button)

                if len(token_value_list) == 0:
                    await ctx.reply(":genie:: You don't have token to withdraw.", delete_after=60)
                else:
                    await ctx.reply(":genie:: Choose token to withdraw.", view=view, delete_after=60)
            elif args[0] == "nft": 
                nft_name_list, nft_address_list = get_user_nfts(from_id, "Solana") 
                view = View()

                for i in range(len(nft_name_list)):
                    nft_button = WithdrawNftButton(
                        name=nft_name_list[i], 
                        mint_address=nft_address_list[i], 
                        to_address=receiver_inbox_address, 
                        max_amount=1,
                    )
                    view.add_item(nft_button)
                if len(nft_name_list) == 0:
                    await ctx.reply(":genie:: You don't have NFT to withdraw.", delete_after=60)
                else:
                    await ctx.reply(":genie:: Choose NFT to withdraw.", view=view, delete_after=60)

        else:
            await ctx.reply(
                "Please try again."
            )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Withdraw(bot))
