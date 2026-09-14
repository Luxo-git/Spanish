# 🇪🇸 Spanish Conjugation Trainer — Mobile App (PWA)

This is a **Progressive Web App**: a website that installs on your phone's
home screen and behaves like a real app — full-screen icon, no browser
address bar, and it keeps working **offline** after the first load.

There's no Apple/Google developer account, no App Store review, and no
`.apk`/`.ipa` file involved — you just need to put these files online
somewhere, then "install" the page from your phone's browser.

## Folder contents

| File / folder            | Purpose                                             |
|---------------------------|------------------------------------------------------|
| `index.html`               | The app's single page                                |
| `style.css`                 | Nature theme (khaki green / brown), mobile layout     |
| `app.js`                    | All the game/course/translation logic                 |
| `manifest.json`             | Tells the phone how to install the app (name, icons)  |
| `service-worker.js`         | Caches the app so it works offline                     |
| `icons/`                    | App icons (192px, 512px, maskable, Apple touch icon)  |

## Step 1 — Put the files online

"Add to Home Screen" and offline support both require the site to be
served over **HTTPS** (or `localhost` for local testing) — opening
`index.html` directly from a file browser on your phone will show the
page, but won't offer a proper install prompt or offline caching.

The easiest free options, roughly ordered from simplest to most durable:

- **GitHub Pages** (free, permanent, needs a GitHub account):
  1. Create a new GitHub repository and upload all the files in this
     folder (keeping the `icons/` subfolder).
  2. In the repo settings → Pages, set the source to the `main` branch.
  3. GitHub gives you a URL like `https://yourname.github.io/your-repo/`.

- **Netlify Drop** (free, no account needed for a quick test):
  1. Go to [app.netlify.com/drop](https://app.netlify.com/drop).
  2. Drag and drop this whole folder onto the page.
  3. You instantly get a public HTTPS URL.

- **Vercel** or **Cloudflare Pages** work the same way if you prefer them.

## Step 2 — Install it on your phone

### iPhone / iPad (Safari)
1. Open the site's URL in **Safari** (must be Safari, not Chrome, for
   the install option to appear on iOS).
2. Tap the **Share** icon (square with an arrow).
3. Tap **Add to Home Screen**.
4. The app icon appears on your home screen, and opens full-screen.

### Android (Chrome)
1. Open the site's URL in **Chrome**.
2. Tap the **⋮** menu (top right).
3. Tap **Add to Home screen** / **Install app**.
4. Confirm — the app icon appears on your home screen and app drawer.

## That's it!

Once installed, tap the icon like any other app. The Conjugation Game,
Course, and Translation sections all work exactly like the desktop
version, adapted for touch and small screens. After the first visit,
it keeps working even with no internet connection.

## Updating the app later

If you change any file and re-upload it, phones that already installed
the app will pick up the update automatically the next time they open
it with an internet connection (the service worker checks for a newer
version in the background).
