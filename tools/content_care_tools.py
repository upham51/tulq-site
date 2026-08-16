#!/usr/bin/env python3
"""
Two free public tools on tulqhealth.com.

    /tools/awv-revenue-calculator          the completion-gap calculator
    /tools/annual-wellness-visit-worksheet the 42 CFR 410.15 charting worksheet

Why these are public and ungated. The Aug 2026 research is explicit that a
DR-0 domain wins AI citations through third-party roundups and through
statistics-dense, genuinely useful pages, not through domain strength, and it
names ChartSpan's interactive savings calculator as a competitor proof asset.
An email wall would make both of these uncrawlable and unlinkable, which is
the entire value. So: no gate, no form, indexed, and linked from /resources/
and from the AWV money page.

A NOTE ON THE CALCULATOR, because it differs from the internal build.

The calculator supplied for this work was a *sales* tool. It embedded a
~600KB table of roughly 8,100 named practices with phone numbers, panel
sizes, and AWV counts, and it had "look up a practice", "size a territory",
and "your fee opportunity" modes written for a rep working a live call.

That is a prospecting database, and publishing it would have meant shipping a
competitor-ready call list of named practices, exposing TULQ's own per-visit
fee assumptions on a public page, and loading 600KB on a page aimed partly at
rural low-bandwidth readers. So the public tool here is the self-serve half
only: a practice enters its own panel and completion rate and sees its own
gap. Same arithmetic, same 2026 rates, no database and no rep view. The
internal tool should stay internal.
"""

from __future__ import annotations

from pathlib import Path

from landing import (
    LandingPage, band, breadcrumb_node, contact_close, crumbs, faq, faq_node,
    note, prose, section_links, sources,
)
from pagekit import CARE

SITE = CARE
FRAGMENTS = Path(__file__).resolve().parent / "fragments"

PFS_LOOKUP = "https://www.cms.gov/medicare/physician-fee-schedule/search"
ECFR_AWV = ("https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/"
            "part-410/subpart-B/section-410.15")
MEDICARE_AWV = "https://www.medicare.gov/coverage/yearly-wellness-visits"
CMS_AWV_MLN = ("https://www.cms.gov/outreach-and-education/medicare-learning-network-mln/"
               "mlnproducts/mln-publications/mln6775421")
CMS_TELEHEALTH = "https://www.cms.gov/medicare/coverage/telehealth"


# ══════════════════════════════════════════════════════════════════════
# /tools/awv-revenue-calculator
# ══════════════════════════════════════════════════════════════════════

CALC_CSS = """
.calc { max-width: 1000px; }
.calc-panel {
  background: rgba(255,255,255,.04);
  border: 1px solid var(--rule-dark);
  border-radius: 4px;
  padding: 30px 32px;
  margin-bottom: 16px;
}
.calc-legend {
  font-family: var(--mono); font-size: 10.5px; letter-spacing: .16em;
  text-transform: uppercase; color: rgba(232,228,216,.55);
  padding-bottom: 13px; margin-bottom: 22px; border-bottom: 1px solid var(--rule-dark);
}
.calc-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.calc-grid--2 { grid-template-columns: repeat(2, 1fr); }
@media (max-width: 820px) { .calc-grid, .calc-grid--2 { grid-template-columns: 1fr; } }

.calc-field label {
  display: block; font-size: 13.5px; color: rgba(232,228,216,.8);
  margin-bottom: 9px; font-weight: 500;
}
.calc-field label b {
  font-family: var(--mono); font-weight: 600; color: var(--amber);
  font-variant-numeric: tabular-nums;
}
.calc-field input[type=number] {
  width: 100%; font-family: var(--mono); font-size: 16px;
  background: rgba(255,255,255,.06); border: 1px solid var(--rule-dark);
  border-radius: 3px; padding: 12px 13px; color: var(--fog);
}
.calc-field input[type=number]:focus {
  outline: none; border-color: var(--river-tolt);
  box-shadow: 0 0 0 3px rgba(168,200,196,.16);
}
.calc-field input[type=range] {
  -webkit-appearance: none; appearance: none; width: 100%; height: 5px;
  border-radius: 999px; margin: 13px 0 3px;
  background: linear-gradient(90deg, var(--amber) 0%, var(--amber) var(--p,50%),
              rgba(255,255,255,.13) var(--p,50%));
}
.calc-field input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none; appearance: none; width: 19px; height: 19px;
  border-radius: 50%; background: var(--basalt); border: 2px solid var(--amber);
  box-shadow: 0 2px 8px rgba(217,138,74,.45); cursor: pointer;
}
.calc-field input[type=range]::-moz-range-thumb {
  width: 19px; height: 19px; border-radius: 50%; background: var(--basalt);
  border: 2px solid var(--amber); cursor: pointer;
}
.calc-hint { font-size: 12.5px; color: rgba(232,228,216,.5); margin-top: 8px; line-height: 1.5; }

.calc-headline {
  text-align: center; padding: 40px 30px; border-radius: 4px;
  background: linear-gradient(165deg, rgba(217,138,74,.16), rgba(255,255,255,.03) 68%);
  border: 1px solid rgba(217,138,74,.3);
}
.calc-headline-lab {
  font-family: var(--mono); font-size: 10.5px; letter-spacing: .16em;
  text-transform: uppercase; color: rgba(232,228,216,.6);
}
.calc-headline-val {
  font-family: var(--mono); font-weight: 600; font-size: clamp(40px, 8vw, 66px);
  line-height: 1; letter-spacing: -.03em; color: var(--amber);
  font-variant-numeric: tabular-nums; margin: 14px 0 9px;
}
.calc-headline-sub { font-size: 14.5px; color: rgba(232,228,216,.7); }

.calc-out { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 16px; }
@media (max-width: 820px) { .calc-out { grid-template-columns: 1fr; } }
.calc-stat {
  background: rgba(255,255,255,.05); border: 1px solid var(--rule-dark);
  border-radius: 4px; padding: 20px 21px;
}
.calc-stat-lab {
  font-family: var(--mono); font-size: 9.5px; letter-spacing: .14em;
  text-transform: uppercase; color: rgba(232,228,216,.5);
}
.calc-stat-val {
  font-family: var(--mono); font-size: 25px; font-weight: 600; margin-top: 7px;
  font-variant-numeric: tabular-nums; letter-spacing: -.02em; color: var(--fog);
}
.calc-stat-val.is-gold { color: var(--amber); }
.calc-stat-val.is-teal { color: var(--river-tolt); }
.calc-stat-note { font-size: 12px; color: rgba(232,228,216,.45); margin-top: 6px; line-height: 1.45; }
"""

CALC_JS = """
(() => {
  const $ = (id) => document.getElementById(id);
  const money = (v) => '$' + Math.round(v).toLocaleString();
  const num   = (v) => Math.round(v).toLocaleString();

  const RANGES = ['gotAwv', 'target', 'acp', 'dep'];
  const NUMS   = ['panel', 'rateFirst', 'rateSub', 'newShare'];

  function paintRange(el) {
    const pct = ((el.value - el.min) / (el.max - el.min)) * 100;
    el.style.setProperty('--p', pct + '%');
    const lab = $('l' + el.id.charAt(0).toUpperCase() + el.id.slice(1));
    if (lab) lab.textContent = el.value + '%';
  }

  function calc() {
    const panel     = Math.max(0, +$('panel').value || 0);
    const gotPct    = +$('gotAwv').value / 100;
    const targetPct = +$('target').value / 100;
    const rateFirst = Math.max(0, +$('rateFirst').value || 0);
    const rateSub   = Math.max(0, +$('rateSub').value || 0);
    const newShare  = Math.min(100, Math.max(0, +$('newShare').value || 0)) / 100;
    const acpPct    = +$('acp').value / 100;
    const depPct    = +$('dep').value / 100;

    // A visit is worth the initial rate for the share of patients who have
    // never had one, and the subsequent rate for everyone else.
    const blended = rateFirst * newShare + rateSub * (1 - newShare);

    // Same-day add-ons. ACP (99497) attaches to either visit type; the
    // depression screen (G0444) is only separately reportable alongside a
    // subsequent visit, so it is scaled by the non-initial share.
    const ACP_RATE = 85, DEP_RATE = 17;
    const addOn = ACP_RATE * acpPct + DEP_RATE * depPct * (1 - newShare);
    const perVisit = blended + addOn;

    const doneNow    = panel * gotPct;
    const doneTarget = panel * Math.max(targetPct, gotPct);
    const missed     = Math.max(0, doneTarget - doneNow);

    $('oGap').textContent  = money(missed * perVisit);
    $('oGapSub').textContent =
      num(missed) + ' additional completed visits a year, at an average of ' +
      money(perVisit) + ' per visit including same-day add-ons.';
    $('oNow').textContent    = money(doneNow * perVisit);
    $('oNowNote').textContent = num(doneNow) + ' visits at today\\u2019s completion rate.';
    $('oTarget').textContent = money(doneTarget * perVisit);
    $('oTargetNote').textContent = num(doneTarget) + ' visits at your target rate.';
    $('oVisits').textContent = num(missed);
    $('oHours').textContent  = num(missed * 0.5);
  }

  RANGES.forEach((id) => {
    const el = $(id);
    if (!el) return;
    paintRange(el);
    el.addEventListener('input', () => { paintRange(el); calc(); });
  });
  NUMS.forEach((id) => { const el = $(id); if (el) el.addEventListener('input', calc); });
  calc();
})();
"""

CALC_BODY = """    <div class="calc rise">
      <div class="calc-panel">
        <div class="calc-legend">Your panel</div>
        <div class="calc-grid">
          <div class="calc-field">
            <label for="panel">Medicare patients in your panel</label>
            <input type="number" id="panel" value="800" step="50" min="0" inputmode="numeric">
            <p class="calc-hint">Traditional Medicare. Advantage patients are contracted
              separately and are not counted here.</p>
          </div>
          <div class="calc-field">
            <label for="gotAwv">Share who had a wellness visit last year: <b id="lGotAwv">28%</b></label>
            <input type="range" id="gotAwv" min="0" max="100" value="28">
            <p class="calc-hint">If you do not know, most practices guess high. Pull the count of
              G0438 and G0439 claims you billed last year.</p>
          </div>
          <div class="calc-field">
            <label for="target">Target completion rate: <b id="lTarget">55%</b></label>
            <input type="range" id="target" min="0" max="100" value="55">
            <p class="calc-hint">What you could reach in year one if the visit stopped competing
              for an examination room.</p>
          </div>
        </div>
      </div>

      <div class="calc-panel">
        <div class="calc-legend">Rates, change any of these</div>
        <div class="calc-grid">
          <div class="calc-field">
            <label for="rateFirst">Initial visit, G0438</label>
            <input type="number" id="rateFirst" value="174" step="1" min="0" inputmode="numeric">
            <p class="calc-hint">2026 national average. Your locality will differ.</p>
          </div>
          <div class="calc-field">
            <label for="rateSub">Subsequent visit, G0439</label>
            <input type="number" id="rateSub" value="138" step="1" min="0" inputmode="numeric">
            <p class="calc-hint">The recurring one, and the one most practices leave unbilled.</p>
          </div>
          <div class="calc-field">
            <label for="newShare">Share who have never had one (percent)</label>
            <input type="number" id="newShare" value="20" step="5" min="0" max="100" inputmode="numeric">
            <p class="calc-hint">Those visits pay the initial rate. Everyone else pays the
              subsequent rate.</p>
          </div>
        </div>

        <div class="calc-legend" style="margin-top:30px">Same-day add-ons</div>
        <div class="calc-grid calc-grid--2">
          <div class="calc-field">
            <label for="acp">Advance care planning attached: <b id="lAcp">30%</b></label>
            <input type="range" id="acp" min="0" max="100" value="30">
            <p class="calc-hint">99497, about $85. The patient owes nothing when it is done on
              the same day as the wellness visit.</p>
          </div>
          <div class="calc-field">
            <label for="dep">Depression screen attached: <b id="lDep">40%</b></label>
            <input type="range" id="dep" min="0" max="100" value="40">
            <p class="calc-hint">G0444, about $17, separately reportable alongside a subsequent
              visit only.</p>
          </div>
        </div>
      </div>

      <div class="calc-headline">
        <div class="calc-headline-lab">Annual wellness visit revenue you are not billing</div>
        <div class="calc-headline-val" id="oGap">$0</div>
        <div class="calc-headline-sub" id="oGapSub"></div>
      </div>

      <div class="calc-out">
        <div class="calc-stat">
          <div class="calc-stat-lab">Billing today</div>
          <div class="calc-stat-val" id="oNow">$0</div>
          <div class="calc-stat-note" id="oNowNote"></div>
        </div>
        <div class="calc-stat">
          <div class="calc-stat-lab">At your target rate</div>
          <div class="calc-stat-val is-gold" id="oTarget">$0</div>
          <div class="calc-stat-note" id="oTargetNote"></div>
        </div>
        <div class="calc-stat">
          <div class="calc-stat-lab">Visits to add per year</div>
          <div class="calc-stat-val is-teal" id="oVisits">0</div>
          <div class="calc-stat-note">Roughly <span id="oHours">0</span> clinical hours at half
            an hour each, which is the part you have to staff.</div>
        </div>
      </div>
    </div>"""


def page_calculator() -> LandingPage:
    qa = [
        ("Where do the default rates come from?",
         "<p>They are 2026 national averages under the Medicare Physician Fee Schedule: about "
         "$174 for an initial annual wellness visit (G0438) and about $138 for each subsequent "
         "one (G0439). Both are adjusted by locality and updated every January, so treat the "
         "defaults as a starting point and overwrite them with your own carrier's amounts.</p>"
         '<p><a class="faq-source" href="' + PFS_LOOKUP + '" target="_blank" '
         'rel="noopener">Source: CMS Physician Fee Schedule lookup</a></p>'),

        ("What completion rate is realistic?",
         "<p>Practices consistently overestimate their current rate, which is why the "
         "calculator asks you to pull the actual count of G0438 and G0439 claims rather than "
         "estimate. The target slider is deliberately yours to set: what is achievable depends "
         "far more on whether the visit has to occupy an examination room than on anything "
         "clinical.</p>"),

        ("Why are advance care planning and the depression screen included?",
         "<p>Because they are the two add-ons most often left unbilled, and both are legitimate "
         "on the same day. Advance care planning (99497) pays roughly $85 and carries no "
         "patient cost sharing when furnished on the same day as the wellness visit. The "
         "depression screen (G0444) pays roughly $17 and is separately reportable alongside a "
         "subsequent visit, so the calculator scales it by the share of visits that are not "
         "initial ones.</p>"
         "<p>Set either slider to zero if you would rather see the visit revenue alone.</p>"),

        ("Does this include care management revenue?",
         "<p>No, deliberately. The wellness visit is a once-a-year payment. The recurring money "
         "is in chronic care management and advanced primary care management, which pay monthly "
         "and for which the wellness visit is a qualifying visit. Mixing them would flatter the "
         'number. <a href="/services/care-management">Care management is costed separately'
         "</a>.</p>"),

        ("Is any of this sent anywhere?",
         "<p>No. The calculator runs entirely in your browser. Nothing is transmitted, nothing "
         "is stored, and there is no form to fill in. Reload the page and it resets.</p>"),
    ]

    page = LandingPage(
        site=SITE,
        slug="tools/awv-revenue-calculator",
        title="Medicare AWV Revenue Gap Calculator | Free | TULQ",
        description=(
            "Free calculator: enter your Medicare panel and completion rate to see the annual "
            "wellness visit revenue your practice is not billing. 2026 rates, no signup."
        ),
        h1="What your <em>uncompleted</em> wellness visits are worth.",
        hero_sub=(
            "A free calculator for the Medicare annual wellness visit completion gap. Enter "
            "your panel and what you billed last year, and see the difference in dollars."
        ),
        hero_eyebrow="Free tool · No signup",
        hero_facts=("2026 national averages", "Runs in your browser", "Nothing is sent anywhere"),
        hero_scene="pines",
        hero_ctas=(
            '<a class="btn btn-primary" href="#calculator" data-magnetic>Run the numbers</a>'
            '<a class="btn btn-ghost" href="/services/medicare-annual-wellness-visits">'
            "See the AWV service</a>"
        ),
        extra_css=CALC_CSS,
        extra_js=CALC_JS,
        priority="0.8",
        reviewed=True,
    )
    trail = [("Tools", "/resources/"), ("AWV revenue calculator", "/tools/awv-revenue-calculator")]

    page.sections = [
        crumbs(trail),

        band(
            prose(
                "      <p>The annual wellness visit pays well, costs the patient nothing, and is "
                "the qualifying visit that makes chronic care management enrollment possible. "
                "Most practices complete it for a minority of their eligible panel, and almost "
                "none of them know the size of the gap in dollars.</p>\n"
                "      <p>This calculates it. Everything updates live, every assumption is "
                "editable, and nothing is sent anywhere.</p>"
            ),
            eyebrow="What this is",
            h2="The gap, in dollars, in <em>about thirty seconds.</em>",
            scene="premise",
        ),

        band(
            CALC_BODY,
            dark=True,
            anchor="calculator",
            eyebrow="The calculator",
            h2="Your panel, your rates.",
            deck="Defaults are 2026 national averages. Overwrite any of them with your own "
                 "carrier's amounts.",
            scene="totem",
        ),

        band(
            note(
                "<p><strong>These are estimates, and they are not a quote.</strong> Payment "
                "amounts are 2026 national averages under the Medicare Physician Fee Schedule "
                "and are adjusted by geography, so your locality will differ. Add-on codes have "
                "their own coverage and documentation rules. Check the "
                f'<a href="{PFS_LOOKUP}" target="_blank" rel="noopener">CMS fee schedule '
                "lookup</a> for your own carrier before making a decision on these numbers. "
                "Nothing here is billing, coding, or legal advice for your practice.</p>",
                kind="caution",
            )
            + "\n" + section_links([
                ("How outsourced AWVs work", "/services/medicare-annual-wellness-visits"),
                ("The AWV documentation worksheet", "/tools/annual-wellness-visit-worksheet"),
                ("Care management, the recurring revenue", "/services/care-management"),
            ]),
            eyebrow="Read the small print",
            h2="What this number is, and is not.",
            scene="why",
        ),

        band(
            faq(qa),
            dark=True,
            eyebrow="Common questions",
            h2="About the arithmetic.",
            extra_class="faq-section",
            scene="pines",
        ),

        band(
            sources(
                [
                    ("CMS Physician Fee Schedule lookup", PFS_LOOKUP),
                    ("42 CFR 410.15, annual wellness visit", ECFR_AWV),
                    ("CMS Medicare Wellness Visits, MLN6775421", CMS_AWV_MLN),
                    ("Medicare.gov yearly wellness visits", MEDICARE_AWV),
                ],
                disclaimer="Rates reviewed August 2026 against the 2026 Medicare Physician Fee "
                           "Schedule. National averages, adjusted by locality, updated each "
                           "January.",
            ),
            eyebrow="Sources",
            h2="Where the defaults come from.",
            scene="bio",
        ),

        contact_close(
            "Bring the number to a fifteen minute call.",
            "We will run the same arithmetic against your real locality rather than a national "
            "average, and tell you what closing the gap would actually cost.",
            cap_title="Program design &amp; compliance",
            cap_body="Visit workflow, supervision model, and a sample completed AWV note.",
        ),
    ]

    page.schema = [
        breadcrumb_node(page, trail),
        {
            "@type": "WebApplication",
            "@id": f"{page.url}#app",
            "name": "Medicare AWV Revenue Gap Calculator",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Any modern web browser",
            "browserRequirements": "Requires JavaScript",
            "url": page.url,
            "description": "A free browser-based calculator that estimates the Medicare annual "
                           "wellness visit revenue a practice is not billing, from its panel "
                           "size and current completion rate, using 2026 national average "
                           "fee schedule rates.",
            "publisher": {"@id": SITE.org_id},
            "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        },
        faq_node(page, qa),
    ]
    return page


# ══════════════════════════════════════════════════════════════════════
# /tools/annual-wellness-visit-worksheet
# ══════════════════════════════════════════════════════════════════════

def page_worksheet() -> LandingPage:
    qa = [
        ("Is any patient information sent to TULQ?",
         "<p>No. The worksheet runs entirely in your browser. Nothing you type is transmitted "
         "to us or to anyone else, and no patient information is written to storage. The only "
         "values that persist between sessions are your own operator details, the nurse name, "
         "supervising physician, and practice, and only if you press save. The session also "
         "wipes itself after twenty minutes of inactivity.</p>"),

        ("What is it built to?",
         "<p>The elements of the annual wellness visit as they are defined at 42 CFR 410.15. "
         "Each section carries the sub-paragraph it corresponds to, and the tool distinguishes "
         "the elements required at an initial visit from those required at a subsequent one, so "
         "a subsequent visit shows only what applies.</p>"
         '<p><a class="faq-source" href="' + ECFR_AWV + '" target="_blank" rel="noopener">'
         "Source: 42 CFR 410.15</a></p>"),

        ("Why is it built around confirming rather than typing?",
         "<p>Because most of an annual wellness visit is confirming that nothing has changed. A "
         "worksheet that demands free text for every element takes far longer than the visit is "
         "worth and produces notes nobody can audit consistently. Every section here closes in "
         "one tap when there is nothing to record, and opens only when there is.</p>"),

        ("Does it replace our EHR?",
         "<p>No. It produces a structured note for you to paste or file into your own record. "
         "It holds nothing, integrates with nothing, and is not a system of record. Think of it "
         "as the paper you would otherwise have printed.</p>"),

        ("Can we use it if we are not a TULQ client?",
         "<p>Yes. It is free, ungated, and there is nothing to sign up for. We built it for our "
         "own nurses and there was no good reason to keep it to ourselves.</p>"),
    ]

    body = (FRAGMENTS / "awv-worksheet-body.html").read_text(encoding="utf-8")

    page = LandingPage(
        site=SITE,
        slug="tools/annual-wellness-visit-worksheet",
        title="Free Annual Wellness Visit Worksheet | 42 CFR 410.15",
        description=(
            "A free browser-based Medicare annual wellness visit worksheet built to the "
            "elements at 42 CFR 410.15. Generates a structured note. No patient data leaves it."
        ),
        h1="Annual wellness visit, <em>confirm and go.</em>",
        hero_sub=(
            "A free charting worksheet built to the annual wellness visit elements at 42 CFR "
            "410.15. Every section closes in one tap when there is nothing to record."
        ),
        hero_eyebrow="Free tool · No signup",
        hero_facts=("Built to 42 CFR 410.15", "Runs in your browser",
                    "No patient data leaves the page"),
        hero_scene="pines",
        hero_ctas=(
            '<a class="btn btn-primary" href="#worksheet" data-magnetic>Open the worksheet</a>'
            '<a class="btn btn-ghost" href="/services/medicare-annual-wellness-visits">'
            "See the AWV service</a>"
        ),
        extra_head='<link rel="stylesheet" href="{p}awv-worksheet.css" />',
        extra_css=(
            # The tool keeps its own dark app canvas, scoped under .awv-tool.
            # It is inset on the dark band rather than restyled to cream: a
            # dense clinical data-entry grid is genuinely easier to work in on
            # a dark ground, and the surrounding page carries the site look.
            ".awv-stage { margin: 0 -18px; }\n"
            ".awv-tool { border: 1px solid var(--rule-dark); border-radius: 4px; overflow: hidden; }\n"
            ".awv-tool .shell { padding-top: 26px; }\n"
            "@media (max-width: 720px) { .awv-stage { margin: 0 -10px; } }\n"
        ),
        extra_js='<script src="{p}awv-worksheet.js"></script>',
        priority="0.8",
        reviewed=True,
    )
    trail = [("Tools", "/resources/"),
             ("AWV worksheet", "/tools/annual-wellness-visit-worksheet")]

    page.sections = [
        crumbs(trail),

        band(
            prose(
                "      <p>Most of an annual wellness visit is confirming that nothing has "
                "changed. The history is the same, the medication list is the same, the "
                "specialists are the same. A worksheet that demands free text for every element "
                "turns that into thirty minutes of typing and produces notes that are hard to "
                "audit consistently.</p>\n"
                "      <p>This one inverts it. Sections stay collapsed until you open them, and "
                "each closes in a single tap: no change since last visit, nothing abnormal, or "
                "patient declined. You open a section only when there is something to record. A "
                "subsequent visit shows only the nine required elements plus the two "
                "discretionary ones.</p>\n"
                "      <p>It is free, there is nothing to sign up for, and nothing you type "
                "leaves your browser.</p>"
            ),
            eyebrow="Why it works this way",
            h2="Built for the visit where <em>nothing has changed.</em>",
            scene="premise",
        ),

        f'<section class="section section-dark" id="worksheet" data-screen-label="The worksheet">\n'
        f'  <div class="container">\n'
        f'    <div class="awv-stage">\n      <div class="awv-tool">\n{body}\n      </div>\n    </div>\n'
        f"  </div>\n</section>",

        band(
            note(
                "<p><strong>This is a documentation aid, not clinical or billing advice.</strong> "
                "It reflects the annual wellness visit elements at 42 CFR 410.15 as of August "
                "2026. Coverage rules, supervision requirements, and payment change, and your "
                "own payer and organizational policies govern. The clinician performing and the "
                "practice billing the visit remain responsible for the accuracy and adequacy of "
                "the record.</p>",
                kind="caution",
            )
            + "\n" + section_links([
                ("How outsourced AWVs work", "/services/medicare-annual-wellness-visits"),
                ("What your completion gap is worth", "/tools/awv-revenue-calculator"),
                ("Care management, the recurring revenue", "/services/care-management"),
            ]),
            eyebrow="Read the small print",
            h2="What this tool is, and is not.",
            scene="why",
        ),

        band(
            faq(qa),
            dark=True,
            eyebrow="Common questions",
            h2="About the worksheet.",
            extra_class="faq-section",
            scene="pines",
        ),

        band(
            sources(
                [
                    ("42 CFR 410.15, annual wellness visit", ECFR_AWV),
                    ("CMS Medicare Wellness Visits, MLN6775421", CMS_AWV_MLN),
                    ("Medicare.gov yearly wellness visits", MEDICARE_AWV),
                    ("CMS Medicare telehealth", CMS_TELEHEALTH),
                ],
                disclaimer="Element set reviewed August 2026 against 42 CFR 410.15.",
            ),
            eyebrow="Sources",
            h2="What the element set is built from.",
            scene="bio",
        ),

        contact_close(
            "If the worksheet is useful, the nurses behind it might be too.",
            "TULQ supplies compact-licensed registered nurses who complete annual wellness "
            "visits by telephone and return the finished documentation to your clinic. Priced "
            "per completed visit.",
            cap_title="Program design &amp; compliance",
            cap_body="Visit workflow, supervision model, and a sample completed AWV note.",
        ),
    ]

    page.schema = [
        breadcrumb_node(page, trail),
        {
            "@type": "WebApplication",
            "@id": f"{page.url}#app",
            "name": "Annual Wellness Visit Worksheet",
            "applicationCategory": "HealthApplication",
            "operatingSystem": "Any modern web browser",
            "browserRequirements": "Requires JavaScript",
            "url": page.url,
            "description": "A free browser-based charting worksheet for the Medicare annual "
                           "wellness visit, structured to the elements at 42 CFR 410.15, which "
                           "generates a copyable structured note. Runs entirely client-side and "
                           "transmits no patient information.",
            "publisher": {"@id": SITE.org_id},
            "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        },
        faq_node(page, qa),
    ]
    return page


def pages() -> list[LandingPage]:
    return [page_calculator(), page_worksheet()]
