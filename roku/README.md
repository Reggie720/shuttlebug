# Shuttlebug for Roku

A Hog Entertainment · Developer build 0.2.3 · Not published or monetized.

Continues the supplied Shuttlebug_Roku_Developer_Starter.zip. The original launcher assets and app identity are retained, with the existing Shuttlebug ladybug added to the SceneGraph header. No website files were changed.

## Included
- Native SceneGraph catalog browsing and title details.
- D-pad navigation, OK selection, Play/Pause, native fullscreen Video and Back.
- Onscreen search by title, genre and synopsis.
- Device-local favorites and progress in the Roku registry; resume/start-over controls.
- Source fallbacks and unavailable-stream messages. The three SideWays episodes use the publisher's full HLS VOD playlists; other titles use progressive MP4. Existing English subtitle tracks are passed to the native player.
- Original creator credits, change notices and license/source links on each title.
- Startup and pre-playback live rights checks. Missing, held, changed or unverified records cannot play. The packaged feed contains only the 17 records marked reviewed in the existing register. No new films were added or rights upgraded.
- Optional unpaid pre-roll/mid-roll test via a native Roku Video node. Tests start OFF and are not persisted. Turn ON in the left menu. The local five-second Shuttlebug house creative has no impression/tracking URLs, uses no ad-server calls and does not request default or paid demand. The 30-second mid-roll is accelerated developer testing only, not a production ad policy.
- Cold/warm contentId input handling for developer deep-link testing, subject to the same rights check.

## Package
`packages/Shuttlebug_Roku_Developer.zip` is a sideloadable development ZIP with `manifest` at its root. It is not a signed store package or a public app. `packages/SHA256SUMS` identifies the exact build. Sources, dependencies, tests and documentation remain outside the install ZIP.

Build locally or in GitHub Actions:
```
cd roku
npm ci --ignore-scripts
npm run build
npm test
```
Tools: Node.js 22, Python 3, pinned BrighterScript compiler and off-device BRS interpreter. Dependency versions are locked. All are free development tools. No paid service or purchase was used.

The build generator reads the existing repository catalog and rights register; disagreements in required license/attribution fields fail the build. It writes Roku-only JSON, validates BrightScript/SceneGraph syntax and creates the ZIP. The workflow repeats this on relevant commits and uploads the package as a build artifact.

## Developer device testing
A Roku device with Developer Mode enabled and an authorized tester on its network is required for local sideloading. An eligible Roku Cloud Emulator account may be an alternative; account availability must be checked. The remote development workspace cannot access your home's private Roku IP.

From your Android phone on the same Wi-Fi as the Roku, the device's Development Application Installer can accept this ZIP after Developer Mode setup. The owner must complete Roku account terms, developer-key creation and any password entry. See DEVICE_TESTS.md for the exact checklist. Keep developer credentials and signing keys out of GitHub.

## Honest validation limits
Compiler and unit/controller tests do not run Roku OS or SceneGraph graphics, and do not decode video through Roku hardware or execute its downloaded RAF library. HTTP/MP4 header checks establish source availability at check time only. This updated build has not been tested on a physical Roku, signed, certified or published. The complete device test matrix remains pending. This build also preserves bookmarks when rights verification is temporarily unavailable, cancels pending playback on Back, saves the latest paused position, rejects duplicate rights records and bounds ad handoff timeouts.

Production monetization requires partner acceptance, approved demand configuration, current Roku ad policy review and hardware validation. The developer app deliberately contains no production ad URL, paid ad credentials or default-demand fallback.

Sources:
- https://developer.roku.com/dev/docs/playing-videos
- https://developer.roku.com/dev/docs/integrating-roku-advertising-framework
- https://developer.roku.com/dev/docs/raf-api
- https://developer.roku.com/dev/docs/implementing-deep-linking
- https://developer.roku.com/dev/docs/channel-publishing-guide
- https://developer.roku.com/dev/docs/rce

Build 0.2.3: Native unpaid test previews keep focus on the scene so Back skips the commercial. Completion/error/12-second timeout stops and hides the ad before resuming content. A film decoder handoff timeout returns to details. A re-entry guard prevents stop events from recursively completing the ad. The retained RAF adapter is inactive for these previews; paid advertising remains unconfigured.

Build 0.2.3 adds Browse > Movies / TV Shows > Show > Season > Episode navigation. Season metadata is retained when supplied; missing season data is labeled Episodes (season unspecified), never invented. Search and Favorites continue to list individual playable titles. Back returns through the folder hierarchy. Off-device compiler, package and grouping tests passed; physical remote navigation and playback remain pending.
