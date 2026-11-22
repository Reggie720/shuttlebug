# Shuttlebug — Roku app 895785

Prepared November 20, 2026 from the implementation. This file does not indicate dashboard changes or public submission. Developer Dashboard access returned a CloudFront 403 in the agent browser, including one reload. Uploaded artwork and existing settings were not changed.

## Verified profile values

| Field | Value |
|---|---|
| App name | Shuttlebug |
| Operator | A Hog Entertainment |
| App type | Video |
| Customer sign-in | No; app has no account/authentication flow |
| Website / Learn more | https://shuttlebug.onrender.com/ |
| Privacy policy | https://shuttlebug.onrender.com/privacy.html |
| Terms | https://shuttlebug.onrender.com/terms.html |
| Support URL | https://shuttlebug.onrender.com/support.html |
| Support/admin/technical email | ahogentertainment@gmail.com |
| Admin/technical contact name | Reginald Dwayne Lawson |
| Phone | Owner must confirm a contact number for this business; do not borrow another business's number |
| Default language | English UI; some catalog sources have other spoken languages/captions |
| Store territory | Initial US scope requested by owner; do not expand without rights review |

## Store text prepared (do not overwrite existing saved copy without review)

Short description (under 300 characters):
Watch free independent films, animation and documentary series on Shuttlebug. Browse titles, search, save favorites and resume watching. No subscription or account required. Available programming may change.

Long description (under 1,500 characters):
Shuttlebug, operated by A Hog Entertainment, brings together a curated selection of authorized independent films, animated shorts and documentary episodes. Discover programming in poster rows, browse television series and available episodes, search by title or series, save favorites and pick up from a saved viewing position. Favorites, progress and recently watched titles stay on your Roku device. No Shuttlebug account or subscription is required. Internet access is required for streaming. Programming, captions and availability vary by title. Current developer test commercials are unpaid demonstrations; paid advertising is not yet active. Commercial catalog expansion and public availability depend on licensing and platform approval.

## Monetization

Planned business model: free to the viewer, advertising supported. No subscriptions, rentals, purchases or cable login exist. Native local test ads are not a live paid-ad integration. The current public app-ads.txt intentionally authorizes no programmatic sellers; do not invent Google, Roku or other seller IDs. Actual partner onboarding, production RAF/VAST integration, consent/identifier handling and certification remain required before paid video ads. The legacy RAF adapter is not used by the native preview path. Do not enroll in paid services or accept monetization agreements without owner approval. Do not mislabel intended AVOD as no planned monetization just to complete a field.

Developer URL resource prepared: https://shuttlebug.onrender.com/app-ads.txt

## Package and testing

Current installable source ZIP: roku/packages/Shuttlebug_Roku_Developer.zip (0.3.1). It is a developer package, not proof of a signed store package. No .pkg was found in this repository. Dashboard/package status could not be inspected. If store packaging requires the device-generated signed .pkg, generating/exporting that file requires the owner's Roku developer signing setup/hardware. Do not disclose signing passwords or private keys in this repository.

Deep-link test examples from the current cleared catalog:
- contentId=bbb, mediaType=movie
- contentId=bbs1, mediaType=episode

Run Roku Dashboard Static Analysis and App Behavior Analysis on the actual submission package once accessible. Current off-device tests cover source/package integrity, rights gates, browsing, search, favorites, bookmarks and test-ad recovery; these do not substitute for Roku certification. Owner reported installation, playback, layout fix, feature tests and a test commercial working; the individual certification matrix is not independently verified.

Existing poster/screenshots must be preserved. Actual 1920×1080 app screenshots must accurately represent the running app; generated brand or concept artwork must not be represented as device screenshots. Current uploads could not be inspected.

## Owner decisions/approvals still needed

- Confirm intended primary audience / Made for Kids setting and appropriate age rating after reviewing the catalog. Merely having animation does not settle these answers. Do not claim child-directed-service compliance from the current implementation.
- Confirm this business's contact phone if required.
- Complete signing/device-only packaging if a signed submission file is not already available in the dashboard.
- Approve any binding distribution/advertising agreement and final public-release submission. No public-release action is authorized yet.

Official reference reviewed: https://developer.roku.com/dev/docs/channel-publishing-guide


## Static-analysis update — 0.3.2 (November 22, 2026)

Prepared after the owner's first signed 0.3.1 upload. Adds RSG 1.3, launch/dialog lifecycle beacons, RAF measurement metadata configuration (with limit-ad-tracking requested; no paid demand requests), memory-monitor subscription/fallback and hidden-resource cleanup. Removes deprecated manifest subtitle/side-icon entries. Keeps supports_input_launch=1 and moves the live roInputEvent branch to the front of the main loop, using the documented event pattern; the prior build already contained this support, so the scanner finding remains unverified until Roku rescans.

This is a sideload ZIP, not a signed store package. Install on the same keyed Roku, test home/playback/Back/resume and cold/warm deep links, then package using the EXISTING genkey password (do not generate a new key). Re-upload the new .pkg and inspect Roku's actual results. Local compilation/tests are not a Roku static-analysis pass. Remaining HD asset warnings and any new scanner results must be resolved before claiming certification readiness. No pre-home user dialog is normally shown, so dialog beacons are conditional on an actual startup error dialog.
