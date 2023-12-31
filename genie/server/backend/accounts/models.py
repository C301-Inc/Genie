from typing import List, Type

from django.db import models

from backend.utils import errors
from backend.utils.models import BaseModel


class SocialAccount(BaseModel):
    class Meta:
        verbose_name: str = "Genie user"
        verbose_name_plural: str = "Genie users"

    nickname: str = models.CharField(
        verbose_name="nickname",
        max_length=50,
        blank=False,
        null=False,
        help_text="nickname used in genie service",
    )

    pub_key: str = models.CharField(
        verbose_name="public key",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="public key",
    )

    secret_key: str = models.BinaryField(
        verbose_name="secret key",
        blank=False,
        null=False,
        help_text="secret key",
    )

    wallet_address: str = models.CharField(
        verbose_name="wallet address",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="wallet address",
    )

    lastfm_id: str = models.CharField(
        verbose_name="last.fm id",
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        help_text="last.fm id",
    )

    did_connect_lastfm: bool = models.BooleanField(
        verbose_name="did connect last.fm",
        default=False,
        help_text="did connect last.fm",
    )

    @classmethod
    def get_by_pub_key(cls: Type["SocialAccount"], pub_key: str) -> "SocialAccount":
        try:
            account: "SocialAccount" = cls.objects.get(pub_key=pub_key)
        except cls.DoesNotExist as e:
            raise errors.AccountNotFound from e

        return account
    
    def __str__(self):
        return f"{self.nickname} - {self.pub_key}"


class Inbox(BaseModel):
    class Meta:
        verbose_name: str = "Inbox"
        verbose_name_plural: str = "Inbox"
        constraints: List[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["pub_key", "network", "sns"],
                name="unique (pub_key, network, sns)",
            ),
        ]

    pub_key: str = models.CharField(
        verbose_name="public key",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="public key",
    )

    secret_key: str = models.BinaryField(
        verbose_name="secret key",
        blank=False,
        null=False,
        help_text="secret key",
    )

    wallet_address: str = models.CharField(
        verbose_name="wallet address",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="wallet address",
    )

    account: "SocialAccount" = models.ForeignKey(
        SocialAccount, on_delete=models.SET_NULL, related_name="inboxes", null=True
    )

    network: "Network" = models.ForeignKey(
        "blockchain.Network", on_delete=models.PROTECT, related_name="inboxes"
    )

    sns: "SNS" = models.ForeignKey(
        "sns.SNS", on_delete=models.PROTECT, related_name="inboxes"
    )

    @classmethod
    def get_inbox(cls: Type["Inbox"], sns, account, network) -> "Inbox":
        try:
            return cls.objects.get(sns=sns, account=account, network=network)
        except cls.DoesNotExist as e:
            raise errors.InboxNotFound from e

    @classmethod
    def check_inbox(cls: Type["Inbox"], sns, account, network) -> "Inbox":
        inbox = cls.objects.filter(sns=sns, account=account, network=network)

        return inbox.exists()

    @classmethod
    def get_by_address(cls: Type["Inbox"], wallet_address) -> "Inbox":
        try:
            return cls.objects.get(wallet_address=wallet_address)
        except cls.DoesNotExist as e:
            raise errors.InboxNotFound from e

    def __str__(self):
        return f"{self.account.nickname}({self.sns.name}) {self.pub_key}"
