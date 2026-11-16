# Shuttlebug

Free red-and-black streaming web app at https://shuttlebug.onrender.com, maintained in Reggie720/shuttlebug. Static HTML/CSS/JS; no Base44, database, subscriptions, API keys, or new hosting resources required.

## Included

- Home, Movies, TV short series, Originals, My List, Settings; search and genre filters.
- Three complete open films: Big Buck Bunny, Elephants Dream, Sintel. Two Caminandes episodes under TV. Original “From the Block to the Beach” remains in production until a finished video is supplied.
- Official Blender-hosted H.264/AAC MP4 streams, selectable 360/480/720p, source fallback, seek, restart, fullscreen, device-local resume, episode-next action and watchlist backup export.
- Film-specific attribution, license deed and publisher links. Original film credits remain intact. Poster thumbnails come from the official publisher; their display is scaled and cropped to fit cards. No endorsement is implied.
- Installable web app: manifest, PNG/maskable/Apple icons, Android install prompt and iOS instructions. Offline navigation shell; videos require internet. Defaults to Home on launch.
- TV layout, visible focus, directional remote/keyboard navigation and Back/Escape handling. Native Remote Playback/AirPlay picker when supported; screen mirroring/HDMI help otherwise.
- Direct sponsor placement and optional AdSense display ad adapter with consent/configuration gates. No ads or tracking scripts run in the default configuration.

## Advertising activation

`config.js` is PUBLIC. Never enter secrets. A sponsor needs an approved name, message and HTTPS destination. Configure `sponsor` to display a labeled link; this does not bill or collect payment.

For AdSense, obtain account/site approval and a real publisher ID and responsive display slot. Complete the provider's required consent/CMP and regional setup first, then populate `adsense`, set `consentReady: true` and enable. The adapter requests ads only if the visitor allows optional ads. The local toggle is not a certified CMP. Add the exact provider-issued ads.txt record if required; do not invent seller IDs. This is a display ad integration, not video pre-roll/VAST. No ad revenue is active until a provider/sponsor is approved and configured. No purchases or paid accounts have been created.

Reference: https://support.google.com/adsense/answer/9183460

## Content permissions

`catalog.js` records exact license versions, credit, publisher, sources and permission links. Caminandes 2's official closing card (about 142s) states CC BY 3.0; Caminandes 3's closing card (about 147s) states CC BY 4.0. Their older mirror copies may differ. Use the rights of the exact film copy being served. Elephants Dream attribution includes Netherlands Media Art Institute.

`python3 tools/refresh-catalog.py` refreshes only the manually curated official publisher IDs. Review changed stream URLs, license records, creator credits and closing cards before publishing the result. Some legacy publisher API license fields are empty; the film-specific permission page and closing card are authoritative. Never add commercial titles or live feeds without documented streaming rights, territories and term. Current open films are globally licensed under the linked CC deeds; media delivery remains a third-party dependency.

## Testing

Install development tools with `npm install`, then run `npm test`. No build step is needed for hosting. Tests cover DOM behavior, storage, catalog contracts, manifest, ad consent and sponsor gates. DOM tests simulate media APIs and do not prove browser playback.

For a full browser check, serve this folder with `npm run serve`, then run `npm run test:browser` in a second terminal. `tests/smoke.cjs` uses Chromium at `/usr/bin/chromium` by default; override `CHROMIUM_PATH` for a different installation. `TEST_URL` can target the live site. It checks real playback, desktop/phone layout, remote focus, saved data, install assets and offline navigation. Real TV receivers and physical phone installation require device testing.

Pre-release verification on 2026-11-15: JS syntax and DOM test suite passed; all five official 360p files downloaded, ffprobe confirmed H.264 video plus AAC audio and full durations, and sample frames/audio decoded with ffmpeg. Full local Chromium execution was unavailable in the agent test environment; live UI testing follows deployment. These checks do not certify all smart TVs or ad-network approval.

## Deployment and cost

Keep the existing Render static site's GitHub auto-deploy settings. Serve the repository root; no runtime service or build is needed. All production files are committed together. Keep config.js network-only so withdrawn ads aren't retained offline; the service worker caches only the app shell, never films or ads. Update the cache version in sw.js when changing shell assets. Publisher media is streamed directly, avoiding video storage on the existing host. No usage-limit or third-party availability guarantees are made.

Native Roku, Fire TV, Android TV and Apple TV store packages, full-length licensed television/live channels, finished Shuttlebug Originals, ad account approval and revenue are not included in this web release.
