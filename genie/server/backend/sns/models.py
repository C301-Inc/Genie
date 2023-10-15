from datetime import datetime
from typing import Type
from django.db import models
from accounts.models import SocialAccount
from backend.utils.models import BaseModel
from backend.utils import errors


class SNS(BaseModel):
    class Meta:
        verbose_name: str = "SNS"
        verbose_name_plural: str = "SNS"

    name: str = models.CharField(
        verbose_name="SNS name",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text="SNS name (ex. Discord, Twitter ...)",
    )


    def __str__(self):
        return f"{self.name}"


class SNSConnectionInfo(BaseModel):
    class Meta:
        verbose_name: str = "SNS-SocialAccount info"
        verbose_name_plural: str = "SNS-SocialAccount info"
        constraints: list[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["sns", "handle", "discriminator"],
                name="unique sns handle",
            ),
        ]

    account: "SocialAccount" = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, related_name="sns_info"
    )

    sns: "SNS" = models.ForeignKey(
        SNS, on_delete=models.PROTECT, related_name="users_info"
    )

    handle: str = models.CharField(
        verbose_name="SNS handle",
        max_length=50,
        blank=False,
        null=False,
        help_text="SNS handle",
    )

    discriminator: str = models.CharField(
        verbose_name="SNS discriminator",
        max_length=100,
        blank=False,
        null=False,
        help_text="SNS discriminator"
    )


    def __str__(self):
        return f"({self.account}) : {self.sns.name} {self.discriminator}"


class Server(BaseModel):
    class Meta:
        verbose_name: str = "Server"
        verbose_name_plural: str = "Server"
        constraints: list[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["sns", "name"],
                name="unique (sns, server)",
            ),
        ]

    sns: "SNS" = models.ForeignKey(
        SNS, on_delete=models.PROTECT, related_name="servers"
    )

    name: str = models.CharField(
        verbose_name="SNS server name",
        max_length=50,
        blank=False,
        null=False,
        help_text="SNS server name (ex. ATIV, NOIS, ...)",
    )


    def __str__(self):
        return f"{self.sns.name} - {self.name}"


class ServerHistory(BaseModel):
    class Meta:
        verbose_name: str = "Server History"
        verbose_name_plural: str = "Server History"

    server: "Server" = models.ForeignKey(
        Server, on_delete=models.PROTECT, related_name="histories"
    )

    date: datetime = models.DateField(
        verbose_name="Date stored history", auto_now_add=True
    )

    member_count: int = models.IntegerField(
        verbose_name="# of server members", null=True
    )

    daily_chat_count: int = models.IntegerField(
        verbose_name="# of chats in server", null=True
    )

    def __str__(self):
        return f"({str(self.server)}) - {self.date}"
