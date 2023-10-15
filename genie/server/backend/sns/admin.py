from django.contrib import admin
from django.utils.safestring import mark_safe
from sns.models import SNS, SNSConnectionInfo, Server, ServerHistory
from backend.utils.models import BaseModelAdmin


class SNSAdmin(BaseModelAdmin):
    list_display: tuple[str, str] = (
        "id",
        "name",
    )

    list_display_links: tuple[str] = ("name",)
    search_fields: tuple[str] = ("name",)


class SNSConnectionInfoAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str] = (
        "id",
        "account",
        "sns",
        "handle",
        "discriminator",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str, str] = (
        "account__nickname",
        "sns__name",
        "handle",
    )


class ServerAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str] = (
        "id",
        "sns",
        "name",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str] = (
        "sns__name",
        "name",
    )


class ServerHistoryAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str] = (
        "id",
        "server",
        "date",
        "member_count",
        "daily_chat_count",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str] = (
        "server__name",
        "server__sns__name",
    )


admin.site.register(SNS, SNSAdmin)
admin.site.register(SNSConnectionInfo, SNSConnectionInfoAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(ServerHistory, ServerHistoryAdmin)
