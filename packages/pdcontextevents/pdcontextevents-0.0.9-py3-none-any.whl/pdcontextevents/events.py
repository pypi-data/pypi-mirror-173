class Events:
    def __init__(self, context, event, hashtag, symbols, user_mentions, urls, media, extended, user_urls):
        self.context = context
        self.event = event
        self.hashtag = hashtag
        self.symbols = symbols
        self.user_mentions = user_mentions
        self.urls = urls
        self.media = media
        self.extended = extended
        self.user_urls = user_urls

        self.event_entities_hashtagsi = []
        self.event_entities_hashtags_indices = []
        self.event_entities_hashtags_text = []
        self.event_entities_symbolsi = []
        self.event_entities_symbols_indices = []
        self.event_entities_symbols_text = []
        self.event_entities_user_mentions_screen_name = []
        self.event_entities_user_mentions_name = []
        self.event_entities_user_mentions_id = []
        self.event_entities_user_mentions_id_str = []
        self.event_entities_user_mentions_indices = []

        self.event_entities_urlsi = []
        self.event_entities_urlsi_display_url = []
        self.event_entities_urlsi_expanded_url = []
        self.event_entities_urlsi_indices = []
        self.event_entities_urlsi_url = []

        self.event_entities_mediai = []
        self.event_entities_media_display_url = []
        self.event_entities_media_expanded_url = []
        self.event_entities_media_id = []
        self.event_entities_media_id_str = []
        self.event_entities_media_indices = []
        self.event_entities_media_media_url = []
        self.event_entities_media_media_url_https = []
        self.event_entities_media_sizes = []
        self.event_entities_media_type = []
        self.event_entities_media_url = []

        self.event_extended_entities_media = []
        self.event_extended_entities_mediai = []
        self.event_extended_entities_mediai_display_url = []
        self.event_extended_entities_mediai_expanded_url = []
        self.event_extended_entities_mediai_id = []
        self.event_extended_entities_mediai_id_str = []
        self.event_extended_entities_mediai_indices = []
        self.event_extended_entities_mediai_media_url = []
        self.event_extended_entities_mediai_media_url_https = []
        self.event_extended_entities_mediai_sizes = []
        self.event_extended_entities_mediai_type = []
        self.event_extended_entities_mediai_url = []

        self.event_user_entities_url_urlsi = []
        self.event_user_entities_url_urlsi_display_url = []
        self.event_user_entities_url_urlsi_expanded_url = []
        self.event_user_entities_url_urlsi_indices = []
        self.event_user_entities_url_urlsi_url = []

    def single_items(self):

        pd_deployment_id = self.context["deployment_id"]
        pd_hops = self.context["hops"]
        pd_id = self.context["id"]
        pd_owner_id = self.context["owner_id"]
        pd_pipeline_id = self.context["pipeline_id"]
        pd_platform_version = self.context["platform_version"]
        pd_replay = self.context["replay"]
        pd_resume = self.context["resume"]
        pd_source_type = self.context["source_type"]
        pd_test = self.context["test"]
        pd_trace_id = self.context["trace_id"]
        pd_ts = self.context["ts"]
        pd_verified = self.context["verified"]
        pd_workflow_id = self.context["workflow_id"]
        pd_workflow_name = self.context["workflow_name"]
        event_contributors = self.event["contributors"]
        event_coordinates = self.event["coordinates"]
        event_created_at = self.event["created_at"]
        event_created_at_iso8601 = self.event["created_at_iso8601"]
        event_created_at_timestamp = self.event["created_at_timestamp"]
        event_display_text_range = self.event["display_text_range"]
        event_entities = self.event["entities"]
        event_favorite_count = self.event["favorite_count"]
        event_favorited = self.event["favorited"]
        event_full_text = self.event["full_text"]
        event_geo = self.event["geo"]
        event_id = self.event["id"]
        event_id_str = self.event["id_str"]
        event_in_reply_to_screen_name = self.event["in_reply_to_screen_name"]
        event_in_reply_to_status_id = self.event["in_reply_to_status_id"]
        event_in_reply_to_status_id_str = self.event["in_reply_to_status_id_str"]
        event_in_reply_to_user_id = self.event["in_reply_to_user_id"]
        event_in_reply_to_user_id_str = self.event["in_reply_to_user_id_str"]
        event_is_quote_status = self.event["is_quote_status"]
        event_lang = self.event["lang"]
        event_metadata = self.event["metadata"]
        event_metadata_iso_language_code = self.event["metadata"]["iso_language_code"]
        event_metadata_result_type = self.event["metadata"]["result_type"]
        event_place = self.event["place"]
        event_possibly_sensitive = self.event["possibly_sensitive"]
        event_retweet_count = self.event["retweet_count"]
        event_retweeted = self.event["retweeted"]
        event_source = self.event["source"]
        event_truncated = self.event["truncated"]
        event_url = self.event["url"]

        event_user = self.event["user"]
        event_user_contributors_enabled = self.event["user"]["contributors_enabled"]
        event_user_created_at = self.event["user"]["created_at"]
        event_user_default_profile = self.event["user"]["default_profile"]
        event_user_default_profile_image = self.event["user"]["default_profile_image"]
        event_user_description = self.event["user"]["description"]
        event_user_entities = self.event["user"]["entities"]
        event_user_entities_description = self.event["user"]["entities"]["description"]
        event_user_entities_description_urls = self.event["user"]["entities"]["description"]["urls"]
        event_user_favourites_count = self.event["user"]["favourites_count"]
        event_user_follow_request_sent = self.event["user"]["follow_request_sent"]
        event_user_followers_count = self.event["user"]["followers_count"]
        event_user_following = self.event["user"]["following"]
        event_user_friends_count = self.event["user"]["friends_count"]
        event_user_geo_enabled = self.event["user"]["geo_enabled"]
        event_user_has_extended_profile = self.event["user"]["has_extended_profile"]
        event_user_id = self.event["user"]["id"]
        event_user_id_str = self.event["user"]["id_str"]
        event_user_is_translation_enabled = self.event["user"]["is_translation_enabled"]
        event_user_is_translator = self.event["user"]["is_translator"]
        event_user_lang = self.event["user"]["lang"]
        event_user_listed_count = self.event["user"]["listed_count"]
        event_user_location = self.event["user"]["location"]
        event_user_name = self.event["user"]["name"]
        event_user_notifications = self.event["user"]["notifications"]
        event_user_profile_background_color = self.event["user"]["profile_background_color"]
        event_user_profile_background_image_url = self.event["user"]["profile_background_image_url"]
        event_user_profile_background_image_url_https = self.event["user"]["profile_background_image_url_https"]
        event_user_profile_background_tile = self.event["user"]["profile_background_tile"]
        try:
            event_user_profile_banner_url = self.event["user"]["profile_banner_url"]
        except KeyError:
            event_user_profile_banner_url = None
        event_user_profile_image_url = self.event["user"]["profile_image_url"]
        event_user_profile_image_url_https = self.event["user"]["profile_image_url_https"]
        event_user_profile_link_color = self.event["user"]["profile_link_color"]
        event_user_profile_sidebar_border_color = self.event["user"]["profile_sidebar_border_color"]
        event_user_profile_sidebar_fill_color = self.event["user"]["profile_sidebar_fill_color"]
        event_user_profile_text_color = self.event["user"]["profile_text_color"]
        event_user_profile_url = self.event["user"]["profile_url"]
        event_user_profile_use_background_image = self.event["user"]["profile_use_background_image"]
        event_user_protected = self.event["user"]["protected"]
        event_user_screen_name = self.event["user"]["screen_name"]
        event_user_statuses_count = self.event["user"]["statuses_count"]
        event_user_time_zone = self.event["user"]["time_zone"]
        event_user_translator_type = self.event["user"]["translator_type"]
        event_user_url = self.event["user"]["url"]
        event_user_utc_offset = self.event["user"]["utc_offset"]
        event_user_verified = self.event["user"]["verified"]
        event_user_withheld_in_countries = self.event["user"]["withheld_in_countries"]
        all_single_items = [pd_deployment_id, pd_hops, pd_id, pd_owner_id, pd_pipeline_id, pd_platform_version, pd_replay, pd_resume, pd_source_type, pd_test, pd_trace_id, pd_ts, pd_verified, pd_workflow_id, pd_workflow_name, self.event, event_contributors, event_coordinates, event_created_at, event_created_at_iso8601, event_created_at_timestamp, event_display_text_range, event_entities, event_favorite_count, event_favorited, event_full_text, event_geo, event_id, event_id_str, event_in_reply_to_screen_name, event_in_reply_to_status_id, event_in_reply_to_status_id_str, event_in_reply_to_user_id, event_in_reply_to_user_id_str, event_is_quote_status, event_lang, event_metadata, event_metadata_iso_language_code, event_metadata_result_type, event_place, event_possibly_sensitive, event_retweet_count, event_retweeted, event_source, event_truncated, event_url, event_user, event_user_contributors_enabled, event_user_created_at, event_user_default_profile, event_user_default_profile_image, event_user_description, event_user_entities, event_user_entities_description, event_user_entities_description_urls, event_user_favourites_count, event_user_follow_request_sent, event_user_followers_count, event_user_following, event_user_friends_count, event_user_geo_enabled, event_user_has_extended_profile, event_user_id, event_user_id_str, event_user_is_translation_enabled, event_user_is_translator, event_user_lang, event_user_listed_count, event_user_location, event_user_name, event_user_notifications, event_user_profile_background_color, event_user_profile_background_image_url, event_user_profile_background_image_url_https, event_user_profile_background_tile, event_user_profile_banner_url, event_user_profile_image_url, event_user_profile_image_url_https, event_user_profile_link_color, event_user_profile_sidebar_border_color, event_user_profile_sidebar_fill_color, event_user_profile_text_color, event_user_profile_url, event_user_profile_use_background_image, event_user_protected, event_user_screen_name, event_user_statuses_count, event_user_time_zone, event_user_translator_type, event_user_url, event_user_utc_offset, event_user_verified, event_user_withheld_in_countries]

        return all_single_items

        # Group B

    def hashtag(self):
        try:
            for i in range(len(self.hashtag)):
                self.event_entities_hashtagsi.append(self.hashtag[i])
                self.event_entities_hashtags_indices.append(self.hashtag[i]["indices"])
                self.event_entities_hashtags_text.append(self.hashtag[i]["text"])
            all_hashtag = [self.hashtag, self.event_entities_hashtagsi, self.event_entities_hashtags_indices, self.event_entities_hashtags_text]
        except KeyError or IndexError:
            print("No Hashtags available")
            all_hashtag = [None, None, None, None]
        return all_hashtag

    # Group C
    def symbols(self):
        try:
            for i in range(len(self.symbols)):
                self.event_entities_symbolsi.append(self.symbols[i])
                self.event_entities_symbols_indices.append(self.symbols[i]["indices"])
                self.event_entities_symbols_text.append(self.symbols[i]["text"])
            all_symbols = [self.symbols, self.event_entities_symbolsi, self.event_entities_symbols_indices, self.event_entities_symbols_text]
        except KeyError or IndexError:
            print("No Symbols available")
            all_symbols = [None, None, None, None]
        return all_symbols

    # Group D
    def user_mentions(self):
        try:
            for i in range(len(self.user_mentions)):
                self.event_entities_user_mentions_screen_name.append(self.user_mentions[i]["screen_name"])
                self.event_entities_user_mentions_name.append(self.user_mentions[i]["name"])
                self.event_entities_user_mentions_id.append(self.user_mentions[i]["id"])
                self.event_entities_user_mentions_id_str.append(self.user_mentions[i]["id_str"])
                self.event_entities_user_mentions_indices.append(self.user_mentions[i]["indices"])
            all_mentions = [self.user_mentions, self.event_entities_user_mentions_screen_name, self.event_entities_user_mentions_name, self.event_entities_user_mentions_id, self.event_entities_user_mentions_id_str, self.event_entities_user_mentions_indices]
        except KeyError or IndexError:
            print("No User Mentions available")
            all_mentions = [None, None, None, None, None, None]
        return all_mentions

    # Group E
    def entities_urls(self):
        try:
            for i in range(len(self.urls)):
                self.event_entities_urlsi.append(self.urls[i])
                self.event_entities_urlsi_display_url.append(self.urls[i]["display_url"])
                self.event_entities_urlsi_expanded_url.append(self.urls[i]["expanded_url"])
                self.event_entities_urlsi_indices.append(self.urls[i]["indices"])
                self.event_entities_urlsi_url.append(self.urls[i]["url"])
            all_urls = [self.urls, self.event_entities_urlsi, self.event_entities_urlsi_display_url, self.event_entities_urlsi_expanded_url, self.event_entities_urlsi_indices, self.event_entities_urlsi_url]
        except KeyError or IndexError:
            print("No Entities_Urls available")
            all_urls = [None, None, None, None, None, None]
        return all_urls

    # Group F
    def entities_media(self):
        try:
            for i in range(len(self.media)):
                self.event_entities_mediai.append(self.media[i])
                self.event_entities_media_display_url.append(self.media[i]["display_url"])
                self.event_entities_media_expanded_url.append(self.media[i]["expanded_url"])
                self.event_entities_media_id.append(self.media[i]["id"])
                self.event_entities_media_id_str.append(self.media[i]["id_str"])
                self.event_entities_media_indices.append(self.media[i]["indices"])
                self.event_entities_media_media_url.append(self.media[i]["media_url"])
                self.event_entities_media_media_url_https.append(self.media[i]["media_url_https"])
                self.event_entities_media_sizes.append(self.media[i]["sizes"])
                self.event_entities_media_type.append(self.media[i]["type"])
                self.event_entities_media_url.append(self.media[i]["url"])
            all_media = [self.media, self.event_entities_mediai, self.event_entities_media_display_url, self.event_entities_media_expanded_url, self.event_entities_media_id, self.event_entities_media_id_str, self.event_entities_media_indices, self.event_entities_media_media_url, self.event_entities_media_media_url_https, self.event_entities_media_sizes, self.event_entities_media_type, self.event_entities_media_url]
        except KeyError or IndexError:
            print("No Entities_Media available")
            all_media = [None, None, None, None, None, None, None, None, None, None, None, None]
        return all_media

    # Group G
    def extended_media(self):
        try:
            for i in range(len(self.extended)):
                self.event_extended_entities_media.append(self.extended["media"])
                self.event_extended_entities_mediai.append(self.extended["media"][i])
                self.event_extended_entities_mediai_display_url.append(self.extended["media"][i]["display_url"])
                self.event_extended_entities_mediai_expanded_url.append(self.extended["media"][i]["expanded_url"])
                self.event_extended_entities_mediai_id.append(self.extended["media"][i]["id"])
                self.event_extended_entities_mediai_id_str.append(self.extended["media"][i]["id_str"])
                self.event_extended_entities_mediai_indices.append(self.extended["media"][i]["indices"])
                self.event_extended_entities_mediai_media_url.append(self.extended["media"][i]["media_url"])
                self.event_extended_entities_mediai_media_url_https.append(self.extended["media"][i]["media_url_https"])
                self.event_extended_entities_mediai_sizes.append(self.extended["media"][i]["sizes"])
                self.event_extended_entities_mediai_type.append(self.extended["media"][i]["type"])
                self.event_extended_entities_mediai_url.append(self.extended["media"][i]["url"])
            all_extended = [self.extended, self.event_extended_entities_media, self.event_extended_entities_mediai, self.event_extended_entities_mediai_display_url, self.event_extended_entities_mediai_expanded_url, self.event_extended_entities_mediai_id, self.event_extended_entities_mediai_id_str, self.event_extended_entities_mediai_indices, self.event_extended_entities_mediai_media_url, self.event_extended_entities_mediai_media_url_https, self.event_extended_entities_mediai_sizes, self.event_extended_entities_mediai_type, self.event_extended_entities_mediai_url]
        except KeyError or IndexError:
            print("No Extended_Media available")
            all_extended = [None, None, None, None, None, None, None, None, None, None, None, None, None]
        return all_extended

    # Group H
    def user_urls(self):
        try:
            for i in range(len(self.user_urls)):
                self.event_user_entities_url_urlsi_display_url.append(self.user_urls[i]["display_url"])
                self.event_user_entities_url_urlsi_expanded_url.append(self.user_urls[i]["expanded_url"])
                self.event_user_entities_url_urlsi_indices.append(self.user_urls[i]["indices"])
                self.event_user_entities_url_urlsi_url.append(self.user_urls[i]["url"])
            all_user_urls = [self.user_urls, self.event_user_entities_url_urlsi, self.event_user_entities_url_urlsi_display_url, self.event_user_entities_url_urlsi_expanded_url, self.event_user_entities_url_urlsi_indices, self.event_user_entities_url_urlsi_url]
        except KeyError or IndexError:
            print("No User_Urls available")
            all_user_urls = [None, None, None, None, None]
        return all_user_urls

