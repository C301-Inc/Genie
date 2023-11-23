from django.contrib import admin

from backend.utils.models import BaseModelAdmin
from track.models import Album, Artist, Track


@admin.register(Artist)
class ArtistAdmin(BaseModelAdmin):
    list_display: tuple[str, str] = (
        "id",
        "name",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str] = ("name",)


@admin.register(Album)
class AlbumAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str] = (
        "id",
        "title",
        "artist_name",
    )

    @admin.display(description="artist name")
    def artist_name(self, obj):
        return obj.artist.name

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str] = ("title", "artist__name")


@admin.register(Track)
class TrackAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str] = (
        "id",
        "title",
        "artist_name",
        "album_title",
    )

    @admin.display(description="artist name")
    def artist_name(self, obj):
        return obj.artist.name

    @admin.display(description="album title")
    def album_title(self, obj):
        return obj.album.title

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str] = ("title", "artist__name", "album__title")
