# aditdev.ai — creator portfolio

The link-in-bio website for [@aditdev.ai](https://www.instagram.com/aditdev.ai/) on Instagram.
One static page, Apple-style: it shows who Adit is, what he teaches, and turns a visitor into a follower.

> AI, decoded for people who ship.

No framework, no build step, no dependencies. It is one `index.html`, one photo and one icon.

---

## What is on the page

| Section | What it does |
| --- | --- |
| Top bar | Wordmark, a **Follow** button that stays on screen, and a thin blue line that shows how far you have scrolled. |
| Hero | Headline where the word "decoded" unscrambles from code symbols. A dot grid lights up around your cursor. Your photo tilts in 3D with a floating `adit@console` terminal. |
| Topic strip | Scrolling list of topics (Claude Code, RAG, MCP …). Stops when you hover over it. |
| Statement | One sentence whose words light up as you scroll. |
| How an AI reads your question | Stays in place while you scroll through 4 steps: sentence, tokens, attention lines, answer written one token at a time. |
| Why your AI forgets | Live demo: type into the box and watch the context window (the AI's "whiteboard") fill up. Old words fall off when it is full. |
| What you'll learn | Three topic cards with a cursor spotlight. |
| Start here | Three reels as dark cards that tilt in 3D. Each card opens its reel on Instagram. |
| Free guides | Four PDF guides. Tapping one opens a 3-step unlock: follow on Instagram, DM the keyword, get the PDF in DMs. |
| Comment AGENT | The 11 Claude skills for LinkedIn guide offer, linked to that reel. |
| Myth or fact? | 4-card game. Pick Myth or Fact, the card flips with the answer, a score shows at the end. |
| Trending on GitHub | The most-starred repos created in the last 7 days, AI-only or everything, refreshed daily by a GitHub Action and filtered for spam. |
| Final call | Big headline whose letters jump when you hover them, a token network that follows your cursor (tap to send a pulse), floating topic pills and the Follow button. |

### Built to Apple's design standard

- One idea per section, generous white space, one accent colour plus one yellow highlight.
- Apple's own font (SF Pro) on iPhone and Mac, Inter everywhere else.
- Light and dark mode follow the visitor's phone setting.
- Every button and link is at least 44 px tall, so it is easy to tap.
- Visible keyboard focus on every control.
- **Reduced motion:** if the visitor's phone is set to reduce motion, every animation is switched off and the page is still complete.
- Cursor effects (tilt, spotlight, magnetic buttons) run only on devices with a mouse. Phones get the clean version.
- No fake numbers or follower counts anywhere.

---

## Files

```
aditdev-creator-portfolio/
├── index.html    the whole site: content, styles (in <style>) and scripts (in <script>)
├── adit.png      profile photo used in the hero
├── favicon.svg   browser tab icon
├── guides/
│   ├── *.pdf     the four free guides (what you send in DMs)
│   ├── src/      the guides as HTML + guide.css (edit these, not the PDFs)
│   └── build.py  turns src/*.html into PDFs with Chrome
├── data/
│   └── trending.json   this week's trending repos (written by the Action)
├── scripts/
│   ├── fetch_trending.py       fetches and filters trending repos
│   └── test_fetch_trending.py  checks the spam filter
├── .github/workflows/trending.yml   runs fetch_trending.py every morning
├── .nojekyll     tells GitHub Pages to serve files as they are
├── .gitignore
└── README.md
```

---

## Run it on your computer

Any static file server works. With Python (already on this machine):

```powershell
cd "C:\Users\aditj\Downloads\Creator Target 2026\aditdev.ai-creator-portfolio"
python -m http.server 5178
```

Then open <http://localhost:5178> in your browser. Press `Ctrl+C` in the terminal to stop.

Opening `index.html` by double-clicking also works, but a server is closer to the real hosted site.

---

## How to change things

Everything lives in `index.html`. Search for the text you want to change.

| To change | Search for | Notes |
| --- | --- | --- |
| Headline | `people who` | The word inside `<span class="dec" id="dec">` is the one that scrambles. |
| Intro line under the headline | `class="lede"` | |
| Instagram link | `instagram.com/aditdev.ai` | Used on every Follow button and reel card. |
| Reel cards | `class="reel spot tilt reveal"` | Each card links to one reel. Swap the `href` and the `<h3>` text to feature a different reel. |
| Myth or fact cards | `const Q = [` | Each item: the statement `q`, the answer `a` (true = fact), and the explanation `why`. |
| Topic strip | `class="track-m"` | Edit both `<ul>` lists the same way. The second one makes the loop seamless. |
| Terminal lines | `const lines =` | The commands typed in the console on the photo. |
| Context-window demo size | `const CAP = 24` | Also update the `24` in the meter text and `aria-valuemax`. |
| AGENT offer | `class="kw"` | Keyword, title and button link. |
| Colours | `:root{` at the top of `<style>` | Light colours first, dark colours in the two blocks below it. Change both. |
| Photo | `adit.png` | Replace the file with a new one of the same name. Portrait (4:5) works best. |
| Footer | `Made by Adit` | |

After any change, refresh the browser. When you are happy, commit and push (see below).

---

## Free guides

| Guide | DM keyword | PDF link to send |
| --- | --- | --- |
| 01 Claude Code setup guide | `SETUP` | https://adit-jana.github.io/aditdev-creator-portfolio/guides/claude-code-setup.pdf |
| 02 Top 10 Claude skills for developers | `SKILLS` | https://adit-jana.github.io/aditdev-creator-portfolio/guides/top-10-dev-skills.pdf |
| 03 Claude design and motion skills | `DESIGN` | https://adit-jana.github.io/aditdev-creator-portfolio/guides/claude-design-skills.pdf |
| 04 Claude for your money | `MONEY` | https://adit-jana.github.io/aditdev-creator-portfolio/guides/claude-for-finance.pdf |

**How delivery works:** the site asks visitors to follow @aditdev.ai and DM the keyword. Reply to each keyword with
its PDF link, by hand or with a DM automation (for example an InstantDM or ManyChat keyword trigger).
The PDFs are public files, so anyone with the link can open them; the keyword step is there to earn the follow.

**Edit a guide:** change `guides/src/<name>.html` (styles in `guides/src/guide.css`), then rebuild all PDFs:

```powershell
python guides/build.py
```

The guide's text and the DM keyword live in two places on the site: the card in `index.html`
(search `class="gcard`) and the `GUIDES` list in the script.

---

## Trending repos

`.github/workflows/trending.yml` runs `scripts/fetch_trending.py` every day at 07:00 IST and commits
`data/trending.json` when it changes. GitHub Pages then redeploys. Run it by hand from the repo's
**Actions** tab → **Refresh trending repos** → **Run workflow**.

"Most starred this week" on GitHub is full of star-farmed clones and hacking tools, so a repo is listed only
if it has a readable description, a licence, real code, at least 15 forks, a sane fork and issue count, and none
of the blocked words (bypass, exploit, crack, credential, proxy …). Test the filter with:

```powershell
cd scripts; python test_fetch_trending.py
```

---

## Put it online (free, with GitHub Pages)

1. Open the repository on GitHub → **Settings** → **Pages**.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Choose branch **main** and folder **/ (root)**, then **Save**.
4. Wait 1–2 minutes. The site will be live at
   `https://adit-jana.github.io/aditdev-creator-portfolio/`

Every push to `main` updates the live site automatically.

### Use your own domain (optional, recommended)

A short domain such as `aditdev.ai` looks far better in an Instagram bio.

1. Buy the domain from any registrar.
2. In **Settings → Pages → Custom domain**, enter the domain and save. GitHub adds a `CNAME` file to the repo.
3. At your registrar, add the DNS records GitHub shows (four `A` records for the root domain, or a `CNAME` record for `www`).
4. When the domain check passes, tick **Enforce HTTPS**.

### Link preview image

When the site is live, change the `og:image` line in `index.html` to the full address of the photo, for example
`https://aditdev.ai/adit.png`. Instagram, WhatsApp and LinkedIn need the full address to show the preview picture.

---

## Add it to Instagram

1. Instagram → your profile → **Edit profile** → **Links** → **Add external link**.
2. Paste the live site address and give it a title such as `Start here`.
3. Open the link from your profile on your phone once to check it.

---

## Update the site

```powershell
cd "C:\Users\aditj\Downloads\Creator Target 2026\aditdev.ai-creator-portfolio"
git add -A
git commit -m "Describe what you changed"
git push
```

---

## Checklist before each update

- [ ] Opens without errors on phone and desktop.
- [ ] Works in light and dark mode.
- [ ] No sideways scrolling on a phone.
- [ ] Every link opens the right place.
- [ ] Any number or claim on the page is true.

---

Made by Adit · [@aditdev.ai](https://www.instagram.com/aditdev.ai/) · © 2026 All rights reserved.
