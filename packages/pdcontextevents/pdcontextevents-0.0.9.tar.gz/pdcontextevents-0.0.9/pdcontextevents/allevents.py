class AllEvents:

    def __init__(self, has_shr, has_shr_count, has_tbl, has_tbl_count):
        self.has_shr = has_shr
        self.has_shr_count = has_shr_count
        self.has_tbl = has_tbl
        self.has_tbl_count = has_tbl_count
        self.event_entities_hashtagsi = []
        self.event_entities_hashtags_indices = []
        self.event_entities_hashtags_text = []
        self.event_entities_symbolsi = []
        self.event_entities_symbols_indices = []
        self.event_entities_symbols_text = []
        self.event_entities_user_mentionsi = []
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

    @staticmethod
    def single_items(context, event, event_user_profile_banner_url):
        pd_deployment_id = context["deployment_id"]
        pd_hops = context["hops"]
        pd_id = context["id"]
        pd_owner_id = context["owner_id"]
        pd_pipeline_id = context["pipeline_id"]
        pd_platform_version = context["platform_version"]
        pd_replay = context["replay"]
        pd_resume = context["resume"]
        pd_source_type = context["source_type"]
        pd_test = context["test"]
        pd_trace_id = context["trace_id"]
        pd_ts = context["ts"]
        pd_verified = context["verified"]
        pd_workflow_id = context["workflow_id"]
        pd_workflow_name = context["workflow_name"]
        event = event
        event_contributors = event["contributors"]
        event_coordinates = event["coordinates"]
        event_created_at = event["created_at"]
        event_created_at_iso8601 = event["created_at_iso8601"]
        event_created_at_timestamp = event["created_at_timestamp"]
        event_display_text_range = event["display_text_range"]
        event_entities = event["entities"]
        event_favorite_count = event["favorite_count"]
        event_favorited = event["favorited"]
        event_full_text = event["full_text"]
        event_geo = event["geo"]
        event_id = event["id"]
        event_id_str = event["id_str"]
        event_in_reply_to_screen_name = event["in_reply_to_screen_name"]
        event_in_reply_to_status_id = event["in_reply_to_status_id"]
        event_in_reply_to_status_id_str = event["in_reply_to_status_id_str"]
        event_in_reply_to_user_id = event["in_reply_to_user_id"]
        event_in_reply_to_user_id_str = event["in_reply_to_user_id_str"]
        event_is_quote_status = event["is_quote_status"]
        event_lang = event["lang"]
        event_metadata = event["metadata"]
        event_metadata_iso_language_code = event["metadata"]["iso_language_code"]
        event_metadata_result_type = event["metadata"]["result_type"]
        event_place = event["place"]
        event_possibly_sensitive = event["possibly_sensitive"]
        event_retweet_count = event["retweet_count"]
        event_retweeted = event["retweeted"]
        event_source = event["source"]
        event_truncated = event["truncated"]
        event_url = event["url"]
        event_user = event["user"]
        event_user_contributors_enabled = event["user"]["contributors_enabled"]
        event_user_created_at = event["user"]["created_at"]
        event_user_default_profile = event["user"]["default_profile"]
        event_user_default_profile_image = event["user"]["default_profile_image"]
        event_user_description = event["user"]["description"]
        event_user_entities = event["user"]["entities"]
        event_user_entities_description = event["user"]["entities"]["description"]
        event_user_entities_description_urls = event["user"]["entities"]["description"]["urls"]
        event_user_favourites_count = event["user"]["favourites_count"]
        event_user_follow_request_sent = event["user"]["follow_request_sent"]
        event_user_followers_count = event["user"]["followers_count"]
        event_user_following = event["user"]["following"]
        event_user_friends_count = event["user"]["friends_count"]
        event_user_geo_enabled = event["user"]["geo_enabled"]
        event_user_has_extended_profile = event["user"]["has_extended_profile"]
        event_user_id = event["user"]["id"]
        event_user_id_str = event["user"]["id_str"]
        event_user_is_translation_enabled = event["user"]["is_translation_enabled"]
        event_user_is_translator = event["user"]["is_translator"]
        event_user_lang = event["user"]["lang"]
        event_user_listed_count = event["user"]["listed_count"]
        event_user_location = event["user"]["location"]
        event_user_name = event["user"]["name"]
        event_user_notifications = event["user"]["notifications"]
        event_user_profile_background_color = event["user"]["profile_background_color"]
        event_user_profile_background_image_url = event["user"]["profile_background_image_url"]
        event_user_profile_background_image_url_https = event["user"]["profile_background_image_url_https"]
        event_user_profile_background_tile = event["user"]["profile_background_tile"]
        event_user_profile_banner_url = event_user_profile_banner_url
        event_user_profile_image_url = event["user"]["profile_image_url"]
        event_user_profile_image_url_https = event["user"]["profile_image_url_https"]
        event_user_profile_link_color = event["user"]["profile_link_color"]
        event_user_profile_sidebar_border_color = event["user"]["profile_sidebar_border_color"]
        event_user_profile_sidebar_fill_color = event["user"]["profile_sidebar_fill_color"]
        event_user_profile_text_color = event["user"]["profile_text_color"]
        event_user_profile_url = event["user"]["profile_url"]
        event_user_profile_use_background_image = event["user"]["profile_use_background_image"]
        event_user_protected = event["user"]["protected"]
        event_user_screen_name = event["user"]["screen_name"]
        event_user_statuses_count = event["user"]["statuses_count"]
        event_user_time_zone = event["user"]["time_zone"]
        event_user_translator_type = event["user"]["translator_type"]
        event_user_url = event["user"]["url"]
        event_user_utc_offset = event["user"]["utc_offset"]
        event_user_verified = event["user"]["verified"]
        event_user_withheld_in_countries = event["user"]["withheld_in_countries"]
        all_single_items = [pd_deployment_id, pd_hops, pd_id, pd_owner_id, pd_pipeline_id, pd_platform_version,
                            pd_replay, pd_resume, pd_source_type, pd_test, pd_trace_id, pd_ts, pd_verified,
                            pd_workflow_id, pd_workflow_name, event, event_contributors, event_coordinates,
                            event_created_at, event_created_at_iso8601, event_created_at_timestamp,
                            event_display_text_range, event_entities, event_favorite_count, event_favorited,
                            event_full_text, event_geo, event_id, event_id_str, event_in_reply_to_screen_name,
                            event_in_reply_to_status_id, event_in_reply_to_status_id_str, event_in_reply_to_user_id,
                            event_in_reply_to_user_id_str, event_is_quote_status, event_lang, event_metadata,
                            event_metadata_iso_language_code, event_metadata_result_type, event_place,
                            event_possibly_sensitive, event_retweet_count, event_retweeted, event_source,
                            event_truncated, event_url, event_user, event_user_contributors_enabled,
                            event_user_created_at, event_user_default_profile, event_user_default_profile_image,
                            event_user_description, event_user_entities, event_user_entities_description,
                            event_user_entities_description_urls, event_user_favourites_count,
                            event_user_follow_request_sent, event_user_followers_count, event_user_following,
                            event_user_friends_count, event_user_geo_enabled, event_user_has_extended_profile,
                            event_user_id, event_user_id_str, event_user_is_translation_enabled,
                            event_user_is_translator, event_user_lang, event_user_listed_count, event_user_location,
                            event_user_name, event_user_notifications, event_user_profile_background_color,
                            event_user_profile_background_image_url, event_user_profile_background_image_url_https,
                            event_user_profile_background_tile, event_user_profile_banner_url,
                            event_user_profile_image_url, event_user_profile_image_url_https,
                            event_user_profile_link_color, event_user_profile_sidebar_border_color,
                            event_user_profile_sidebar_fill_color, event_user_profile_text_color,
                            event_user_profile_url, event_user_profile_use_background_image, event_user_protected,
                            event_user_screen_name, event_user_statuses_count, event_user_time_zone,
                            event_user_translator_type, event_user_url, event_user_utc_offset, event_user_verified,
                            event_user_withheld_in_countries]
        return all_single_items

    # Group B
    def hashtag(self, hashtag):
        for i in range(len(hashtag)):
            self.event_entities_hashtagsi.append(hashtag[i])
            self.event_entities_hashtags_indices.append(hashtag[i]["indices"])
            self.event_entities_hashtags_text.append(hashtag[i]["text"])
        all_hashtag = [self.event_entities_hashtagsi, self.event_entities_hashtags_indices,
                       self.event_entities_hashtags_text]
        return all_hashtag
    # Group C
    def symbols(self, symbols):
        for i in range(len(symbols)):
            self.event_entities_symbolsi.append(symbols[i])
            self.event_entities_symbols_indices.append(symbols[i]["indices"])
            self.event_entities_symbols_text.append(symbols[i]["text"])
        all_symbols = [self.event_entities_symbolsi, self.event_entities_symbols_indices,
                       self.event_entities_symbols_text]
        return all_symbols
    # Group D
    def user_mentions(self, user_mentions):
        for i in range(len(user_mentions)):
            self.event_entities_user_mentionsi.append(user_mentions[i])
            self.event_entities_user_mentions_screen_name.append(user_mentions[i]["screen_name"])
            self.event_entities_user_mentions_name.append(user_mentions[i]["name"])
            self.event_entities_user_mentions_id.append(user_mentions[i]["id"])
            self.event_entities_user_mentions_id_str.append(user_mentions[i]["id_str"])
            self.event_entities_user_mentions_indices.append(user_mentions[i]["indices"])
        all_mentions = [self.event_entities_user_mentionsi, self.event_entities_user_mentions_screen_name,
                        self.event_entities_user_mentions_name, self.event_entities_user_mentions_id,
                        self.event_entities_user_mentions_id_str, self.event_entities_user_mentions_indices]
        return all_mentions
    # Group E
    def entities_urls(self, urls):
        for i in range(len(urls)):
            self.event_entities_urlsi.append(urls[i])
            self.event_entities_urlsi_display_url.append(urls[i]["display_url"])
            self.event_entities_urlsi_expanded_url.append(urls[i]["expanded_url"])
            self.event_entities_urlsi_indices.append(urls[i]["indices"])
            self.event_entities_urlsi_url.append(urls[i]["url"])
        all_urls = [self.event_entities_urlsi, self.event_entities_urlsi_display_url,
                    self.event_entities_urlsi_expanded_url, self.event_entities_urlsi_indices,
                    self.event_entities_urlsi_url]
        return all_urls
    # Group F
    def entities_media(self, media):
        for i in range(len(media)):
            self.event_entities_mediai.append(media[i])
            self.event_entities_media_display_url.append(media[i]["display_url"])
            self.event_entities_media_expanded_url.append(media[i]["expanded_url"])
            self.event_entities_media_id.append(media[i]["id"])
            self.event_entities_media_id_str.append(media[i]["id_str"])
            self.event_entities_media_indices.append(media[i]["indices"])
            self.event_entities_media_media_url.append(media[i]["media_url"])
            self.event_entities_media_media_url_https.append(media[i]["media_url_https"])
            self.event_entities_media_sizes.append(media[i]["sizes"])
            self.event_entities_media_type.append(media[i]["type"])
            self.event_entities_media_url.append(media[i]["url"])
        all_media = [self.event_entities_mediai, self.event_entities_media_display_url,
                     self.event_entities_media_expanded_url, self.event_entities_media_id,
                     self.event_entities_media_id_str, self.event_entities_media_indices,
                     self.event_entities_media_media_url, self.event_entities_media_media_url_https,
                     self.event_entities_media_sizes, self.event_entities_media_type, self.event_entities_media_url]
        return all_media
    # Group G
    def extended_media(self, extended):
        for i in range(len(extended)):
            self.event_extended_entities_media.append(extended["media"])
            self.event_extended_entities_mediai.append(extended["media"][i])
            self.event_extended_entities_mediai_display_url.append(extended["media"][i]["display_url"])
            self.event_extended_entities_mediai_expanded_url.append(extended["media"][i]["expanded_url"])
            self.event_extended_entities_mediai_id.append(extended["media"][i]["id"])
            self.event_extended_entities_mediai_id_str.append(extended["media"][i]["id_str"])
            self.event_extended_entities_mediai_indices.append(extended["media"][i]["indices"])
            self.event_extended_entities_mediai_media_url.append(extended["media"][i]["media_url"])
            self.event_extended_entities_mediai_media_url_https.append(extended["media"][i]["media_url_https"])
            self.event_extended_entities_mediai_sizes.append(extended["media"][i]["sizes"])
            self.event_extended_entities_mediai_type.append(extended["media"][i]["type"])
            self.event_extended_entities_mediai_url.append(extended["media"][i]["url"])
        all_extended = [self.event_extended_entities_media, self.event_extended_entities_mediai,
                        self.event_extended_entities_mediai_display_url,
                        self.event_extended_entities_mediai_expanded_url, self.event_extended_entities_mediai_id,
                        self.event_extended_entities_mediai_id_str, self.event_extended_entities_mediai_indices,
                        self.event_extended_entities_mediai_media_url,
                        self.event_extended_entities_mediai_media_url_https,
                        self.event_extended_entities_mediai_sizes, self.event_extended_entities_mediai_type,
                        self.event_extended_entities_mediai_url]
        return all_extended
    # Group H
    def user_urls(self, user_urls):
        for i in range(len(user_urls)):
            self.event_user_entities_url_urlsi_display_url.append(user_urls[i]["display_url"])
            self.event_user_entities_url_urlsi_expanded_url.append(user_urls[i]["expanded_url"])
            self.event_user_entities_url_urlsi_indices.append(user_urls[i]["indices"])
            self.event_user_entities_url_urlsi_url.append(user_urls[i]["url"])
        all_user_urls = [self.event_user_entities_url_urlsi,
                         self.event_user_entities_url_urlsi_display_url,
                         self.event_user_entities_url_urlsi_expanded_url,
                         self.event_user_entities_url_urlsi_indices, self.event_user_entities_url_urlsi_url]
        return all_user_urls
    # Group I
    def keyword(self):
        keywords = [self.has_shr, self.has_shr_count, self.has_tbl, self.has_tbl_count]
        return keywords

    @staticmethod
    def data(all_single_items, all_hashtag, all_symbols, all_mentions, all_urls, all_media, all_extended, all_user_urls, keywords):
        data = {
                # Group A
                "pd_deployment_id": all_single_items[0],
                "pd_hops": all_single_items[1],
                "pd_id": all_single_items[2],
                "pd_owner_id": all_single_items[3],
                "pd_pipeline_id": all_single_items[4],
                "pd_platform_version": all_single_items[5],
                "pd_replay": all_single_items[6],
                "pd_resume": all_single_items[7],
                "pd_source_type": all_single_items[8],
                "pd_test": all_single_items[9],
                "pd_trace_id": all_single_items[10],
                "pd_ts": all_single_items[11],
                "pd_verified": all_single_items[12],
                "pd_workflow_id": all_single_items[13],
                "pd_workflow_name": all_single_items[14],
                "event": all_single_items[15],
                "event_contributors": all_single_items[16],
                "event_coordinates": all_single_items[17],
                "event_created_at": all_single_items[18],
                "event_created_at_iso8601": all_single_items[19],
                "event_created_at_timestamp": all_single_items[20],
                "event_display_text_range": all_single_items[21],
                "event_entities": all_single_items[22],
                "event_favorite_count": all_single_items[23],
                "event_favorited": all_single_items[24],
                "event_full_text": all_single_items[25],
                "event_geo": all_single_items[26],
                "event_id": all_single_items[27],
                "event_id_str": all_single_items[28],
                "event_in_reply_to_screen_name": all_single_items[29],
                "event_in_reply_to_status_id": all_single_items[30],
                "event_in_reply_to_status_id_str": all_single_items[31],
                "event_in_reply_to_user_id": all_single_items[32],
                "event_in_reply_to_user_id_str": all_single_items[33],
                "event_is_quote_status": all_single_items[34],
                "event_lang": all_single_items[35],
                "event_metadata": all_single_items[36],
                "event_metadata_iso_language_code": all_single_items[37],
                "event_metadata_result_type": all_single_items[38],
                "event_place": all_single_items[39],
                "event_possibly_sensitive": all_single_items[40],
                "event_retweet_count": all_single_items[41],
                "event_retweeted": all_single_items[42],
                "event_source": all_single_items[43],
                "event_truncated": all_single_items[44],
                "event_url": all_single_items[45],
                "event_user": all_single_items[46],
                "event_user_contributors_enabled": all_single_items[47],
                "event_user_created_at": all_single_items[48],
                "event_user_default_profile": all_single_items[49],
                "event_user_default_profile_image": all_single_items[50],
                "event_user_description": all_single_items[51],
                "event_user_entities": all_single_items[52],
                "event_user_entities_description": all_single_items[53],
                "event_user_entities_description_urls": all_single_items[54],
                "event_user_favourites_count": all_single_items[55],
                "event_user_follow_request_sent": all_single_items[56],
                "event_user_followers_count": all_single_items[57],
                "event_user_following": all_single_items[58],
                "event_user_friends_count": all_single_items[59],
                "event_user_geo_enabled": all_single_items[60],
                "event_user_has_extended_profile": all_single_items[61],
                "event_user_id": all_single_items[62],
                "event_user_id_str": all_single_items[63],
                "event_user_is_translation_enabled": all_single_items[64],
                "event_user_is_translator": all_single_items[65],
                "event_user_lang": all_single_items[66],
                "event_user_listed_count": all_single_items[67],
                "event_user_location": all_single_items[68],
                "event_user_name": all_single_items[69],
                "event_user_notifications": all_single_items[70],
                "event_user_profile_background_color": all_single_items[71],
                "event_user_profile_background_image_url": all_single_items[72],
                "event_user_profile_background_image_url_https": all_single_items[73],
                "event_user_profile_background_tile": all_single_items[74],
                "event_user_profile_banner_url": all_single_items[75],
                "event_user_profile_image_url": all_single_items[76],
                "event_user_profile_image_url_https": all_single_items[77],
                "event_user_profile_link_color": all_single_items[78],
                "event_user_profile_sidebar_border_color": all_single_items[79],
                "event_user_profile_sidebar_fill_color": all_single_items[80],
                "event_user_profile_text_color": all_single_items[81],
                "event_user_profile_url": all_single_items[82],
                "event_user_profile_use_background_image": all_single_items[83],
                "event_user_protected": all_single_items[84],
                "event_user_screen_name": all_single_items[85],
                "event_user_statuses_count": all_single_items[86],
                "event_user_time_zone": all_single_items[87],
                "event_user_translator_type": all_single_items[88],
                "event_user_url": all_single_items[89],
                "event_user_utc_offset": all_single_items[90],
                "event_user_verified": all_single_items[91],
                "event_user_withheld_in_countries": all_single_items[92],
                # Group B
                "event_entities_hashtagsi": all_hashtag[0],
                "event_entities_hashtags_indices": all_hashtag[1],
                "event_entities_hashtags_text": all_hashtag[2],
                # Group C
                "event_entities_symbolsi": all_symbols[0],
                "event_entities_symbols_indices": all_symbols[1],
                "event_entities_symbols_text": all_symbols[2],
                # Group D
                "event_entities_user_mentionsi": all_mentions[0],
                "event_entities_user_mentions_screen_name": all_mentions[1],
                "event_entities_user_mentions_name": all_mentions[2],
                "event_entities_user_mentions_id": all_mentions[3],
                "event_entities_user_mentions_id_str": all_mentions[4],
                "event_entities_user_mentions_indices": all_mentions[5],
                # Group E
                "event_entities_urlsi": all_urls[0],
                "event_entities_urlsi_display_url": all_urls[1],
                "event_entities_urlsi_expanded_url": all_urls[2],
                "event_entities_urlsi_indices": all_urls[3],
                "event_entities_urlsi_url": all_urls[4],
                # Group F
                "event_entities_mediai": all_media[0],
                "event_entities_mediai_display_url": all_media[1],
                "event_entities_mediai_expanded_url": all_media[2],
                "event_entities_mediai_id": all_media[3],
                "event_entities_mediai_id_str": all_media[4],
                "event_entities_mediai_indices": all_media[5],
                "event_entities_mediai_media_url": all_media[6],
                "event_entities_mediai_media_url_https": all_media[7],
                "event_entities_mediai_sizes": all_media[8],
                "event_entities_mediai_type": all_media[9],
                "event_entities_mediai_url": all_media[10],
                # Group G
                "event_extended_entities_media": all_extended[0],
                "event_extended_entities_mediai": all_extended[1],
                "event_extended_entities_mediai_display_url": all_extended[2],
                "event_extended_entities_mediai_expanded_url": all_extended[3],
                "event_extended_entities_mediai_id": all_extended[4],
                "event_extended_entities_mediai_id_str": all_extended[5],
                "event_extended_entities_mediai_indices": all_extended[6],
                "event_extended_entities_mediai_media_url": all_extended[7],
                "event_extended_entities_mediai_media_url_https": all_extended[8],
                "event_extended_entities_mediai_sizes": all_extended[9],
                "event_extended_entities_mediai_type": all_extended[10],
                "event_extended_entities_mediai_url": all_extended[11],
                # Group H
                "event_user_entities_url_urls": all_user_urls[0],
                "event_user_entities_url_urlsi_display_url": all_user_urls[1],
                "event_user_entities_url_urlsi_expanded_url": all_user_urls[2],
                "event_user_entities_url_urlsi_indices": all_user_urls[3],
                "event_user_entities_url_urlsi_url": all_user_urls[4],
                # Group I
                "has_shr": keywords[0],
                "has_shr_count": keywords[1],
                "has_tbl": keywords[2],
                "has_tbl_count": keywords[3],
        }
        return data