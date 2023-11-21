import graphene

from accounts.models import SocialAccount
from backend.utils import lastfm
from sns.models import SNS, SNSConnectionInfo
from track.graphql.schema import TrackCountType
from track.models import Track


class TrackQuery(graphene.ObjectType):
    get_track_counts = graphene.NonNull(
        graphene.List(graphene.NonNull(TrackCountType)),
        discriminator=graphene.String(required=True),
    )

    def resolve_get_track_counts(self, info: graphene.ResolveInfo, **kwargs):
        discriminator = kwargs.get("discriminator")

        sns = SNS.get_by_name("Discord")
        account = SNSConnectionInfo.get_account(sns=sns, discriminator=discriminator)

        if account.did_connect_lastfm is False:
            return []

        track_list = Track.objects.filter(is_live=True)
        track_count_list = []

        for track in track_list:
            streaming_count = lastfm.get_playcount(
                lastfm_id=account.lastfm_id, track_title=track.title
            )
            track_count_list.append(
                TrackCountType(track=track, streaming_count=streaming_count)
            )

        return track_count_list
