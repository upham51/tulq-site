#!/usr/bin/env python3
"""
Content for the mainstream track on tulqhealth.com.

This is the contested side: DR 19-32 incumbents who have been publishing
since 2008. The research is explicit that head terms are a slow climb and
that the winnable ground is long-tail cost, reimbursement, and comparison
content. That is what this module weights toward.

Two hand-written pages from PR #88 already own the hospice and rural
health clinic terms:

    /nurse-triage-for-hospice
    /nurse-triage-for-rural-health-clinics

Note that the RHC page covers critical access hospitals too. So the pillars
here deliberately cover only what those two do not - home health, and
federally qualified / community health centers - and link across rather
than competing for the same queries. Do not broaden them back into hospice,
RHC, or CAH territory without retiring the PR #88 pages first.

Reimbursement figures are cited with their program year and source, and
every page says to check the current fee schedule before modelling on them.
"""

from __future__ import annotations

from pagekit import (
    CARE, Page, article_node, card_grid, faq_block, faq_node,
    service_node, sources_block,
)

SITE = CARE


# ══════════════════════════════════════════════════════════════════════
# PILLAR — Home health
# (hospice is covered by /nurse-triage-for-hospice)
# ══════════════════════════════════════════════════════════════════════

def pillar_home_health() -> Page:
    qa = [
        ("Do you replace our on-call nurse or sit in front of them?",
         "<p>In front of them. TULQ takes first call, resolves what the protocol allows "
         "a nurse to resolve, and escalates to your on-call clinician when the "
         "disposition requires it. Your team stays in the loop on the calls that need "
         "them and stops being woken for the ones that don't.</p>"),
        ("We're a hospice as well as a home health agency. Which page applies?",
         "<p>Both, and the service is the same line. The hospice side has its own "
         "requirements around the Medicare Condition of Participation for 24-hour nurse "
         "availability &mdash; <a href=\"/nurse-triage-for-hospice\">that is covered "
         "here</a>. This page is about the home health side: OASIS, HHVBP, and "
         "acute-care utilization.</p>"),
        ("How fast do calls get answered?",
         "<p>Our model is answer-on-connect rather than queue-and-callback. TULQ is "
         "launching in 2026, so we are not going to quote you an average speed to "
         "answer we have not yet measured &mdash; but it is a fair thing to write into "
         "a contract as a service level, and we are happy to have it there.</p>"),
        ("Can you document into our EMR?",
         "<p>Encounter documentation is captured on every call and returned to you. The "
         "specific integration path depends on your system; some agencies take a "
         "structured export, others take documentation into a shared workflow. Scope it "
         "explicitly during implementation rather than assuming it.</p>"),
        ("Is this cheaper than staffing our own on-call?",
         "<p>Usually, but you should check rather than take our word for it. Add up "
         "on-call differentials and stipends, overtime, the next-day productivity you "
         "lose, and your actual cost of replacing a clinician who leaves over call "
         "burden. <a href=\"/resources/true-cost-of-after-hours-on-call\">We lay out "
         "the full calculation here.</a></p>"),
    ]

    page = Page(
        site=SITE,
        slug="for/home-health",
        title="Home Health After-Hours Nurse Triage Line | TULQ",
        description=(
            "Outsourced after-hours nurse triage for home health agencies. Licensed RNs "
            "on first call, Schmitt-Thompson protocols, HHVBP-aware. Talk to our team."
        ),
        eyebrow="Home health",
        h1="Your clinicians should sleep. <em>Someone should answer.</em>",
        deck=(
            "After-hours on-call is the most reliable source of clinician burnout in "
            "home health, and the least visible line item in the budget. Outsourced "
            "nurse triage addresses both, if it is actually nurse triage."
        ),
        crumbs=[("Who we serve", "/for/home-health")],
        reviewed=True,
        priority="0.9",
        cta_title="See what coverage would look like.",
        cta_body=(
            "Tell us your census, your after-hours call volume, and how your on-call "
            "rotation works today. We will walk through what changes and what doesn't."
        ),
    )

    page.body = f"""    <p>Every home health agency solves after-hours the same way at first: a rotation.
    Clinicians take call in turn, carry the phone, and answer whatever comes in. It
    works until it doesn't, and what breaks it is rarely a single dramatic night.</p>

    <p>It is the accumulation. The nurse who took four calls between midnight and
    five and still has a full visit schedule. The one who has started dreading her
    rotation two days out. The one who leaves for a clinic job with no call, and takes
    six years of experience with her.</p>

    <div class="callout callout--teal">
      <div class="callout-head">Running a hospice too?</div>
      <p>The hospice side carries its own Medicare Condition of Participation for
      24-hour nurse availability, and it is worth reading separately.
      <a href="/nurse-triage-for-hospice">Nurse triage for hospice is covered
      here.</a> It is the same line and the same nurses &mdash; the compliance framing
      is what differs.</p>
    </div>

    <h2>What the on-call rotation actually costs</h2>

    <p>The cost of on-call is spread across line items that never get totalled in the
    same place, which is why agencies consistently underestimate it:</p>

    <ul>
      <li><strong>Direct pay.</strong> On-call differentials, stipends, and per-call
      rates.</li>
      <li><strong>Overtime.</strong> When a night call turns into a visit, or when it
      runs long enough to push into the next shift.</li>
      <li><strong>Next-day productivity.</strong> A clinician who was up at three is
      not doing a full day's work at nine, and the visits still have to happen.</li>
      <li><strong>Turnover.</strong> The expensive one. Recruiting, onboarding, and
      ramping a replacement clinician costs a multiple of the differential you were
      paying, and call burden is a documented driver of clinical turnover.</li>
    </ul>

    <p><a href="/resources/true-cost-of-after-hours-on-call">The full calculation, with
    a worked example, is here.</a></p>

    <h2>Triage, not an answering service</h2>

    <p>The market has two things in it that sound similar and are not.</p>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr>
            <th>&nbsp;</th>
            <th>Medical answering service</th>
            <th>Nurse triage</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Who answers</td>
            <td>Non-clinical operator</td>
            <td class="tick">Licensed registered nurse</td>
          </tr>
          <tr>
            <td>Can assess a symptom</td>
            <td class="cross">No</td>
            <td class="tick">Yes, against protocol</td>
          </tr>
          <tr>
            <td>Can reach a disposition</td>
            <td class="cross">No</td>
            <td class="tick">Yes</td>
          </tr>
          <tr>
            <td>What reaches your clinician</td>
            <td>Every call that isn't obviously routine</td>
            <td class="tick">Only calls the protocol escalates</td>
          </tr>
          <tr>
            <td>Clinical documentation</td>
            <td>A message</td>
            <td class="tick">An assessed encounter</td>
          </tr>
          <tr>
            <td>Cost</td>
            <td>Lower</td>
            <td>Higher &mdash; and the difference is the clinical work</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>An answering service reduces the number of times the phone rings at your
    clinician's house by exactly zero. It changes who dials it.
    <a href="/resources/nurse-triage-vs-answering-service">More on the distinction.</a></p>

    <h2>Where after-hours coverage touches your payment</h2>

    <p>For home health specifically, after-hours access is not only an operational
    question. It runs into the value-based programs:</p>

    <div class="card-grid">
      <div class="card">
        <div class="card-tag">HHVBP</div>
        <h3>Acute-care utilization</h3>
        <p>Acute-care utilization is a lever inside the expanded model, with CMS moving
        to a within-stay Potentially Preventable Hospitalization measure beginning with
        CY2025.</p>
      </div>
      <div class="card">
        <div class="card-tag">Quality</div>
        <h3>OASIS and HHQRP</h3>
        <p>Assessment and quality reporting requirements continue to expand. An
        after-hours encounter your team never learns about is a gap in the record as
        well as in the care.</p>
      </div>
      <div class="card">
        <div class="card-tag">Retention</div>
        <h3>Clinical staffing</h3>
        <p>The measure nobody reports publicly. Call burden is a documented driver of
        turnover, and turnover is the most expensive line item on the page.</p>
      </div>
    </div>

    <p>None of these move because you bought a phone line. They move because the
    patient who called at midnight reached a nurse who helped, and because the symptom
    that would have become an admission got managed at home. The measurement follows
    the care. <a href="/resources/hhvbp-ed-use">How that pathway actually works.</a></p>

    <h2>How the service works</h2>

    <ol>
      <li><strong>You define the rules.</strong> Which call types resolve at triage,
      which escalate, who they escalate to, and what your after-hours clinical
      boundaries are.</li>
      <li><strong>We take first call.</strong> A licensed RN answers, assesses against
      Schmitt-Thompson protocols, and reaches a documented disposition.</li>
      <li><strong>Escalation runs your way.</strong> When a call needs your clinician,
      the nurse reaches them directly with the assessment already done.</li>
      <li><strong>Documentation comes back.</strong> Every encounter, returned for your
      clinical and compliance record.</li>
    </ol>

    <div class="callout">
      <div class="callout-head">The honest caveat</div>
      <p>TULQ is launching in 2026. We do not have a decade of call volume statistics
      to show you, and any vendor comparison we published that pretended otherwise
      would be worthless. What we can be evaluated on today is the clinical model, our
      director's credentials, licensure, protocol standard, escalation design, and
      pricing structure &mdash; and we would rather be judged on those than on a number
      we cannot yet substantiate.</p>
    </div>

    <h2>Read next</h2>

    {card_grid([
        ("Hospice", "Nurse triage for hospice",
         "The Medicare Condition of Participation for 24-hour nurse availability, and what satisfying it looks like.",
         "/nurse-triage-for-hospice"),
        ("Cost", "The true cost of after-hours on-call",
         "The four line items agencies never total in the same place, with a worked example.",
         "/resources/true-cost-of-after-hours-on-call"),
        ("HHVBP", "HHVBP and ED use",
         "How the CY2025 shift to within-stay potentially preventable hospitalization changes the lever.",
         "/resources/hhvbp-ed-use"),
        ("Compare", "Comparing triage vendors",
         "IntellaTriage, Conduit, AccessNurse — what each is built for, and how to evaluate them.",
         "/compare/"),
    ])}

    {faq_block(qa)}

    {sources_block([
        "CMS, expanded Home Health Value-Based Purchasing (HHVBP) model.",
        "CMS, Home Health Quality Reporting Program and OASIS requirements.",
        "American Academy of Ambulatory Care Nursing, <em>Scope and Standards of Practice for Professional Telehealth Nursing</em>.",
        "Schmitt-Thompson telephone triage protocols.",
    ], disclaimer=(
        "Quality program requirements change annually. Verify current measure "
        "specifications and effective dates against CMS guidance before relying on "
        "them. TULQ is launching in 2026; this page describes the service model, not "
        "past contract performance."
    ))}"""

    page.schema = [
        service_node(
            page,
            name="After-hours nurse triage for home health agencies",
            service_type="Telephone nurse triage",
            description=(
                "Outsourced after-hours and on-call nurse triage for home health "
                "agencies. U.S. state-licensed registered nurses take first call on "
                "Schmitt-Thompson protocols, escalate to the agency's on-call clinician "
                "per the agency's rules, and return encounter documentation."
            ),
            audience="Home health agencies",
        ),
        faq_node(page, qa),
    ]
    return page


# ══════════════════════════════════════════════════════════════════════
# PILLAR — FQHC / community health centers
# (RHCs and critical access hospitals are covered by
#  /nurse-triage-for-rural-health-clinics)
# ══════════════════════════════════════════════════════════════════════

def pillar_health_centers() -> Page:
    qa = [
        ("Does after-hours coverage satisfy an FQHC access requirement?",
         "<p>Health center program requirements include ensuring patients have access "
         "to services after regular hours, and a professional coverage arrangement is "
         "one recognized way to meet it. Whether a specific arrangement satisfies your "
         "obligations is a question for your compliance staff and your operational site "
         "visit &mdash; not something a vendor should tell you it has handled.</p>"),
        ("We're a rural health clinic or a critical access hospital. Right page?",
         "<p>No &mdash; we wrote one specifically for you. "
         "<a href=\"/nurse-triage-for-rural-health-clinics\">Nurse triage for rural "
         "health clinics and critical access hospitals is here.</a> This page is for "
         "federally qualified and community health centers, which sit under HRSA "
         "program requirements rather than the CMS conditions of participation.</p>"),
        ("Can we bill anything for it?",
         "<p>Not for the triage call itself as a rule. Where after-hours access matters "
         "financially is as a component of care-management programs that do have "
         "billable codes &mdash; Advanced Primary Care Management being the current "
         "example. <a href=\"/resources/apcm-billing-fqhc-rhc\">We walk through APCM "
         "here.</a></p>"),
        ("Our providers already carry a phone. What changes?",
         "<p>They stop carrying it, and they stop being the filter. Today every "
         "after-hours call is a provider's judgment call about whether it was worth "
         "being woken for. With triage in front, a licensed RN makes that assessment "
         "against protocol, and your provider hears about the calls that genuinely "
         "need them &mdash; with the assessment already done.</p>"),
        ("Is this affordable for a safety-net budget?",
         "<p>It has to be, or it is not a real option for this segment. We price on a "
         "flat monthly structure rather than per-call, so a bad flu season does not "
         "produce a budget surprise, and so the number you put in a grant application "
         "is the number you pay.</p>"),
    ]

    page = Page(
        site=SITE,
        slug="for/health-centers",
        title="FQHC &amp; Community Health Center Nurse Triage | TULQ",
        description=(
            "24/7 nurse triage for federally qualified health centers and community "
            "health centers. Flat monthly pricing built for safety-net budgets. Talk to us."
        ),
        eyebrow="Health centers",
        h1="Coverage for the clinics <em>that can't add a shift.</em>",
        deck=(
            "Federally qualified and community health centers carry the same after-hours "
            "obligation as everyone else and have the least room to staff it. "
            "Outsourced nurse triage is the option that does not require hiring."
        ),
        crumbs=[("Who we serve", "/for/health-centers")],
        reviewed=True,
        priority="0.9",
        cta_title="Built for a safety-net budget.",
        cta_body=(
            "Tell us your panel size and after-hours volume and we will give you a flat "
            "monthly number you can put in a budget or a grant application."
        ),
    )

    page.body = f"""    <p>A federally qualified health center's after-hours problem is simple to state
    and hard to solve: the phone rings and there is no one whose job it is to answer
    it clinically.</p>

    <p>The usual fixes do not fit. Extending clinic hours requires clinicians you
    cannot recruit. Putting providers on call burns the small number you have. An
    answering service is affordable and does not make a clinical decision. What is left
    is outsourced nurse triage, and the reason it is not universal in this segment is
    that most of the market is priced for organizations with more margin.</p>

    <div class="callout callout--teal">
      <div class="callout-head">Rural health clinic or critical access hospital?</div>
      <p>Those designations carry different regulators and different after-hours
      expectations, and they have their own page.
      <a href="/nurse-triage-for-rural-health-clinics">Nurse triage for rural health
      clinics and critical access hospitals is covered here.</a> Same line, same
      nurses; the compliance framing is what differs.</p>
    </div>

    <h2>What the program requirements actually ask for</h2>

    <p>Health center program requirements include ensuring patients can access services
    after regular business hours, with professional coverage arrangements recognized as
    a way to meet it. In practice this often falls to providers carrying a phone on top
    of a full panel.</p>

    <p>FQHCs also sit inside the care-management economics that have changed most
    recently. Advanced Primary Care Management, launched by CMS on January 1, 2025
    under the CY2025 Physician Fee Schedule, bundles a set of care-management
    expectations &mdash; including 24/7 access to care and continuity with the care team
    &mdash; into billable codes G0556, G0557, and G0558.
    <a href="/resources/apcm-billing-fqhc-rhc">We go through what that means for a
    health center here.</a></p>

    <h2>Why the usual fixes don't fit a health center</h2>

    <p>Every alternative to outsourced triage runs into the same constraint, which is
    that health centers are short of exactly the people the alternative requires:</p>

    <ul>
      <li><strong>Extending clinic hours</strong> needs clinicians you are already
      struggling to recruit and retain.</li>
      <li><strong>Provider call rotations</strong> burn the small number you have, and
      call burden is a documented driver of clinical turnover.</li>
      <li><strong>An answering service</strong> is affordable and cannot make a
      clinical decision, so every ambiguous call still reaches a provider.
      <a href="/resources/nurse-triage-vs-answering-service">The distinction matters
      more at 2 a.m. than it does on a price sheet.</a></li>
      <li><strong>Telling patients to use the ED appropriately</strong> assumes there
      is something else for them to do at eleven at night.</li>
    </ul>

    <p>Outsourced nurse triage is the only one of the four that does not consume
    clinical staff you do not have.</p>

    <div class="callout callout--amber">
      <div class="callout-head">Why per-call pricing is wrong for this segment</div>
      <p>A per-call model transfers volume risk to the buyer. For a health center
      operating on grant funding and a fixed budget, a bad respiratory season becomes a
      budget variance you have to explain. Flat monthly pricing costs the vendor
      predictability and buys you the ability to plan. For safety-net facilities that is
      not a preference, it is the difference between a viable line item and an
      unfundable one.</p>
    </div>

    <h2>What changes operationally</h2>

    <ol>
      <li><strong>Your providers stop carrying the phone.</strong> A licensed RN takes
      first call and resolves what protocol allows.</li>
      <li><strong>Escalation follows your rules.</strong> You define which call types
      reach your clinician and how.</li>
      <li><strong>Morning starts informed.</strong> Encounter documentation comes back,
      so the schedule reflects who called overnight.</li>
      <li><strong>ED use gets a filter.</strong> The patient who needed reassurance and
      a next-day appointment gets that instead of a drive.</li>
    </ol>

    <h2>Read next</h2>

    {card_grid([
        ("Reimbursement", "APCM billing at an FQHC or RHC",
         "G0556, G0557, G0558 — what the codes cover, who can bill them, and where 24/7 access fits.",
         "/resources/apcm-billing-fqhc-rhc"),
        ("RHC &amp; CAH", "Nurse triage for rural clinics and hospitals",
         "Rural health clinics and critical access hospitals sit under different rules. Their page is here.",
         "/nurse-triage-for-rural-health-clinics"),
        ("Cost", "The true cost of after-hours on-call",
         "The four line items that never get totalled in the same place, with a worked example.",
         "/resources/true-cost-of-after-hours-on-call"),
        ("Basics", "Nurse triage vs answering service",
         "The distinction that justifies the price difference, in one table.",
         "/resources/nurse-triage-vs-answering-service"),
    ])}

    {faq_block(qa)}

    {sources_block([
        "HRSA Health Center Program requirements &mdash; after-hours coverage.",
        "HRSA Health Center Program Compliance Manual.",
        "CMS CY2025 Physician Fee Schedule &mdash; Advanced Primary Care Management.",
        "National Association of Community Health Centers &mdash; APCM guidance.",
    ], disclaimer=(
        "Program requirements and payment rates change annually. Nothing here is "
        "compliance advice &mdash; verify against current HRSA, CMS, and MAC guidance, "
        "and confirm any coverage arrangement with your own compliance staff."
    ))}"""

    page.schema = [
        service_node(
            page,
            name="24/7 nurse triage for federally qualified and community health centers",
            service_type="Telephone nurse triage",
            description=(
                "24/7 telephone nurse triage for federally qualified health centers and "
                "community health centers, staffed by U.S. state-licensed registered "
                "nurses on Schmitt-Thompson protocols and priced on a flat monthly "
                "structure for safety-net budgets."
            ),
            audience=(
                "Federally qualified health centers and community health centers"
            ),
        ),
        faq_node(page, qa),
    ]
    return page
