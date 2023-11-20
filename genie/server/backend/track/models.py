from typing import Type

from django.db import models

from backend.utils.models import BaseModel


class Artist(BaseModel):
    class Meta:
        verbose_name: str = "Artist"
        verbose_name_plural: str = "Artists"

    name: str = models.CharField(
        verbose_name="name",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text="artist name",
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Album(BaseModel):
    class Meta:
        verbose_name: str = "Album"
        verbose_name_plural: str = "Albums"

    title: str = models.CharField(
        verbose_name="title",
        max_length=50,
        blank=False,
        null=False,
        help_text="album title",
    )

    artist: Type[Artist] = models.ForeignKey(
        verbose_name="artist",
        to=Artist,
        on_delete=models.PROTECT,
        related_name="albums",
        help_text="artist",
    )

    def __str__(self) -> str:
        return f"{self.title} in {self.artist.name}"


class Track(BaseModel):
    class Meta:
        verbose_name: str = "Track"
        verbose_name_plural: str = "Tracks"

    title: str = models.CharField(
        verbose_name="title",
        max_length=50,
        blank=False,
        null=False,
        help_text="track title",
    )

    artist: Type[Artist] = models.ForeignKey(
        verbose_name="artist",
        to=Artist,
        on_delete=models.PROTECT,
        related_name="tracks",
        help_text="artist",
    )

    album: Type[Album] = models.ForeignKey(
        verbose_name="album",
        to=Album,
        on_delete=models.PROTECT,
        related_name="tracks",
        help_text="album",
    )

    is_live: bool = models.BooleanField(
        verbose_name="is live",
        default=True,
        help_text="is live",
    )

    def __str__(self) -> str:
        return f"{self.title} in {self.album.title} by {self.artist.name}"
