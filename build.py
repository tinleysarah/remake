#!/usr/bin/env python3
"""Generate the static site.

Run:  python3 build.py
Writes plain .html files next to this script (and into recipes/), so the folder
can be served as-is by any static host, including GitHub Pages.

All copy here is placeholder text written for this remake. Change SITE_NAME,
the prices and the wording to make it yours.
"""
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))

SITE_NAME = "Wellness Studio"
COACH_NAME = "Your Name"
TAGLINE = "Nutrition and wellness coaching, built around real life."

NAV = [
    ("About", "about.html"),
    ("Services", "services.html"),
    ("Coaching", "coaching.html"),
    ("Recipes", [("Seasonal recipes", "seasonal-recipes.html"), ("Meal plans", "meal-plans.html")]),
    ("Contact", "contact.html"),
]

SOCIAL_ICONS = {
    "Instagram": '<rect x="3.5" y="3.5" width="17" height="17" rx="4.5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="17" cy="7" r="1.1"/>',
    "Facebook": '<path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H8v3h2.5V21z"/>',
    "YouTube": '<path fill-rule="evenodd" d="M6 6h12a3.5 3.5 0 0 1 3.5 3.5v5A3.5 3.5 0 0 1 18 18H6a3.5 3.5 0 0 1-3.5-3.5v-5A3.5 3.5 0 0 1 6 6zm4 3.3v5.4l4.8-2.7z"/>',
}

RECIPES = [
    {
        "slug": "oat-honey-face-mask",
        "title": "Oat and honey face mask",
        "tone": "sage",
        "season": "Winter",
        "meta": "Makes 1 mask · 5 minutes",
        "intro": "Not everything from the kitchen needs to be eaten. This two-minute mask is a gentle way to end a long week, using things you probably already have in the cupboard.",
        "ingredients": ["2 tablespoons fine rolled oats", "1 tablespoon runny honey", "1 tablespoon plain yogurt", "A few drops of warm water"],
        "method": ["Blitz or crush the oats until they are roughly the texture of coarse flour.", "Stir in the honey and yogurt, loosening with warm water until spreadable.", "Smooth over clean skin, avoiding the eyes, and leave for ten minutes.", "Rinse with lukewarm water and pat dry. Patch-test first if your skin is sensitive."],
    },
    {
        "slug": "salmon-grain-bowl",
        "title": "Salmon and greens grain bowl",
        "tone": "clay",
        "season": "Spring",
        "meta": "Serves 2 · 25 minutes",
        "intro": "A weeknight bowl that covers protein, whole grains and plenty of greens without much washing-up. Swap the salmon for baked tofu if you prefer.",
        "ingredients": ["2 salmon fillets", "150 g brown rice or farro", "2 large handfuls of spinach or kale", "Half a cucumber, sliced", "1 tablespoon soy sauce or tamari", "1 teaspoon sesame oil", "Juice of half a lemon", "Toasted sesame seeds, to finish"],
        "method": ["Cook the grains according to the packet and keep warm.", "Season the salmon and roast at 200°C (400°F) for 12 minutes, until it flakes easily.", "Wilt the greens in a hot pan with a splash of water.", "Whisk the soy sauce, sesame oil and lemon juice into a quick dressing.", "Divide the grains between two bowls, top with greens, cucumber and salmon, then spoon over the dressing and scatter with sesame seeds."],
    },
    {
        "slug": "berry-yogurt-bowl",
        "title": "Berry yogurt breakfast bowl",
        "tone": "stone",
        "season": "Summer",
        "meta": "Serves 1 · 5 minutes",
        "intro": "A breakfast that takes less time than waiting for toast. The mix of protein, fibre and fruit keeps energy steady through the morning.",
        "ingredients": ["200 g thick plain yogurt", "A generous handful of mixed berries", "2 tablespoons oats or low-sugar granola", "1 tablespoon chopped nuts or seeds", "A drizzle of honey, optional"],
        "method": ["Spoon the yogurt into a bowl.", "Top with the berries, oats and nuts.", "Add honey if you like things sweeter, and eat straight away."],
    },
    {
        "slug": "smashed-avocado-toast",
        "title": "Smashed avocado toast",
        "tone": "moss",
        "season": "Summer",
        "meta": "Serves 1 · 10 minutes",
        "intro": "A classic for good reason. Good bread, a ripe avocado and enough acid and salt to wake everything up.",
        "ingredients": ["1 thick slice of sourdough or seeded bread", "Half a ripe avocado", "A squeeze of lime or lemon", "A pinch of chilli flakes", "Flaky salt and black pepper", "1 soft-boiled or poached egg, optional"],
        "method": ["Toast the bread until properly crisp.", "Roughly mash the avocado with the citrus juice, salt and pepper.", "Pile onto the toast, add the chilli flakes, and top with the egg if using."],
    },
    {
        "slug": "ginger-lime-fizz",
        "title": "Ginger lime fizz",
        "tone": "sage",
        "season": "Autumn",
        "meta": "Makes 4 glasses · 15 minutes plus cooling",
        "intro": "A homemade alternative to shop-bought soft drinks, with far less sugar and a proper ginger kick.",
        "ingredients": ["A thumb-sized piece of fresh ginger, sliced", "2 tablespoons honey or maple syrup", "250 ml water", "Juice of 2 limes", "Sparkling water and ice, to serve"],
        "method": ["Simmer the ginger, honey and water gently for ten minutes, then leave to cool.", "Strain the syrup and stir in the lime juice.", "Pour a little syrup over ice and top up with sparkling water, adjusting to taste."],
    },
]


# ---------------------------------------------------------------- helpers

def ph(label, ratio="4 / 3", tone="moss", seed=0):
    """Tonal placeholder artwork that stands in for a photograph."""
    s = seed * 37
    cx = 20 + (s % 55)
    cy = 22 + ((s * 3) % 50)
    rot = (s * 7) % 360
    lx = 30 + ((s * 5) % 40)
    ly = 45 + ((s * 11) % 30)
    return (
        '<div class="ph ph-{tone}" style="aspect-ratio: {ratio}" role="img" aria-label="{label}">'
        '<svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
        '<circle cx="{cx}" cy="{cy}" r="26" fill="rgba(255,255,255,0.10)"/>'
        '<circle cx="{cx2}" cy="{cy2}" r="15" fill="rgba(0,0,0,0.12)"/>'
        '<path transform="translate({lx} {ly}) rotate({rot})" d="M0 0C12-16 36-16 48 0 36 16 12 16 0 0Z" fill="rgba(255,255,255,0.16)"/>'
        '<path transform="translate({lx2} {ly2}) rotate({rot2})" d="M0 0C9-12 27-12 36 0 27 12 9 12 0 0Z" fill="rgba(0,0,0,0.10)"/>'
        "</svg>"
        '<span class="ph-label" aria-hidden="true">Photo placeholder</span>'
        "</div>"
    ).format(
        tone=tone, ratio=ratio, label=escape(label, quote=True),
        cx=cx, cy=cy, cx2=100 - cx, cy2=100 - cy,
        lx=lx, ly=ly, rot=rot, lx2=100 - lx, ly2=max(10, ly - 30), rot2=(rot + 140) % 360,
    )


def nav_html(root, current):
    items = []
    for label, target in NAV:
        if isinstance(target, list):
            sub = "".join(
                '<li><a href="{r}{h}"{c}>{l}</a></li>'.format(
                    r=root, h=h, l=l, c=' aria-current="page"' if h == current else "")
                for l, h in target
            )
            items.append(
                '<li class="has-menu"><a href="{r}{h}">{l}</a><ul>{sub}</ul></li>'.format(
                    r=root, h=target[0][1], l=label, sub=sub)
            )
        else:
            items.append('<li><a href="{r}{h}"{c}>{l}</a></li>'.format(
                r=root, h=target, l=label, c=' aria-current="page"' if target == current else ""))
    return "".join(items)


def page(path, title, description, body, theme="on-mist", footer_theme=None):
    """Wrap a page body in the shared shell and write it to disk."""
    depth = path.count("/")
    root = "../" * depth
    current = path if depth == 0 else ""
    if footer_theme is None:
        footer_theme = "on-mist"
    social = "".join(
        '<a href="#" data-placeholder="social" aria-label="{n} (add your link)">'
        '<svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg></a>'.format(n=n, p=p)
        for n, p in SOCIAL_ICONS.items()
    )
    foot_links = [("Home", "index.html"), ("About", "about.html"), ("Services", "services.html"),
                  ("Coaching", "coaching.html"), ("Seasonal recipes", "seasonal-recipes.html"),
                  ("Meal plans", "meal-plans.html"), ("Work with me", "work-with-me.html"), ("Contact", "contact.html")]
    foot_nav = "".join('<li><a href="{r}{h}">{l}</a></li>'.format(r=root, h=h, l=l) for l, h in foot_links)
    full_title = title if title == SITE_NAME else "{} — {}".format(title, SITE_NAME)
    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&amp;family=Marcellus&amp;display=swap">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/styles.css">
<script>document.documentElement.className = "js";</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header {theme}">
  <div class="hdr-row">
    <div class="social">{social}</div>
    <a class="brand" href="{root}index.html">{site}</a>
    <div class="hdr-actions"><a class="btn btn-sm" href="{root}work-with-me.html">Work with me</a></div>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
  </div>
  <nav class="site-nav" id="site-nav" aria-label="Main"><ul>{nav}<li class="nav-cta"><a href="{root}work-with-me.html">Work with me</a></li></ul></nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer {footer_theme}" id="footer">
  <h2>Fresh recipes, once a month.</h2>
  <form class="signup" data-demo-form="Thanks. This demo sign-up is not connected to a mailing list yet." novalidate>
    <label class="visually-hidden" for="signup-email">Email address</label>
    <input id="signup-email" type="email" name="email" placeholder="Email address" autocomplete="email" required>
    <button class="btn btn-sm" type="submit">Sign up</button>
    <p class="form-note" role="status" style="flex-basis:100%"></p>
  </form>
  <ul class="foot-nav">{foot_nav}</ul>
  <p class="fine">{site} · {tagline}</p>
</footer>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
""".format(
        full_title=escape(full_title), description=escape(description, quote=True), root=root,
        theme=theme, social=social, site=escape(SITE_NAME), nav=nav_html(root, current),
        body=body.replace("{root}", root), footer_theme=footer_theme, foot_nav=foot_nav,
        tagline=escape(TAGLINE),
    )
    out = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path


def recipe_tile(r, i, root="{root}"):
    return (
        '<a class="tile" href="{root}recipes/{slug}.html">{img}<span class="tile-title">{title}</span></a>'
    ).format(root=root, slug=r["slug"], title=escape(r["title"]),
             img=ph("Placeholder image for " + r["title"], "4 / 5", r["tone"], i + 3))


# ---------------------------------------------------------------- pages

def build():
    written = []

    # ---- Home
    tiles = "".join(recipe_tile(r, i) for i, r in enumerate(RECIPES))
    body = """
<section class="section hero on-olive" id="hero">
  <div class="inner">
    <p class="eyebrow">Certified nutrition and wellness coaching</p>
    <h1>Eating well,<br>one calm habit at a time</h1>
    <div class="hero-media">{hero_img}</div>
  </div>
</section>

<section class="section on-olive" id="offerings">
  <div class="inner">
    <p class="eyebrow center">Ways to work together</p>
    <div class="grid cols-3 cards-ruled" style="margin-top:2.5rem">
      <article class="card">
        <h2>1:1 Coaching</h2>
        <p>A plan shaped around your goals, your schedule and the food you actually enjoy, with regular check-ins to keep it moving.</p>
        <a class="btn" href="{root}coaching.html">Learn more<span class="visually-hidden"> about 1:1 coaching</span></a>
      </article>
      <article class="card">
        <h2>Online Courses</h2>
        <p>Self-paced lessons on the foundations of eating and living well. Start whenever suits you and revisit as often as you like.</p>
        <a class="btn" href="{root}services.html#courses">Learn more<span class="visually-hidden"> about online courses</span></a>
      </article>
      <article class="card">
        <h2>Live Events</h2>
        <p>Friendly, beginner-level workshops and webinars. Bring your questions and leave with something practical to try that week.</p>
        <a class="btn" href="{root}services.html#events">Learn more<span class="visually-hidden"> about live events</span></a>
      </article>
    </div>
  </div>
</section>

<section class="section on-mist" id="nutrition">
  <div class="inner grid cols-2 split">
    <div class="media-first">{nutrition_img}</div>
    <div>
      <p class="eyebrow">Nutrition guidance</p>
      <h2>A kinder relationship with food</h2>
      <div class="grid cols-2" style="margin-top:2rem; gap:2rem">
        <div>
          <h3 style="font-size:1.0625rem; letter-spacing:.08em">Start somewhere easy</h3>
          <p>Cook one new thing this week. The free recipes and meal plans are designed to be nourishing and genuinely good to eat.</p>
          <a class="text-link" href="{root}seasonal-recipes.html">Browse seasonal recipes</a>
        </div>
        <div>
          <h3 style="font-size:1.0625rem; letter-spacing:.08em">Work on something specific</h3>
          <p>Allergies, a health condition or a long history of dieting can make food feel complicated. A tailored plan can help.</p>
          <a class="text-link" href="{root}contact.html">Arrange a consultation</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section tight on-mist" id="coaching">
  <div class="inner grid cols-2 split">
    <div>
      <p class="eyebrow">Wellness coaching</p>
      <h2>A plan that fits your life</h2>
      <p class="lede">Coaching looks at the whole picture. Together we build one joined-up plan that can draw on nutrition, movement, sleep, stress management and other practices that suit you.</p>
      <p style="margin-top:1.75rem"><a class="btn" href="{root}contact.html">Book a free consultation</a></p>
    </div>
    <div class="media-first">{coaching_img}</div>
  </div>
</section>

<section class="section on-olive" id="recipes">
  <div class="inner">
    <h2 class="center" style="margin-bottom:2.5rem">Recipes</h2>
    <div class="grid cols-5">{tiles}</div>
  </div>
</section>
""".format(
        root="{root}", tiles=tiles,
        hero_img=ph("Placeholder for a wide portrait of the coach at a table", "16 / 8", "moss", 1),
        nutrition_img=ph("Placeholder for a photo of fresh seasonal produce", "4 / 5", "clay", 2),
        coaching_img=ph("Placeholder for a photo of a coaching session", "4 / 5", "sage", 5),
    )
    written.append(page("index.html", SITE_NAME, TAGLINE, body, theme="on-olive"))

    # ---- About
    body = """
<section class="section on-mist" id="intro">
  <div class="inner grid cols-2 split">
    <div class="media-first">{img}</div>
    <div>
      <h1>Hello, I’m {coach}.</h1>
      <p class="lede">I’m a certified nutrition and wellness coach. I help busy people eat well and feel better without rigid rules or all-or-nothing plans.</p>
      <p>This is placeholder text for your story. Say how you came to this work, who you most enjoy helping, and what someone can expect in a first conversation with you. Two or three short paragraphs is plenty.</p>
    </div>
  </div>
</section>

<section class="section on-olive" id="approach">
  <div class="inner narrow center">
    <p class="eyebrow">My approach</p>
    <p class="statement">Small, repeatable changes beat dramatic overhauls. We start with what already works and build from there.</p>
  </div>
</section>

<section class="section on-mist" id="steps">
  <div class="inner grid cols-2 cards-ruled">
    <article class="card">
      <h2>Picture it</h2>
      <p>We begin by getting clear on what feeling well means to you. Not a number on a scale, but how you want your days to go: energy, sleep, mood, confidence in the kitchen.</p>
    </article>
    <article class="card">
      <h2>Practise it</h2>
      <p>Then we turn that picture into a handful of habits, tried one at a time. Each session we keep what helped, drop what didn’t and choose the next small step.</p>
    </article>
  </div>
</section>
""".format(img=ph("Placeholder for a portrait of the coach", "4 / 5", "stone", 4), coach=escape(COACH_NAME))
    written.append(page("about.html", "About", "Meet the coach behind {} and the approach to nutrition and wellness coaching.".format(SITE_NAME), body))

    # ---- Services
    body = """
<section class="section on-mist center" id="services-intro">
  <div class="inner narrow">
    <h1>Services</h1>
    <p class="lede">Three ways to get support, depending on how much structure and one-to-one time you want.</p>
  </div>
</section>

<section class="section tight on-mist" id="events">
  <div class="inner grid cols-2 split top">
    <div class="media-first">{img1}</div>
    <div>
      <h2>Live Events</h2>
      <ul class="event-list">
        <li><h3>Gluten-free baking basics</h3><span class="when">12 June · 1–3 pm</span><p>Reliable everyday bakes without specialist ingredients.</p></li>
        <li><h3>Starting a meditation habit</h3><span class="when">19 June · 1–3 pm</span><p>Five-minute practices you can keep up on a busy day.</p></li>
        <li><h3>Staying steady under stress</h3><span class="when">26 June · 1–3 pm</span><p>Practical tools for the moments that usually derail you.</p></li>
      </ul>
      <p class="price-line">Every event · $45 a month</p>
    </div>
  </div>
</section>

<section class="section on-olive" id="courses">
  <div class="inner grid cols-2 split top">
    <div>
      <h2>Online Courses</h2>
      <div class="grid cols-2" style="gap:2rem">
        <article>
          {img2}
          <h3 style="margin-top:1rem">Reset and Restore</h3>
          <p>A four-week course on meals, sleep and routines that help you feel like yourself again.</p>
        </article>
        <article>
          {img3}
          <h3 style="margin-top:1rem">Herbs and Oils 101</h3>
          <p>A plain-spoken introduction to using herbs and essential oils sensibly at home.</p>
        </article>
      </div>
      <p class="price-line">Every course · $600 a year</p>
    </div>
    <div class="media-first">{img4}</div>
  </div>
</section>

<section class="section on-mist" id="one-to-one">
  <div class="inner grid cols-2 split">
    <div class="media-first">{img5}</div>
    <div>
      <h2>1:1 Coaching</h2>
      <h3>Weekly sessions</h3>
      <p>Regular one-to-one time to set priorities, solve problems as they come up and adjust your plan as life changes. Sessions run online or in person.</p>
      <p class="price-line">Free first consultation · $120 per session</p>
      <p style="margin-top:1.75rem"><a class="btn" href="{root}work-with-me.html">Work with me</a></p>
    </div>
  </div>
</section>
""".format(
        root="{root}",
        img1=ph("Placeholder for a photo from a live workshop", "4 / 5", "clay", 6),
        img2=ph("Placeholder image for the Reset and Restore course", "1 / 1", "sage", 7),
        img3=ph("Placeholder image for the Herbs and Oils course", "1 / 1", "stone", 8),
        img4=ph("Placeholder for a photo of someone studying online", "4 / 5", "moss", 9),
        img5=ph("Placeholder for a photo of a one-to-one session", "4 / 5", "sage", 10),
    )
    written.append(page("services.html", "Services", "Live events, online courses and one-to-one coaching, with placeholder pricing.", body))

    # ---- Coaching
    faqs = [
        ("How long does coaching usually last?", "Most people work with me for three to six months. That is long enough to build habits and see them hold through a few real-life disruptions."),
        ("Do I need to follow a set diet?", "No. We work with the foods you like and the way your household already eats, and adjust from there."),
        ("Are sessions online or in person?", "Either. Online sessions run by video call, and in-person sessions are available locally."),
        ("What happens in the free consultation?", "It is a relaxed twenty-minute conversation about what you want help with and whether coaching is the right fit."),
        ("Can you work alongside my doctor?", "Yes. Coaching complements medical care and never replaces it. I am happy to follow guidance from your healthcare team."),
        ("What if I need to pause?", "Life happens. You can pause and pick up again when things settle, with no penalty."),
    ]
    faq_html = "".join("<details><summary>{}</summary><p>{}</p></details>".format(escape(q), escape(a)) for q, a in faqs)
    body = """
<section class="section on-mist center" id="coaching-intro">
  <div class="inner narrow">
    <h1>Coaching</h1>
    <p class="lede">One-to-one support, built on three ideas.</p>
  </div>
</section>

<section class="section tight on-mist" id="pillars">
  <div class="inner grid cols-3">
    <article>{img1}<h2 style="margin-top:1.25rem">Personal</h2><p>Your plan starts from your goals, tastes, budget and week, not from a template.</p></article>
    <article>{img2}<h2 style="margin-top:1.25rem">Focused</h2><p>We choose one or two priorities at a time so progress is visible and manageable.</p></article>
    <article>{img3}<h2 style="margin-top:1.25rem">Joined-up</h2><p>Food, movement, rest and stress all affect each other, so we look at them together.</p></article>
  </div>
</section>

<section class="section on-olive" id="feel">
  <div class="inner narrow center">
    <p class="eyebrow">How you’ll feel</p>
    <p class="statement">Clearer, steadier and more confident about what to eat, with more energy for everything else.</p>
  </div>
</section>

<section class="section on-mist" id="get">
  <div class="inner grid cols-2 split top">
    <div>
      <p class="eyebrow">What you’ll get</p>
      <h2>Support between sessions, not just during them</h2>
    </div>
    <ul class="checks">
      <li>A written plan after your first session, updated as you go</li>
      <li>Weekly or fortnightly one-to-one sessions</li>
      <li>Meal ideas and shopping lists matched to your plan</li>
      <li>Message support for quick questions between sessions</li>
      <li>Free access to live events while you are a client</li>
    </ul>
  </div>
</section>

<section class="section tight on-mist" id="faqs">
  <div class="inner narrow">
    <h2 class="center">FAQs</h2>
    <div class="faq">{faq}</div>
    <p class="center" style="margin-top:2.5rem"><a class="btn" href="{root}contact.html">Book a free consultation</a></p>
  </div>
</section>
""".format(
        root="{root}", faq=faq_html,
        img1=ph("Placeholder image for personal coaching", "4 / 5", "sage", 11),
        img2=ph("Placeholder image for focused coaching", "4 / 5", "clay", 12),
        img3=ph("Placeholder image for joined-up coaching", "4 / 5", "stone", 13),
    )
    written.append(page("coaching.html", "Coaching", "How one-to-one coaching works, what is included and answers to common questions.", body))

    # ---- Seasonal recipes
    seasons = [
        ("Spring", "Tender greens, herbs and lighter plates.", "sage"),
        ("Summer", "Berries, tomatoes and food that needs little cooking.", "clay"),
        ("Autumn", "Roots, squash and warming spice.", "moss"),
        ("Winter", "Slow cooking, citrus and store-cupboard comfort.", "stone"),
    ]
    blocks = []
    for i, (name, line, tone) in enumerate(seasons):
        links = "".join(
            '<li><a href="{root}recipes/' + r["slug"] + '.html">' + escape(r["title"]) + "</a></li>"
            for r in RECIPES if r["season"] == name
        )
        blocks.append(
            '<article id="{id}">{img}<h2 style="margin-top:1.25rem">{name}</h2><p>{line}</p>'
            '<ul style="padding-left:1.1rem; margin:0">{links}</ul></article>'.format(
                id=name.lower(), img=ph("Placeholder image for " + name.lower() + " recipes", "3 / 4", tone, 14 + i),
                name=name, line=line, links=links)
        )
    body = """
<section class="section on-mist center" id="seasonal-intro">
  <div class="inner narrow">
    <h1>Seasonal recipes</h1>
    <p class="lede">Cooking with what is in season is cheaper, tastier and an easy way to add variety.</p>
  </div>
</section>
<section class="section tight on-mist" id="seasons">
  <div class="inner grid cols-4">{blocks}</div>
</section>
""".format(blocks="".join(blocks))
    written.append(page("seasonal-recipes.html", "Seasonal recipes", "Free recipes grouped by season: spring, summer, autumn and winter.", body))

    # ---- Meal plans
    plans = [
        ("Gut Health", "Seven days built around fibre, fermented foods and plenty of plants.", "sage"),
        ("Anti-inflammatory", "Oily fish, olive oil, colourful vegetables and whole grains across a full week.", "clay"),
        ("Immune Support", "Meals rich in vitamin C, zinc and protein for the colder months.", "stone"),
    ]
    plan_html = "".join(
        "<article>{img}<h3 style=\"margin-top:1.25rem\">{name}</h3><p>{line}</p></article>".format(
            img=ph("Placeholder image for the " + name + " meal plan", "4 / 5", tone, 20 + i), name=name, line=line)
        for i, (name, line, tone) in enumerate(plans)
    )
    body = """
<section class="section on-mist center" id="plans-intro">
  <div class="inner narrow">
    <p class="eyebrow">Meal plans</p>
    <h1>Food that supports your health</h1>
    <p class="lede">Each plan is a week of breakfasts, lunches and dinners with a shopping list. Use one as written or borrow the parts you like.</p>
  </div>
</section>
<section class="section tight on-mist" id="plans">
  <div class="inner grid cols-3">{plans}</div>
  <p class="center" style="margin-top:3rem"><a class="btn" href="{root}contact.html">Ask for a tailored plan</a></p>
</section>
""".format(root="{root}", plans=plan_html)
    written.append(page("meal-plans.html", "Meal plans", "Week-long meal plans for gut health, lower inflammation and immune support.", body))

    # ---- Work with me
    body = """
<section class="section on-olive center" id="work-intro">
  <div class="inner narrow">
    <h1>Start feeling better from here.</h1>
    <p class="lede">Pick the level of support that suits you now. You can change at any time.</p>
  </div>
</section>
<section class="section tight on-olive" id="options">
  <div class="inner grid cols-3 cards-ruled">
    <article class="card">
      <h2>1:1 Coaching</h2>
      <p class="eyebrow">Free consultation</p>
      <p>Personal sessions and a plan made for you. Begin with a no-obligation conversation.</p>
      <a class="btn" href="{root}contact.html">Book a call</a>
    </article>
    <article class="card">
      <h2>Online Courses</h2>
      <p class="eyebrow">$600 a year · every course</p>
      <p>Learn at your own pace with full access to the course library.</p>
      <a class="btn" href="{root}services.html#courses">See the courses</a>
    </article>
    <article class="card">
      <h2>Live Events</h2>
      <p class="eyebrow">$45 a month · every event</p>
      <p>Join any workshop or webinar on the calendar, live or on replay.</p>
      <a class="btn" href="{root}services.html#events">See what’s on</a>
    </article>
  </div>
</section>
<section class="section on-olive" id="work-media" style="padding-top:0">
  <div class="inner">{img}</div>
</section>
""".format(root="{root}", img=ph("Placeholder for a wide photo of a calm kitchen table", "16 / 7", "sage", 24))
    written.append(page("work-with-me.html", "Work with me", "Choose between one-to-one coaching, online courses and live events.", body, theme="on-olive"))

    # ---- Contact
    body = """
<section class="section on-mist" id="contact">
  <div class="inner grid cols-2 split top">
    <div>
      <h1>Contact me</h1>
      <p class="lede">Questions about coaching, courses or events? Send a note and I’ll reply within two working days.</p>
      <p>This form is a front-end demo. Connect it to your email or form service before going live.</p>
    </div>
    <form class="form" data-demo-form="Thanks. This demo form is not connected yet, so nothing was sent." novalidate>
      <div class="row">
        <div class="field"><label for="first">First name</label><input id="first" name="first" autocomplete="given-name" required></div>
        <div class="field"><label for="last">Last name</label><input id="last" name="last" autocomplete="family-name" required></div>
      </div>
      <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="message">Message</label><textarea id="message" name="message" required></textarea></div>
      <div><button class="btn" type="submit">Send</button></div>
      <p class="form-note" role="status"></p>
    </form>
  </div>
</section>
"""
    written.append(page("contact.html", "Contact", "Get in touch about coaching, courses or events.", body))

    # ---- Recipe posts
    for i, r in enumerate(RECIPES):
        others = [RECIPES[(i + 1) % len(RECIPES)], RECIPES[(i + 2) % len(RECIPES)]]
        more = "".join(recipe_tile(o, i + j + 30) for j, o in enumerate(others))
        body = """
<article>
<section class="section on-mist" id="recipe">
  <div class="inner narrow">
    <p class="recipe-meta"><a href="{root}seasonal-recipes.html">Recipes</a> · {season} · {meta}</p>
    <h1>{title}</h1>
    <p class="lede">{intro}</p>
    {img}
  </div>
</section>
<section class="section tight on-mist recipe-body" id="method">
  <div class="inner narrow grid cols-2 split top">
    <div><h2 style="font-size:1.0625rem; letter-spacing:.08em">Ingredients</h2><ul>{ingredients}</ul></div>
    <div><h2 style="font-size:1.0625rem; letter-spacing:.08em">Method</h2><ol>{method}</ol></div>
  </div>
</section>
</article>
<section class="section on-olive" id="more">
  <div class="inner narrow">
    <h2 class="center" style="margin-bottom:2rem">More recipes</h2>
    <div class="grid cols-2">{more}</div>
  </div>
</section>
""".format(
            root="{root}", season=r["season"], meta=escape(r["meta"]), title=escape(r["title"]), intro=escape(r["intro"]),
            img=ph("Placeholder image for " + r["title"], "16 / 9", r["tone"], 40 + i),
            ingredients="".join("<li>{}</li>".format(escape(x)) for x in r["ingredients"]),
            method="".join("<li>{}</li>".format(escape(x)) for x in r["method"]),
            more=more,
        )
        written.append(page("recipes/{}.html".format(r["slug"]), r["title"], r["intro"].split(". ")[0].rstrip(".") + ".", body))

    return written


if __name__ == "__main__":
    for p in build():
        print("wrote", p)
