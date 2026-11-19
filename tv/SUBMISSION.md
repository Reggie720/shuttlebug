# Shuttlebug LG submission preparation — 2026-11-19

Publisher: A Hog Entertainment. Support: ahogentertainment@gmail.com.
App ID: com.ahogentertainment.shuttlebug. Version: 0.1.0.
Package: packages/com.ahogentertainment.shuttlebug_0.1.0_all.ipk.

This is a packaged web application, not the original redirect launcher. Build with `python3 tools/build-tv.py` then `npx --package @webos-tools/cli ares-package .tv-build -o tv/packages`. Official LG CLI 3.2.6 successfully generated and inspected this package. Packaging success does not establish TV compatibility or store eligibility.

Target initial evaluation: webOS 22 and newer. Earlier models are not claimed supported. Actual supported model years must be selected only after device testing. Internet is required; film providers may buffer or change availability. WebM titles may not decode on every LG model. No DRM or protected commercial asset delivery has been implemented; Echelon delivery requirements remain to be agreed.

## Listing draft
Title: Shuttlebug
Short description: Independent movies and series, free to watch.
Description: Discover credited independent films and documentary series with Shuttlebug from A Hog Entertainment. Browse with your TV remote, save favorites and resume watching on the same device. Available titles and playback compatibility vary. Internet required. Commercial catalog expansion is pending licensing agreements. No subscription required.
Privacy: https://shuttlebug.onrender.com/privacy.html
Terms: https://shuttlebug.onrender.com/terms.html
Category proposal: Entertainment. Price: Free.
Territories and age rating: owner must select after title-level territory and ratings review. Do not select worldwide by assumption.

## UX scenario draft
1. Launch: black background, red accents and ladybug identity, Home catalog.
2. Use arrows and OK to select Movies, TV or Settings; visible focus follows remote.
3. Select Big Buck Bunny; choose Play; choose Full screen.
4. Pause/resume using media keys or onscreen Play/Pause; seek using onscreen 10-second controls.
5. Back closes details and saves position. Open the same film and choose Play to resume.
6. Save/remove a film in My List. Confirm persistence after app restart.
7. Back from browsing returns Home. Back on Home must invoke the platform exit behavior; verify on device before submission.
8. Offline startup, unavailable media and network recovery must be tested on TV.
9. Use hosted partner demo to test unpaid pre/mid-rolls. Production ads disabled.

## Submission blockers and honest checklist
- LG Seller Lounge account, business verification, terms acceptance and authorized access: pending.
- Physical LG device: pending. No installation, decoder, remote, app-exit or suspend/resume test is claimed.
- Official LG UX template and mandatory self-checklist: download in Seller Lounge, transfer this scenario, fill actual results. Do not mark untested checks passed.
- Store artwork: existing icons included; store-specific dimensions/screenshots still require portal specifications and capture from tested TV app.
- Content age ratings, supported countries, minimum models and accessibility checks: pending.
- Monetization partner approval and production VAST SDK integration: pending.
- Public LG listing: not submitted, not approved, not published.

## Alternative public launches
Amazon Fire TV is the best next candidate for reuse of this web code; a native TV shell/packaged app and Amazon review are still required. Amazon developer registration is free. It is not a guaranteed faster public launch. New Fire TV devices may use different operating systems; choose target devices before building.
Roku enrollment/development/publication is free, but needs a separate SceneGraph/BrightScript implementation and certification; a beta access code is not a public Streaming Store app.
Google Play registration is $25, above this task's $10 ceiling; applicable new-personal-account testing adds at least 14 days. No purchase authorized or made.

Sources:
https://webostv.developer.lge.com/develop/tools/cli-installation
https://webostv.developer.lge.com/distribute/app-approval-process
https://developer.amazon.com/docs/app-submission/publish-app-login-and-add-app.html
https://developer.roku.com/dev/docs/roku-overview
https://developer.roku.com/dev/docs/channel-publishing-guide
https://support.google.com/googleplay/android-developer/answer/6112435
https://support.google.com/googleplay/android-developer/answer/14151465
