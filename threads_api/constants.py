"""
Constants & Endpoint Definitions for Threads Web Automation
Extracted from Threads web client JS bundles and traffic analysis.
"""

# Base URLs
BASE_URL = "https://www.threads.com"
GRAPHQL_URL = "https://www.threads.com/api/graphql"
GRAPHQL_QUERY_URL = "https://www.threads.com/graphql/query"
RUPLOAD_PHOTO_URL = "https://www.threads.com/rupload_igphoto"
RUPLOAD_VIDEO_URL = "https://www.threads.com/rupload_igvideo"

# App & Environment Constants
BARCELONA_APP_ID = "238260118697367"
ASBD_ID = "359341"
DEFAULT_LSD = "XDFILY4U8qvauprMBQ7JoF"
DEFAULT_JAZOEST = "22766"
BLOKS_VERSION_ID = "eb91d73a91a524be8e4f4d5e3793a8eada30ccc66f6990edc31e5ddf8c1c3a2c"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/154.0.0.0 Safari/537.36"
)

# GraphQL Document IDs
DOC_ID_LIKE = "24753372994365040"
DOC_ID_UNLIKE = "24987148517646229"
DOC_ID_CREATE_REPOST = "31967938062853815"
DOC_ID_DELETE_REPOST = "24726616043664185"
DOC_ID_FEED_DIRECT = "29230682679857431"
DOC_ID_FEED_PAGINATION = "28024722197206043"
DOC_ID_POST_DETAIL = "28881847464743900"
DOC_ID_POST_REPLIES = "40279895674942729"
DOC_ID_USER_PROFILE = "28550444331289839"
DOC_ID_ARCHIVE_POST = "28179348525053908"
DOC_ID_DELETE_ARCHIVED_POST = "27887507347598022"

# REST Endpoints
ENDPOINT_CONFIGURE_TEXT = "/api/v1/media/configure_text_only_post/"
ENDPOINT_CONFIGURE_FEED_IMAGE = "/api/v1/media/configure_text_post_app_feed/"
ENDPOINT_CONFIGURE_SIDECAR = "/api/v1/media/configure_text_post_app_sidecar/"

# Common Relay Feature Flags for Barcelona (Threads Web)
DEFAULT_RELAY_FLAGS = {
    "__relay_internal__pv__BarcelonaHasCommunityPermalinkPivotsrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasPodcastV2Consumptionrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasPodcastV2Productionrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasInsightsPermalinkUFIrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasBestOfThreadsrelayprovider": True,
    "__relay_internal__pv__BarcelonaShouldShowFediverseM1Featuresrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasDearAlgoConsumptionrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasMetaAiContentAttachmentsrelayprovider": False,
    "__relay_internal__pv__BarcelonaShouldFetchPostAuthorFullNamerelayprovider": False,
    "__relay_internal__pv__BarcelonaIsLoggedInrelayprovider": True,
    "__relay_internal__pv__BarcelonaMessagesHasLiveChatMessagingrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasEventBadgerelayprovider": False,
    "__relay_internal__pv__BarcelonaMessagingHasMetaAIBotrelayprovider": False,
    "__relay_internal__pv__BarcelonaGenAIRepliesEnabledrelayprovider": True,
    "__relay_internal__pv__BarcelonaIsSearchDiscoveryEnabledrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasCommunitiesrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasGameScoreSharerelayprovider": True,
    "__relay_internal__pv__BarcelonaHasPublicViewCountCardrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasCommunityEmojiUpdateCardrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasCommunityEntityCardrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasScorecardCommunityrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasSportTeamAllegianceCardrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasNewspaperLinkStylerelayprovider": False,
    "__relay_internal__pv__BarcelonaHasMessagingrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasPodcastTranscriptConsumptionrelayprovider": True,
    "__relay_internal__pv__BarcelonaOptionalCookiesEnabledrelayprovider": True,
    "__relay_internal__pv__BarcelonaShouldFulfillLightboxQueryrelayprovider": True,
    "__relay_internal__pv__BarcelonaCanSeeSponsoredContentrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasWebFaviconsrelayprovider": False,
    "__relay_internal__pv__BarcelonaIsCrawlerrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasDearAlgoWebProductionrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasCommunityTopContributorsrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasUnseenRepliesrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasCustomLikesConsumptionrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasViewerRepliedrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasPrivateRepliesDeprecationrelayprovider": True,
    "__relay_internal__pv__BarcelonaHasGhostPostEmojiActivationrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasGhostPostProductionrelayprovider": False,
    "__relay_internal__pv__BarcelonaHasNewsletterLinkPreviewrelayprovider": False,
    "__relay_internal__pv__BarcelonaShouldShowFediverseM075Featuresrelayprovider": True,
    "__relay_internal__pv__BarcelonaIsInternalUserrelayprovider": False
}
