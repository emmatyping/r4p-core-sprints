# CPython Rust API design discussion

A short introduction to the safe Rust API design for CPython extension
modules, for an audience of Python core developers. The 30-minute slot is
split into about nine minutes of slides and the rest for discussion.

```sh
npm install
npm run dev       # present at http://localhost:3030
npm run build     # static site in dist/
npm run export    # PDF (uses playwright-chromium)
```

`slides.md` has twelve introductory slides, followed by a blank screen. After
the closing invitation, advance once and leave the audience view blank for
the discussion. Presenter notes include timings, explanations of the
technical terms, and discussion prompts that do not appear on screen.

| Slides | Topic | Target time |
| --- | --- | --- |
| 1–2 | Review invitation and roadmap | 0:00–1:10 |
| 3 | API goals | 1:10–1:55 |
| 4–6 | C and Rust contracts, capabilities, common mistakes | 1:55–4:45 |
| 7 | Interpreter changes and explicit thread-state APIs | 4:45–5:45 |
| 8 | Core team confidence contributing in C and Rust | 5:45–6:20 |
| 9 | Core team interest in contributing in Rust | 6:20–6:55 |
| 10 | Dependency review, vendoring and acceptance criteria | 6:55–7:40 |
| 11 | Explore buffers, panics, dependencies and platform support | 7:40–8:55 |
| 12 | Invite discussion and repeat the PR link | 8:55–9:10 |
| 13 | Blank screen; discussion prompts in presenter notes | 9:10–30:00 |

The roadmap is copied from `../rust4cpython/slides.md`. The design content
follows `../cpython/RUST_API.md`; the review destination is
[PR 45](https://github.com/Rust-for-CPython/cpython/pull/45).

`deep-dive.md` is an older, longer walkthrough, kept for backup or follow-up;
it has not been revised with this short talk:
`npx slidev deep-dive.md`.

The talk uses the neversink theme (`orange-light`) with a softer cream
background and rounded cards and callouts in `styles/index.css`. It keeps
the original roadmap layout, a simple ordered list of goals, and a Mermaid
capability diagram.

Images live in `public/images`; Ferris and the Rust for CPython logo come
from the original talk. PR links use the theme’s `QRCode` component.
`components/IconTitle.vue` renders a slide title with a Ferris icon.

The two survey slides use 36 responses from the CPython core team survey.
Confidence is about contributing to CPython; the Rust question assumes a
PyO3-like API. Confidence and interest are shown separately. The charts
show counts for every rating, with the same count axis on the C and Rust
charts. The 4–5 summaries describe those ratings rather than assuming
verbal agreement categories: the CSV does not include the original scale
labels. Respondents are not necessarily representative of the whole team.

Aggregate counts and the exact questions are in
`data/core-team-survey-2026.json`; `components/SurveyCharts.vue` reads that
file for labels, response counts and percentages. Only aggregate data is
included in the deck. The raw CSV, timestamps and individual feedback are
not copied into the project.

To regenerate the three standalone SVG charts and aggregate data from the
CSV (Matplotlib is only needed for regeneration):

```sh
uv run --with matplotlib scripts/generate_survey_charts.py /path/to/survey.csv
```
