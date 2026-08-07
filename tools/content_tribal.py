#!/usr/bin/env python3
"""
Content for the tribal / IHS track on tulq.health.

This is the lane the research identified as uncontested: none of the
established nurse-triage vendors publish anything for tribal health
programs, IHS beneficiaries, PRC budget protection, or Buy Indian Act
contracting.

Everything factual here comes from public sources - statute, CFR, IHS
program documentation, and SAM.gov notices. Claims about TULQ itself are
limited to what the homepage already states.
"""

from __future__ import annotations

from pagekit import (
    TRIBAL, Page, card_grid, faq_block, faq_node, article_node,
    service_node, sources_block,
)

SITE = TRIBAL


# ══════════════════════════════════════════════════════════════════════
# PILLAR 1 - Tribal health & IHS
# ══════════════════════════════════════════════════════════════════════

def pillar_tribal_ihs() -> Page:
    page = Page(
        site=SITE,
        slug="for/tribal-health-ihs",
        title="IHS Nurse Advice Line for Tribal Health | TULQ",
        description=(
            "A 24/7 nurse advice line for IHS service units, 638 tribal health programs, "
            "and Urban Indian Organizations. Native-owned and RN-answered. Talk to us."
        ),
        eyebrow="Tribal health &amp; IHS",
        h1="A nurse line built for <em>Indian Country.</em>",
        deck=(
            "Every national nurse-triage vendor serves hospices, home health agencies, "
            "and health plans. None of them were built for a tribal health program with "
            "a finite Purchased/Referred Care budget and patients three hours from the "
            "nearest emergency department. TULQ was."
        ),
        crumbs=[("Who we serve", "/for/tribal-health-ihs")],
        reviewed=True,
        priority="0.9",
        cta_title="Bring the line to your service unit.",
        cta_body=(
            "Whether you run a 638 program, an IHS service unit, or an Urban Indian "
            "Organization, we can walk through what after-hours coverage would look "
            "like for your population."
        ),
    )

    qa = [
        ("Do we have to go through an IHS Area solicitation?",
         "<p>Not if you operate under a 638 contract or a self-governance compact. "
         "Programs that have assumed operation of their own health services under the "
         "Indian Self-Determination and Education Assistance Act make their own "
         "procurement decisions, including after-hours coverage. IHS-operated service "
         "units generally do procure through their Area office, and those requirements "
         "surface on SAM.gov, see our "
         "<a href=\"/for/contracting-officers\">page for contracting officers</a>.</p>"),
        ("How does a nurse line protect our PRC budget?",
         "<p>Purchased/Referred Care pays for care delivered outside your facility, and "
         "an outside emergency department visit is one of the more expensive things PRC "
         "buys. When a caller who needs a next-morning appointment goes to the ER "
         "instead, because there was nowhere else to call at 11 p.m., that "
         "is a PRC expense that did not have to happen. Nurse triage puts a clinical "
         "decision between the symptom and the emergency department. "
         "<a href=\"/resources/nurse-advice-line-prc-budget\">We walk through the "
         "mechanics here.</a></p>"),
        ("What makes this different from any other nurse triage vendor?",
         "<p>Two things that are structural rather than marketing. First, ownership: "
         "TULQ is wholly owned by an enrolled citizen of the Snoqualmie Indian Tribe, "
         "which makes it eligible to compete as an Indian Economic Enterprise under the "
         "Buy Indian Act. Second, design: cultural competency sits at the protocol "
         "level rather than in a training module: how the nurse asks about pain, "
         "how she reads a multigenerational household, what she assumes about the "
         "distance to definitive care.</p>"),
        ("Are your nurses licensed in our state?",
         "<p>Telephone triage nurses must hold licensure appropriate to the state where "
         "the patient is located. TULQ staffs U.S. state-licensed registered nurses and "
         "scopes licensure coverage to the service area of each engagement. That is a "
         "question worth asking every vendor you evaluate, and worth putting in the "
         "contract.</p>"),
        ("Can you serve an Urban Indian Organization?",
         "<p>Yes. UIOs are a distinct segment with a distinct problem: they serve a "
         "large share of the AI/AN population but sit outside the Purchased/Referred "
         "Care program, so there is no PRC allocation behind an outside emergency room "
         "visit. The case for after-hours triage at a UIO is about access and "
         "continuity rather than budget protection. "
         "<a href=\"/resources/after-hours-coverage-urban-indian-organizations\">More "
         "on that here.</a></p>"),
    ]

    page.body = f"""    <p>Roughly 2.8 million American Indian and Alaska Native people rely on the
    Indian Health Service system for care, delivered through IHS-operated service
    units, tribally operated 638 programs, and Urban Indian Organizations. What
    almost none of those facilities can staff around the clock is the telephone.</p>

    <p>When the clinic closes, the options narrow to two: wait until morning, or go
    to the emergency department. One of those is bad for the patient. The other is
    expensive for the program, and in a Purchased/Referred Care system, it is
    expensive in a way that has a hard ceiling.</p>

    <h2>The problem nobody built for</h2>

    <p>The telephone triage industry is mature. Vendors have been operating since the
    mid-1990s and they are competent at what they do. But look at who they built for:
    hospices, home health agencies, physician groups, health plans, and health
    systems. Their case studies are about hospice CAHPS scores and emergency
    department avoidance for commercially insured populations.</p>

    <p>That is a real business. It is not this one. A tribal health program's
    after-hours problem has three features that the mainstream market does not
    share:</p>

    <ul>
      <li><strong>A capped, appropriated budget.</strong> Purchased/Referred Care
      funds are finite and allocated annually. An avoidable ER visit is not a
      utilization statistic; it is money that a program cannot spend on something
      else, and when the allocation is committed, later requests can be deferred.</li>
      <li><strong>Distance.</strong> For many service populations, "just go to the
      ER" means an hour or more of driving, often at night, often in weather, often
      by someone who should not be driving.</li>
      <li><strong>A history that shapes the call.</strong> Institutional medical care
      in Indian Country arrives carrying the boarding-school era, chronic
      underfunding, and generations of being treated as a case rather than a person.
      A triage nurse who does not know that misreads what she is hearing.</li>
    </ul>

    <h2>What TULQ actually does</h2>

    <p>A patient calls one number, any hour. A U.S. state-licensed registered nurse
    picks up, not a call center agent, not a queue, not a voicemail box. The
    nurse assesses the caller against Schmitt-Thompson telephone triage protocols,
    the physician-authored standard used across the industry, and reaches one of a
    defined set of dispositions: care for it at home, be seen in the clinic tomorrow,
    go to urgent care, or go to the emergency department now.</p>

    <p>The encounter is documented and returned to the program, so the clinic that
    opens at eight in the morning already knows who called at two.</p>

    <div class="callout callout--teal">
      <div class="callout-head">The part that is table stakes</div>
      <p>Every serious nurse triage vendor runs Schmitt-Thompson or an equivalent
      protocol set. Any vendor telling you their protocol library is the
      differentiator is selling you the floor. Ask instead about who answers, what
      licensure they hold, how escalation works, and what the documentation looks
      like when it lands in your system.</p>
    </div>

    <h2>Who this is built for</h2>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr>
            <th>Program type</th>
            <th>What after-hours coverage solves</th>
            <th>How it usually gets procured</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>IHS-operated service units</td>
            <td>Round-the-clock access for the service population without adding
            overnight clinical staff; ER diversion against the PRC allocation.</td>
            <td>Area office contracting, posted on SAM.gov, frequently as a
            Buy Indian Act set-aside.</td>
          </tr>
          <tr>
            <td>638 tribal health programs</td>
            <td>The same coverage, under the program's own clinical governance and
            its own definition of culturally appropriate care.</td>
            <td>Direct procurement by the tribe or tribal organization. No IHS
            solicitation required.</td>
          </tr>
          <tr>
            <td>Self-governance compacts</td>
            <td>Coverage designed around a compact's own service array rather than a
            standard IHS scope of work.</td>
            <td>Direct procurement under the compact.</td>
          </tr>
          <tr>
            <td>Urban Indian Organizations</td>
            <td>Continuity for an urban AI/AN patient population that has no PRC
            backstop and often no other culturally grounded option after hours.</td>
            <td>Direct procurement, often against Title V or grant funding.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>Native-owned, and why that is a procurement fact</h2>

    <p>TULQ is wholly owned by Michael Chavez Ross, an enrolled citizen of the
    Snoqualmie Indian Tribe. That is a statement about the company's structure, and
    under federal procurement law it has consequences: the Buy Indian Act, at
    25 U.S.C. &sect; 47, authorizes IHS to set requirements aside for Indian-owned
    economic enterprises, and IHS strengthened that preference in a 2022 final
    rule.</p>

    <p>For a contracting officer running market research, the practical question is
    whether a capable Indian enterprise exists for this requirement. When the answer
    is no, the requirement moves to another set-aside authority or to open
    competition. <a href="/buy-indian-act">We explain how that mechanism works, and
    what it takes to qualify, here.</a></p>

    <div class="callout">
      <div class="callout-head">To be clear about what we are not</div>
      <p>TULQ is not affiliated with, sponsored by, or endorsed by the Snoqualmie
      Indian Tribe. Our founder's tribal citizenship is held in his personal
      capacity. The company is separately and wholly owned by him.</p>
    </div>

    <h2>Cultural competency, specifically</h2>

    <p>"Culturally competent" is a phrase that has been worn smooth by overuse. Here
    is what we mean by it operationally:</p>

    <ul>
      <li><strong>The nurse does not treat a caregiver as an obstacle.</strong> When
      a granddaughter calls about her grandmother, she is often the person who
      manages that household's health. Protocols that insist on speaking only to the
      patient generate friction and end calls early.</li>
      <li><strong>Distance is a clinical variable.</strong> A disposition of "go to
      the ER" means something different at fifteen minutes than at two hours. The
      nurse should know which one she is saying.</li>
      <li><strong>Stoicism is not the absence of symptoms.</strong> A caller who
      understates pain is common enough in Indian Country that a triage nurse who
      takes self-reported severity at face value will systematically under-triage.</li>
      <li><strong>Distrust is information, not non-compliance.</strong> A patient
      hesitant about the emergency department may be describing a prior experience
      accurately. The right response is to work the problem, not to note refusal.</li>
    </ul>

    <p>None of that is exotic. It is what a nurse who knows the population does
    without being asked, and what a nurse who does not know the population gets
    wrong at scale.</p>

    <h2>Where to go next</h2>

    {card_grid([
        ("Contracting", "For contracting officers",
         "Sources Sought, market research, NAICS codes, and how IHS nurse advice line requirements reach the market.",
         "/for/contracting-officers"),
        ("Set-asides", "The Buy Indian Act, explained",
         "25 U.S.C. § 47, the 2022 IHS final rule, and the difference between an IEE and an ISBEE.",
         "/buy-indian-act"),
        ("Geography", "Coverage by IHS Area",
         "All twelve IHS Areas, the states each covers, and where nurse advice line procurement has been active.",
         "/areas/"),
        ("PRC", "Protecting the PRC budget",
         "How avoidable emergency department use draws down a finite Purchased/Referred Care allocation.",
         "/resources/nurse-advice-line-prc-budget"),
    ])}

    {faq_block(qa)}

    {sources_block([
        ("Indian Health Service, <em>Purchased/Referred Care</em> program documentation.",
             "https://www.ihs.gov/prc/"),
        ("Buy Indian Act, 25 U.S.C. &sect; 47, and the IHS Buy Indian Act final rule (2022).",
             "https://www.federalregister.gov/documents/2022/01/13/2021-28156/acquisition-regulations-buy-indian-act-procedures-for-contracting"),
        ("Indian Self-Determination and Education Assistance Act of 1975, P.L. 93-638 (25 U.S.C. &sect; 5301).",
             "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section5301&num=0&edition=prelim"),
        ("Indian Health Care Improvement Act, Title V (Urban Indian Health Program).",
             "https://www.ihs.gov/urban/"),
        ("Schmitt-Thompson telephone triage protocols.",
             "https://www.stcc-triage.com/"),
    ], disclaimer=(
        "TULQ is launching in 2026. Nothing on this page describes contract "
        "performance or call volumes we have not yet delivered. Service-population "
        "figures are drawn from published IHS program materials and change over time."
    ))}"""

    page.schema = [
        service_node(
            page,
            name="24/7 nurse advice line for tribal health programs and IHS service units",
            service_type="Telephone nurse triage",
            description=(
                "A 24/7 telephone nurse advice line answered by U.S. state-licensed "
                "registered nurses using Schmitt-Thompson protocols, built for Indian "
                "Health Service service units, 638 tribal health programs operating "
                "under ISDEAA, self-governance compacts, and Urban Indian Organizations."
            ),
            audience=(
                "IHS service units, 638 tribal health programs, self-governance "
                "compacts, and Urban Indian Organizations"
            ),
        ),
        faq_node(page, qa),
    ]
    return page


# ══════════════════════════════════════════════════════════════════════
# PILLAR 2 - Buy Indian Act
# ══════════════════════════════════════════════════════════════════════

def pillar_buy_indian_act() -> Page:
    page = Page(
        site=SITE,
        slug="buy-indian-act",
        title="Buy Indian Act Nurse Triage Vendor | ISBEE | TULQ",
        description=(
            "How the Buy Indian Act (25 U.S.C. § 47) applies to IHS nurse advice line "
            "contracts, what separates an IEE from an ISBEE, and what officers verify."
        ),
        eyebrow="Federal contracting",
        h1="The Buy Indian Act, <em>in plain language.</em>",
        deck=(
            "A 1910 statute, a 2022 final rule, and one of the least well-documented "
            "corners of federal procurement. If you are a contracting officer scoping a "
            "nurse advice line requirement (or a Native-owned firm trying to "
            "compete for one), this is what actually governs it."
        ),
        crumbs=[("Buy Indian Act", "/buy-indian-act")],
        priority="0.8",
        cta_title="Responding to a Buy Indian set-aside?",
        cta_body=(
            "If you are a contracting officer conducting market research, or another "
            "Indian enterprise looking for a teaming partner on a nurse triage "
            "requirement, get in touch."
        ),
    )

    qa = [
        ("What is the difference between an IEE and an ISBEE?",
         "<p>An Indian Economic Enterprise (IEE) meets the Buy Indian Act's ownership, "
         "control, and management tests: broadly, majority ownership and control "
         "by one or more Indians or Indian Tribes. An Indian Small Business Economic "
         "Enterprise (ISBEE) is an IEE that <em>also</em> qualifies as a small business "
         "under the SBA size standard for the NAICS code on the solicitation. Every "
         "ISBEE is an IEE; not every IEE is an ISBEE.</p>"),
        ("Is the status certified by anyone?",
         "<p>No. Unlike 8(a) or HUBZone, Buy Indian status is self-certified. The "
         "enterprise represents its eligibility in its offer. That does not make it "
         "informal; the representation must be accurate at the time of offer, at "
         "the time of award, and throughout performance, and a contracting officer can "
         "challenge it. A false representation carries the consequences any false "
         "certification to the government carries.</p>"),
        ("Does the Buy Indian Act come before other set-asides?",
         "<p>Under the 2022 IHS final rule, contracting officers are directed to give "
         "the Buy Indian Act preference first consideration for applicable "
         "acquisitions, ahead of other socioeconomic set-aside authorities. In practice "
         "this is why so many IHS nurse advice line requirements appear on SAM.gov as "
         "Buy Indian set-asides rather than as small-business or 8(a) actions.</p>"),
        ("What happens if no capable Indian enterprise responds?",
         "<p>The requirement does not stay unfilled. If market research does not "
         "identify a capable Indian enterprise at a fair and reasonable price, the "
         "contracting officer may proceed under another authority or through open "
         "competition. That is the mechanism by which non-Native firms end up holding "
         "IHS nurse advice line contracts, not because the preference failed, "
         "but because nobody eligible answered the Sources Sought notice.</p>"),
        ("Which NAICS codes show up on these requirements?",
         "<p>Nurse advice line and telephone triage requirements at IHS facilities have "
         "been solicited under several codes, most commonly 621111 (Offices of "
         "Physicians), 621399 (Offices of All Other Miscellaneous Health Practitioners), "
         "and occasionally 541990 (All Other Professional, Scientific, and Technical "
         "Services). The code matters because it sets the SBA size standard, which "
         "determines whether the ISBEE tier is available.</p>"),
    ]

    page.body = f"""    <p>The Buy Indian Act is short, old, and consequential. Enacted in 1910 and
    codified at <strong>25 U.S.C. &sect; 47</strong>, it authorizes the Secretary of
    the Interior (and, through subsequent transfers of authority, the Indian
    Health Service) to purchase products and services from Indian-owned
    economic enterprises, using Indian labor, "so far as may be practicable."</p>

    <p>For most of its history the statute was applied unevenly. That changed with
    the IHS Buy Indian Act final rule in 2022, which tightened the definitions,
    clarified the representation requirements, and instructed contracting officers to
    consider the Buy Indian preference <em>first</em> for applicable acquisitions.</p>

    <h2>The two tiers</h2>

    <p>Nearly every question about Buy Indian eligibility resolves to which of two
    categories an enterprise falls into.</p>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr>
            <th>&nbsp;</th>
            <th>Indian Economic Enterprise (IEE)</th>
            <th>Indian Small Business Economic Enterprise (ISBEE)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Ownership test</td>
            <td>Majority owned by one or more Indians or Indian Tribes</td>
            <td>Same</td>
          </tr>
          <tr>
            <td>Control test</td>
            <td>Indian ownership must control management and daily operations</td>
            <td>Same</td>
          </tr>
          <tr>
            <td>Size test</td>
            <td class="cross">None</td>
            <td class="tick">Must meet the SBA size standard for the solicitation's
            NAICS code</td>
          </tr>
          <tr>
            <td>Certified by</td>
            <td>Self-certification</td>
            <td>Self-certification</td>
          </tr>
          <tr>
            <td>When eligibility must hold</td>
            <td>At offer, at award, and throughout performance</td>
            <td>Same</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>How a requirement actually reaches the market</h2>

    <p>Contracting officers do not set a requirement aside on a hunch. The sequence
    on a typical IHS nurse advice line acquisition looks like this:</p>

    <ol>
      <li><strong>Market research.</strong> The contracting officer determines whether
      capable Indian enterprises exist for the requirement. The HHS Acquisition
      Regulation coverage on Buy Indian market research is the governing procedure,
      and it is frequently cited by number in the solicitation itself.</li>
      <li><strong>A Sources Sought notice.</strong> Posted publicly on SAM.gov, this
      asks interested enterprises to describe their capability and represent their
      status. It is market research, not a solicitation; responding does not
      obligate anyone, and publishing one does not guarantee an award will
      follow.</li>
      <li><strong>The set-aside decision.</strong> If capable Indian enterprises
      respond, the requirement is set aside for IEEs or ISBEEs. If they do not, it
      proceeds another way.</li>
      <li><strong>The solicitation.</strong> An RFQ or RFP, with the Buy Indian
      representation provisions incorporated.</li>
    </ol>

    <div class="callout callout--amber">
      <div class="callout-head">The step that decides the outcome</div>
      <p>Step two is where most of these requirements are actually won or lost. A
      Sources Sought notice with no qualified Indian responses is the documented
      justification for going elsewhere. An Indian enterprise that watches SAM.gov
      and answers those notices, even when the notice is not yet a contract, is doing the single highest-leverage thing available to it.</p>
    </div>

    <h2>What contracting officers verify</h2>

    <p>A representation is a starting point, not the end of it. Expect a contracting
    officer to look at:</p>

    <ul>
      <li><strong>SAM.gov registration</strong> that is active, with the entity name,
      CAGE code, and business-type representations internally consistent. A mismatch
      between the legal entity name on the registration and the name on the offer is
      a common and entirely avoidable disqualifier.</li>
      <li><strong>Evidence of tribal citizenship or tribal ownership</strong> for the
      owners on whom the representation rests.</li>
      <li><strong>Actual control</strong>: whether the Indian owner runs the
      company, or whether management and daily operations sit somewhere else.</li>
      <li><strong>Capability for this requirement</strong>, which for clinical
      services means licensure, protocols, staffing model, and documentation, not
      just corporate status.</li>
    </ul>

    <h2>Where TULQ sits</h2>

    <p>TULQ is wholly owned by Michael Chavez Ross, an enrolled citizen of the
    Snoqualmie Indian Tribe, who serves as its CEO and President. On that basis the
    company is eligible to compete as an Indian Economic Enterprise under
    25 U.S.C. &sect; 47.</p>

    <p>The clinical side is led by Jayson Forrest Minagawa, RN, BSN, whose background
    runs across ICU, telehealth, corrections triage, and skilled-nursing leadership.
    That combination (Native ownership plus a credentialed clinical operator) is the thing a Buy Indian set-aside for a nurse advice line is actually
    looking for, and it is rarer in the market than it should be.</p>

    {faq_block(qa)}

    {sources_block([
        ("Buy Indian Act, 25 U.S.C. &sect; 47.",
             "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section47&num=0&edition=prelim"),
        ("Indian Health Service, Buy Indian Act Acquisition Regulation final rule (2022).",
             "https://www.federalregister.gov/documents/2022/01/13/2021-28156/acquisition-regulations-buy-indian-act-procedures-for-contracting"),
        ("HHS Acquisition Regulation (HHSAR), 48 CFR Part 326, Buy Indian Act coverage.",
             "https://www.ecfr.gov/current/title-48/chapter-3/subchapter-D/part-326"),
        ("U.S. Small Business Administration size standards by NAICS code.",
             "https://www.sba.gov/document/support-table-size-standards"),
        ("SAM.gov contract opportunities, Indian Health Service.",
             "https://sam.gov/search/?index=opp"),
    ], disclaimer=(
        "This page is a plain-language explainer, not legal or acquisition advice. "
        "Regulations are amended; verify current requirements against the CFR, the "
        "HHSAR, and the terms of the specific solicitation before relying on any of it."
    ))}"""

    page.schema = [faq_node(page, qa)]
    return page


# ══════════════════════════════════════════════════════════════════════
# PILLAR 3 - For contracting officers
# ══════════════════════════════════════════════════════════════════════

def pillar_contracting_officers() -> Page:
    page = Page(
        site=SITE,
        slug="for/contracting-officers",
        title="IHS Nurse Triage Sources Sought &amp; RFQs | TULQ",
        description=(
            "For IHS contracting officers researching nurse advice line requirements: "
            "capability summary, NAICS codes, and recent procurement history by Area."
        ),
        eyebrow="For contracting officers",
        h1="A capability statement <em>you can search for.</em>",
        deck=(
            "If you are conducting market research on a nurse advice line or telephone "
            "triage requirement and trying to establish whether a capable Indian "
            "enterprise exists, this page exists to answer that question without a "
            "phone call."
        ),
        crumbs=[("For contracting officers", "/for/contracting-officers")],
        priority="0.8",
        cta_title="Conducting market research?",
        cta_body=(
            "Send us the notice number and the response deadline. We answer Sources "
            "Sought notices, and we are glad to be a data point in your market research "
            "whether or not it ends in an award."
        ),
    )

    qa = [
        ("Are you registered in SAM.gov?",
         "<p>Yes. TULQ maintains an active SAM.gov registration with a UEI and CAGE "
         "code. If any representation on the registration does not match what you see "
         "on an offer, contact us directly and we will resolve it rather than leaving "
         "you to reconcile it.</p>"),
        ("What is your Buy Indian status?",
         "<p>TULQ is wholly owned and controlled by an enrolled citizen of the "
         "Snoqualmie Indian Tribe and is eligible to compete as an Indian Economic "
         "Enterprise under 25 U.S.C. &sect; 47. Whether the ISBEE tier applies depends "
         "on the SBA size standard for the NAICS code on your solicitation; at "
         "our size, it generally does. "
         "<a href=\"/buy-indian-act\">Background on the distinction.</a></p>"),
        ("Will you respond to a Sources Sought notice even if an award is uncertain?",
         "<p>Yes, and we would rather you ask. A Sources Sought notice with no "
         "qualified Indian responses becomes the documented basis for moving the "
         "requirement to another authority. If we are capable of performing, the useful "
         "thing for both of us is that the record reflects it.</p>"),
        ("Can you team with another enterprise?",
         "<p>Yes. Some requirements are larger than a single small enterprise should "
         "take on alone, and some combine nurse triage with adjacent services. We are "
         "open to teaming and to subcontracting arrangements, in either direction.</p>"),
        ("What clinical documentation can you provide during evaluation?",
         "<p>Licensure verification for assigned nursing staff, the protocol standard "
         "in use, the escalation and documentation workflow, HIPAA safeguards, and "
         "clinical leadership credentials. A capability statement is available on "
         "request through our <a href=\"/contact\">contact page</a>.</p>"),
    ]

    page.body = f"""    <h2>What we do, in one paragraph</h2>

    <p>TULQ operates a 24/7 telephone nurse advice line. U.S. state-licensed
    registered nurses answer inbound calls, assess callers against Schmitt-Thompson
    telephone triage protocols, reach a documented disposition, and escalate or refer
    according to the protocol and the client's own escalation rules. Encounter
    documentation is returned to the facility. The service is designed for Indian
    Health Service service units, tribally operated 638 programs, self-governance
    compacts, and Urban Indian Organizations.</p>

    <h2>Procurement facts</h2>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr><th>Item</th><th>Detail</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Entity</td>
            <td>TULQ LLC</td>
          </tr>
          <tr>
            <td>Buy Indian status</td>
            <td>Indian Economic Enterprise: wholly owned and controlled by an
            enrolled citizen of the Snoqualmie Indian Tribe (25 U.S.C. &sect; 47)</td>
          </tr>
          <tr>
            <td>Typical NAICS</td>
            <td>621111 &middot; 621399 &middot; 541990: we can represent under
            the code on your solicitation</td>
          </tr>
          <tr>
            <td>Registrations</td>
            <td>Active SAM.gov registration; UEI and CAGE on file</td>
          </tr>
          <tr>
            <td>Clinical standard</td>
            <td>Schmitt-Thompson telephone triage protocols; U.S. state-licensed RNs</td>
          </tr>
          <tr>
            <td>Clinical leadership</td>
            <td>Jayson Forrest Minagawa, RN, BSN (Clinical Director)</td>
          </tr>
          <tr>
            <td>Capability statement</td>
            <td>Available on request</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>Where these requirements have been appearing</h2>

    <p>Nurse advice line and telephone triage requirements surface across the IHS
    system irregularly, but recent public activity has concentrated in a handful of
    Areas. The notices below are matters of public record on SAM.gov, listed here as
    context for the shape of this market, not as live opportunities.</p>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr>
            <th>IHS Area</th>
            <th>Facility</th>
            <th>Public record</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><a href="/areas/great-plains-area">Great Plains</a></td>
            <td>Woodrow Wilson Keeble Memorial Health Care Center, Sisseton SD</td>
            <td>Sources Sought IHS1520417 (Dec 2025), following IHS1507826 (early
            2025). ISBEE/IEE set-aside, NAICS 621111. Toll-free nurse advice and
            medical library line intended to reduce ER use.</td>
          </tr>
          <tr>
            <td><a href="/areas/phoenix-area">Phoenix</a></td>
            <td>Colorado River, Uintah &amp; Ouray, Southern Bands; Phoenix Indian
            Medical Center</td>
            <td>RFQ-26-PHX-046 covering three service units; Sources Sought
            SS-25-PHX-002 for PIMC. Buy Indian market research, NAICS 621399.</td>
          </tr>
          <tr>
            <td><a href="/areas/navajo-area">Navajo</a></td>
            <td>Gallup Service Unit</td>
            <td>Sources Sought published January 2025; five-year period of
            performance; NAICS 621399; Buy Indian Act preference.</td>
          </tr>
          <tr>
            <td><a href="/areas/albuquerque-area">Albuquerque</a></td>
            <td>Santa Fe Indian Health Center; Acoma-Ca&ntilde;oncito-Laguna</td>
            <td>RFQ 75H70725Q00103 awarded August 2025. Separate ACL Sources Sought
            for 24/7 nurse phone triage as an ISBEE set-aside, NAICS 541990.</td>
          </tr>
          <tr>
            <td><a href="/areas/portland-area">Portland</a></td>
            <td>Yakama Indian Health Center, Toppenish WA</td>
            <td>RFQ 75H71325Q00030, "24 Hour Nurse Advice Line," base year plus four
            option years. Solicited as a Women-Owned Small Business set-aside rather
            than under Buy Indian, NAICS 621111.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="callout">
      <div class="callout-head">Two caveats worth stating plainly</div>
      <p>A Sources Sought notice is market research, not a commitment to solicit or
      award. And we have deliberately left obligation amounts off this page: the
      dollar figures circulating for several of these actions come from third-party
      estimates rather than confirmed FPDS records, and we would rather publish
      nothing than publish a number you would then have to correct.</p>
    </div>

    <h2>The structural observation</h2>

    <p>Several of the requirements above were set aside under the Buy Indian Act, and
    at least one recent award went to a firm that is not an Indian Economic
    Enterprise. That is not a criticism of the contracting officers involved; it is the documented, correct outcome when market research does not surface a
    capable Indian enterprise at a fair and reasonable price.</p>

    <p>It is also the gap TULQ was built to close. A credentialed, RN-led, Native-owned
    enterprise that actually answers Sources Sought notices removes the justification
    for deviating from the preference.</p>

    {faq_block(qa)}

    {sources_block([
        ("SAM.gov contract opportunities, the Indian Health Service notices cited above.",
             "https://sam.gov/search/?index=opp"),
        ("Buy Indian Act, 25 U.S.C. &sect; 47, and the IHS Buy Indian Act final rule (2022).",
             "https://www.federalregister.gov/documents/2022/01/13/2021-28156/acquisition-regulations-buy-indian-act-procedures-for-contracting"),
        ("HHS Acquisition Regulation (HHSAR), 48 CFR Part 326.",
             "https://www.ecfr.gov/current/title-48/chapter-3/subchapter-D/part-326"),
        ("U.S. Small Business Administration size standards by NAICS code.",
             "https://www.sba.gov/document/support-table-size-standards"),
    ], disclaimer=(
        "Solicitation details are summarized from public SAM.gov postings and were "
        "accurate as posted; notices are amended, cancelled, and superseded. Always "
        "work from the current notice. TULQ is launching in 2026 and this page "
        "describes capability and corporate status, not past contract performance."
    ))}"""

    page.schema = [faq_node(page, qa)]
    return page
