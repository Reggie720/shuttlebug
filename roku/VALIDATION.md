# Build 0.3.0 validation

Off-device checks cover BrighterScript compilation, XML parsing/script links, complete ZIP/source byte matching, rights intersection and held-title exclusion, search/favorites/bookmarks, RowList focus/selection mapping, empty shelf suppression, series grouping, catalog-added sorting, sanitized local history and native-ad failure recovery. Automated mocks do not render SceneGraph or decode video.

The application preserves the existing 17 cleared catalog entries, playback source overrides and caption records. Test commercials are unpaid, disabled by default, and have no paid demand or tracking endpoints. The retained RAF adapter is inactive for local native previews. No website content was changed.

Physical Roku testing remains required for layout/overscan, poster downloads, directional focus, keyboard, series/season/episode Back behavior, player decoding/seeking/subtitles, pre-roll and mid-roll transitions, failed-ad timeout/Back, saved favorites/progress/history across launch and Home/suspend. This new build has not been physically tested by the developer. Earlier builds were reported working by the owner.

Public store publishing, screenshots, signed packaging, certification and paid advertising are not claimed.

0.3.1: The owner confirmed 0.3.0 movie playback on a physical Roku. The photo showed the brand overlapping Home. This patch confines the wordmark to the sidebar below the ladybug, removes the old runtime font override, and wraps the company name. Updated visual spacing still requires device confirmation.
