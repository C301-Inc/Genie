from django.contrib import admin
from accounts.models import SocialAccount, Inbox
from backend.utils.models import BaseModelAdmin


class SocialAccountAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str] = (
        "id",
        "nickname",
        "pub_key",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str] = ("nickname",)


class InboxAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str] = (
        "id",
        "account",
        "network",
        "sns",
        "pub_key",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str, str] = (
        "account__nickname",
        "sns__name",
        "network__name",
    )


admin.site.register(SocialAccount, SocialAccountAdmin)
admin.site.register(Inbox, InboxAdmin)

admin.site.site_header = "Genie Admin Site"
admin.site.site_title = "Genie Admin Site"
admin.site.index_title = "Genie Admin Site"
