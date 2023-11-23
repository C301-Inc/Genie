from django.contrib import admin
from blockchain.models import Network, Coin, Collection, NFT, CoinTransactionHistory, NFTTransactionHistory
from backend.utils.models import BaseModelAdmin


class NetworkAdmin(BaseModelAdmin):
    list_display: tuple[str, str] = (
        "id",
        "name",
    )

    list_display_links: tuple[str] = ("name",)
    search_fields: tuple[str] = ("name",)


class CoinAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str] = (
        "id",
        "network",
        "name",
        "ticker",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str, str] = ("network__name", "name", "ticker")


class CollectionAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str] = (
        "id",
        "network",
        "name",
        "mint_address",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str] = (
        "network__name",
        "name",
    )


class NFTAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str] = (
        "id",
        "network",
        "name",
        "mint_address",
        "collection",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str] = (
        "network__name",
        "name",
    )


class CoinTransactionHistoryAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str, str, str] = (
        "id",
        "from_inbox",
        "to_inbox",
        "tx_hash",
        "server",
        "coin",
        "amount",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str] = ("server__name",)


class NFTTransactionHistoryAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str, str] = (
        "id",
        "from_inbox",
        "to_inbox",
        "tx_hash",
        "server",
        "nft",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str] = ("server__name",)


admin.site.register(Network, NetworkAdmin)
admin.site.register(Coin, CoinAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(NFT, NFTAdmin)
admin.site.register(CoinTransactionHistory, CoinTransactionHistoryAdmin)
admin.site.register(NFTTransactionHistory, NFTTransactionHistoryAdmin)
