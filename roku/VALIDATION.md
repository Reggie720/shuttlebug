# Validation record — November 19, 2026

## Completed off-device
- BrighterScript 0.73.8 parsed and validated all shipped BrightScript and SceneGraph XML without errors.
- The native BrightScript logic was executed using the BRS 0.45.0 interpreter: allow/hold revocation, changed-license rejection, missing-rights fail-closed behavior, case-insensitive search, empty results, save/remove favorites, bookmark validation and unpaid ad-pod invariants passed.
- Controller functions were exercised with mock node objects: pause/resume commands, key-up handling, Back stops/hides film, root exit signal, navigation focus handoff, one-shot mid-roll latch, saved position and decoder-stop-before-RAF sequencing passed.
- Package validation passed: manifest at ZIP root, matching component scripts and current feed, no held titles, all 17 rights/attribution records match the canonical register, no dependencies/tests packed into the app.
- HTTP range probes retrieved MP4 headers for at least one source for each of the 17 enabled titles; details are in tests/source-checks.json. This proves reachability, not continuous availability or on-Roku decoding.
- The unpaid five-second H.264 test commercial is copied unchanged from the existing Shuttlebug house creative. Test RAF pods have empty tracking arrays, local media only and no getAds/default/paid-demand calls.
- Build uses existing red-and-black starter assets and the existing ladybug image. Website code and the canonical rights register were not modified.

## Not yet tested or approved
Actual SceneGraph rendering/focus on Roku; native player decoding/seeking on each target model; downloaded RAF runtime rendering and Back handling; real registry persistence; suspend/Home/relaunch behavior; deep-link ECP input on hardware; subtitle/accessibility behavior; Roku static analysis/certification and store approval.

The BRS interpreter is not a Roku emulator. Mock controller checks do not establish native widget or RAF behavior. No Roku account, developer key, device or paid advertising partner was accessed. No money was spent. No public or beta publication is claimed.
