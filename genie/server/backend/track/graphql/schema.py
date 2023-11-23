import graphene
from graphene_django.types import DjangoObjectType

from track.models import Album, Artist, Track


class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist
        fields = ("name",)


class AlbumType(DjangoObjectType):
    class Meta:
        model = Album
        fields = ("title", "artist")


class TrackType(DjangoObjectType):
    class Meta:
        model = Track
        fields = ("title", "artist", "album")


class TrackCountType(DjangoObjectType):
    track = graphene.NonNull(TrackType)
    streaming_count = graphene.NonNull(graphene.Int)
