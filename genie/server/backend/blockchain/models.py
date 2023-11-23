from typing import Type
from django.db import models
from accounts.models import SocialAccount, Inbox
from sns.models import Server
from backend.utils.models import BaseModel
from backend.utils import errors


class Network(BaseModel):
    class Meta:
        verbose_name: str = "Network"
        verbose_name_plural: str = "Network"

    name: str = models.CharField(
        verbose_name="Network name",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text="Network name (ex. Solana ...)",
    )

    @classmethod
    def get_by_name(cls: Type["Network"], name: str) -> "Network":
        try:
            network: "Network" = cls.objects.get(name=name)
        except cls.DoesNotExist as e:
            raise errors.NetworkNotFound from e

        return network

    def __str__(self):
        return f"{self.name}"


class Coin(BaseModel):
    class Meta:
        verbose_name: str = "Coin"
        verbose_name_plural: str = "Coin"
        constraints: list[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["network", "mint_address"],
                name="unique coin (network, mint_address)",
            ),
        ]

    network: "Network" = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name="coins"
    )

    name: str = models.CharField(
        verbose_name="Coin name",
        max_length=50,
        blank=True,
        null=False,
        help_text="Coin name (ex. Solana, USDCoin ...)",
    )

    ticker: str = models.CharField(
        verbose_name="Coin ticker",
        max_length=10,
        blank=True,
        null=True,
        help_text="Coin ticker (ex. SOL, USDC ...)",
    )

    mint_address: str = models.CharField(
        verbose_name="mint address",
        max_length=100,
        blank=False,
        null=False,
        help_text="mint address",
    )

    @classmethod
    def get_by_mint(cls: Type["Coin"], network, mint_address: str) -> "Coin":
        coin = cls.objects.filter(network=network, mint_address=mint_address)

        if coin.exists():
            if coin[0].ticker is not None:
                return coin[0].ticker
            return mint_address

        cls.objects.create(network=network, name="", mint_address=mint_address)
        return mint_address
    
    def __str__(self):
        return f"{self.network.name} - {self.name}"


class Collection(BaseModel):
    class Meta:
        verbose_name: str = "NFT Collection"
        verbose_name_plural: str = "NFT Collection"

    network: "Network" = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name="nft_collections"
    )

    name: str = models.CharField(
        verbose_name="NFT name",
        max_length=50,
        blank=False,
        null=False,
        help_text="NFT name (ex. NOIS, Sodead ...)",
    )

    mint_address: str = models.CharField(
        verbose_name="mint address",
        max_length=100,
        blank=True,
        null=True,
        help_text="mint address",
    )

    def __str__(self):
        return f"{self.network.name} - {self.name}"


class NFT(BaseModel):
    class Meta:
        verbose_name: str = "NFT"
        verbose_name_plural: str = "NFTs"
        constraints: list[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["network", "mint_address"],
                name="unique nft (network, mint_address)",
            ),
        ]

    network: "Network" = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name="NFT"
    )

    name: str = models.CharField(
        verbose_name="NFT name",
        max_length=50,
        blank=False,
        null=False,
        help_text="NFT name (ex. NOIS #100, ...)",
    )

    mint_address: str = models.CharField(
        verbose_name="mint address",
        max_length=100,
        blank=False,
        null=False,
        help_text="mint address",
    )

    collection: "Collection" = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name="NFT", blank=True, null=True
    )

    @classmethod
    def register_nft(cls: Type["NFT"], network, name, mint_address) -> "NFT":
        nft = cls.objects.filter(network=network, name=name, mint_address=mint_address)

        if nft.exists():
            return

        cls.objects.create(network=network, name=name, mint_address=mint_address)
        
        return 

    def __str__(self):
        return f"{self.network.name} - {self.name}"


class NFTTransactionHistory(BaseModel):
    class Meta:
        verbose_name: str = "NFT Transaction History"
        verbose_name_plural: str = "NFT Transaction History"

    from_inbox: "Inbox" = models.ForeignKey(
        Inbox,
        on_delete=models.CASCADE,
        related_name="from_nft_tx",
        null=True,
        blank=True,
    )

    to_inbox: "Inbox" = models.ForeignKey(
        Inbox,
        on_delete=models.CASCADE,
        related_name="to_nft_tx",
        null=True,
        blank=True,
    )

    tx_hash: str = models.CharField(
        verbose_name="tx_hash",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="tx hash",
    )

    server: "Server" = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="nft_tx_histories",
        null=False,
        blank=False,
    )

    nft: "NFT" = models.ForeignKey(
        NFT,
        on_delete=models.CASCADE,
        related_name="nft_tx_histories",
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.tx_hash}({self.nft})"


class CoinTransactionHistory(BaseModel):
    class Meta:
        verbose_name: str = "Coin Transaction History"
        verbose_name_plural: str = "Coin Transaction History"

    from_inbox: "Inbox" = models.ForeignKey(
        Inbox,
        on_delete=models.CASCADE,
        related_name="from_coin_tx",
        null=False,
        blank=False,
    )

    to_inbox: "Inbox" = models.ForeignKey(
        Inbox,
        on_delete=models.CASCADE,
        related_name="to_coin_tx",
        null=False,
        blank=False,
    )

    tx_hash: str = models.CharField(
        verbose_name="tx_hash",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="tx hash",
    )

    server: "Server" = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="coin_tx_histories",
        null=False,
        blank=False,
    )

    coin: "Coin" = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
        related_name="coin_tx_histories",
        null=False,
        blank=False,
    )


    amount: float = models.CharField(
        verbose_name="coin_amount",
        max_length=100,
        blank=False,
        null=False,
        default="0",
        help_text="sent coin amount",
    )

    def __str__(self):
        return f"{self.tx_hash}({self.coin})"
