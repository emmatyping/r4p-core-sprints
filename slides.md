---
theme: neversink
addons:
  - window-mockup
title: Rust for CPython Core Dev Sprints
info: |
  An approximately nine-minute introduction followed by discussion of the proposed
  safe Rust API for in-tree CPython extension modules.
layout: cover
class: talk-cover
color: orange-light
defaults:
  color: orange-light
  class: talk
transition: fade
mdc: true
drawings:
  persist: false
---

<div class="flex items-center justify-between gap-8">
<div>
  <h1>Rust for CPython</h1>
</div>
<img class="w-64 h-64 shrink-0" src="/images/r4p.svg" alt="Rust for CPython logo" />
</div>

<div class="absolute bottom-8 left-8 text-sm">Emma Smith - 2026-10-20</div>

---
layout: default
---

<IconTitle icon="unsafe_ferris">How Rust handles common C API mistakes</IconTitle>

<div class="error-columns">
  <span>C API: mistake in extension code</span>
  <span>Rust API: how it’s handled</span>
</div>

<div class="error-groups">
  <section class="error-group error-group--compile">
    <h3>Compile time</h3>
    <div class="error-row"><p>Use a borrowed pointer after its owner is released.</p><p>Lifetimes tie the borrow to its owner and reject that use.</p></div>
  </section>
  <section class="error-group error-group--runtime">
    <h3>Runtime</h3>
    <div class="error-row"><p>Cast an object to an improper Python type.</p><p>By default, check the Python type before creating a typed handle.</p></div>
  </section>
  <section class="error-group error-group--mixed">
    <h3>Compile time + runtime</h3>
    <div class="error-row"><p>Miss a decref, or decref twice.</p><p>Ownership prevents double release and objects created in local scope automatically dropped at end of scope.</p></div>
    <div class="error-row"><p>Use an object while detached or in the wrong interpreter.</p><p>Require a capability at compile time to call into the interpreter; check interpreter identity at runtime.</p></div>
  </section>
</div>

<!--
3:50–4:45 · 55 seconds

The left column describes mistakes in C extension code; the right shows
how the Rust API handles them. The group headings describe when Rust's
checks or automatic handling take effect.

Compile time: the compiler rejects a borrow that outlives its owner.
Runtime: Python types are dynamic, so the API checks them before creating
a typed handle.

The mixed group combines static guarantees with work done at runtime.
Ownership prevents consuming a handle twice, while Drop automatically
queues reference release on ordinary returns and error paths. A missed
manual decref is avoided by this cleanup; it is not a runtime error check.
The queued decref does not necessarily destroy the object immediately.

Context arguments establish permission to use Python at compile time;
stored handles also need an interpreter-identity check at runtime.
Result carries an explicit success or exception in Rust, while wrappers
check the error indicators of C calls at runtime.

Safe Rust still allows deliberate leaks and logic bugs. The goal is to
prevent memory-unsafe uses through the safe interface.
-->

---
layout: default
---

<IconTitle icon="ferris_thinking">Changes needed in CPython C code</IconTitle>

<div class="talk-columns runtime-options">
  <div class="card">
    <h3>Required by the current safety design</h3>
    <p>Block attach, detach, and swap operations on a thread while its Rust context is available. Prevent clearing or deleting the thread state while Rust still depends on it.</p>
    <p>Keep the interpreter alive while a Rust call still depends on it.</p>
  </div>
  <div class="card">
    <h3>Performance improvement changes</h3>
    <p>Add private C APIs that take <code>PyThreadState *</code> explicitly, instead of repeatedly looking up the current state.</p>
  </div>
</div>

<!--
4:45–5:45 · 60 seconds

A library-only wrapper is not enough for this particular design. Another
extension can change thread state, or finalization can start while Rust
still has references into interpreter-owned memory. The current proposal
therefore needs runtime checks, lifetime protection and deferred releases.

The attachment checks apply to the current OS thread while its Rust context
is available. Suspending the context permits attachment changes. A separate
per-state protection count prevents clearing or deletion until Rust is done
with the state, including while detached; it does not reserve the state
against attachment by another thread.

Those safety mechanisms are separate from possible optimizations. Passing
an explicit thread state could avoid repeated thread-local lookups on hot
paths without changing the Rust-facing API. I don't want to imply a speedup
before measuring it, or assume that a new API has to be public.

For the discussion: where would you draw the boundary? Would broader C API
usefulness matter, or could a private change justified by Rust be enough?
What evidence would make the maintenance and performance cost acceptable?
-->

---
layout: default
---

<IconTitle icon="ferris_thinking">Confidence contributing to CPython</IconTitle>

<SurveyCharts kind="confidence" />

<!--
5:45–6:20 · 35 seconds

These are 36 responses from CPython core team members. The questions ask
about confidence contributing to CPython, rather than general proficiency
in a language. The Rust question specifically assumes a PyO3-like Rust API.

Both charts use the same response-count axis and show every rating from
1 to 5. C has 25 ratings of 4 or 5; Rust has 9. These are self-reported
ratings from respondents, not an assessment of the whole core team.

The CSV does not include verbal scale anchors, so the charts retain the
numeric ratings. The source questions and aggregate counts are saved with
the deck. No individual feedback is quoted here.
-->

---
layout: default
---

<IconTitle icon="ferris_smile">Interest in contributing in Rust</IconTitle>

<SurveyCharts kind="interest" />

<!--
6:20–6:55 · 35 seconds

This is a separate question to the same 36 core team respondents:
"I am interested in contributing to CPython in Rust."

The full distribution is 2, 4, 11, 8 and 11 responses at ratings 1 through 5.
Nineteen respondents rated it 4 or 5, about 53 percent. Eleven chose 3 and
six chose 1 or 2. The CSV does not retain verbal scale labels, so we show
numeric ratings rather than inventing agreement categories.

Interest and confidence are different questions. This is useful context
for discussing what documentation, examples and review support a Rust API
would need; it is not a vote on adopting this design.
-->

---
layout: default
---

<IconTitle icon="ferris_thinking">Managing Rust dependencies</IconTitle>

<div class="takeaway dependency-policy"><b>Proposed policy:</b> all new dependencies must be reviewed before inclusion. All dependency sources will be vendored by default.</div>

<div class="card dependency-criteria">
  <h3>Criteria for new dependencies</h3>
  <ol>
    <li><b>Tiered platforms:</b> must support every tiered platform or provide a portable fallback.</li>
    <li><b>Other platforms:</b> should not substantially narrow CPython’s platform support.</li>
    <li><b>Dependency footprint:</b> should have few required dependencies, including transitive crates.</li>
    <li><b>Build time:</b> should not significantly slow CPython’s builds.</li>
    <li><b>Build integration:</b> should be practical on each platform; consult platform maintainers.</li>
  </ol>
</div>

<!--
6:55–7:40 · 45 seconds

One concern is that a small Rust dependency could bring in a large required
dependency tree and increase build or maintenance costs.

The proposal is to review new dependencies before adding them and vendor
all dependency sources by default. Review should include required
transitive crates and the features we enable, not just the direct entries
in Cargo.toml. Vendoring is the default source-distribution policy; the
acceptance criteria still apply to each addition.

A dependency must work on every tiered platform, directly or through a
portable fallback. We should also preserve broad support outside those
platforms, keep the required dependency tree small, and avoid a significant
build-time penalty. Build integration must be practical for each platform,
so consult platform maintainers before settling on a dependency.
-->

---
layout: default
---

<IconTitle icon="ferris_question">Topics for discussion</IconTitle>

<div class="question-grid">
  <div class="card">
    <h3>1. API design</h3>
    <p>Any thoughts, questions, or ideas for the new Rust API?</p>
  </div>
  <div class="card">
    <h3>2. Making Rust work for contributors</h3>
    <p>While there is a lack of confidence in contributing to CPython in Rust, there is significant interest.</p>
  </div>
  <div class="card">
    <h3>3. Dependency management</h3>
    <p>Do our rules for introducing and auditing dependencies make sense?</p>
  </div>
  <div class="card">
    <h3>4. Platform support</h3>
    <p>Where do we draw the line on platform support? Obviously tiered platforms must be supported, but what about other platforms?</p>
  </div>
</div>

<div class="flex items-center gap-5 mt-8">
    <QRCode value="https://github.com/Rust-for-CPython/cpython/pull/45" :size="104" :margin="4" render-as="svg" aria-label="QR code for the design pull request" />
    <div class="text-lg leading-snug">
      API design draft<br/>
      <a href="https://github.com/Rust-for-CPython/cpython/pull/45">Rust-for-CPython/cpython#45</a>
    </div>
  </div>

<!--
7:40–8:55 · 75 seconds

These are the issues I most want to explore with the group, in this order.

First, buffers. Keeping memory alive is not enough to justify a Rust slice:
another thread may still mutate a writable exporter. We need to decide
which copying, locking or exporter guarantees are realistic.

Second, panic handling. The current design uses panic=unwind and catches
ordinary function panics as SystemError. Traversal panics and some failed
cleanup paths must abort because continuing could violate safety. Which
boundaries and recovery policies should we support?

Third, dependency management. We have proposed review before adding new
dependencies, vendored sources by default, and criteria for portability,
dependency count, build time and integration. Are these criteria sufficient,
and how should we review changes to the required dependency graph?

Fourth, platform support. Tiered platforms must work, with a portable
fallback if necessary. How much support should we promise beyond them?
Consult platform maintainers early about the practical build implications.
This is an invitation to explore the design, rather than a list of decisions
to settle during the introduction.
-->
