# Roku developer testing and store preparation

Status: NOT YET RUN ON ROKU. Populate model, Roku OS version, date, tester and actual results before submission. No item below is marked passed based on a compiler check.

## Install from an Android phone
1. Use a Roku device and Android phone on the same private Wi-Fi.
2. On the Roku remote, enter the official Developer Mode sequence: Home three times, Up twice, Right, Left, Right, Left, Right. The owner must review/accept the developer terms and set the developer password.
3. Record the development installer address shown on the Roku. Open that exact local address in your phone browser; sign in with the device developer credentials.
4. Upload `Shuttlebug_Roku_Developer.zip` and choose Install. Sideloading replaces the existing development app on that device. A signed public store app is a separate process.
5. For debugging, use the Roku debug console/tools on the same network; do not expose developer ports to the internet.

## Test matrix
| Test | Expected behavior | Actual result |
|---|---|---|
| Startup online | Live rights check; only currently reviewed titles shown | Pending device |
| Startup offline / failed rights service | No playable catalog; retry Browse after reconnect | Pending device |
| D-pad and OK | Visible focus; browse list, title detail and menu selection work | Pending device |
| Search | Keyboard entry, Search/Cancel and case-insensitive results; no held titles | Pending device |
| Favorites | Save/remove using detail action or Options; persists after Home/relaunch | Pending device |
| Film playback | Correct full film decodes, native fullscreen, audio, aspect ratio | Pending per title/model |
| Pause/resume / seek | Play toggles; native transport works; Back stops video | Pending device |
| Continue watching | Position restored; start-over resets; completed film restarts from zero | Pending device |
| Pre-roll test | Enable unpaid tests; local five-second creative; RAF labeling plus unpaid label; film starts | Pending device |
| Mid-roll test | After 30 seconds, content decoder stops; RAF plays one unpaid pod; film resumes saved position | Pending device |
| Ad Back / timeout | Back returns to details; watchdog avoids indefinite test-ad blockage | Pending device |
| Credits | Original attribution, source, license and change notices readable | Pending device |
| Rights revocation | A held/changed record is removed at next verification and cannot start | Pending controlled device test |
| Decode/network failure | Try another packaged source, then display an understandable error | Pending device |
| Back/Home | Back moves up then exits at root; Home exits; later launch recovers preferences | Pending device |
| Cold/warm deep link | Known cleared contentId plays after rights check; unknown/held ID refused | Pending device |
| Warm link during test ad | Queued until ad completes, then permission rechecked | Pending device |
| Low-memory / resume | No orphan Video/RAF nodes or unwanted audio after leaving playback | Pending device |

The shipped source checks cover URL reachability, not Roku hardware decoding. Test all 17 titles; fragmented MP4 streams and provider availability deserve particular attention. Where source subtitles are needed, external-subtitle integration/accessibility review remains a release prerequisite; this build preserves embedded media but does not configure external subtitle tracks.

## Listing draft
Name: Shuttlebug
Publisher: A Hog Entertainment
Summary: Explore independent movies and documentary episodes, free to watch.
Description: Browse credited independent films and documentary series with Shuttlebug. Search, save favorites and resume watching on the same Roku device. Internet required. Catalog availability varies with content permissions and provider availability. No subscription or account required. A Hog Entertainment does not imply endorsement by the content creators.
Support: ahogentertainment@gmail.com
Privacy: https://shuttlebug.onrender.com/privacy.html
Terms: https://shuttlebug.onrender.com/terms.html
Category proposal: Movies & TV. Price proposal: Free.
Age rating, countries and supported devices: must be selected after actual content/device review. Do not assume worldwide rights or a family rating.

Existing splash and app icon are included. Portal-specific artwork and authentic Roku screenshots still need to be checked/captured against current portal specifications. No fabricated screenshots are provided.

## Store requirements still pending
- Owner-controlled Roku developer account, applicable agreements and account access.
- Actual device/emulator results, Roku certification/static analysis and deep-link testing.
- Device-created developer signing key and signed publication package. The source ZIP is not this package.
- Store artwork, screenshots, territory/rating/accessibility decisions and privacy disclosures for the eventual advertising configuration.
- If paid advertising is later enabled: approved partner terms and tags, Roku ad-requirement review, tracking/consent validation and appropriate production break timing. Thirty-second breaks are test-only and must not ship as a paid schedule.
- Public app submission, Roku review and approval. A sideload or beta code does not constitute a public Streaming Store launch.

The app's current content is the reviewed open-content subset. There is no Echelon commercial license or 30-title commercial slate in this package.
