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

## Performance

The site adapts to each device. It starts at a quality level based on the device and connection (`perf-1` balanced for 4-thread CPUs, low-memory devices and entry phones; `perf-2` lite for slow data, data-saver or reduced motion). It then watches the real frame rate and steps down if a device drops below 40 fps. The chosen level is remembered for 3 days.

- Full: 3D sky, moving gallery wall, glass blur.
- Balanced: 3D at 1x resolution and 30 fps, still gallery wall, lighter blur, no grain.
- Lite: no 3D (Three.js is never downloaded), no blur, no gallery wall; the hero shows the logo instead.

## Contact form

The DM page sends leads to Netlify Forms (form name `contact`). Turn on **Forms → Enable form detection** in Netlify once, and add an email notification. If a send fails, the chat offers a pre-filled WhatsApp message instead.
