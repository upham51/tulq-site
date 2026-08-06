#!/usr/bin/env python3
"""
Content for the mainstream track on tulqhealth.com.

This is the contested side: DR 19-32 incumbents who have been publishing
since 2008. The research is explicit that head terms are a slow climb and
that the winnable ground is long-tail cost, reimbursement, and comparison
content. That is what this module weights toward.

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
# PILLAR — Hospice & home health
# ══════════════════════════════════════════════════════════════════════

def pillar_hospice_home_health() -> Page:
    qa = [
        ("Do you replace our on-call nurse or sit in front of them?",
         "<p>In front of them. TULQ takes first call, resolves what the protocol allows "
         "a nurse to resolve, and escalates to your on-call clinician when the "
         "disposition requires it. Your team stays in the loop on the calls that need "
         "them and stops being woken for the ones that don't.</p>"),
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
        ("What happens on a death call?",
         "<p>It goes to your clinician, every time. Pronouncement, family support at the "
         "bedside, and the coordination that follows are your team's work, not a triage "
         "line's. What TULQ does is take that call immediately, gather what your "
         "clinician needs, and reach them without the family sitting in a queue.</p>"),
        ("Is this cheaper than staffing our own on-call?",
         "<p>Usually, but you should check rather than take our word for it. Add up "
         "on-call differentials and stipends, overtime, the next-day productivity you "
         "lose, and your actual cost of replacing a clinician who leaves over call "
         "burden. <a href=\"/resources/true-cost-of-after-hours-on-call\">We lay out "
         "the full calculation here.</a></p>"),
    ]

    page = Page(
        site=SITE,
        slug="for/hospice-home-health",
        title="Hospice &amp; Home Health After-Hours Nurse Triage | TULQ",
        description=(
            "Outsourced after-hours nurse triage for hospice and home health agencies. "
            "Licensed RNs on first call, Schmitt-Thompson protocols. Talk to our team."
        ),
        eyebrow="Hospice &amp; home health",
        h1="Your clinicians should sleep. <em>Someone should answer.</em>",
        deck=(
            "After-hours on-call is the single most reliable source of clinician burnout "
            "in hospice and home health, and the least visible line item in the budget. "
            "Outsourced nurse triage addresses both, if it is actually nurse triage."
        ),
        crumbs=[("Who we serve", "/for/hospice-home-health")],
        reviewed=True,
        priority="0.9",
        cta_title="See what coverage would look like.",
        cta_body=(
            "Tell us your census, your after-hours call volume, and how your on-call "
            "rotation works today. We will walk through what changes and what doesn't."
        ),
    )

    page.body = f"""    <p>Every hospice and home health agency solves after-hours the same way at first:
    a rotation. Clinicians take call in turn, carry the phone, and answer whatever comes
    in. It works until it doesn't, and what breaks it is rarely a single dramatic
    night.</p>

    <p>It is the accumulation. The nurse who took four calls between midnight and
    five and still has a full visit schedule. The one who has started dreading her
    rotation two days out. The one who leaves for a clinic job with no call, and takes
    six years of experience with her.</p>

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

    <h2>Where after-hours coverage touches your scores</h2>

    <p>For hospice and home health specifically, after-hours access is not only an
    operational question. It shows up in publicly reported quality measures:</p>

    <div class="card-grid">
      <div class="card">
        <div class="card-tag">Hospice</div>
        <h3>CAHPS Hospice Survey</h3>
        <p>Several measures turn on nights and weekends &mdash; getting help as soon
        as it was needed, training and emotional support for the family, team
        communication. Those answers are formed at 2 a.m.</p>
      </div>
      <div class="card">
        <div class="card-tag">Home health</div>
        <h3>HHVBP</h3>
        <p>Acute-care utilization is a lever inside the expanded model, with CMS moving
        to a within-stay Potentially Preventable Hospitalization measure beginning with
        CY2025.</p>
      </div>
      <div class="card">
        <div class="card-tag">Hospice</div>
        <h3>HQRP and HOPE</h3>
        <p>The Hospice Outcomes &amp; Patient Evaluation instrument replaced HIS
        effective October 1, 2025, changing what gets collected and when.</p>
      </div>
    </div>

    <p>None of these move because you bought a phone line. They move because the family
    that called at midnight reached a nurse who helped, and because the symptom that
    would have become an admission got managed at home. The measurement follows the
    care.</p>

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

    <div class="callout callout--teal">
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
        ("Cost", "The true cost of after-hours on-call",
         "The four line items agencies never total in the same place, with a worked example.",
         "/resources/true-cost-of-after-hours-on-call"),
        ("CAHPS", "Nurse triage and hospice CAHPS scores",
         "Which survey measures after-hours access actually touches, and which it doesn't.",
         "/resources/hospice-cahps-after-hours"),
        ("HHVBP", "HHVBP and ED use",
         "How the CY2025 shift to within-stay potentially preventable hospitalization changes the lever.",
         "/resources/hhvbp-ed-use"),
        ("Compare", "Comparing triage vendors",
         "IntellaTriage, Conduit, AccessNurse — what each is built for, and how to evaluate them.",
         "/compare/"),
    ])}

    {faq_block(qa)}

    {sources_block([
        "CMS, CAHPS Hospice Survey materials.",
        "CMS, expanded Home Health Value-Based Purchasing (HHVBP) model.",
        "CMS, Hospice Quality Reporting Program and the HOPE instrument.",
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
            name="After-hours nurse triage for hospice and home health agencies",
            service_type="Telephone nurse triage",
            description=(
                "Outsourced after-hours and on-call nurse triage for hospice and home "
                "health agencies. U.S. state-licensed registered nurses take first "
                "call on Schmitt-Thompson protocols, escalate to the agency's on-call "
                "clinician per the agency's rules, and return encounter documentation."
            ),
            audience="Hospice agencies and home health agencies",
        ),
        faq_node(page, qa),
    ]
    return page


# ══════════════════════════════════════════════════════════════════════
# PILLAR — FQHC / RHC / CAH
# ══════════════════════════════════════════════════════════════════════

def pillar_rural_fqhc_cah() -> Page:
    qa = [
        ("Does after-hours coverage satisfy an FQHC access requirement?",
         "<p>Health center program requirements include ensuring patients have access "
         "to services after regular hours, and a professional coverage arrangement is "
         "one recognized way to meet it. Whether a specific arrangement satisfies your "
         "obligations is a question for your compliance staff and your operational site "
         "visit &mdash; not something a vendor should tell you it has handled.</p>"),
        ("Can we bill anything for it?",
         "<p>Not for the triage call itself as a rule. Where after-hours access matters "
         "financially is as a component of care-management programs that do have "
         "billable codes &mdash; Advanced Primary Care Management being the current "
         "example. <a href=\"/resources/apcm-billing-fqhc-rhc\">We walk through APCM "
         "here.</a></p>"),
        ("We're a critical access hospital. Doesn't the ED already cover this?",
         "<p>Your emergency department covers people who come in. It does not cover the "
         "patient at home at 11 p.m. deciding whether to drive in &mdash; and for a CAH, "
         "a share of those who do drive in did not need to. Nurse triage sits in front "
         "of that decision.</p>"),
        ("Is this affordable for a safety-net budget?",
         "<p>It has to be, or it is not a real option for this segment. We price on a "
         "flat monthly structure rather than per-call, so a bad flu season does not "
         "produce a budget surprise, and so the number you put in a grant application "
         "is the number you pay.</p>"),
        ("Do your nurses hold licensure in our state?",
         "<p>Telephone triage nurses must hold licensure appropriate to the state where "
         "the patient is located. We scope licensure coverage to the service area of "
         "each engagement, and it is worth writing into the contract with any vendor "
         "you evaluate.</p>"),
    ]

    page = Page(
        site=SITE,
        slug="for/rural-fqhc-cah",
        title="FQHC, RHC &amp; CAH After-Hours Nurse Triage | TULQ",
        description=(
            "24/7 nurse triage for federally qualified health centers, rural health "
            "clinics, and critical access hospitals. Flat monthly pricing built for "
            "safety-net budgets."
        ),
        eyebrow="FQHC, RHC &amp; CAH",
        h1="Coverage for the clinics <em>that can't add a shift.</em>",
        deck=(
            "Rural safety-net facilities have the same after-hours obligation as "
            "everyone else and the least room to staff it. Outsourced nurse triage is "
            "the option that does not require hiring."
        ),
        crumbs=[("Who we serve", "/for/rural-fqhc-cah")],
        reviewed=True,
        priority="0.9",
        cta_title="Built for a safety-net budget.",
        cta_body=(
            "Tell us your panel size and after-hours volume and we will give you a flat "
            "monthly number you can put in a budget or a grant application."
        ),
    )

    page.body = f"""    <p>A federally qualified health center, a rural health clinic, and a critical
    access hospital have different designations, different payment methodologies, and
    different regulators. After hours, they have the same problem: the phone rings and
    there is no one whose job it is to answer it clinically.</p>

    <p>The usual fixes do not fit. Extending clinic hours requires clinicians you
    cannot recruit. Putting providers on call burns the small number you have. An
    answering service is affordable and does not make a clinical decision. What is left
    is outsourced nurse triage, and the reason it is not universal in this segment is
    that most of the market is priced for organizations with more margin.</p>

    <h2>Each designation, specifically</h2>

    <h3>Federally qualified health centers</h3>

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

    <h3>Rural health clinics</h3>

    <p>RHCs face the same after-hours access expectations with, typically, an even
    smaller clinical staff. Many are attached to a critical access hospital, which means
    the after-hours question is really a question about how the hospital's ED gets
    used.</p>

    <h3>Critical access hospitals</h3>

    <p>CAHs operate under conditions of participation that include maintaining 24-hour
    emergency care services, within the limits that define the designation &mdash; no
    more than 25 inpatient beds, and a location standard relative to other hospitals.</p>

    <p>The ED is staffed. The telephone usually is not. A patient at home deciding
    whether to come in at midnight has no clinical voice to consult, so a share of them
    come in when they did not need to, and a share stay home when they should have
    come.</p>

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
        ("Compliance", "After-hours coverage for critical access hospitals",
         "What the conditions of participation require, and what they leave to you.",
         "/resources/critical-access-hospital-after-hours"),
        ("Cost", "The true cost of after-hours on-call",
         "The four line items that never get totalled in the same place.",
         "/resources/true-cost-of-after-hours-on-call"),
        ("Basics", "Nurse triage vs answering service",
         "The distinction that justifies the price difference, in one table.",
         "/resources/nurse-triage-vs-answering-service"),
    ])}

    {faq_block(qa)}

    {sources_block([
        "HRSA Health Center Program requirements &mdash; after-hours coverage.",
        "CMS conditions of participation for critical access hospitals.",
        "CMS CY2025 Physician Fee Schedule &mdash; Advanced Primary Care Management.",
        "Rural Health Information Hub &mdash; critical access hospital resources.",
        "National Association of Community Health Centers &mdash; APCM guidance.",
    ], disclaimer=(
        "Program requirements and payment rates change annually. Nothing here is "
        "compliance advice &mdash; verify against current HRSA, CMS, and MAC guidance, "
        "and confirm any coverage arrangement with your own compliance staff."
    ))}"""

    page.schema = [
        service_node(
            page,
            name="24/7 nurse triage for FQHCs, rural health clinics, and critical access hospitals",
            service_type="Telephone nurse triage",
            description=(
                "24/7 telephone nurse triage for federally qualified health centers, "
                "rural health clinics, and critical access hospitals, staffed by U.S. "
                "state-licensed registered nurses on Schmitt-Thompson protocols and "
                "priced on a flat monthly structure for safety-net budgets."
            ),
            audience=(
                "Federally qualified health centers, rural health clinics, and "
                "critical access hospitals"
            ),
        ),
        faq_node(page, qa),
    ]
    return page
