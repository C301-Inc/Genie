import asyncio
import discord
from discord.ui import Modal, TextInput
from discord.interactions import Interaction
from discord._types import ClientT
from utils.api_call import send_token, send_nft, withdraw_token, withdraw_nft


class SendTokenModal(Modal):
    def __init__(self, to_address, mint_address, server_id, max_amount, channel, title="Send Token"):
        super().__init__(title=title)
        self.title = title
        self.amount_input = TextInput(
            style=discord.TextStyle.short,
            label=f"Amount: {max_amount}"[:44],
            required=True,
            placeholder="Type token amount to send.",
        )
        self.add_item(self.amount_input)
        self.mint_address = mint_address
        self.to_address = to_address
        self.server_id = server_id
        self.channel = channel

    async def on_submit(self, interaction: Interaction[ClientT]):
        await interaction.response.defer(
            ephemeral=True
        )

        asyncio.create_task(self.handle_send_token(interaction))

    async def handle_send_token(self, interaction):
        discord_id = interaction.user.id
        
        await interaction.followup.send(
            content=":genie:: Process...",
            ephemeral=True
        )

        tx_hash = send_token(
            discord_id=str(discord_id), 
            network_name="Solana", 
            mint_address=self.mint_address, 
            amount=float(self.amount_input.value), 
            to_address=self.to_address, 
            server_id=str(self.server_id)
        )

        if tx_hash is None:
            await interaction.followup.send(
                content=f":genie:: Send fail! Please try again.\n",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                content=f":genie:: Send success! Tx_hash is {tx_hash}.\n",
                ephemeral=True
            )

        await self.channel.send(
            f"<@{discord_id}> just send you {self.amount_input.value} {self.title}!\n"
        )


class SendNftModal(Modal):
    def __init__(self, to_address, mint_address, server_id, max_amount, channel, title="Send NFT"):
        super().__init__(title=title)
        self.title = title
        self.amount_input = TextInput(
            style=discord.TextStyle.short,
            label=f"Amount: {max_amount}"[:44],
            required=True,
            placeholder="Type NFT amount to send.",
        )
        self.add_item(self.amount_input)
        self.mint_address = mint_address
        self.to_address = to_address
        self.server_id = server_id
        self.channel = channel

    async def on_submit(self, interaction: Interaction[ClientT]):
        await interaction.response.defer(
            ephemeral=True
        )

        asyncio.create_task(self.handle_send_nft(interaction))

    async def handle_send_nft(self, interaction):
        discord_id = interaction.user.id

        await interaction.followup.send(
            content=":genie:: Process...",
            ephemeral=True
        )


        tx_hash = send_nft(
            discord_id=str(discord_id), 
            network_name="Solana", 
            mint_address=self.mint_address, 
            to_address=self.to_address, 
            server_id=str(self.server_id)
        )

        if tx_hash is None:
            await interaction.followup.send(
                content=f":genie:: Send fail! Please try again.\n",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                content=f":genie:: Send success! Tx_hash is {tx_hash}.\n",
                ephemeral=True
            )

        await self.channel.send(
            f"<@{discord_id}> just send you 1 {self.title}!\n"
        )


class WithdrawTokenModal(Modal):
    def __init__(self, to_address, mint_address, max_amount, title="Withdraw Token"):
        super().__init__(title=title)
        self.title = title
        self.amount_input = TextInput(
            style=discord.TextStyle.short,
            label=f"Amount: {max_amount}"[:44],
            required=True,
            placeholder="Type token amount to withdraw.",
        )
        self.add_item(self.amount_input)
        self.mint_address = mint_address
        self.to_address = to_address

    async def on_submit(self, interaction: Interaction[ClientT]):
        await interaction.response.defer(
            ephemeral=True
        )

        asyncio.create_task(self.handle_withdraw_token(interaction))

    async def handle_withdraw_token(self, interaction):
        discord_id = interaction.user.id
        
        await interaction.followup.send(
            content=":genie:: Process...",
            ephemeral=True
        )

        tx_hash = withdraw_token(
            discord_id=str(discord_id), 
            network_name="Solana", 
            mint_address=self.mint_address, 
            amount=float(self.amount_input.value), 
            to_address=self.to_address, 
        )

        if tx_hash is None:
            await interaction.followup.send(
                content=f":genie:: Withdraw fail! Please try again.\n",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                content=f":genie:: Withdraw success! Tx_hash is {tx_hash}.\n",
                ephemeral=True
            )


class WithdrawNftModal(Modal):
    def __init__(self, to_address, mint_address, max_amount, title="Send NFT"):
        super().__init__(title=title)
        self.title = title
        self.amount_input = TextInput(
            style=discord.TextStyle.short,
            label=f"Amount: {max_amount}"[:44],
            required=True,
            placeholder="Type NFT amount to send.",
        )
        self.add_item(self.amount_input)
        self.mint_address = mint_address
        self.to_address = to_address

    async def on_submit(self, interaction: Interaction[ClientT]):
        await interaction.response.defer(
            ephemeral=True
        )

        asyncio.create_task(self.handle_withdraw_nft(interaction))

    async def handle_withdraw_nft(self, interaction):
        discord_id = interaction.user.id

        await interaction.followup.send(
            content=":genie:: Process...",
            ephemeral=True
        )

        tx_hash = withdraw_nft(
            discord_id=str(discord_id), 
            network_name="Solana", 
            mint_address=self.mint_address, 
            to_address=self.to_address, 
        )

        if tx_hash is None:
            await interaction.followup.send(
                content=f":genie:: Withdraw fail! Please try again.\n",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                content=f":genie:: Withdraw success! Tx_hash is {tx_hash}.\n",
                ephemeral=True
            )

