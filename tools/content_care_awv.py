#!/usr/bin/env python3
"""
tulqhealth.com/awv - the plain English guide to how a nurse-run annual
wellness visit gets paid.

Why this page exists as its own URL, given two AWV pages already do:

    /services/medicare-annual-wellness-visits   the money page. Targets
        "annual wellness visit outsourcing". Sells the service, quotes the
        rates, and states the supervision nuance in one inset note.
    /resources/who-can-perform-annual-wellness-visit   the resource post.
        Targets "who can perform an annual wellness visit", an evaluative
        query, and separates performing from billing.
    /awv   this page. Targets the trust question a compliance officer or a
        practice administrator asks after the sales call: show me the rule.
        It walks the whole chain, rule by rule, and describes the workflow
        end to end rather than the offer.

Per the one-segment-one-page rule in CLAUDE.md, this page does not quote
per-visit reimbursement and does not argue completion rates. Those belong
to the money page and to /resources/increase-awv-completion-rates
respectively, and this page links to both rather than restating them.

The regulatory spine, all three legs verified against the eCFR text as of
August 2026 rather than from memory:

    42 CFR 410.15        "health professional" includes a medical
                         professional, or a team of them, working under the
                         direct supervision of a physician.
    42 CFR 410.26(a)(1)  "auxiliary personnel" is any individual acting
                         under the physician's supervision, regardless of
                         whether they are an employee, a leased employee,
                         or an independent contractor.
    42 CFR 410.32(b)(3)(ii) and 410.26(a)(2)
                         direct supervision means present in the office
                         suite and immediately available, and that presence
                         may be virtual, through real-time audio and video
                         excluding audio-only, for services without a 010
                         or 090 global surgery indicator. Adopted
                         permanently in the CY2026 Physician Fee Schedule
                         final rule, 90 FR 50007, effective 1 January 2026.

That third leg is newer than the rest of the site. Two pages written before
the CY2026 rule still described direct supervision as office-suite-only,
and were corrected in the same change that added this page. If a future
edit reintroduces "not reachable by phone" as the whole of the definition,
it is wrong: check the current text of 410.32(b)(3)(ii) before restoring it.

The URL is /awv, the correct acronym and the one the rest of the repo
already uses (awv-worksheet.js, /tools/awv-revenue-calculator). care/_redirects
sends the common transposition /avw to it with a 301.
"""

from __future__ import annotations

from landing import (
    LandingPage, band, breadcrumb_node, contact_close, crumbs, faq, faq_node,
    ledger, prose, section_links, service_node, source_link, sources, split,
)
from pagekit import CARE

SITE = CARE

# ── Sources. Every one requested and returning 200 in August 2026; the
#    eCFR sections were additionally read through the eCFR versioner API,
#    which is the same text the HTML pages render. See CLAUDE.md: link the
#    primary document, never a summary of it.
ECFR_410_15 = ("https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/"
               "part-410/subpart-B/section-410.15")
ECFR_410_26 = ("https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/"
               "part-410/subpart-B/section-410.26")
ECFR_410_32 = ("https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/"
               "part-410/subpart-B/section-410.32")
CMS_PFS_2026 = ("https://www.cms.gov/newsroom/fact-sheets/calendar-year-cy-2026-"
                "medicare-physician-fee-schedule-final-rule-cms-1832-f")
FR_PFS_2026 = ("https://www.federalregister.gov/documents/2025/11/05/2025-19787/"
               "medicare-and-medicaid-programs-cy-2026-payment-policies-under-the-"
               "physician-fee-schedule-and-other")
CMS_AWV_MLN = ("https://www.cms.gov/outreach-and-education/medicare-learning-network-mln/"
               "mlnproducts/mln-publications/mln6775421")
MEDICARE_AWV = "https://www.medicare.gov/coverage/yearly-wellness-visits"
CMS_TELEHEALTH = "https://www.cms.gov/medicare/coverage/telehealth"
PFS_LOOKUP = "https://www.cms.gov/medicare/physician-fee-schedule/search"


# ── Page-scoped components ────────────────────────────────────────────
#
# Two shapes this page needs that the shared vocabulary does not have: a
# three-link chain of rules where each link visibly depends on the one
# before it, and a hand-off timeline where every row carries an owner.
# They are used once, on one page, so they live here as extra_css rather
# than in the LANDING PAGES block of care/styles.css. Everything is
# namespaced .awv- and scoped to a dark band.

AWV_CSS = """
/* ── The chain of three rules. Each link is a card with a citation, the
   rule in plain English, and a floor-mounted consequence line. The
   connector is drawn on the second and third links so the row reads as
   one dependent chain rather than three independent claims. ── */
.awv-chain {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  align-items: stretch;
}
.awv-link {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 34px 30px 30px;
  background: rgba(20, 28, 30, .5);
  border: 1px solid var(--rule-dark);
  border-radius: 4px;
  transition: border-color .45s var(--ease-out-soft), background .45s var(--ease-out-soft);
}
.awv-link:hover {
  border-color: rgba(168, 200, 196, .3);
  background: rgba(20, 28, 30, .62);
}
.awv-link + .awv-link::before {
  content: "";
  position: absolute;
  left: -31px;
  top: 57px;
  width: 31px;
  height: 1px;
  background: linear-gradient(90deg, rgba(168, 200, 196, .12), rgba(168, 200, 196, .5));
}
.awv-link + .awv-link::after {
  content: "";
  position: absolute;
  left: -19px;
  top: 53px;
  width: 7px;
  height: 7px;
  border: 1px solid rgba(168, 200, 196, .55);
  background: var(--basalt);
  transform: rotate(45deg);
}
.awv-num {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  margin-bottom: 22px;
  font-family: var(--serif);
  font-size: 19px;
  line-height: 1;
  color: var(--river-tolt);
  background: rgba(168, 200, 196, .08);
  border: 1px solid rgba(168, 200, 196, .3);
}
.awv-cite {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--amber);
  margin-bottom: 10px;
}
.awv-link h3 {
  font-family: var(--serif);
  font-weight: 400;
  font-size: 26px;
  line-height: 1.18;
  letter-spacing: -.01em;
  color: var(--fog);
  margin: 0 0 14px;
}
.awv-link p {
  font-size: 16px;
  line-height: 1.68;
  color: rgba(232, 228, 216, .72);
  margin: 0 0 18px;
}
.awv-link strong { color: var(--fog); font-weight: 600; }
/* Footers sit on the card floor, with the min-height the longest one
   needs, so the dashed rules stay level across the row. */
.awv-so {
  margin-top: auto;
  min-height: 74px;
  padding-top: 16px;
  border-top: 1px dashed rgba(232, 228, 216, .18);
  font-family: var(--mono);
  font-size: 11.5px;
  line-height: 1.65;
  letter-spacing: .02em;
  color: rgba(232, 228, 216, .58);
}
.awv-so b { color: var(--river-tolt); font-weight: 500; }

@media (max-width: 900px) {
  .awv-chain { grid-template-columns: 1fr; gap: 34px; }
  .awv-link + .awv-link::before {
    left: 52px; top: -34px; width: 1px; height: 34px;
    background: linear-gradient(180deg, rgba(168, 200, 196, .12), rgba(168, 200, 196, .5));
  }
  .awv-link + .awv-link::after { left: 49px; top: -22px; }
  .awv-so { min-height: 0; }
}

/* ── The hand-off timeline. One rail, five stops, an owner badge on
   every stop, because who does each step is the entire point. ── */
.awv-flow { max-width: 900px; }
.awv-step {
  position: relative;
  display: grid;
  grid-template-columns: 52px 1fr;
  gap: 24px;
  padding-bottom: 34px;
}
.awv-step:last-child { padding-bottom: 0; }
.awv-step::before {
  content: "";
  position: absolute;
  left: 25px;
  top: 46px;
  bottom: 6px;
  width: 1px;
  background: linear-gradient(180deg, rgba(168, 200, 196, .34), rgba(168, 200, 196, .1));
}
.awv-step:last-child::before { display: none; }
.awv-stop {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-family: var(--mono);
  font-size: 13px;
  letter-spacing: .04em;
  color: var(--river-tolt);
  background: var(--basalt);
  border: 1px solid rgba(168, 200, 196, .3);
}
.awv-step-body { padding-top: 5px; }
.awv-step-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 8px;
}
.awv-step-body h4 {
  font-family: var(--serif);
  font-weight: 400;
  font-size: 23px;
  line-height: 1.24;
  color: var(--fog);
  margin: 0;
}
.awv-step-body p {
  font-size: 16px;
  line-height: 1.68;
  color: rgba(232, 228, 216, .72);
  margin: 0;
  max-width: 62ch;
}

@media (max-width: 620px) {
  .awv-step { grid-template-columns: 40px 1fr; gap: 18px; }
  .awv-stop { width: 40px; height: 40px; font-size: 11.5px; }
  .awv-step::before { left: 19px; top: 36px; }
}
"""


def _chain() -> str:
    links = [
        {
            "num": "I",
            "cite": "42 CFR 410.15",
            "title": "A nurse may do the visit.",
            "body": "Medicare's own definition of the health professional who furnishes an "
                    "annual wellness visit includes <strong>a medical professional, or a team "
                    "of them, working under the direct supervision of a physician.</strong> "
                    "The doctor does not have to be the person having the conversation. Most "
                    "of the visit is history, structured screening, and a written prevention "
                    "schedule, which is nursing work.",
            "so": "So the visit does not need <b>your physician's calendar.</b>",
        },
        {
            "num": "II",
            "cite": "42 CFR 410.26(a)(1)",
            "title": "The nurse need not be your employee.",
            "body": "Auxiliary personnel means any individual acting under the physician's "
                    "supervision, <strong>regardless of whether that individual is an "
                    "employee, a leased employee, or an independent contractor</strong> of "
                    "the physician or of the entity that contracts with them. A practice may "
                    "contract the nurse in.",
            "so": "So the practice can contract with <b>TULQ for the nurse.</b>",
        },
        {
            "num": "III",
            "cite": "42 CFR 410.32(b)(3)(ii)",
            "title": "The supervision may be virtual.",
            "body": "Direct supervision means present in the office suite and immediately "
                    "available throughout. Since 1 January 2026 that presence "
                    "<strong>may be a virtual one, through real-time audio and video "
                    "excluding audio-only.</strong> It was adopted permanently in the CY2026 "
                    "Physician Fee Schedule final rule, not extended as a flexibility with an "
                    "expiry date.",
            "so": "So the nurse can work <b>from anywhere you can reach.</b>",
        },
    ]
    out = []
    for link in links:
        out.append(f"""      <article class="awv-link rise">
        <div class="awv-num" aria-hidden="true">{link["num"]}</div>
        <div class="awv-cite">{link["cite"]}</div>
        <h3>{link["title"]}</h3>
        <p>{link["body"]}</p>
        <div class="awv-so">{link["so"]}</div>
      </article>""")
    return '    <div class="awv-chain">\n' + "\n".join(out) + "\n    </div>"


def _flow() -> str:
    steps = [
        ("The front desk prints the chart summary.",
         "A short medication list and health history goes to the nurse before the call. "
         "Nobody at TULQ needs a login to produce it.",
         "you"),
        ("The nurse calls the patient.",
         "A licensed registered nurse conducts the wellness visit by telephone, covering "
         "every element the benefit requires, while the supervising physician is reachable "
         "on live video.",
         "tulq"),
        ("The nurse writes the note.",
         "The visit is documented in TULQ's own system and rendered as a finished document, "
         "complete and ready for a signature rather than a transcript for someone else to "
         "convert.",
         "tulq"),
        ("The document is delivered securely.",
         "It travels to the practice through an agreed private channel under a signed "
         "business associate agreement. It does not travel through anyone's inbox.",
         "tulq"),
        ("Your staff sign it and file it.",
         "The supervising physician reviews and signs, and your own people file it in your "
         "own medical record system. The chart is never touched by an outside hand.",
         "you"),
    ]
    out = []
    for i, (title, body, owner) in enumerate(steps, start=1):
        badge = ('<span class="lp-own lp-own--t">TULQ</span>' if owner == "tulq"
                 else '<span class="lp-own lp-own--y">Your practice</span>')
        out.append(f"""      <div class="awv-step rise">
        <div class="awv-stop" aria-hidden="true">{i:02d}</div>
        <div class="awv-step-body">
          <div class="awv-step-head">
            <h4>{title}</h4>
            {badge}
          </div>
          <p>{body}</p>
        </div>
      </div>""")
    return '    <div class="awv-flow">\n' + "\n".join(out) + "\n    </div>"


# ══════════════════════════════════════════════════════════════════════
# /awv
# ══════════════════════════════════════════════════════════════════════

def page_awv_explainer() -> LandingPage:
    qa = [
        ("Can a registered nurse perform a Medicare annual wellness visit?",
         "<p>Yes. The regulation defining who may furnish the visit lists a physician, a "
         "qualified non-physician practitioner such as a physician assistant, nurse "
         "practitioner or clinical nurse specialist, and also a medical professional or a "
         "team of medical professionals working under the direct supervision of a "
         "physician. A registered nurse works under that third route.</p>"
         "<p>What the nurse cannot do is make the supervision requirement or the billing "
         "obligation disappear. Both stay with your practice.</p>"
         + source_link("42 CFR 410.15", ECFR_410_15)),

        ("Does the nurse have to be employed by our practice?",
         "<p>No. The incident-to regulation defines auxiliary personnel as any individual "
         "acting under the supervision of the physician, regardless of whether that person "
         "is an employee, a leased employee, or an independent contractor of the physician "
         "or of the entity that contracts with them. That is the provision a staffing "
         "arrangement rests on, and it is the same one behind a locum nurse or a contracted "
         "phlebotomist.</p>"
         + source_link("42 CFR 410.26", ECFR_410_26)),

        ("Does the physician have to be in the building?",
         "<p>Not since 1 January 2026. Direct supervision still means the physician is "
         "immediately available to furnish assistance and direction throughout, but the "
         "presence required may now be a virtual one, through real-time audio and video "
         "interactive telecommunications. Audio-only does not satisfy it, and the allowance "
         "does not extend to services carrying a 010 or 090 global surgery indicator, which "
         "the wellness visit does not.</p>"
         "<p>CMS adopted this permanently in the CY2026 Physician Fee Schedule final rule "
         "rather than extending it as a dated flexibility, which is what makes a standing "
         "telephone visit programme practical to run.</p>"
         + source_link("42 CFR 410.32(b)(3)(ii)", ECFR_410_32)),

        ("Who submits the claim to Medicare?",
         "<p>Your practice does, under your own supervising physician, exactly as if one of "
         "your own staff had performed the visit. TULQ never bills Medicare, never submits "
         "a claim, and never appears on one. Only the supervising physician or practitioner "
         "may bill for incident-to services, which the regulation states in as many "
         "words.</p>"
         + source_link("42 CFR 410.26(b)(5)", ECFR_410_26)),

        ("How is TULQ paid, then?",
         "<p>By the practice, as a flat fee for each completed visit. That is a private "
         "commercial transaction, separate from the Medicare claim, and it is the same shape "
         "as the arrangement a practice already has with a staffing agency or a billing "
         "service.</p>"
         "<p>We do not take a percentage of what you collect. A revenue share is not "
         "unlawful and several vendors run one, but it is a different compliance posture, "
         "and a flat fee per completed visit is the one we would rather explain to your "
         "compliance officer.</p>"),

        ("Do your nurses need access to our EHR?",
         "<p>No, and by default they do not have it. Your front desk sends a short chart "
         "summary out, the nurse works from that, and a finished document comes back through "
         "a secure channel for your own staff to sign and file. No TULQ credential exists in "
         "your system unless you decide to create one.</p>"
         "<p>Some practices prefer to grant delegated access so the note lands directly "
         "where the biller looks. That works too, under a signed business associate "
         "agreement. The point is that it is your choice rather than a condition of the "
         "service.</p>"),

        ("Can the visit really be done over the telephone?",
         "<p>For established patients, yes. The annual wellness visit sits on the Medicare "
         "telehealth list and audio-only delivery is permitted under the telehealth "
         "flexibilities, which the Consolidated Appropriations Act of 2026 extended through "
         "31 December 2027. New patients generally still need to be seen in person.</p>"
         "<p>Note that these two rules are separate and it is worth keeping them apart. The "
         "supervising physician's virtual presence is permanent. The patient-facing "
         "audio-only allowance is dated, so check the current CMS telehealth list rather "
         "than assuming the position holds.</p>"
         + source_link("CMS Medicare telehealth", CMS_TELEHEALTH)),

        ("What stops this from being a documentation problem later?",
         "<p>The note has to show more than that a conversation happened. It has to evidence "
         "each required element, name who performed the visit and their credential, and "
         "record that the supervising physician was available throughout. Ours does all "
         "three on every visit, because a wellness visit programme that cannot prove the "
         "supervision is the one that becomes a repayment.</p>"
         + source_link("CMS Medicare Wellness Visits, MLN6775421", CMS_AWV_MLN)),
    ]

    page = LandingPage(
        site=SITE,
        slug="awv",
        title="How Nurse-Led Annual Wellness Visits Get Paid | TULQ",
        description=(
            "A plain English guide to the three federal rules that let a contracted nurse "
            "complete your Medicare annual wellness visits by phone. Read the chain."
        ),
        h1="Three federal rules, <em>one wellness visit.</em>",
        hero_sub=(
            "How a contracted registered nurse can complete your Medicare annual wellness "
            "visits by telephone, why Medicare pays your practice for them, and where every "
            "part of that sits in the regulations."
        ),
        hero_eyebrow="Plain English guide",
        hero_facts=("42 CFR 410.15", "42 CFR 410.26", "Virtual supervision, permanent in 2026"),
        hero_scene="petroglyph",
        hero_ctas=(
            '<a class="btn btn-primary" href="#chain" data-magnetic>Read the chain'
            '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">'
            '<path d="M3 7h8m0 0L7.5 3.5M11 7l-3.5 3.5" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
            '<a class="btn btn-ghost" href="/services/medicare-annual-wellness-visits">'
            "See the service</a>"
        ),
        priority="0.8",
        reviewed=True,
        extra_css=AWV_CSS,
    )
    trail = [("Services", "/services/"), ("How wellness visit payment works", "/awv")]

    page.sections = [
        crumbs(trail),

        band(
            prose(
                "      <p>Medicare pays for a yearly check-in with every patient who has Part "
                "B, called the annual wellness visit. It is not a physical, there is no "
                "examination, and the patient owes nothing for it. It is a conversation: "
                "health history, medications, risk factors like falls or low mood, and a "
                "written plan for the screenings and preventive care that should happen over "
                "the next several years.</p>\n"
                "      <p>Medicare pays the practice for that conversation using one code for "
                "a patient's first ever visit and a second code for every year after it. The "
                "money is not in dispute and never has been. What practices ask us about is "
                "the arrangement: <em>a nurse we do not employ, on a telephone, while our "
                "physician is somewhere else.</em> That is the part this page is for.</p>\n"
                "      <p>The short version is that it rests on three rules that were already "
                "on the books, and it is written out below in the order they apply.</p>"
            ),
            eyebrow="What this visit actually is",
            h2="A conversation, <em>not an examination.</em>",
            scene="premise",
        ),

        band(
            _chain(),
            dark=True,
            anchor="chain",
            eyebrow="The chain",
            h2="Each link is <em>an existing federal rule.</em>",
            deck="Read left to right. The first rule says a nurse may do the visit. The second "
                 "says that nurse need not be on your payroll. The third says the supervising "
                 "physician need not be in the room. Nothing here is a workaround, and nothing "
                 "here is novel.",
            scene="totem",
        ),

        band(
            split(
                {"label": "What TULQ never does",
                 "body": "        <p><strong>We never bill Medicare.</strong> No claim is "
                         "submitted by us, on your behalf or otherwise, and TULQ does not "
                         "appear on the claim you submit.</p>\n"
                         "        <p><strong>We are not paid by Medicare.</strong> No part of "
                         "our fee comes out of a federal programme directly, and we do not "
                         "take a percentage of what you collect.</p>\n"
                         "        <p><strong>We do not hold your credentials.</strong> No TULQ "
                         "login exists in your medical record system unless you choose to "
                         "create one.</p>"},
                {"label": "What your practice does",
                 "body": "        <p><strong>You bill Medicare</strong> under your own "
                         "supervising physician, exactly as you would if the visit had been "
                         "performed by someone on your own staff. Only the supervising "
                         "practitioner may bill an incident-to service, and that is you.</p>\n"
                         "        <p><strong>You pay TULQ a flat fee</strong> for each "
                         "completed visit, as an ordinary commercial expense, in the same "
                         "shape as a staffing agency or a billing service.</p>\n"
                         "        <p><strong>You keep the record and the relationship.</strong> "
                         "The signed note lives in your system, filed by your people.</p>"},
            ),
            eyebrow="Who bills, who pays whom",
            h2="TULQ never touches <em>a Medicare claim.</em>",
            deck="This is the question a compliance officer asks first, so it gets answered "
                 "before anything else on this page.",
            scene="why",
        ),

        band(
            _flow(),
            dark=True,
            anchor="how",
            eyebrow="From a phone call into the chart",
            h2="Five steps, and none of them <em>hand us a password.</em>",
            deck="This is the part people usually picture wrong. The finished note reaches the "
                 "chart as a signed document, filed by your own staff, so there is no gap in "
                 "who controls the record and no outside access to your software.",
            scene="cave",
        ),

        band(
            ledger([
                {"title": "What the visit has to cover",
                 "note": "The elements the regulation requires before the visit is billable. "
                         "Our nurses cover every one on every call.",
                 "items": [
                     ("Administer or review a health risk assessment", "tulq"),
                     ("Establish or update medical and family history", "tulq"),
                     ("List the current providers and suppliers involved in the patient's care",
                      "tulq"),
                     ("Record height, weight, body mass index and blood pressure", ""),
                     ("Detect any cognitive impairment", "tulq"),
                     ("Review risk factors for depression", "tulq"),
                     ("Review functional ability and level of safety, including fall risk",
                      "tulq"),
                     ("Establish a written screening schedule for the next five to ten years",
                      "tulq"),
                     ("Furnish personalised health advice and referrals", "tulq"),
                     ("Review any current opioid prescriptions and screen for substance use "
                      "disorder", "tulq"),
                 ]},
                {"title": "What the record has to prove",
                 "note": "A visit that happened but cannot be evidenced is the one that becomes "
                         "a repayment two years later.",
                 "items": [
                     ("Each required element was actually covered, element by element", "tulq"),
                     ("Who performed the visit, and under what licence", "tulq"),
                     ("That the supervising physician was available throughout", ""),
                     ("The patient's eligibility, including that twelve months have passed",
                      "tulq"),
                     ("The physician's review and signature", "you"),
                     ("The note filed in the practice's own medical record", "you"),
                     ("The claim, submitted under the supervising physician", "you"),
                 ]},
            ]),
            eyebrow="Why it counts as a real visit",
            h2="Every required element, <em>evidenced.</em>",
            deck="A licensed nurse performing every required element under a physician's "
                 "real-time supervision, with a signed record proving it, is what the benefit "
                 "asks for. Shared rows are ones neither side owns alone.",
            scene="bio",
        ),

        band(
            prose(
                "      <p>A federal rule lets a nurse do this visit instead of the physician. A "
                "second federal rule lets that nurse be supplied by an outside company rather "
                "than being an employee of the practice. A third lets the physician supervise "
                "by live video instead of standing in the room.</p>\n"
                "      <p>The practice bills Medicare as usual and pays TULQ separately for the "
                "nurse's time. The signed record ends up filed in the practice's own system by "
                "the practice's own staff. <strong>Every piece of that chain is built on an "
                "existing federal rule, not a workaround.</strong></p>\n"
                "      <p>None of which is the same as saying it runs itself. The supervision "
                "obligation is real, the documentation standard is real, and both sit with "
                "your practice. What we are telling you is where they sit, not that they went "
                "away.</p>",
                wide=True,
            )
            + "\n" + section_links([
                ("What the service costs and how it runs",
                 "/services/medicare-annual-wellness-visits"),
                ("Run the revenue arithmetic on your own panel",
                 "/tools/awv-revenue-calculator"),
                ("Who may perform the visit, and who may bill it",
                 "/resources/who-can-perform-annual-wellness-visit"),
            ]),
            dark=True,
            eyebrow="The bottom line",
            h2="No workaround, <em>just the rules as written.</em>",
            scene="pines",
        ),

        band(
            faq(qa),
            eyebrow="Common questions",
            h2="What compliance officers ask us.",
            extra_class="faq-section",
            scene="story",
        ),

        band(
            sources(
                [
                    ("42 CFR 410.15, annual wellness visits providing personalized prevention "
                     "plan services", ECFR_410_15),
                    ("42 CFR 410.26, services and supplies incident to a physician's "
                     "professional services", ECFR_410_26),
                    ("42 CFR 410.32(b)(3)(ii), levels of supervision", ECFR_410_32),
                    ("CMS, CY2026 Medicare Physician Fee Schedule final rule fact sheet, "
                     "CMS-1832-F", CMS_PFS_2026),
                    ("CY2026 Physician Fee Schedule final rule, 90 FR 50007, 5 November 2025",
                     FR_PFS_2026),
                    ("CMS, Medicare Wellness Visits, MLN6775421", CMS_AWV_MLN),
                    ("Medicare.gov, yearly wellness visits", MEDICARE_AWV),
                    ("CMS, Medicare telehealth", CMS_TELEHEALTH),
                    ("CMS, Physician Fee Schedule lookup", PFS_LOOKUP),
                ],
                disclaimer=(
                    "This page summarises federal requirements as they stood in August 2026 "
                    "for a general audience. It is not legal, billing, or compliance advice "
                    "and it does not substitute for review by qualified counsel or your own "
                    "compliance officer. Coverage and supervision rules change, and the "
                    "patient-facing audio-only telehealth allowance in particular carries a "
                    "date, so confirm the current position with CMS and your MAC before "
                    "relying on any of it."
                ),
            ),
            dark=True,
            eyebrow="Sources",
            h2="Read the rules yourself.",
            deck="Every claim on this page is linked to the primary document rather than to a "
                 "summary of it. Nothing below is behind a paywall.",
            scene="totem",
        ),

        contact_close(
            "Send this page to your compliance officer.",
            "That is genuinely the fastest way to find out whether this works for you. If the "
            "answer comes back with questions, put us on the call. We would rather have the "
            "hard conversation before a contract than after a claim.",
            cap_title="Compliance packet",
            cap_body="Supervision model, sample completed note, and the business associate "
                     "agreement we sign.",
            cap_note="Ask and we will send it the same day, with the regulatory citations "
                     "written out in full so your counsel can check them rather than take "
                     "our word for it.",
        ),
    ]

    page.schema = [
        breadcrumb_node(page, trail),
        service_node(
            page,
            "Contracted nurse Medicare annual wellness visits",
            "Preventive care services",
            "Licensed registered nurses supplied to a physician practice as auxiliary "
            "personnel under 42 CFR 410.26, who complete the Medicare annual wellness visit "
            "by telephone under the practice's direct supervision. The practice supervises, "
            "signs, and submits the claim.",
            audience="Physician practices, rural health clinics, and federally qualified "
                     "health centers",
        ),
        faq_node(page, qa),
    ]
    return page


def pages() -> list[LandingPage]:
    return [page_awv_explainer()]
