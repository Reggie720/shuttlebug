// Public configuration only. Never put credentials or private keys in this file.
window.SHUTTLEBUG_CONFIG = {
  featuredId: 'spring',
  startHere: ['spring', 'valkaama', 'bbs1', 'pepper6', 'cosmos', 'sintel'],
  seriesOrder: ['BBS: The Documentary', 'Pepper & Carrot', 'Caminandes'],
  // Owner's standing requirement. New titles must be reviewed before publication.
  audioPolicy: 'Original recorded performances or no dialogue. No robotic-sounding voices, synthetic narration, or artificial dubs.',
  // Activate only after a real sponsor approves their creative and destination.
  sponsor: null, // {name: 'Sponsor name', message: 'Approved message', url: 'https://…'}
  // Optional display ads; not video pre-roll. Keep disabled until approved by AdSense
  // and the site's required regional consent/CMP setup is complete.
  adsense: { enabled: false, publisher: '', slot: '', consentReady: false }
};
