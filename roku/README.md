# Shuttlebug Roku

A Hog Entertainment · Developer build 0.3.0 · Public store approval pending.

The existing SceneGraph application now uses a featured artwork banner and horizontal poster shelves. It retains the same live rights gate, native film playback, optional unpaid test ads, search, favorites and device registry bookmarks. Website code is unchanged.

## Home and catalog

Only the live-cleared intersection of `catalog.js` and `compliance/rights-register.json` is displayed. Populated shelves include Featured Movies, Newly Added Movies, genre rows, TV Shows, Documentary Episodes, Continue Watching, My Favorites and Recently Watched. Empty shelves are omitted. There is no Popular ranking because aggregate viewing data is not available. Featured currently means the available movie selection, not a claim of popularity. Newly Added sorts by existing catalog `added` dates; missing dates are excluded from that shelf. New licensed catalog entries are included at the next package build, not downloaded silently at runtime.

TV Shows opens Series > Season > Episodes. Missing season metadata is honestly labeled “Episodes (season unspecified).” Episode numbers, artwork, descriptions and runtimes come from the existing catalog. Search includes series names. Poster cards, featured previews and title details show available release year, genre and runtime. Ratings are displayed only when explicitly marked verified; missing ratings are omitted. Missing artwork uses a branded fallback.

Continue Watching uses saved resume positions. Recently Watched uses a bounded local history recorded only when the native player reports playing. These rows and favorites are filtered against currently cleared titles. Existing favorites and progress registry keys are preserved. New history stays on the Roku; it is not advertising analytics.

## Remote

Arrows navigate the sidebar and horizontal rows; OK opens details or series folders. Back returns through episode/season/series levels, then navigation, then exits from the root. Star toggles favorites for playable cards. Search uses the Roku keyboard. Native Video retains Play/Pause, seeking, subtitles and Back handling. Test ads remain OFF by default, explicitly unpaid and separate from paid demand. Back skips test previews; completion, error and a 12-second watchdog clear the ad. Decoder handoff timeout returns to details rather than leaving an ad overlay.

## Build

From the repository root:

```sh
npm ci --ignore-scripts --prefix roku
npm run build --prefix roku
npm test --prefix roku
```

Output: `roku/packages/Shuttlebug_Roku_Developer.zip`, with SHA-256 in `roku/packages/SHA256SUMS`. Install this ZIP as-is; do not unzip or upload the whole repository.

## Install on your existing developer-mode Roku

1. Connect your Chromebook and Roku to the same Wi-Fi or phone hotspot.
2. Download the developer ZIP to the Chromebook.
3. Open `http://ROKU_IP` in Chrome, using the Roku IP in Settings > Network > About.
4. Sign into the developer installer as `rokudev` with your existing developer password.
5. Choose Upload, select the ZIP, then Install or Replace. Launch Shuttlebug if it does not open automatically.

The installer must be on the same local network. This is a developer installation, not a public Roku Store release. A developer channel slot holds one app. Avoid deleting the channel or resetting your device if you want to preserve local settings.

## Artwork and submission

`images/` contains the branded app tile, splash and ladybug; `store/` contains FHD/HD/SD poster exports and a 1920×1080 brand image. These are original Shuttlebug artwork prepared for submission, not certification approval. Actual app screenshots must be captured from the installed Roku build; a brand image is not a screenshot. Store listing requirements, signing, device validation and Roku approval remain separate steps.

See VALIDATION.md and DEVICE_TESTS.md for the test limits.
