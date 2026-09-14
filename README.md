# Talisha Grobler, media kit

A one-page media kit aimed at brand reps. Plain HTML, CSS and JavaScript,
with no build step, no dependencies, no framework. Open it and it works.

```bash
# any of these
open index.html                 # straight from Finder
python3 -m http.server 8080     # then http://localhost:8080
npx serve .
```

Deploy by dragging the folder onto Netlify, Vercel, Cloudflare Pages or
GitHub Pages. There's nothing to compile.

```
index.html    all the markup and copy
styles.css    all the styling, the accent colour lives at the very top
script.js     nav, scroll reveal, form validation, Formspree submit
assets/       drop photos, logos and video thumbnails here
```

---

## 1. Wire up the form (do this first, 2 minutes)

Submissions go to **management@talishagrobler.com** through
[Formspree](https://formspree.io). Free tier is 50 submissions a month,
which is plenty.

1. Go to **https://formspree.io** and click **Sign up**.
2. Register with **management@talishagrobler.com**, which is the inbox the
   inquiries land in, so it has to be this address.
3. Once you're in: **+ New Project** → name it anything → **+ New Form**.
   Call the form *Talisha, Partnership Inquiries*.
4. Formspree shows you an endpoint that looks like this:

   ```
   https://formspree.io/f/mabcdefg
   ```

   The part after `/f/`, in this case `mabcdefg`, is your **form ID**.
5. Open `index.html` and go to **line 422**, the `<form>` tag in the contact
   section. Replace `YOUR_FORM_ID` with your ID:

   ```html
   <form id="inquiryForm" action="https://formspree.io/f/mabcdefg" method="POST" novalidate>
   ```
6. Save, reload the page, and **send yourself one test inquiry**. Formspree
   emails a one-time confirmation link the very first time, so click it or
   nothing after that gets delivered.

Until step 5 is done the form validates normally but shows an amber
*"Form not connected yet"* note instead of pretending to send. That's
deliberate: no silent failures, no fake success screen.

If a submission fails after it's connected, the visitor sees either
Formspree's own reason (quota used up, form deactivated) or a fallback that
points them at the email address. A dropped connection never surfaces a raw
browser error.

**Worth knowing**

- The `_subject` hidden field sets the subject line in the inbox. Change the
  wording there if you like.
- `_gotcha` is a honeypot: bots fill it in, humans never see it, and Formspree
  bins those. Leave it alone.
- Formspree's dashboard keeps every submission, so nothing is lost even if an
  email goes astray.

---

## 2. Swap in the real content

Everything replaceable is marked with a comment in `index.html`. Search for
`TODO` to find them all at once.

### What still needs you

1. **Formspree ID** (section 1 above). The form is dead until this is in.
2. **Three logo files**: Juce, Cotton On, Brutal Fruit.

That's it. Every photo, figure and link on the page is real.

Nothing else is outstanding. The analytics, charts and downloadable PDF are
all in and filled with real figures.

Everything else is in. Search `TODO` in `index.html` to jump between them.

---

### Photos: done

| File | What it is | Where it shows |
|---|---|---|
| `assets/hero.jpg` | balcony shot | hero, 4:5 |
| `assets/about.jpg` | beach shot | About section, 4:5 |
| `assets/contact.jpg` | street shot | Work with me, beside the form, 4:5 |


All three were cropped from the HEIC originals. The beach one is anchored a
little above centre to keep sky above her; the street one is anchored low,
which trims the houses at the top and keeps her whole crouch including the
boot. The original is 9:16 and the slot is 4:5, so something had to go;
keeping her complete beat keeping headroom.

The street photo sits in the **Work with me** section, in the empty half of
the column beside the form. It's hidden below 880px on purpose, so on a phone
nothing gets between the copy and the form.

All three slots are self-activating: saving a file at the right path is all
it takes, there is no HTML to edit and no CSS to write. Around 1600px on the
long edge, run through [squoosh.app](https://squoosh.app), under 300KB.

**How the slots work.** Each holds the real `<img>` plus a grey placeholder.
The placeholder is hidden by default, so the moment the file exists the photo
shows. If the file is missing the `<img>` fires `onerror`, removes itself and
flips the slot to `.no-photo`, revealing the placeholder. Either way the
layout holds and you never see a broken image icon. Both directions were
tested.

**A note for next time:** a photo attached to a chat message never lands on
disk, so it can't be read from there. Saving it as a real file first, as you
did with the HEICs, is what makes it usable. HEIC is fine, it gets converted.

### Phone mockups: done

Both frames carry her real profile screenshots, `assets/phone-instagram.jpg`
and `assets/phone-tiktok.jpg`. The iOS status bar was trimmed off the top of
each so the real clock and battery don't sit above the frame's own dynamic
island. Both are clickable and open the profiles.

To refresh them later, drop new screenshots in under the same names, same
crop rule: trim the status bar, keep roughly 9:19.5.

The `aspect-ratio` sits on `.phone-screen`, not on `.phone-shell`. That
matters: with it on the shell, the bezel padding came off both dimensions and
left the screen at 2.239 while the screenshots are 2.167, so
`object-fit:cover` quietly shaved a few pixels off each side of every
screenshot. Keep the ratio on the screen and the shell will size around it.

### Analytics: done

Two parts now. **Six headline tiles plus the two phone mockups**, and below
them **five charts** breaking the audience down properly.

Headline tiles, and where each comes from:

| Shown | Source |
|---|---|
| 79.1K Instagram followers | her profile |
| 323.6K TikTok followers | her profile |
| 12M views | 6.4M TikTok post views + 5.63M Instagram |
| 654K interactions | TikTok 536.2K likes + 1.8K comments + 10.8K shares, plus Instagram's 105.1K |
| 80% aged 18 to 34 | 77.4% Instagram, 83.4% TikTok |
| 75% South African | Instagram top locations |

**Three charts on the page**, laid out like the Instagram and TikTok
analytics screens, show first and read second:

| Chart | Form |
|---|---|
| Gender | semicircle gauge per platform, figure in the opening |
| Age range | bar list per platform, 13-17 through 55+ |
| Views by format | Instagram, Stories / Posts / Reels |

**Two more live only in the PDF**: follower locations and traffic source.
That's deliberate, it gives the download something to be for, and the CTA on
the page says so.

**Editing a figure is a one-number change.** Bars read their length from an
inline `style="--v:NN"`, a percentage of the track. The gauges are a single
SVG arc each, where `stroke-dasharray` sets how far the coloured part travels
round the semicircle (the path is `pi x 78 = 245` units long, so 61.8% is
`245 x 0.618`, minus 3 for the gap). Search `AUDIENCE CHARTS` in
`index.html`.

**After any change, re-run `python3 scripts/build-pdf.py`** so the downloadable
PDF still matches. The two are not linked.

**Two honesty notes are built into the charts.** TikTok's report starts at 18,
so its 13-17 row is an empty track reading `n/a`, with no bar element at all,
rather than a zero-width bar that could be mistaken for a real zero.
Instagram's 55-64 and 65+ are added together to line up with TikTok's single
55+ bracket. In the PDF, the locations chart shows each platform's own top
five rather than merging them, because the fifth country differs (Namibia on
Instagram, Canada on TikTok) and merging would have meant inventing a figure.

**Colours.** Instagram is the site pink `#FF2D6F`, TikTok a blue `#2A78D6`.
That pair was checked for colour-blind separation rather than picked by eye
(protanopia/deuteranopia deltaE 16.1 against a target of 8). Every value is
also printed next to its mark, so colour is never the only cue.

### The downloadable PDF

The **Download my analytics** button serves
`assets/talisha-grobler-media-kit.pdf`, a one page A4 sheet with the same
figures laid out for print.

**It carries the three charts from the page**, gauges included, in the same
colours and order, **plus two the page doesn't show**: top locations and
traffic source per platform. So the download is worth clicking rather than
being a copy of what they just read.

It's a real vector PDF, around 6KB, text stays sharp at any zoom and can be
selected and copied. Not a screenshot. The gauges are drawn as real bezier
arcs, so they stay crisp in print too.

**To regenerate it** after changing any number:

```bash
python3 scripts/build-pdf.py
```

All the figures live in the `DATA` block at the top of that script. Change
them there, re-run, and remember to change the matching numbers in
`index.html` too, the two are not linked.

The script has no dependencies. It writes the PDF by hand using the built-in
Helvetica fonts, so there is nothing to `pip install` and it will still run on
a machine years from now. There is an assertion in it that fails the build if
the footer note ever grows long enough to collide with the email address.

### Things a brand rep may ask

Over this period TikTok post views were **down 37.4%** against the previous
window, and Instagram net followers were **-1,281**. Nothing on the site
claims otherwise, it shows current reach rather than trend, but don't get
caught out by the question.

Instagram's audience is **11.1% aged 13-17**. That is on the age chart now,
openly. Alcohol brands ask about under-18 share directly, and Brutal Fruit is
on the logo strip.

### Brand logos: 7 of 10 done

The brand strip is a marquee: it scrolls right to left, edge to edge, and
pauses when you hover it.

**Seven are real logo files**, in `assets/logos/`:

| File | Source |
|---|---|
| `garnier.svg` | Wikimedia Commons, *Garnier wordmark.svg* |
| `redken.svg` | Wikimedia Commons, *Redken logo.svg* |
| `bereal.svg` | Wikimedia Commons, *BeReal-Logo-Wide.svg* |
| `lancome.svg` | Wikimedia Commons, *Lancôme logo.svg* |
| `edgars.png` | Wikimedia Commons, *Edgars (department store) logo.png* |
| `hisense.svg` | Wikimedia Commons, *Hisense logo.svg* |
| `nivea.svg` | Wikimedia Commons, *NIVEA logo 2021.svg* |

Each was opened and checked against the right brand before going in. Edgars
is the South African department store, and Lancôme is the *Paris* wordmark
rather than the Faubourg Saint-Honoré variant. Every SVG was also scanned for
embedded scripts and external entities; all clean.

**Three are still set in type**, *Juce*, *Cotton On* and *Brutal Fruit*,
because Commons has no usable file for them. To finish those, get an SVG or
transparent PNG (the brand's own press or media page is usually the best
source) into `assets/logos/` and swap the `<span>` for an `<img>`, exactly
like the others:

```html
<li class="marquee-item"><img src="assets/logos/cotton-on.svg" alt="Cotton On" /></li>
```

They're marked `TODO` in the markup. Logos render greyscale and come to full
colour on hover, which keeps a mixed set of brand colours reading as one
strip. **The strip does not stop when you hover it**, it keeps scrolling; only
the individual cell you're over responds. A keyboard user tabbing into the
strip does pause it, so the focused item doesn't slide out from under them.

**You only edit one list.** Search for `BRAND MARQUEE` and you'll find a
single `<ul>`. `script.js` clones it as many times as it takes to fill the
screen, two copies on a laptop and six on an ultrawide, so there are never
duplicate lists to keep in sync, and no empty gap at the loop point on a big
monitor. Add or remove brands freely.

Speed is one line in `styles.css`:

```css
--marquee-speed: 42s;   /* time for one pass of the row. Lower = faster. */
```

That's the time for *one row* to travel past, and the duration scales with the
number of clones, so the actual scroll speed stays identical whether someone
is on a phone or a 34" monitor, and adding brands doesn't slow it down.

With JavaScript off the row simply sits still. Still readable, just not
moving.

*A note on logo cell sizing:* `.marquee-item` sets a **definite** `width`, not
`min-width`. That matters, because with `flex:none` and only a min-width the cell has
no resolvable width, so a logo's intrinsic size (Garnier's SVG is 1962px wide)
drives the layout and the image blows straight out of its cell. If you restyle
this, keep the definite width and the absolute `max-height` on the `img`.

### TikTok videos: done

All six links are live and verified, and **the thumbnails came straight from
TikTok** rather than from screenshots. TikTok's public oEmbed endpoint hands
back the cover image for any public video, so there was nothing to screenshot.

| Card | Brand |
|---|---|
| 1 | Hisense |
| 2 | Nails by Kriston |
| 3 | Nivea |
| 4 | Garnier |
| 5 | Darry Ring |
| 6 | CellConnect ZA |

Note card 5 is **Darry Ring**, spelled with the double R. TikTok's own caption
credits `@DarryRing_official`.

Links use canonical `tiktok.com/@talishagrobler/video/<id>` URLs rather than
the `vt.tiktok.com` short links: permanent, one less redirect, and no share
tokens sitting in a public page.

**If you swap a video out**, edit `VIDS` in `scripts/fetch-thumbnails.py` and
run it:

```bash
python3 scripts/fetch-thumbnails.py
```

It refetches every cover image into `assets/videos/`. The thumbnail URLs
TikTok returns are signed and expire, which is why the script downloads the
files rather than linking to them. Then update the `href` and `<h3>` on that
card in `index.html`.

Want view counts under the titles? Change the `<p>` to:

```html
<p><span class="views">330K views</span> · Watch on TikTok</p>
```

The `.views` style, accent colour and semibold, is already there.

**On embeds:** you can paste TikTok's official embed code instead (Share →
Embed, plus `<script async src="https://www.tiktok.com/embed.js"></script>`
before `</body>`), and the comment in the code shows how. But six live players
pull in several megabytes of TikTok's JavaScript and visibly slow the page. A
brand rep opening this on their phone between meetings will notice. The
thumbnails link out and load instantly.

### Salt Studio: parked until launch

The whole Salt Studio section is **off the live page** for now, along with
every mention of it: the nav link, the hero strapline, the footer pill and
link, the meta descriptions, and the subtitle on the PDF.

Nothing was thrown away. The section is kept whole in
**`disabled/salt-studio-section.html`**, with a numbered list at the top of
that file covering all five places to touch when it launches. Its CSS was
deliberately left in `styles.css`, so there is nothing to restore there.

One thing to check before it goes back up: `saltstudio.co.za` needs to
actually resolve.

### Social links: done

Both handles are wired up throughout: **@talishagrobler** on TikTok and
**@talisha.grobler** on Instagram. They appear on the two phone mockups, the
two follower cards, the footer icons, and the *"The rest are over on TikTok"*
link under the videos.

These use clean canonical URLs, deliberately, rather than the share links with
`?_r=1&_t=...` or `?stkn=...` on them. Those carry share/session tokens that
have no business on a public page, and they can expire.

## 3. Copy

The copy is a real first draft in her voice, not filler, and it can ship as is.
Things you might want to change:

- **Tagline.** Four options are in an HTML comment right above the hero
  `<p class="lede">`. Option A is live; swap in another by moving it.
- **About paragraphs.** Marked `ABOUT COPY`. This is Talisha's own wording,
  only lightly tidied, so change it carefully. The turned-down-offers line and
  the "AI and fake stories" close are the two that do the most work; a brand
  rep reading this is deciding whether her recommendations carry weight.

  The three bullets underneath are hers too: creative freedom but can follow a
  brief, quick and open communication, and the range of work she covers.
  There used to be a fourth about exclusivity, usage rights and whitelisting.
  It was dropped to keep to the three, but it's genuinely useful to a brand
  rep, so add it back as a fourth `<li>` if you want it:

  ```html
  <li>Happy to sort out exclusivity, usage rights or whitelisting, just ask.</li>
  ```
- **Pricing line.** In the contact section: *"Every brand's different, so
  every quote is too."* Deliberately no rate card.
- **The small-brands note**, under the brand marquee, the "you don't need a
  big budget" message about local pricing for upcoming brands. Search for
  `SMALL BRANDS NOTE`.

One spelling note: the site uses UK/SA spelling throughout (*colour*,
*favourite*) except the videos heading, which is *"Some of my favorite
partnership videos :)"* exactly as asked. If you'd rather it matched, that's
the one word to change.

---

## Design notes

One accent colour, used sparingly: buttons, the hero underline, stat units,
list markers, social hovers. Everything else is neutral. It's defined once at
the top of `styles.css`:

```css
--accent: #FF2D6F;  /* change this and the whole site follows */
```

Mobile-first throughout; the layout is built for a phone and widens up.
Reduced-motion preferences are respected, and the form is keyboard-navigable
with proper labels and `aria-invalid` on failed fields.

If JavaScript doesn't load, the page still works: the reveal animations simply
don't run, the browser's own `required` / email validation takes over, and the
form posts to Formspree the normal way, so you'd get Formspree's own thank-you
page instead of the built-in success card. (`novalidate` is set from
`script.js` rather than in the markup precisely so this fallback survives.)


---

## Motion

The page has a light motion layer: reveals as sections come up, a hero photo
that drifts a little slower than the scroll, counters that tick up the first
time the stat tiles are seen, charts that draw themselves in, a scroll
progress hairline under the header, nav links that follow the section you're
reading, buttons that lean slightly toward the cursor, and and a soft pink glow
that follows the pointer inside the analytics cards.

**It is built to fail safe.** Everything that starts hidden or shrunk is gated
behind a `.js-motion` class that `script.js` puts on `<html>` as it runs. With
JavaScript off, or if the script throws before that line, the page renders
complete and static rather than blank. There are two further nets: any reveal
target that has scrolled into view gets revealed on scroll whether or not the
IntersectionObserver fired, and the charts draw themselves after 2.5 seconds
regardless. The worst case is "no animation", never "invisible content".

**The glow is contained to the analytics bubbles.** It lives inside each of
the six stat tiles and the three chart cards, clipped to the card it belongs
to, and it exists nowhere else on the page. The pseudo-element sits in the
card's own stacking context at `z-index:-1`, which paints it above the card's
background but below its content, so it can never wash over text or catch a
click.

The scope is one selector in `script.js`: `#stats .stat, #stats .chart-card`.

`prefers-reduced-motion: reduce` turns all of it off, and the pointer effects
only attach on devices with a real pointer.

**What could not be tested here.** The browser available during this build
runs neither `requestAnimationFrame` nor `IntersectionObserver` reliably, so
most of the scroll-triggered pieces could not be exercised in place. The
counters were the exception and are confirmed working: they were caught
mid-count in a render and then settled on exactly the right values. What was verified
instead: no console errors, correct end states once the classes are applied,
the no-JS fallback, the reveal and chart nets (by stubbing rAF in a harness),
and the counter itself, which was extracted from `script.js` and run in Node
against every value on the page (counts up, keeps decimal places, never
overshoots, lands exactly on the original string). **Worth an eyeball in a
real browser** to judge whether the timings feel right, they are a taste call
and easy to tune: reveal duration in the `.reveal` transition, counter
duration in the `DUR` constant, parallax strength in the `0.075` multiplier.

## Caching

`index.html` loads `styles.css?v=9` and `script.js?v=9`. **Bump that number
whenever you edit either file.** Without it browsers happily serve a stale
copy, which during this build produced a page that looked broken, photos
without their rounded corners sitting above placeholders that should have
been hidden, purely because the old CSS was still cached.
