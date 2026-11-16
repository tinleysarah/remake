#!/usr/bin/env python3
"""Check the generated site and write REPORT.md.

Run:  python3 check.py

Static checks run here against the .html files. Browser checks (layout at
desktop and phone widths, console errors, menu, FAQ, forms) cannot be run
from Python, so their recorded results are read from checks/browser.json.

The report's last line is REMAKE COMPLETE only if every check passes.
"""
import json
import os
import re
import sys
from datetime import date
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))

# Page set and section layout the remake has to match (taken from the
# structure of the source demo: its pages, and the blocks on each page).
EXPECTED = {
    "index.html": ["hero", "offerings", "nutrition", "coaching", "recipes"],
    "about.html": ["intro", "approach", "steps"],
    "services.html": ["services-intro", "events", "courses", "one-to-one"],
    "coaching.html": ["coaching-intro", "pillars", "feel", "get", "faqs"],
    "seasonal-recipes.html": ["seasonal-intro", "seasons"],
    "meal-plans.html": ["plans-intro", "plans"],
    "work-with-me.html": ["work-intro", "options"],
    "contact.html": ["contact"],
    "recipes/oat-honey-face-mask.html": ["recipe", "method", "more"],
    "recipes/salmon-grain-bowl.html": ["recipe", "method", "more"],
    "recipes/berry-yogurt-bowl.html": ["recipe", "method", "more"],
    "recipes/smashed-avocado-toast.html": ["recipe", "method", "more"],
    "recipes/ginger-lime-fizz.html": ["recipe", "method", "more"],
}
NAV_TARGETS = ["about.html", "services.html", "coaching.html", "seasonal-recipes.html",
               "meal-plans.html", "contact.html", "work-with-me.html"]
# Counts the source demo has that the remake should also have.
COUNTS = {
    "index.html": {"offer cards": ("#offerings article", 3), "recipe tiles": ("#recipes a.tile", 5)},
    "services.html": {"events": ("#events li", 3), "courses": ("#courses article", 2)},
    "coaching.html": {"pillars": ("#pillars article", 3), "FAQ entries": ("#faqs details", 6)},
    "seasonal-recipes.html": {"seasons": ("#seasons article", 4)},
    "meal-plans.html": {"plans": ("#plans article", 3)},
    "work-with-me.html": {"options": ("#options article", 3)},
    "about.html": {"steps": ("#steps article", 2)},
}
ALLOWED_EXTERNAL = ("https://fonts.googleapis.com", "https://fonts.gstatic.com")
FORBIDDEN_WORDS = ("squarespace", "myhra", "sqs-", "static1.")


class Doc(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.stack = []          # (tag, id)
        self.ids = []
        self.h1 = 0
        self.title = ""
        self._in_title = False
        self.lang = None
        self.meta = {}
        self.links = []          # hrefs
        self.assets = []         # src / stylesheet href
        self.external = []
        self.placeholders = 0
        self.unlabelled = []
        self.inputs = []
        self.labels = set()
        self.found = []          # (ancestor id, tag, class list)
        self.has_header = self.has_footer = self.has_main = False
        self.doctype = False

    def handle_decl(self, decl):
        if decl.lower().startswith("doctype html"):
            self.doctype = True

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        void = tag in ("meta", "link", "img", "input", "br", "hr", "circle", "path", "rect")
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name"):
            self.meta[a["name"]] = a.get("content", "")
        if tag == "h1":
            self.h1 += 1
        if tag == "header":
            self.has_header = True
        if tag == "footer":
            self.has_footer = True
        if tag == "main":
            self.has_main = True
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "a" and "href" in a:
            href = a["href"]
            if href == "#":
                self.placeholders += 1
            else:
                self.links.append(href)
        if tag == "link" and a.get("rel") in ("stylesheet", "icon"):
            self.assets.append(a.get("href", ""))
        if tag in ("script", "img") and a.get("src"):
            self.assets.append(a["src"])
        if tag == "img" and not a.get("alt") and a.get("alt") != "":
            self.unlabelled.append("img")
        if a.get("role") == "img" and not a.get("aria-label"):
            self.unlabelled.append("role=img")
        if tag in ("input", "textarea"):
            self.inputs.append(a.get("id"))
        if tag == "label" and a.get("for"):
            self.labels.add(a["for"])
        ancestors = [i for _, i in self.stack if i]
        classes = (a.get("class") or "").split()
        for anc in ancestors:
            self.found.append((anc, tag, classes))
        if not void:
            self.stack.append((tag, a.get("id")))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self._in_title:
            self.title += data

    def count(self, selector):
        """Tiny selector support: '#id tag' or '#id tag.class'."""
        anc, rest = selector.split()
        anc = anc.lstrip("#")
        tag, _, cls = rest.partition(".")
        return sum(1 for a, t, c in self.found if a == anc and t == tag and (not cls or cls in c))


def run():
    results = []   # (group, name, ok, detail)

    def add(group, name, ok, detail=""):
        results.append((group, name, bool(ok), detail))

    docs = {}
    for path in EXPECTED:
        full = os.path.join(HERE, path)
        if not os.path.isfile(full):
            add("Pages", "{} exists".format(path), False, "file missing")
            continue
        with open(full, encoding="utf-8") as fh:
            raw = fh.read()
        d = Doc()
        d.feed(raw)
        docs[path] = (d, raw)
    add("Pages", "All {} pages generated".format(len(EXPECTED)), len(docs) == len(EXPECTED),
        "{} of {} present".format(len(docs), len(EXPECTED)))

    placeholders = 0
    for path, (d, raw) in sorted(docs.items()):
        base = os.path.dirname(os.path.join(HERE, path))
        missing = [s for s in EXPECTED[path] if s not in d.ids]
        add("Section layout", "{}: sections {}".format(path, ", ".join(EXPECTED[path])), not missing,
            "missing: " + ", ".join(missing) if missing else "")
        for label, (sel, want) in COUNTS.get(path, {}).items():
            got = d.count(sel)
            add("Section layout", "{}: {} {}".format(path, want, label), got == want, "found {}".format(got))

        shell = []
        if not d.doctype: shell.append("no doctype")
        if d.lang != "en": shell.append("no lang")
        if not d.title.strip(): shell.append("no title")
        if not d.meta.get("description"): shell.append("no meta description")
        if "width=device-width" not in d.meta.get("viewport", ""): shell.append("no viewport")
        if d.h1 != 1: shell.append("{} h1 elements".format(d.h1))
        if not (d.has_header and d.has_main and d.has_footer): shell.append("missing header/main/footer")
        add("Page shell", "{}: doctype, lang, title, description, viewport, one h1, landmarks".format(path),
            not shell, "; ".join(shell))

        depth = path.count("/")
        hrefs = [h for h in d.links]
        nav_missing = [t for t in NAV_TARGETS if ("../" * depth + t) not in hrefs]
        add("Navigation", "{}: links to every main page".format(path), not nav_missing,
            "missing: " + ", ".join(nav_missing) if nav_missing else "")

        broken = []
        for href in d.links + d.assets:
            if href.startswith(("http://", "https://")):
                d.external.append(href)
                continue
            if href.startswith(("mailto:", "tel:")):
                continue
            target, _, frag = href.partition("#")
            if not target:                      # same-page anchor
                if frag and frag not in d.ids:
                    broken.append(href)
                continue
            dest = os.path.normpath(os.path.join(base, target))
            if not os.path.isfile(dest):
                broken.append(href)
            elif frag:
                rel = os.path.relpath(dest, HERE)
                if rel in docs and frag not in docs[rel][0].ids:
                    broken.append(href)
        add("Links", "{}: internal links and assets resolve".format(path), not broken,
            "broken: " + ", ".join(sorted(set(broken))) if broken else "")

        bad_ext = [e for e in d.external if not e.startswith(ALLOWED_EXTERNAL)]
        low = raw.lower()
        copied = [w for w in FORBIDDEN_WORDS if w in low]
        add("Original content", "{}: no source-site assets, links or brand names".format(path),
            not bad_ext and not copied, "; ".join(bad_ext + copied))

        unl = list(d.unlabelled) + ["input #{}".format(i) for i in d.inputs if i not in d.labels]
        add("Accessibility", "{}: images described, form fields labelled".format(path), not unl, ", ".join(unl))
        placeholders += d.placeholders

    # Browser checks, recorded after running them in a real browser.
    bpath = os.path.join(HERE, "checks", "browser.json")
    browser = {}
    if os.path.isfile(bpath):
        with open(bpath, encoding="utf-8") as fh:
            browser = json.load(fh)
    needed = ["desktop_no_horizontal_scroll", "phone_no_horizontal_scroll", "no_console_errors",
              "web_fonts_load", "mobile_menu_toggles", "recipes_dropdown_opens", "faq_opens_and_closes",
              "forms_validate_and_confirm", "content_and_navigation_work_without_javascript"]
    for key in needed:
        item = browser.get("checks", {}).get(key)
        if not item:
            add("Browser", key.replace("_", " "), False, "not yet recorded")
        else:
            add("Browser", key.replace("_", " "), item.get("result") == "pass", item.get("detail", ""))

    return results, placeholders, browser


def write_report(results, placeholders, browser):
    total = len(results)
    passed = sum(1 for r in results if r[2])
    complete = passed == total
    lines = ["# Remake report", "",
             "Source: `https://myhra-demo.squarespace.com` (structure only)  ",
             "Generated: {} by `check.py`".format(date.today().isoformat()), "",
             "**{} of {} checks passed.**".format(passed, total), "",
             "## Scope", "",
             "This remake reproduces the demo's page set, navigation and section-by-section layout as a",
             "hand-written static site. The demo is Squarespace's own template, so its wording, photographs",
             "and licensed fonts were deliberately not copied: the copy is new placeholder text, images are",
             "tonal placeholders, and the fonts are open-licensed (Marcellus, EB Garamond).", "",
             "Not included, because they need a backend or an account system: the cart, the login link,",
             "and live delivery for the newsletter and contact forms (both are front-end demos that say so).",
             "", "## Results", ""]
    groups = []
    for g, _, _, _ in results:
        if g not in groups:
            groups.append(g)
    for g in groups:
        rows = [r for r in results if r[0] == g]
        ok = sum(1 for r in rows if r[2])
        lines.append("### {} ({}/{})".format(g, ok, len(rows)))
        lines.append("")
        for _, name, good, detail in rows:
            mark = "PASS" if good else "FAIL"
            lines.append("- {} · {}{}".format(mark, name, " — " + detail if detail else ""))
        lines.append("")
    if browser.get("environment"):
        lines += ["Browser checks were run in: {}".format(browser["environment"]), ""]
    lines += ["## Left for you to fill in", "",
              "- {} placeholder social links (`href=\"#\"`), {} per page".format(placeholders, 3),
              "- Site name, coach name and prices: edit the constants at the top of `build.py`, then run `python3 build.py`",
              "- Real photographs in place of the tonal placeholders",
              "- A form or mailing-list service for the contact and sign-up forms", "",
              "## Status", "",
              "REMAKE COMPLETE" if complete else "REMAKE INCOMPLETE"]
    with open(os.path.join(HERE, "REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return complete, passed, total


if __name__ == "__main__":
    res, ph_count, br = run()
    done, p, t = write_report(res, ph_count, br)
    for g, name, ok, detail in res:
        if not ok:
            print("FAIL", g, "|", name, "|", detail)
    print("{} / {} passed -> {}".format(p, t, "REMAKE COMPLETE" if done else "REMAKE INCOMPLETE"))
    sys.exit(0 if done else 1)
