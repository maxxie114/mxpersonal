# Max Xie’s portfolio

The source for [mxpersonal.com](https://www.mxpersonal.com/), Peixi “Max” Xie’s portfolio in AI engineering and computational linguistics. The [project case studies](https://www.mxpersonal.com/projects.html) cover work such as FoxStar Agent, browser agents, and graph neural networks. The [research collection](https://www.mxpersonal.com/publications.html) includes ECOLE Lab’s metaphor annotation work, an M.A. capstone on LLM evaluation, and a conference poster on English /r/.

## Run the site locally

The site serves static HTML, CSS, and JavaScript. Its build and validation scripts use only the Python standard library. From the repository root, run:

```sh
python tools/build.py
python tools/check.py
python -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open [the local preview](http://127.0.0.1:4173/). On Windows you can use `py -3.10` in place of `python`. After editing a source file, rerun the build and refresh the browser.

## Update the portfolio

| To change | Edit |
| --- | --- |
| Project descriptions, research entries, work experience, or awards | [tools/content.py](tools/content.py) |
| Featured projects, case-study figures, captions, or source credits | [tools/project_media.py](tools/project_media.py) and [assets/portfolio/](assets/portfolio/) |
| Homepage copy, navigation, page layouts, or the contact form embed | [tools/build.py](tools/build.py) |
| Styling or browser interactions | [portfolio-v2.css](assets/css/portfolio-v2.css) and [portfolio-v2.js](assets/js/portfolio-v2.js) |
| The web version of the résumé | [tools/resume-body.html](tools/resume-body.html) |

The build writes the generated pages to the repository root and assembles the public site in `dist/`. It also generates `robots.txt`, `sitemap.xml`, and `llms.txt`. The checker validates local links, research citation metadata, and the downloadable résumé’s checksum.

To publish an update, commit the edited sources, public assets, and regenerated root files together, then push to `master` for automated deployment. Git ignores `dist/`, local planning notes, and coding-assistant settings.
