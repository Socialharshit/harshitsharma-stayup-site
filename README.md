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

## Before launch

Replace `YOUR-DOMAIN.com` with the real domain in `site/index.html`, `site/robots.txt` and `site/sitemap.xml`.

## Contact form

The DM page sends leads to Netlify Forms (form name `contact`). Turn on **Forms → Enable form detection** in Netlify once, and add an email notification. If a send fails, the chat offers a pre-filled WhatsApp message instead.
