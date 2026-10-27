# harshitsharma-stayup-site
StayUp Marketing Agency Website

The live website for StayUp Social: Home, Services, Work and DM pages.

## Layout

- `site/` is the website itself. Only this folder is published.
- `site/index.html` holds the whole site (layout, styles and scripts).
- `site/logo`, `site/services`, `site/reels`, `site/bg`, `site/clients`, `site/founder` hold the media.
- `site/vendor/three.min.js` is the 3D library, served from the site itself.
- `netlify.toml` tells Netlify to publish `site/` and sets caching and security headers.

## Publishing

Netlify deploys automatically every time `main` changes. Every deploy is kept, so any earlier version can be restored from **Netlify → Deploys → Publish deploy**.

## Domain

The site lives at https://stayupsocial.com (registered at GoDaddy). `www.stayupsocial.com` redirects there (see `netlify.toml`). The canonical link, link-preview tags, `robots.txt` and `sitemap.xml` all use this address.

## Performance

Every device gets the same full look (3D sky, moving gallery wall, glass). The heavy effects are built to be cheap to draw:

- The 3D sky uses dynamic resolution: on a weaker graphics chip it renders a little softer instead of dropping frames, then sharpens again. It redraws at 30 fps while nothing is moving and at 60 fps while scrolling.
- The gallery wall moves with CSS animations, which run off the main thread, and fades its centre columns with per-column opacity instead of full-screen masks.
- Glass blur radii are moderate, and the film grain uses a normal blend.
- Three.js loads after the page and the images load lazily, so the first screen appears quickly on 4G.

## Contact form

The DM page sends leads to Netlify Forms (form name `contact`). Turn on **Forms → Enable form detection** in Netlify once, and add an email notification. If a send fails, the chat offers a pre-filled WhatsApp message instead.
