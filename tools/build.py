"""Build the portfolio with Python 3.8+ and the standard library."""
import hashlib
import json
import shutil
import tempfile
from html import escape
from pathlib import Path
from urllib.parse import urlparse

from content import (AWARDS, CAP, DEVPOST, EMAIL, EXPERIENCE, GITHUB, LINKEDIN, PAPER,
                     PAPER_SOURCE, PAPER_TITLE, POSTER, PROJECTS, RESEARCH)
from project_media import FEATURED, FIGURES

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.mxpersonal.com/"
PROJECTS = [p for p in PROJECTS if p.publish and p.visibility == "public"]
PAGES = {}
RESUME_PDF = "resume_ai_linguist.pdf"
RESUME_PDF_SHA256 = "307cd846cbe5604c1a35e5c88e5781dbc3f677777a6984f6d76d32be9f675a41"
ICONS = {
    "arrow": "M4 12h15m-6-6 6 6-6 6", "external": "M6 18 18 6M6 6h12v12",
    "sun": "M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5M16.5 12a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0",
    "menu": "M3 6h18M3 12h18M3 18h18", "book": "M3 5c4-1 6 0 9 2 3-2 5-3 9-2v14c-3-1-6 0-9 2-3-2-6-3-9-2zM12 7v14",
    "layers": "m2 8 10-5 10 5-10 5zM2 12l10 5 10-5M2 16l10 5 10-5",
    "cap": "m2 9 10-5 10 5-10 5zM6 12v5c3 3 9 3 12 0v-5M22 9v7",
    "pin": "M19 10c0 5-7 12-7 12S5 15 5 10a7 7 0 1 1 14 0zM14 10a2 2 0 1 1-4 0 2 2 0 0 1 4 0",
    "award": "M16.5 8a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0M8 12l-2 9 6-3 6 3-2-9",
}
def icon(name):
    return f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{ICONS[name]}"/></svg>'


def link(label, href, style="text-link", symbol="arrow"):
    if urlparse(href).scheme not in ("", "mailto", "https"):
        raise ValueError(f"Unsupported link {href}")
    return f'<a class="{style}" href="{escape(href)}">{escape(label)}{icon(symbol) if symbol else ""}</a>'


def wordmark():
    return '<a class="brand" href="index.html" aria-label="Max Xie, home"><span class="monogram" aria-hidden="true">mx</span>Max Xie<span class="slash" aria-hidden="true">/</span></a>'


def page(file, title, desc, body, active="", schema=None, canonical=None, refresh=None):
    nav = []
    for name, dest in (("About","about.html"),("Projects","projects.html"),("Research","publications.html"),("Résumé","resume.html"),("Contact","contact.html")):
        cur = ' aria-current="page"' if file == dest else ''
        nav.append(f'<a class="navlink {"chosen" if name == active else ""} {"contact-link" if name == "Contact" else ""}" href="{dest}"{cur}>{name}{icon("external") if name=="Contact" else ""}</a>')
    url = SITE + (canonical or ("" if file == "index.html" else file))
    meta = f'<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>' if schema else ''
    article = schema and schema.get("@type") == "ScholarlyArticle"
    document_title = title if article else f"{title} · Max Xie"
    if article:
        citation_fields = {
            "citation_title": schema["headline"],
            "citation_author": schema["author"]["name"],
            "citation_author_institution": schema["author"]["affiliation"]["name"],
            "citation_publication_date": schema["datePublished"].replace("-", "/"),
            "citation_pdf_url": schema["encoding"]["contentUrl"],
            "citation_language": schema["inLanguage"],
        }
        meta += "\n" + "\n".join(
            f'<meta name="{field}" content="{escape(value)}">' for field, value in citation_fields.items()
        )
    base = '<base href="/">' if file == "404.html" else ""
    redirect = f'<meta http-equiv="refresh" content="0;url={refresh}">' if refresh else ''
    PAGES[file] = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">{base}<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(document_title)}</title><meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}"><meta property="og:url" content="{url}"><meta property="og:type" content="{'article' if article else 'website'}">
<link rel="describedby" href="llms.txt" title="Portfolio guide for agents">
<meta property="og:title" content="{escape(title)} · Max Xie"><meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{SITE}assets/portfolio/social.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/portfolio/icon.svg"><link rel="stylesheet" href="assets/css/portfolio-v2.css"><script defer src="assets/js/portfolio-v2.js"></script>{meta}{redirect}
</head><body><a class="skip" href="#content">Skip to content</a><header><div class="wrap mast">{wordmark()}
<nav id="navigation" aria-label="Main navigation">{''.join(nav)}</nav><div class="nav-tools">
<button id="theme" hidden aria-label="Light theme" aria-pressed="false" title="Light theme">{icon("sun")}</button>
<button id="menu" hidden aria-label="Navigation menu" aria-expanded="false" aria-controls="navigation">{icon("menu")}</button>
</div></div></header><main id="content" class="wrap">{body}</main>
<footer><div class="wrap footer-inner"><span>© 2026 Max Xie</span><nav aria-label="Footer">{link("GitHub",GITHUB,"","external")}{link("LinkedIn",LINKEDIN,"","external")}{link("Email","mailto:"+EMAIL,"",None)}{link("Contact","contact.html","",None)}</nav></div></footer></body></html>'''


def eyebrow(text):
    return f'<div class="eyebrow"><span></span>{text}</div>'


def intro_paragraphs(paragraphs):
    return ''.join(f'<p class="intro">{escape(paragraph)}</p>' for paragraph in paragraphs)


def cover(p):
    return (f'<div class="cover"><img src="assets/portfolio/covers/{p.slug}.webp" '
            'alt="" loading="lazy" width="1080" height="520"></div>')


def project_figures(p):
    figures = []
    for fig in FIGURES[p.slug]:
        image = "assets/portfolio/" + fig.asset
        source = link("Source", fig.source, "text-link") if fig.source else ""
        figures.append(f'<figure class="project-figure"><a class="figure-zoom" data-open-figure href="{image}" '
                       f'aria-label="View full size: {escape(fig.alt)}"><img src="{image}" alt="{escape(fig.alt)}" '
                       f'width="{fig.width}" height="{fig.height}" loading="lazy"></a>'
                       f'<figcaption>{escape(fig.caption)}<div class="figure-links">'
                       f'<a class="text-link" data-open-figure href="{image}">Full size{icon("arrow")}</a>'
                       f'{source}</div></figcaption></figure>')
    return "".join(figures) + '''
    <dialog id="figure-viewer" aria-label="Enlarged project figure">
      <div class="viewer-toolbar"><button type="button" class="button secondary" id="figure-scale">Zoom in</button>
      <form method="dialog"><button class="button secondary" autofocus>Close</button></form></div>
      <div class="viewer-image" tabindex="0" role="region" aria-label="Figure image"><img alt=""></div>
    </dialog>'''


def card(p, heading="h3"):
    tags = ''.join(f'<li>{t}</li>' for t in p.stack)
    artifact = ""
    if p.page == CAP:
        artifact = link("Paper PDF", PAPER, "quiet", "external")
    elif p.website:
        artifact = link("Website", p.website, "quiet", "external")
    elif p.repo:
        artifact = link("GitHub", p.repo, "quiet", "external")
    elif p.extra:
        artifact = link(*p.extra[0], "quiet", "external")
    return f'''<article class="card" data-filters="{escape('|'.join(p.filters))}">{cover(p)}
<div class="card-body"><div class="meta">{escape(p.category)} <i> / </i> {escape(p.status)}</div>
<{heading} class="card-title"><a href="{p.page}">{escape(p.title)}</a></{heading}><p>{escape(p.summary)}</p><ul class="tags">{tags}</ul>
<div class="card-links">{link("Case study",p.page,"case-link").replace('<a ',f'<a aria-label="Read the {escape(p.title)} case study" ')}{artifact}</div></div></article>'''


def cta():
    return '<section class="cta"><h2>Let’s build something useful.</h2>'+link("Get in touch","contact.html","button primary")+'</section>'


def home():
    proof = ''.join(f'<div>{icon(sym)}<span>{label}</span></div>' for sym,label in (
        ("pin","San Francisco, CA"),("cap","M.A. in Linguistics")))
    proof += f'<a href="#qubemc">{icon("layers")}Founder · QubeMC {icon("arrow")}</a>'
    proof += f'<a href="#recognition">{icon("award")}Hackathon awards {icon("arrow")}</a>'
    capabilities = ''.join(f'<article><h3>{title}</h3><p>{desc}</p>{link(label,url)}</article>' for title,desc,label,url in (
        ("Agent systems","Giving agents tools, permissions and a plan a person can inspect.","Explore Paigent Studio","project-paigent-studio.html"),
        ("Evaluation & language","Designing tasks that reveal what a model can do with unfamiliar language.","Read the capstone",CAP),
        ("Production engineering","Connecting web services, real-time streams and the infrastructure that runs them.","Explore Litmus","project-litmus.html")))
    by_slug = {p.slug: p for p in PROJECTS}
    awards = ''.join(
        f'<li><div class="award-result"><b>{escape(a.place)}</b><small>{escape(a.date)}</small></div>'
        f'<div><h3>{link(a.project, by_slug[a.project_slug].page, "title-link", None)}</h3><p>{escape(a.prize)}</p>'
        f'<small>{escape(a.event)} · Hosted by {escape(a.host)}</small>'
        f'<small>Affiliation · {escape(a.affiliation)}</small></div>'
        f'<div class="award-links">{link(*a.local_record) if a.local_record else ""}'
        f'{link(a.link_label, a.url, "text-link", "external")}</div></li>'
        for a in AWARDS
    )
    body = f'''<section id="home" class="hero">
<figure class="hero-portrait"><img src="assets/portfolio/max.webp" width="384" height="512" fetchpriority="high" alt="Max outdoors in the coastal hills">
<figcaption><strong>Peixi “Max” Xie</strong>AI engineer &amp; computational linguist</figcaption></figure><div>
<h1>Building AI systems that work <em>beyond the demo.</em></h1>
<p class="intro">I build AI agents for browsers, voice calls and group chats, and design tests to find out where they fall short.</p>
<div class="actions">{link("Explore projects","projects.html","button primary")}{link("Read research","publications.html","button secondary","book")}{link("GitHub",GITHUB,"quiet","external")}</div></div>
</section>
<div class="proof">{proof}</div>
<section class="section" id="highlights">{eyebrow("Portfolio")}<div class="heading-row"><h2>Selected work<span>.</span></h2>{link("All projects","projects.html")}</div>
<div class="cards">{''.join(card(by_slug[slug]) for slug in FEATURED)}</div></section>
<section class="spotlight" id="qubemc" aria-labelledby="qubemc-title"><div>{eyebrow("My startup")}<h2 id="qubemc-title">QubeMC</h2>
<p>I’m building QubeMC into an AI company for gaming. I’m starting with tools that help game-server operators diagnose problems and automate routine maintenance while keeping control over what changes on their servers.</p>
<div class="actions">{link("Visit QubeMC","https://www.qubemc.com/","button secondary","external")}</div></div>
<figure class="startup-photo"><img src="assets/portfolio/qubemc-lobby.webp" width="880" height="490" loading="lazy" alt="A city of block-built towers around the central plaza in QubeMC’s Minecraft lobby."><figcaption>From QubeMC’s roots in Minecraft</figcaption></figure></section>
<section class="section ruled" id="skills">{eyebrow("Practice")}<h2>What I work on<span>.</span></h2><div class="capabilities">{capabilities}</div></section>
<section class="spotlight"><div>{eyebrow("Research spotlight")}<h2>When the benchmark changes, so do the rankings.</h2><p>My SFSU capstone compares four language models across static knowledge questions, dynamic reasoning tasks and expert linguistics problems.</p><div class="actions">{link("Methodology",CAP+"#methodology")}{link("Read paper",PAPER,"quiet","external")}</div></div>
<a class="figure-link" href="{CAP}#findings"><img src="assets/portfolio/benchmark-figure.webp" alt="Figure 1 compares the four models across three benchmarks. Read the findings." width="1200" height="720" loading="lazy"></a></section>
<section class="section ruled" id="recognition">{eyebrow("Team awards · San Francisco")}<h2>Hackathon recognition<span>.</span></h2><ul class="rows awards">{awards}</ul></section>
<section class="about-preview" id="about"><div>{eyebrow("About Max")}<h2>I’m Max Xie.</h2></div><div>
<p>I earned an M.A. in Linguistics and an M.A. Computational Linguistics Certificate at San Francisco State University. My research there explored what happens to meaning when a language model simplifies a passage.</p>
<p>I’m a nine-time hackathon winner. I like building something a teammate can try the same day, whether it’s a browser agent that learns a repeated task or a tool that explains why a crypto wallet was flagged.</p>
{link("More about my background","about.html")}</div></section>{cta()}'''
    page("index.html","AI Engineer & Computational Linguist", "Max Xie builds voice AI, tool-using agents and language model evaluations in San Francisco.", body, schema={"@context":"https://schema.org","@type":"Person","name":"Peixi Xie","alternateName":"Max Xie","url":SITE,"jobTitle":"AI Engineer","sameAs":[GITHUB,LINKEDIN]})


def page_head(kicker,title,*paragraphs):
    intro = intro_paragraphs(paragraphs)
    return f'<div class="page-head">{eyebrow(kicker)}<h1>{title}<em>.</em></h1>{intro}</div>'


def projects():
    filters = ''.join(f'<button data-filter="{f}" aria-pressed="{str(f=="All").lower()}">{f}</button>' for f in ("All","Agents","Browser Agents","Machine Learning","Deep Learning","LLM Evaluation","Security","Infrastructure","Experimental"))
    body = page_head(
        "Projects", "Selected engineering work",
        "I build language tools and AI agents. During my M.A. in Linguistics at San Francisco State University, "
        "I focused on computational linguistics, studying how well language models reason about language and "
        "what happens to meaning when they simplify a text. I use Python, Java and SQL to build data pipelines, "
        "and Linux and Docker to run the systems that depend on them.",
        "I’m a nine-time hackathon winner. I enjoy working with a team to turn an idea into a prototype we can "
        "test in a weekend. Recent projects include multi-agent workflows built with LangChain and Google ADK, "
        "and a crypto risk analysis tool that uses TRM APIs to help explain what’s happening on-chain."
    )
    body += f'<div class="filterbar" role="group" aria-label="Filter projects" hidden>{filters}</div><span class="sr-only" id="filter-count" role="status"></span><section aria-label="Project case studies" class="cards listings">{"".join(card(p, "h2") for p in PROJECTS)}</section>'
    page("projects.html","Engineering projects","Explore FoxStar Agent for WeChat, browser agents, graph neural networks and speech research by Max Xie.",body+cta(),"Projects")
    for i,p in enumerate(PROJECTS):
        if p.page == CAP:
            continue
        sections = []
        for title, description, sources in p.subprojects:
            links = ''.join(link(label, url, "text-link", "external") for label, url in sources)
            sections.append(f'<section class="subproject"><h2>{escape(title)}</h2><p>{escape(description)}</p><div class="actions">{links}</div></section>')
        sections.extend(f'<section><h2>{title}</h2><p>{text}</p></section>' for title,text in p.sections)
        sections.insert(1, project_figures(p))
        buttons = link("Visit website",p.website,"button primary","external") if p.website else ""
        buttons += link("Source repository",p.repo,"button secondary","external") if p.repo else ""
        buttons += ''.join(link(label,url,"text-link","external") for label,url in p.extra)
        actions = f'<div class="actions">{buttons}</div>' if buttons else ""
        next_p = PROJECTS[(i+1)%len(PROJECTS)]
        body = f'''<div class="back">{link("← Projects","projects.html","quiet",None)}</div>
        <div class="detail-top"><div>{eyebrow(p.category)}<h1>{p.title}</h1><p class="intro">{p.summary}</p>{actions}</div>{cover(p)}</div>
        <div class="detail-layout"><aside><h2>At a glance</h2><dl><dt>Role & context</dt><dd>{p.role}</dd><dt>Status</dt><dd>{p.status}</dd><dt>Stack</dt><dd>{' · '.join(p.stack)}</dd></dl></aside>
        <div class="article"><div class="flow" aria-label="System flow">{' <span aria-hidden="true">→</span> '.join(p.flow)}</div>{''.join(sections)}
        <div class="next">{link("Next case study · "+next_p.title,next_p.page)}</div></div></div>'''
        page(p.page,p.title,p.summary,body,"Projects")


def research():
    cards = []
    back = '<div class="back">' + link("← Research", "publications.html", "quiet", None) + '</div>'
    for entry in RESEARCH:
        resource = f'<div class="actions">{link(*entry.resource)}</div>' if entry.resource else ""
        cards.append(f'<article class="research-item"><div class="meta">{escape(entry.context)}</div>'
                     f'<h2>{link(entry.title, entry.page, "title-link", None)}</h2>'
                     f'<p>{escape(entry.summary)}</p>{resource}</article>')
        if entry.page == CAP:
            continue
        sections = ''.join(f'<section><h2>{escape(heading)}</h2><p>{escape(text)}</p></section>'
                           for heading, text in entry.sections)
        detail = (f'{back}<article class="research-detail"><div class="research-heading">'
                  f'{eyebrow(escape(entry.context))}<h1>{escape(entry.title)}</h1>'
                  f'<p class="intro">{escape(entry.summary)}</p>{resource}</div>'
                  f'<div class="article">{sections}</div></article>')
        page(entry.page, entry.title, entry.summary, detail, "Research")
    body = page_head("Research","Language & evaluation","Papers, lab work and early research on how language is produced, understood and measured.")
    page("publications.html","Research & publications","Read Max Xie’s capstone, lab research, conference poster and patent.",body+f'<div class="search" hidden><label for="research-query">Search research</label><input type="search" id="research-query" placeholder="Title, topic or institution"></div><div class="research-list">{"".join(cards)}</div><p id="search-status" role="status"></p>'+cta(),"Research")
    abstract = (ROOT/"tools/abstract.txt").read_text(encoding="utf8").strip()
    citation = f"Xie, P. (2026). {PAPER_TITLE} [M.A. capstone, San Francisco State University]."
    cap = next(p for p in PROJECTS if p.page == CAP)
    body = f'''{back}<div class="detail-top detail-heading"><div>{eyebrow("M.A. capstone · San Francisco State University")}
    <h1>{escape(PAPER_TITLE)}</h1>
    <p class="byline">Peixi Xie · Department of English · <time datetime="2026-04-01">April 1, 2026</time></p>
    </div>{cover(cap)}</div><div class="paper-summary"><section id="abstract" class="article paper-abstract"><h2>Abstract</h2><p>{escape(abstract)}</p></section>
    <div class="actions">{link("Read Paper",PAPER,"button primary","book")}{link("Source repository",cap.repo,"text-link","external")}</div></div>
    <div class="detail-layout"><aside><h2>In this study</h2><nav aria-label="Study sections"><a href="#abstract">Abstract</a><a href="#methodology">Methodology</a><a href="#findings">Findings</a><a href="#limits">Limitations</a><a href="#citation">Citation</a></nav></aside>
    <article class="article">
    <section id="methodology"><h2>One cohort, three tests</h2><p>I asked whether model rankings remain stable when static multiple-choice questions give way to recent reasoning tasks and expert language analysis. I ran GPT-5.4, Claude Sonnet 4.6, GLM-5.1 and MiniMax M2.7 through all three settings.</p>
    <ul><li><strong>MMLU</strong> — 480 questions across eight subjects, graded from the selected answer.</li><li><strong>LiveBench</strong> — 100 language and reasoning items, graded programmatically.</li><li><strong>Metalinguistics</strong> — 120 open-ended items scored by GPT-5.4 against a rubric, including syntax and phonology tasks.</li></ul></section>
    <section id="findings"><h2>What changed</h2><p>All four models scored above 85% on the selected MMLU questions. Claude Sonnet 4.6 led LiveBench at 84.6%, while the other three scored between 53.9% and 59.6%. GLM-5.1 led the metalinguistic tasks, closely followed by GPT-5.4.</p>
    <figure><img width="1200" height="720" src="assets/portfolio/benchmark-figure.webp" alt="Grouped bar chart comparing accuracy. Exact percentages are available in the table below." loading="lazy"><figcaption>Figure 1 from the paper, page 19. Accuracy on the selected benchmark subsets.</figcaption></figure>
    <details><summary>View figure data as a table</summary><table><thead><tr><th>Model</th><th>MMLU</th><th>LiveBench</th><th>Beguš</th></tr></thead><tbody>{''.join('<tr><th scope="row">'+name+'</th>'+''.join('<td>'+val+'%</td>' for val in vals)+'</tr>' for name,vals in [('GPT-5.4',('85.8','53.9','61.8')),('Sonnet 4.6',('95.4','84.6','57.4')),('GLM-5.1',('96.0','59.6','62.8')),('MiniMax M2.7',('90.6','59.5','37.7'))])}</tbody></table></details></section>
    <section id="limits"><h2>What the comparison can establish</h2><p>The subsets differ in difficulty, format and scoring. A drop on LiveBench cannot isolate training-data contamination. The linguistic scores depend on one model judge, and the analysis excludes requests that timed out or exhausted their token budgets.</p></section>
    <section id="citation"><h2>Citation</h2><blockquote>{citation}</blockquote><button id="copy-citation" class="button secondary" hidden>Copy citation</button><span role="status" id="copy-status"></span></section></article></div>'''
    paper_schema = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "url": SITE + CAP, "headline": PAPER_TITLE, "abstract": abstract,
        "genre": "M.A. capstone", "inLanguage": "en", "datePublished": "2026-04-01",
        "author": {"@type": "Person", "name": "Peixi Xie",
                   "affiliation": {"@type": "CollegeOrUniversity", "name": "San Francisco State University"}},
        "encoding": {"@type": "MediaObject", "contentUrl": SITE + PAPER, "encodingFormat": "application/pdf"},
    }
    page(CAP, PAPER_TITLE, cap.summary, body, "Research", schema=paper_schema)


def personal():
    rows=''.join(f'<li><span>{date}</span><div><strong>{title}</strong><p>{desc}</p></div></li>' for date,title,desc in EXPERIENCE)
    body = f'''<section class="bio-head"><div>{eyebrow("About Max")}<h1>Engineer by practice.<br><em>Linguist by training.</em></h1><p class="intro">I’m Peixi “Max” Xie, an AI engineer in San Francisco with a background in speech research and natural language processing.</p></div><img src="assets/portfolio/max.webp" alt="Portrait of Max Xie"></section>
    <section class="section ruled"><div class="split"><h2>From speech research to applied AI.</h2><div>
    <p>At UC Santa Cruz, I used ultrasound to study how the tongue moves during speech. At San Francisco State University, I earned an M.A. in Linguistics and an M.A. Computational Linguistics Certificate. My graduate research focused on AI-assisted text simplification and how four language models performed on knowledge, reasoning and linguistics tasks.</p>
    <p>I’m a nine-time hackathon winner. I use LangChain and Google ADK to prototype agent workflows. For one hackathon, my team used TRM APIs to help explain risk signals in cryptocurrency data. Across these projects, I work with Python, Java and SQL, and use Linux and Docker to run the services.</p></div></div></section>
    <section class="section ruled" id="experience">{eyebrow("Background")}<h2>Experience<span>.</span></h2><ul class="rows">{rows}</ul>{link("Visit QubeMC","https://www.qubemc.com/","text-link","external")}</section>
    <section class="section ruled"><div class="split"><h2>Languages.</h2><p>English, Mandarin, Cantonese and intermediate Spanish.</p></div></section>{cta()}'''
    page("about.html","About Max","Peixi Max Xie’s background in AI engineering, computational linguistics and Linux infrastructure.",body,"About")
    body = page_head("Contact","Let’s build something useful","Have a question about a project, a research idea or an engineering opportunity? I’d like to hear from you.")
    contacts = (
        ("Business email", EMAIL, "mailto:" + EMAIL),
        ("QubeMC business phone", "(415) 364-8613", "tel:+14153648613"),
        ("GitHub", "maxxie114", GITHUB),
        ("LinkedIn", "Peixi Xie", LINKEDIN),
    )
    contact_links = ''.join(f'<a href="{url}"><span class="meta">{label}</span><strong>{name}</strong>{icon("external")}</a>' for label,name,url in contacts)
    body += f'''<div class="contact-layout">
    <div class="contact-form-panel"><div id="JFWebsiteWidget-01a1bebbb8c070008b5b57e38de11e4efa68"></div></div>
    <nav class="contacts" aria-label="Direct contact and profiles">{contact_links}</nav></div>
    <script src="https://www.jotform.com/website-widgets/embed/01a1bebbb8c070008b5b57e38de11e4efa68" defer></script>'''
    page("contact.html","Contact","Send Max Xie a message, reach him by business email or phone, or find him on GitHub and LinkedIn.",body,"Contact")


def llms_guide():
    lines = [
        "# Peixi (Max) Xie",
        "",
        "> Portfolio of a San Francisco AI engineer and computational linguist. The site documents engineering projects, research at San Francisco State and UC Santa Cruz, and team hackathon awards.",
        "",
    ]
    sections = {
        "Portfolio": [
            ("About Max", "about.html", "Education, experience and research background."),
            ("Project index", "projects.html", "Browse project case studies by topic."),
            ("Research index", "publications.html", "Studies, lab work, conference poster and patent."),
            ("Hackathon recognition", "index.html#recognition", "Placements, projects and award records."),
            ("QubeMC", "index.html#qubemc", "Max’s startup and its focus on AI for gaming and game-server management."),
            ("Résumé", "resume.html", "Professional experience, education and downloadable résumé."),
            ("Contact", "contact.html", "Public contact channels."),
        ],
        "Research": [(r.title, r.page, r.summary) for r in RESEARCH] + [
            ("Capstone paper (PDF)", PAPER, "Full text of the M.A. capstone."),
            ("English /r/ conference poster (PDF)", POSTER, "Original poster with ultrasound images and tongue contours."),
        ],
        "Project case studies": [(p.title, p.page, p.summary) for p in PROJECTS if p.page != CAP],
    }
    for heading, entries in sections.items():
        lines.extend([f"## {heading}", ""])
        lines.extend(f"- [{name}]({SITE}{path}): {description}" for name, path, description in entries)
        lines.append("")
    return "\n".join(lines)


def compile_site():
    if hashlib.sha256((ROOT/RESUME_PDF).read_bytes()).hexdigest() != RESUME_PDF_SHA256:
        raise ValueError(f"Résumé integrity check failed for {RESUME_PDF}")
    for p in PROJECTS:
        if (p.repo is not None and not p.repo.startswith(GITHUB+"/")) or any(url != POSTER and not url.startswith("https://") for _,url in p.extra):
            raise ValueError(f"Unexpected public URL for {p.slug}")
    home()
    projects()
    research()
    personal()
    resume_body = (ROOT/"tools/resume-body.html").read_text(encoding="utf8")
    page("resume.html", "Résumé", "Peixi Max Xie’s résumé in computational linguistics, research and engineering.", resume_body, "Résumé")
    public_pages = list(PAGES)
    for alias, dest in [("home.html","index.html"),("self_introduction_max_en.html","about.html")]:
        page(alias,"Max Xie’s portfolio","Continue to the portfolio.",'<div class="page-head"><h1>Max Xie</h1>'+link("Continue",dest)+'</div>',canonical=dest,refresh=dest)
    page("404.html","Page unavailable","Find your way back to Max Xie’s portfolio.",page_head("404","Page unavailable","This address doesn’t lead to a portfolio page.")+link("Return home","index.html","button primary"))
    for filename,html in PAGES.items():
        (ROOT/filename).write_text(html+'\n',encoding="utf8")
    urls = [SITE+("" if f=="index.html" else f) for f in public_pages]
    (ROOT/"sitemap.xml").write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{url}</loc></url>' for url in urls)+'</urlset>\n',encoding="utf8")
    (ROOT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+SITE+"sitemap.xml\n",encoding="utf8")
    (ROOT/"llms.txt").write_text(llms_guide(), encoding="utf8")
    # Stage an allowlist so a private planner or editor file cannot enter a release.
    # Scholar associates the abstract with a PDF in the same directory.
    # Keep the earlier download URL working for existing links.
    shutil.copyfile(ROOT/PAPER_SOURCE, ROOT/PAPER)
    files = [*PAGES,RESUME_PDF,PAPER,PAPER_SOURCE,POSTER,"robots.txt","llms.txt","sitemap.xml","assets/css/main.css","assets/css/portfolio-v2.css","assets/js/portfolio-v2.js","assets/img/max_selfie.jpg","assets/bootstrap/css/bootstrap.min.css","assets/bootstrap/js/bootstrap.min.js","assets/fonts/fontawesome-all.min.css"]
    files.extend(str(p.relative_to(ROOT)) for p in (ROOT/"assets/fonts").glob("fa-*-*") if p.is_file())
    files.extend(a.local_record[1] for a in AWARDS if a.local_record)
    files.extend(f"assets/portfolio/covers/{p.slug}.webp" for p in PROJECTS)
    files.extend("assets/portfolio/"+fig.asset for figures in FIGURES.values() for fig in figures)
    files.extend("assets/portfolio/"+name for name in (
        "inter-latin.woff2","inter-license.txt","max.webp","qubemc-lobby.webp","benchmark-figure.webp","aml-baseline-curves.webp","litmus.svg","crypto-risk-agent.svg","icon.svg","social.png"))
    output=ROOT/"dist"
    with tempfile.TemporaryDirectory(dir=ROOT) as staging:
        stage=Path(staging)
        for name in files:
            dest=stage/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/name,dest)
        if output.exists():
            if output.is_symlink() or not (output/".portfolio-build").is_file():
                raise ValueError("dist already exists and is not a generated portfolio build")
            shutil.rmtree(output)
        (stage/".portfolio-build").touch()
        stage.rename(output)
    print(f"Built {len(PAGES)} HTML pages in dist. Résumé PDF SHA-256 check passed.")


if __name__ == "__main__":
    compile_site()


