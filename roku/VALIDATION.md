# Validation record — November 19, 2026

Build: 0.2.3. This record distinguishes off-device checks from unrun device tests.

## Completed off-device
- BrighterScript 0.73.8 parsed and validated all shipped BrightScript and SceneGraph XML without errors.
- The native BrightScript logic was executed using the BRS 0.45.0 interpreter: allow/hold revocation, changed-license rejection, missing-rights fail-closed behavior, case-insensitive search, empty results, save/remove favorites, bookmark validation and unpaid ad-pod invariants passed.
- Controller functions were exercised with mock node objects: pause/resume commands, key-up handling, Back stops/hides film, root exit signal, navigation focus handoff, one-shot mid-roll latch, saved position and decoder-stop-before-ad sequencing passed.
- Additional regression checks passed: pending Play is canceled by Back; a timed-out ad handoff returns safely; Back during an ad takes priority over a queued deep link; pause saves the latest position; buffering notifications cannot overwrite a resume bookmark; native stop returns from the player; duplicate and malformed rights records are rejected. Temporary verification failures no longer erase bookmarks.
- Package validation passed: manifest at ZIP root, matching component scripts and current feed, no held titles, all 17 rights/attribution records match the canonical register, no dependencies/tests packed into the app.
- HTTP range probes retrieved MP4 headers for at least one source for each of the 17 enabled titles; details are in tests/source-checks.json. This proves reachability, not continuous availability or on-Roku decoding.
- Media inspection demuxed H.264 video and AAC audio for the 14 selected progressive MP4 sources. The three SideWays candidates reported initial-fragment durations, so Roku now uses publisher-supplied adaptive HLS instead. Each HLS VOD playlist has an end marker and a full episode duration (324.68, 361.60 and 333.76 seconds). Evidence: tests/media-probes.json and tests/hls-checks.json. This is not a full-film decode or a Roku playback test.
- Poster and English external subtitle URLs are absolute HTTPS URLs; native subtitle track selection remains subject to Roku device settings and testing.
- The unpaid five-second H.264 test commercial is copied unchanged from the existing Shuttlebug house creative. Test RAF pods have empty tracking arrays, local media only and no getAds/default/paid-demand calls.
- Build uses existing red-and-black starter assets and the existing ladybug image. Website code and the canonical rights register were not modified.

## Not yet tested or approved
Actual SceneGraph rendering/focus on Roku; native player decoding/seeking on each target model; native test-ad rendering and Back handling; real registry persistence; suspend/Home/relaunch behavior; deep-link ECP input on hardware; subtitle/accessibility behavior; Roku static analysis/certification and store approval.

The BRS interpreter is not a Roku emulator. Mock controller checks do not establish native widget or RAF behavior. No Roku account, developer key, device or paid advertising partner was accessed. No money was spent. No public or beta publication is claimed.

Build 0.2.3: Native unpaid test previews keep focus on the scene so Back skips the commercial. Completion/error/12-second timeout stops and hides the ad before resuming content. A film decoder handoff timeout returns to details. A re-entry guard prevents stop events from recursively completing the ad. The retained RAF adapter is inactive for these previews; paid advertising remains unconfigured.

Build 0.2.3 adds Browse > Movies / TV Shows > Show > Season > Episode navigation. Season metadata is retained when supplied; missing season data is labeled Episodes (season unspecified), never invented. Search and Favorites continue to list individual playable titles. Back returns through the folder hierarchy. Off-device compiler, package and grouping tests passed; physical remote navigation and playback remain pending.
