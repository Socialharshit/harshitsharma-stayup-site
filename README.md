# harshitsharma-stayup-site
StayUp Marketing Agency Website

The live website for StayUp Social: Home, Services, Work and DM pages.

## Layout

- `site/` is the website itself. Only this folder is published.
- `site/index.html` holds the whole site (layout, styles and scripts). It is the only page file to edit.
- `site/services.html`, `site/work.html` and `site/contact.html` are made from it by `python3 tools/build_pages.py`. Run that after every change to `index.html`. Each copy opens on its own view with its own title, description and canonical address, taken from the `#routes` block in `index.html`.
- `site/logo`, `site/services`, `site/reels`, `site/bg`, `site/clients`, `site/founder` hold the media.
- `site/vendor/three.min.js` is the 3D library, served from the site itself.
- `netlify.toml` tells Netlify to publish `site/` and sets caching and security headers.

## Publishing

Netlify deploys automatically every time `main` changes. Every deploy is kept, so any earlier version can be restored from **Netlify → Deploys → Publish deploy**.

## Domain

The site lives at https://stayupsocial.com (registered at GoDaddy). `www.stayupsocial.com` redirects there (see `netlify.toml`). The canonical link, link-preview tags, `robots.txt` and `sitemap.xml` all use this address.

## Work page

The Work page is one masonry feed (the `WORK` list in `index.html`): a sticky glass filter bar (All, Posts, Reels, Websites, Branding, Campaigns, AI), Reels that play on hover, websites that scroll on hover, columns that drift at different speeds, and a full-screen viewer.

## Search and AI visibility

- Every view has a real address: `/`, `/services`, `/work`, `/contact` (`/dm` redirects to `/contact`). Moving between views updates the address bar, title and canonical link, and Back/Forward work.
- `index.html` carries the business details (ProfessionalService with the nine services) as structured data (JSON-LD). The services list is read from the `SERVICES` array, so update both together.
- FAQ structured data is rebuilt by `tools/build_pages.py` from the visible questions: `#faq-home` for the home page and `#faq-svc` for Services. Edit the questions in the page, then run the script.
- `sitemap.xml` lists the four pages. `robots.txt` allows every crawler, including AI search crawlers.
- `llms.txt` is a plain-text summary of the business for AI assistants.
- `404.html` is shown for any address that doesn't exist.

## Performance

Every device gets the same full look (3D sky, moving gallery wall, glass). The heavy effects are built to be cheap to draw:

- The 3D sky uses dynamic resolution: on a weaker graphics chip it renders a little softer instead of dropping frames, then sharpens again. It redraws at 30 fps while nothing is moving and at 60 fps while scrolling.
- The gallery wall moves with CSS animations, which run off the main thread, and fades its centre columns with per-column opacity instead of full-screen masks.
- Glass blur radii are moderate, and the film grain uses a normal blend.
- The home hero is editorial (MotionSites style): a centred headline with a serif-italic accent word (Instrument Serif), words that blur into focus once on load, a glass pill badge and a liquid-glass button, over the moving background grid.
- Client logos glide in two rows (opposite directions) under Our Clients. Each row holds three identical sets and moves one set per loop, so it never jumps; it pauses on hover and off screen.
- Three.js loads after the page's own pictures (on the window `load` event), so content shows first on slow 4G.
- Pictures in views that are not showing never download: hero images and logos are lazy, and video posters are set only when the video nears the screen (`lazyPosters`).
- The Services grid and the Work feed reserve their height before they are built, so nothing jumps while loading.

## Contact form

The DM page sends leads to Netlify Forms (form name `contact`). Turn on **Forms → Enable form detection** in Netlify once, and add an email notification. If a send fails, the chat offers a pre-filled WhatsApp message instead.
