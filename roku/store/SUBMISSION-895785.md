# Shuttlebug — app 895785 release handoff

Updated November 23, 2026. Next source build: **0.3.3**. Public release is not approved or scheduled.

## Verified progress

- Owner created the developer signing key on their Roku and retained its generated password privately. Never run genkey again merely to package an update. No signing secret is stored here.
- Owner signed, downloaded and uploaded 0.3.2. Current portal package begins P6ca3; do not mistake the older Pe15 package or source ZIP for this build.
- Owner's 0.3.2 rescan cleared RSG 1.3, AppLaunchComplete and General Audience Measurement errors. The visible remaining error is roInput support, requirement 5.2. Some warnings remain in the captured results; this is not a certification pass.
- Owner confirmed 0.3.2 launches, plays a film and returns to details with Back.
- Owner tested a live /input?contentId=bbb&mediaType=movie POST. Roku returned HTTP 200; after dismissing the Digital Clock screensaver, the owner confirmed Big Buck Bunny played. This is owner-reported hardware evidence for warm input, not independent cold-launch or full certification verification.
- Email verification and linked-device prerequisites were completed. Listing setup, assets, app profile and monetization were saved by the owner. Portal may still require payout enrollment. Actual current account state must be reviewed in the authenticated portal; do not assume final completion.

## Prepared 0.3.3 changes

- Route input-event argument maps directly to an always-notifying SceneGraph field, following Roku's published SGDEX event-forwarding example. Cold-launch arguments have their own field and share string validation with warm input. Both feed the existing rights-gated playback path. This is a scanner-compatibility adjustment, NOT proof the remaining scanner error is resolved.
- Keep supports_input_launch=1, RSG 1.3, launch/dialog beacons, limit-ad-tracking request, required RAF measurement metadata and memory monitoring.
- Export existing branding as a 290x218 manifest HD icon, 1280x720 HD splash and 720x480 SD splash. The Streaming Store's separate 336x210 artwork is preserved under store assets.
- Remove InitClientCertificates from the public HTTPS rights-register request. This endpoint does not use mutual TLS or require a device-attestation token. Retain Roku's CA trust bundle and HTTPS validation; do not disable server-certificate checks.
- Tests cover package/image integrity, input argument validation, cold/warm callback routing, queued links during an ad, held-content rejection, controls, bookmarks, launch-beacon one-shot behavior and memory cleanup.

## What can be completed without the stick

Source fixes, local compilation/tests, CI, publication of the source update, accurate policy pages and release/review notes. This source ZIP cannot replace the signed .pkg already in Roku's dashboard. Roku's scanner cannot validate unsubmitted local changes.

## When the stick reconnects

1. Connect the laptop and the SAME keyed Roku to the same private Wi-Fi/hotspot. Use the Roku's then-current IP, not a stale address.
2. Install the 0.3.3 source ZIP using the device's Development Application Installer. Verify launch, film/episode playback, Back, resume and cold/warm links. Keep optional test ads OFF for normal use.
3. In Packager, enter Shuttlebug 0.3.3 and the existing genkey signing password. Generate/download the NEW .pkg. The rokudev login password is different from the signing password.
4. Upload that .pkg to https://developer.roku.com/apps/public/895785/package and run Static Analysis. Review actual results. The minimum firmware setting for RSG 1.3 is 15.1 or later; the owner previously selected v15.1.0 b1.
5. If requirement 5.2 persists despite device verification, use the review-request draft below. Do not continue arbitrary code rewrites to guess what the scanner recognizes.
6. Complete Deep Linking and App Behavior Analysis using the actual package/device. Review content rating, authentic screenshots, payout requirements and final owner approval before any public submission.

Deep-link IDs: bbb / movie, bbs1 / episode. Cold launch uses /launch/dev; warm input uses /input. Held and unknown IDs must not play. A screensaver can obscure the test; dismiss it before observing the outcome.

## Saved app information

| Field | Value |
|---|---|
| Name / operator | Shuttlebug / A Hog Entertainment |
| App type | Video |
| Sign-in / customer payments | None |
| Website / Learn more | https://shuttlebug.onrender.com/ |
| Privacy | https://shuttlebug.onrender.com/privacy.html |
| Terms | https://shuttlebug.onrender.com/terms.html |
| Support | https://shuttlebug.onrender.com/support.html |
| Business email | ahogentertainment@gmail.com |
| Administrative / technical contact | Reginald Dwayne Lawson |
| Owner instructions/files email | readysetgoo720@gmail.com |
| Phone | Owner entered a number in the private portal; verify there rather than publishing it in this repository |
| Territory | Initial US scope; do not expand without rights review |
| Audience | General audience including family material; not automatically an all-ages rating |

The monetization Developer URL field accepts the ROOT: https://shuttlebug.onrender.com . Its app-ads.txt is served at /app-ads.txt and currently authorizes no programmatic sellers. Paid demand, subscriptions, purchases and sponsorships are not active. Optional house commercials are unpaid tests. Production ad partners/tags/consent remain separate work before paid ads launch.

Short description (under 300 characters):
Watch free independent films, animation and documentary series on Shuttlebug. Browse titles, search, save favorites and resume watching. No subscription or account required. Available programming may change.

Long description (under 1,500 characters):
Shuttlebug, operated by A Hog Entertainment, brings together a curated selection of authorized independent films, animated shorts and documentary episodes. Discover programming in poster rows, browse television series and available episodes, search by title or series, save favorites and pick up from a saved viewing position. Favorites, progress and recently watched titles stay on your Roku device. No Shuttlebug account or subscription is required. Internet access is required for streaming. Programming, captions and availability vary by title. Current developer test commercials are unpaid demonstrations; paid advertising is not yet active. Commercial catalog expansion and public availability depend on licensing and platform approval.

Preserve saved listing artwork. Use authentic captures for screenshot requirements; branding/concept images are not evidence of the running app. Do not add unlicensed programming.

## Review-request draft — NOT SENT

Subject: Shuttlebug 895785 — requirement 5.2 roInput static-analysis finding

Hello Roku Developer Support,

Shuttlebug (app 895785) has a remaining static-analysis finding for roInput support, requirement 5.2. The submitted 0.3.2 package includes supports_input_launch=1, creates roInput, attaches it to the app message port, handles roInputEvent and forwards contentId into the rights-checked playback flow. During a test on the owner's Roku Streaming Stick running Roku OS 16.0.4, an ECP POST to /input?contentId=bbb&mediaType=movie returned HTTP 200 and the owner confirmed Big Buck Bunny played after dismissing the screensaver.

A 0.3.3 source update aligns event forwarding with the SGDEX reference sample and validates launch/input argument maps consistently. It has not yet been signed, submitted or verified on hardware. Please identify the specific missing pattern or behavior behind the finding, or advise how to submit runtime evidence for review if the finding persists after the next signed upload.

Thank you,
Reginald Lawson — A Hog Entertainment
ahogentertainment@gmail.com

Do not send automatically. Update this draft with the actual latest package/version and results before the owner approves contacting support. Never attach a signing password.

## Official references consulted

- https://developer.roku.com/dev/docs/roinput
- https://partnersuccess.roku.com/hc/en-us/articles/360049122434-I-have-added-supports-input-launch-1-in-my-manifest-but-still-am-getting-a-Static-Analysis-error (attached SGDEX sample)
- https://developer.roku.com/dev/docs/channel-manifest
- https://developer.roku.com/dev/docs/measuring-channel-performance
- https://developer.roku.com/dev/docs/raf-api
