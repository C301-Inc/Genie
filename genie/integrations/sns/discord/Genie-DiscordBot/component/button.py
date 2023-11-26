import os
from discord import ButtonStyle
from discord.ui import Button
from discord.interactions import Interaction
from discord._types import ClientT
from component.modal import SendTokenModal, SendNftModal, WithdrawTokenModal, WithdrawNftModal


class TokenButton(Button):
    def __init__(self, ticker, mint_address, to_address, server_id, max_amount, channel):
        super().__init__(label=ticker, style=ButtonStyle.primary)
        self.ticker = ticker
        self.mint_address = mint_address
        self.to_address = to_address
        self.server_id = server_id
        self.max_amount = max_amount
        self.channel = channel

    async def callback(self, interaction: Interaction[ClientT]):
        discord_name = interaction.user.name
        discord_id = interaction.user.id
        discord_discriminator = interaction.user.discriminator
        
        send_token_modal = SendTokenModal(
            title=self.ticker, 
            to_address=self.to_address, 
            mint_address=self.mint_address, 
            server_id=self.server_id, 
            max_amount=self.max_amount,
            channel=self.channel
        )
        await interaction.response.send_modal(send_token_modal)


class NftButton(Button):
    def __init__(self, name, mint_address, to_address, server_id, max_amount, channel):
        super().__init__(label=name, style=ButtonStyle.primary)
        self.name = name
        self.mint_address = mint_address
        self.to_address = to_address
        self.server_id = server_id
        self.max_amount = max_amount
        self.channel = channel

    async def callback(self, interaction: Interaction[ClientT]):
        discord_name = interaction.user.name
        discord_id = interaction.user.id
        discord_discriminator = interaction.user.discriminator
        
        send_nft_modal = SendNftModal(
            title=self.name, 
            to_address=self.to_address, 
            mint_address=self.mint_address, 
            server_id=self.server_id, 
            max_amount=self.max_amount,
            channel=self.channel
        )
        await interaction.response.send_modal(send_nft_modal)


class WithdrawTokenButton(Button):
    def __init__(self, ticker, mint_address, to_address, max_amount):
        super().__init__(label=ticker, style=ButtonStyle.primary)
        self.ticker = ticker
        self.mint_address = mint_address
        self.to_address = to_address
        self.max_amount = max_amount

    async def callback(self, interaction: Interaction[ClientT]):
        discord_name = interaction.user.name
        discord_id = interaction.user.id
        discord_discriminator = interaction.user.discriminator
        
        withdraw_token_modal = WithdrawTokenModal(
            title=self.ticker, 
            to_address=self.to_address, 
            mint_address=self.mint_address, 
            max_amount=self.max_amount,
        )
        await interaction.response.send_modal(withdraw_token_modal)


class WithdrawNftButton(Button):
    def __init__(self, name, mint_address, to_address, max_amount):
        super().__init__(label=name, style=ButtonStyle.primary)
        self.name = name
        self.mint_address = mint_address
        self.to_address = to_address
        self.max_amount = max_amount

    async def callback(self, interaction: Interaction[ClientT]):
        discord_name = interaction.user.name
        discord_id = interaction.user.id
        discord_discriminator = interaction.user.discriminator
        
        withdraw_nft_modal = WithdrawNftModal(
            title=self.name, 
            to_address=self.to_address, 
            mint_address=self.mint_address, 
            max_amount=self.max_amount,
        )
        await interaction.response.send_modal(withdraw_nft_modal)

