#!/usr/bin/env python3
"""
The /resources track on tulq.health, plus the tribal comparison page.

These are the top-of-funnel and authority pieces the research called for:
genuinely citable explainers that tribal health orgs, journalists, and
researchers have a reason to link to. Every factual claim is sourced to
public material - IHS, CMS, KFF, statute, CFR.
"""

from __future__ import annotations

from pagekit import (
    TRIBAL, Page, article_node, card_grid, faq_block, faq_node, sources_block,
)

SITE = TRIBAL


def _post(slug: str, title: str, description: str, eyebrow: str, h1: str,
          deck: str, body: str, *, reviewed: bool = False,
          qa: list | None = None, sources: list[str] | None = None,
          disclaimer: str = "", cta_title: str = "", cta_body: str = "") -> Page:
    page = Page(
        site=SITE,
        slug=f"resources/{slug}",
        title=title,
        description=description,
        eyebrow=eyebrow,
        h1=h1,
        deck=deck,
        body="",
        crumbs=[("Resources", "/resources/"), (eyebrow, f"/resources/{slug}")],
        page_type="Article",
        reviewed=reviewed,
        priority="0.6",
        cta_title=cta_title,
        cta_body=cta_body,
    )
    parts = [body]
    if qa:
        parts.append(faq_block(qa))
    if sources:
        parts.append(sources_block(sources, disclaimer=disclaimer))
    page.body = "\n\n    ".join(parts)
    page.schema = [article_node(page)]
    if qa:
        page.schema.append(faq_node(page, qa))
    return page


# ══════════════════════════════════════════════════════════════════════

def post_prc_budget() -> Page:
    qa = [
        ("Does IHS pay for an emergency room visit?",
         "<p>Sometimes, and not automatically. If the visit is at a non-IHS facility, "
         "payment runs through Purchased/Referred Care, which has eligibility rules, "
         "notification deadlines, medical priority criteria, and a finite annual "
         "allocation. IHS is also generally the payer of last resort, so alternate "
         "resources must be pursued first. A patient who assumes the visit is covered "
         "may end up personally billed.</p>"),
        ("What is the notification deadline for a PRC emergency?",
         "<p>PRC programs require notification within a defined window after emergency "
         "care is received, and the window is short. Missing it is one of the more "
         "common reasons a claim is denied. The exact requirement is set in program "
         "regulation; check with your PRC office rather than relying on a "
         "general figure.</p>"),
        ("Is nurse triage a PRC-payable service?",
         "<p>That is the wrong frame. A nurse advice line is generally procured as a "
         "service contract by the facility or program, funded from operating budget "
         "rather than drawn from the PRC allocation. Its relationship to PRC is on the "
         "other side of the ledger: it exists to reduce what PRC has to pay for.</p>"),
    ]

    body = """    <p>Ask a tribal health director what keeps them up at night and Purchased/Referred
    Care will be on the short list. Not because the program is badly run, but because
    of a structural feature that is easy to state and hard to live with: the money
    runs out.</p>

    <h2>How PRC actually works</h2>

    <p>Purchased/Referred Care (PRC, and before 2014, Contract Health Services) is how the Indian Health Service pays for care that a patient needs but
    that the local IHS or tribal facility cannot provide. Specialty consults, surgery,
    imaging that isn't available on site, and emergency care at an outside hospital all
    run through it.</p>

    <p>Four features of the program matter for this discussion:</p>

    <ul>
      <li><strong>It is appropriated, not entitled.</strong> PRC receives an annual
      allocation. It is not an open-ended benefit that expands to meet demand.</li>
      <li><strong>IHS is generally the payer of last resort.</strong> If a patient has
      Medicare, Medicaid, private insurance, or another alternate resource, that
      resource is pursued first.</li>
      <li><strong>Eligibility is specific.</strong> Residence in a defined delivery
      area, tribal membership or descent criteria, and notification requirements all
      apply.</li>
      <li><strong>Care is prioritized medically.</strong> When funds are constrained,
      programs work down a medical priority framework. Lower-priority referrals get
      deferred, which in practice can mean denied.</li>
    </ul>

    <div class="callout callout--amber">
      <div class="callout-head">The sentence that matters</div>
      <p>When a program's PRC funds are committed for the year, the next referral does
      not simply cost more. It may not happen. Deferred services are a documented,
      recurring feature of the program, not an anomaly.</p>
    </div>

    <h2>Where the emergency department fits</h2>

    <p>An emergency department visit at a non-IHS hospital is one of the more expensive
    single items PRC buys, and it is the item over which a program has the least
    control. Nobody schedules it. It arrives as a bill.</p>

    <p>Some of those visits are exactly what an emergency department is for. Chest
    pain, stroke symptoms, major trauma, an infant with a high fever: those are
    correct decisions, and a nurse advice line should send them.</p>

    <p>But a meaningful share of after-hours emergency department use nationally is for
    conditions that could have been managed in a primary care setting the following
    morning. In a system with a commercial payer, that is an efficiency problem. In a
    PRC system, it is a rationing problem: the money spent on an avoidable visit in
    March is not available for a referral in August.</p>

    <h2>Why the alternative is usually nothing</h2>

    <p>Here is the part that gets missed. Telling patients to use the emergency
    department appropriately assumes there is something else to do at eleven at
    night. For much of Indian Country there isn't.</p>

    <ul>
      <li>The clinic is closed and will not open until morning.</li>
      <li>Urgent care, where it exists at all, is often the same drive as the ER.</li>
      <li>The nearest emergency department may be an hour or more away, which
      means the decision to go is itself costly, and the decision not to go is
      frightening.</li>
      <li>A general nurse line, if the patient has access to one through another
      payer, does not know the patient, the facility, or the referral pathway.</li>
    </ul>

    <p>A parent with a feverish child at 2 a.m. and no one to ask is not making a
    utilization decision. They are guessing. Some of them guess toward the emergency
    department when they did not need to, and some guess away from it when they did.
    Both errors are expensive; the second one is worse.</p>

    <h2>What a nurse advice line changes</h2>

    <p>It puts a clinician in the gap. A registered nurse assesses the caller against
    physician-authored protocols and reaches a defined disposition, home care,
    clinic in the morning, urgent care, or emergency department now. Three things
    follow from that:</p>

    <ol>
      <li><strong>Avoidable visits get diverted.</strong> The caller who needed
      reassurance and a next-day appointment gets exactly that, and the PRC allocation
      is not touched.</li>
      <li><strong>Necessary visits get accelerated.</strong> The caller who was going
      to wait until morning with symptoms that should not wait is told to go now. That
      one costs PRC money, and is the reason the service is clinically worth
      having, independent of the budget.</li>
      <li><strong>The clinic starts the day informed.</strong> Encounter documentation
      comes back to the program, so the morning schedule reflects who called
      overnight.</li>
    </ol>

    <div class="callout callout--teal">
      <div class="callout-head">How to model this honestly</div>
      <p>Any vendor who hands you a guaranteed diversion percentage is guessing.
      The defensible way to size it is with your own numbers: your after-hours call
      volume, your PRC spend on outside emergency department visits, and a
      conservative assumption about what share of those visits were primary-care
      treatable. Run the arithmetic yourself and treat the result as a range, not a
      forecast.</p>
    </div>

    <h2>The part that is not about money</h2>

    <p>It would be possible to write this entire piece as a budget argument, and the
    budget argument is real. But the reason to answer the phone at 2 a.m. is that
    somebody is on the other end of it.</p>

    <p>For a population that has spent generations being told, in one way or another,
    to wait, a nurse who picks up on the first ring and already understands the
    household she is talking to is not a cost-containment measure. The PRC savings are
    a consequence of doing the right thing, which is a much better order for those two
    to come in.</p>"""

    return _post(
        slug="nurse-advice-line-prc-budget",
        title="How a Nurse Advice Line Protects Your PRC Budget",
        description=(
            "Purchased/Referred Care is a finite annual allocation and avoidable ER visits "
            "draw against it. How nurse triage changes the arithmetic. Read more."
        ),
        eyebrow="PRC &amp; ER diversion",
        h1="What a nurse line does to <em>your PRC budget.</em>",
        deck=(
            "Purchased/Referred Care is appropriated annually and it runs out. Every "
            "avoidable emergency department visit is money that will not be there for "
            "a referral later in the year. Here is the mechanism, and how to size it "
            "honestly."
        ),
        body=body,
        reviewed=True,
        qa=qa,
        sources=[
            ("Indian Health Service, <em>Purchased/Referred Care</em> program documentation.",
             "https://www.ihs.gov/prc/"),
            ("Indian Health Care Improvement Act, payer of last resort provisions, 25 U.S.C. &sect; 1621e.",
             "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section1621e&num=0&edition=prelim"),
            ("42 CFR Part 136, Indian Health and Purchased/Referred Care regulations.",
             "https://www.ecfr.gov/current/title-42/chapter-I/subchapter-M/part-136"),
            ("Peterson-KFF Health System Tracker, emergency department cost analyses.",
             "https://www.healthsystemtracker.org/brief/emergency-department-visits-exceed-affordability-thresholds-for-many-consumers-with-private-insurance/"),
        ],
        disclaimer=(
            "This is a general explainer, not program guidance. PRC eligibility, "
            "notification deadlines, and medical priority determinations are set by "
            "regulation and administered locally; work from your own PRC office "
            "and the current CFR."
        ),
        cta_title="Want to run the numbers for your program?",
        cta_body=(
            "We are glad to walk through the arithmetic with your PRC and finance staff "
            "using your own call volume and referral data, without a sales pitch "
            "attached."
        ),
    )


def post_what_is_prc() -> Page:
    qa = [
        ("Is Purchased/Referred Care the same as insurance?",
         "<p>No. PRC is a payment program of limited scope, funded by annual "
         "appropriation and subject to eligibility rules, notification deadlines, and "
         "medical priority. It does not function like a health plan, and it is "
         "generally the payer of last resort behind Medicare, Medicaid, and private "
         "coverage.</p>"),
        ("Why was the name changed from Contract Health Services?",
         "<p>The program was renamed Purchased/Referred Care in 2014. The intent was "
         "descriptive accuracy (the program purchases care and manages referrals) "
         "rather than any change in how it works. Older documents, and plenty "
         "of people who have worked in the system a long time, still say CHS.</p>"),
        ("Do Urban Indian Organizations have PRC?",
         "<p>No. PRC operates through IHS-operated and tribally operated facilities. "
         "Urban Indian Organizations, funded under Title V of the Indian Health Care "
         "Improvement Act, sit outside it, which is a distinct and often "
         "overlooked gap. <a href=\"/resources/after-hours-coverage-urban-indian-"
         "organizations\">More on the UIO situation.</a></p>"),
    ]

    body = """    <p>Purchased/Referred Care is one of those programs that everyone inside the IHS
    system understands intuitively and almost nobody outside it understands at all.
    That gap causes real problems, for patients who assume a visit is covered,
    for outside hospitals billing the wrong party, and for vendors pitching tribal
    health programs on economics they have not bothered to learn.</p>

    <h2>The short version</h2>

    <p>The Indian Health Service delivers care directly at its own facilities and at
    tribally operated facilities. When a patient needs care that the local facility
    cannot provide, PRC is the mechanism by which IHS pays an outside provider for
    it.</p>

    <p>That is the whole concept. The complications are all in the conditions.</p>

    <h2>The conditions</h2>

    <h3>Eligibility is not the same as being an IHS patient</h3>

    <p>PRC eligibility generally requires that a person be a member of, or in some
    cases a descendant of a member of, a federally recognized tribe, <em>and</em> that
    they reside within a defined Purchased/Referred Care Delivery Area associated with
    the program. Someone who is unambiguously eligible for direct care at a facility
    may still not be eligible for PRC.</p>

    <h3>IHS is the payer of last resort</h3>

    <p>Statute directs that PRC pays after other resources. Medicare, Medicaid, private
    insurance, VA benefits, and state programs are pursued first. Programs spend
    substantial staff time on alternate resource determination, and a patient who
    declines to apply for coverage they are eligible for can jeopardize PRC payment.</p>

    <h3>Notification deadlines are real and short</h3>

    <p>For emergency care received outside the system, notification to the PRC program
    must happen within a defined window after the visit. Miss it and the claim can be
    denied regardless of medical necessity. This is one of the most common ways
    patients end up personally liable for a bill they reasonably believed was
    covered.</p>

    <h3>Care is prioritized when money is short</h3>

    <p>PRC programs apply a medical priority framework, funding the most urgent
    categories first. When the allocation is constrained, lower-priority services are
    deferred. &ldquo;Deferred&rdquo; is the program's word; from the patient's side it
    can be indistinguishable from denied.</p>

    <div class="callout">
      <div class="callout-head">What this means practically</div>
      <p>A tribal health program managing PRC is doing something closer to running a
      fixed-budget insurance plan than to running a clinic. Every dollar spent on care
      that did not need to be purchased is a dollar unavailable for care that does.</p>
    </div>

    <h2>Why after-hours access sits in the middle of this</h2>

    <p>The category of PRC spending most sensitive to what happens at night is
    emergency department use at outside hospitals. It is expensive, unscheduled, and
    partly discretionary, not in the sense that patients are being frivolous,
    but in the sense that a portion of after-hours ED volume nationally is for
    conditions treatable in primary care the next day.</p>

    <p>The lever on that portion is not patient education. It is having somewhere else
    to call. <a href="/resources/nurse-advice-line-prc-budget">We work through that
    argument in detail here</a>, including how to size it against your own data rather
    than a vendor's assumption.</p>

    <h2>A note for vendors and outside providers</h2>

    <p>If you are selling into tribal health and you have not internalized how PRC
    works, it will show. Pitches built on commercial-payer economics (per-member
    per-month savings, shared-risk arrangements, utilization curves drawn from
    commercially insured populations) land badly on a program whose actual
    constraint is an appropriation that runs out.</p>"""

    return _post(
        slug="what-is-purchased-referred-care",
        title="What Is Purchased/Referred Care (PRC)? | TULQ",
        description=(
            "A plain-language explainer on Purchased/Referred Care: eligibility, payer "
            "of last resort, notification deadlines, medical priority, and why the "
            "budget runs out."
        ),
        eyebrow="PRC explained",
        h1="Purchased/Referred Care, <em>explained.</em>",
        deck=(
            "The program that pays when an IHS or tribal facility cannot provide the "
            "care itself, and the four conditions that make it far more "
            "constrained than outsiders assume."
        ),
        body=body,
        reviewed=True,
        qa=qa,
        sources=[
            ("Indian Health Service, <em>Purchased/Referred Care</em> program documentation.",
             "https://www.ihs.gov/prc/"),
            ("42 CFR Part 136, Indian Health regulations.",
             "https://www.ecfr.gov/current/title-42/chapter-I/subchapter-M/part-136"),
            ("Indian Health Care Improvement Act, 25 U.S.C. &sect; 1621e (payer of last resort).",
             "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section1621e&num=0&edition=prelim"),
        ],
        disclaimer=(
            "General explainer only. Eligibility, deadlines, and priority "
            "determinations are set by regulation and administered locally; verify "
            "against the current CFR and your PRC office."
        ),
    )


def post_isbee_vs_iee() -> Page:
    qa = [
        ("Can a tribally owned corporation be an IEE?",
         "<p>Yes. The Buy Indian Act definitions cover enterprises owned by one or more "
         "Indians or Indian Tribes. A tribally owned corporation and an individually "
         "Indian-owned company can both qualify, provided the ownership, control, and "
         "management tests are met.</p>"),
        ("Do I need to register anywhere to be an ISBEE?",
         "<p>There is no separate ISBEE registry. You need an active SAM.gov "
         "registration with accurate business-type representations, and you represent "
         "your Buy Indian status in your offer. The absence of a certifying body is why "
         "the accuracy of your SAM.gov record carries so much weight.</p>"),
        ("What if the NAICS code changes the size standard?",
         "<p>Then your tier can change with it. An enterprise that qualifies as an "
         "ISBEE under a NAICS code with a $10 million size standard might exceed the "
         "standard under a different code on a different solicitation. Read the code on "
         "each notice; do not assume last year's answer holds.</p>"),
    ]

    body = """    <p>Two acronyms do most of the work in Buy Indian Act contracting, and they are
    routinely used interchangeably by people who should know better. The distinction is
    simple, and getting it wrong on an offer is an unforced error.</p>

    <h2>IEE: Indian Economic Enterprise</h2>

    <p>An Indian Economic Enterprise is a business that meets the Buy Indian Act's
    ownership and control requirements: broadly, that it is owned by one or more
    Indians or Indian Tribes, and that the Indian ownership controls both management
    and daily operations.</p>

    <p>There is no size limit. A large tribally owned enterprise and a two-person
    consultancy can both be IEEs.</p>

    <h2>ISBEE: Indian Small Business Economic Enterprise</h2>

    <p>An ISBEE is an IEE that <em>also</em> meets the Small Business Administration
    size standard for the NAICS code on the specific solicitation.</p>

    <p>That second test is the entire difference. It is also why the answer is
    solicitation-specific: size standards vary by NAICS code, so the same company can
    be an ISBEE on one requirement and an IEE-but-not-ISBEE on another.</p>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr><th>Question</th><th>IEE</th><th>ISBEE</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Indian owned and controlled?</td>
            <td class="tick">Required</td>
            <td class="tick">Required</td>
          </tr>
          <tr>
            <td>Meets SBA size standard for the solicitation's NAICS?</td>
            <td class="cross">Not required</td>
            <td class="tick">Required</td>
          </tr>
          <tr>
            <td>Answer can change between solicitations?</td>
            <td>Rarely: only if ownership changes</td>
            <td>Yes: the NAICS code sets the size standard</td>
          </tr>
          <tr>
            <td>Certified by a third party?</td>
            <td class="cross">No: self-certified</td>
            <td class="cross">No: self-certified</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>Which one does a solicitation call for?</h2>

    <p>Read the notice. IHS set-asides appear both ways, and the notice will say which.
    A nurse advice line requirement solicited under NAICS 621111 with an ISBEE
    set-aside is asking a different question than the same requirement solicited under
    621399 as Buy Indian competitive.</p>

    <p>Where an Area has a stated practice of procuring from small Indian firms, the
    ISBEE tier is where most of the action is.</p>

    <h2>Self-certification is not the same as informal</h2>

    <p>Because there is no certifying body, some enterprises treat the representation
    casually. That is a mistake. The representation must be accurate at the time of
    offer, at the time of award, and throughout performance. A contracting officer can
    challenge it, and a false representation to the government carries the consequences
    any false certification carries.</p>

    <div class="callout callout--amber">
      <div class="callout-head">The failure mode nobody warns you about</div>
      <p>The most common problem is not a bad-faith representation; it is a
      SAM.gov record that does not match the offer. A legal entity name that differs by
      a word, a CAGE code tied to a prior entity, business-type checkboxes that were set
      once and never revisited. Contracting officers reconcile those records, and a
      mismatch reads as a red flag whether or not it is one. Audit your registration
      before you need it, not after a notice drops.</p>
    </div>

    <h2>Why any of this matters for nurse triage</h2>

    <p>Nurse advice line requirements at IHS facilities are frequently set aside under
    the Buy Indian Act, and just as frequently end up with non-Native firms, not because the preference is weak, but because when market research surfaces no
    capable Indian enterprise, the contracting officer is right to proceed another way.</p>

    <p>The remedy is unglamorous: eligible enterprises that watch SAM.gov, keep their
    registrations clean, and answer Sources Sought notices.
    <a href="/for/contracting-officers">More on how those notices work.</a></p>"""

    return _post(
        slug="isbee-vs-iee-set-asides",
        title="ISBEE vs IEE: Which Buy Indian Set-Aside Applies?",
        description=(
            "The difference between an Indian Economic Enterprise and an Indian Small "
            "Business Economic Enterprise, and why it changes with the NAICS code."
        ),
        eyebrow="Set-asides",
        h1="ISBEE or IEE? <em>One test apart.</em>",
        deck=(
            "Two acronyms, one difference: whether you also meet the SBA size standard "
            "for the NAICS code on that particular solicitation. Here is what turns on "
            "it."
        ),
        body=body,
        qa=qa,
        sources=[
            ("Buy Indian Act, 25 U.S.C. &sect; 47.",
             "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section47&num=0&edition=prelim"),
            ("Indian Health Service, Buy Indian Act Acquisition Regulation final rule (2022).",
             "https://www.federalregister.gov/documents/2022/01/13/2021-28156/acquisition-regulations-buy-indian-act-procedures-for-contracting"),
            ("HHS Acquisition Regulation (HHSAR), 48 CFR Part 326.",
             "https://www.ecfr.gov/current/title-48/chapter-3/subchapter-D/part-326"),
            ("U.S. Small Business Administration size standards by NAICS code.",
             "https://www.sba.gov/document/support-table-size-standards"),
        ],
        disclaimer=(
            "Plain-language explainer, not legal or acquisition advice. Verify against "
            "the current CFR, HHSAR, and the terms of the specific solicitation."
        ),
    )


def post_culturally_competent() -> Page:
    body = """    <p>&ldquo;Culturally competent&rdquo; appears in almost every health services
    solicitation aimed at Indian Country, and in almost every vendor response. It has
    been used so widely and so loosely that it has stopped carrying information.</p>

    <p>So here is an attempt to say what it means for one narrow thing: a nurse on a
    telephone, assessing a caller she cannot see, against a protocol written for a
    general population.</p>

    <h2>The protocol is not the problem</h2>

    <p>Schmitt-Thompson telephone triage protocols are good. They are physician-authored,
    extensively validated, and used across the industry for the right reasons. Nothing
    below is an argument for abandoning them.</p>

    <p>But a protocol is a decision structure, not a conversation. It tells the nurse
    what to ask and how to weight the answers. It cannot tell her what a particular
    caller means by an answer, or what they left out, or why.</p>

    <h2>Four places the gap opens</h2>

    <h3>1. Who is allowed to be on the phone</h3>

    <p>A protocol assumes a patient, or a parent of a patient. In many AI/AN households
    the person who manages health is a grandmother, an auntie, or an adult grandchild, someone who knows the patient's medications, history, and baseline better
    than the patient will recite it at 2 a.m.</p>

    <p>A nurse who insists on speaking only to the patient is not being rigorous. She
    is discarding the best available source of clinical information, and she is
    signaling that this system does not understand how the family works.</p>

    <h3>2. What understated pain means</h3>

    <p>Stoicism about pain is common enough across Indian Country that a triage nurse
    who takes a self-reported pain score at face value will systematically
    under-triage. The correction is not to inflate every score; it is to ask
    differently (about function, about sleep, about what the person has stopped
    being able to do) and to weigh the answers against what the caller is not
    saying.</p>

    <h3>3. Distance as a clinical variable</h3>

    <p>&ldquo;Go to the emergency department&rdquo; is one disposition with wildly
    different meanings. At fifteen minutes it is an inconvenience. At two hours, on a
    winter road, for an elder who should not be driving and has no one to drive them,
    it is a decision with its own risk profile.</p>

    <p>A nurse who does not know which situation she is in will either send people on
    trips they should not make or, worse, hedge toward home care because she senses
    resistance without understanding it. Knowing the geography of the service
    population is a clinical competency, not a customer service nicety.</p>

    <h3>4. Hesitancy as information</h3>

    <p>A caller who is reluctant to go to a particular hospital may be describing an
    accurate memory of how they were treated there. Institutional medical care in
    Indian Country carries the boarding-school era, decades of underfunding, and
    plenty of individual experiences that would make anyone cautious.</p>

    <p>Charting that as refusal or non-compliance is both clinically useless and
    corrosive. Treating it as a problem to solve (a different facility, a
    different timing, a call ahead) is the job.</p>

    <div class="callout callout--teal">
      <div class="callout-head">The through-line</div>
      <p>None of these four are about beliefs, ceremony, or traditional medicine, which
      is where cultural competency training usually goes. They are about household
      structure, communication norms, geography, and history, things that change
      what a symptom description means and what a disposition costs.</p>
    </div>

    <h2>How you would actually evaluate a vendor on this</h2>

    <p>Cultural competency is easy to claim and hard to verify. Some questions that
    produce real answers:</p>

    <ul>
      <li>Who wrote your cultural adaptation, and what is their relationship to the
      communities you would be serving?</li>
      <li>Is it a training module the nurses take once, or is it in the workflow the
      nurse follows on every call?</li>
      <li>How do your nurses handle a call from a family member rather than the
      patient? Show me the actual step.</li>
      <li>Does your disposition logic account for travel distance to the nearest
      emergency department? How?</li>
      <li>What happens when a caller declines a disposition?</li>
      <li>Who in your organization is accountable for this, and what is their
      background?</li>
    </ul>

    <p>A vendor with a good answer will have specifics. A vendor without one will
    return to the phrase.</p>

    <h2>Where TULQ stands</h2>

    <p>TULQ is wholly owned by an enrolled citizen of the Snoqualmie Indian Tribe and
    clinically led by a registered nurse whose career runs through ICU, telehealth,
    corrections triage, and skilled-nursing leadership. The cultural orientation is
    built into how the line is designed rather than added as a training layer.</p>

    <p>We would also rather be asked the questions above than take the phrase on
    credit. <a href="/for/tribal-health-ihs">More about how the line is built.</a></p>"""

    return _post(
        slug="culturally-competent-telephone-triage",
        title="Culturally Competent Telephone Triage for AI/AN Patients",
        description=(
            "What cultural competency means on a triage call: household structure, "
            "understated pain, distance as a clinical variable, and how to test a claim."
        ),
        eyebrow="Clinical practice",
        h1="What <em>culturally competent</em> means on a triage call.",
        deck=(
            "The phrase is in every solicitation and every vendor response, which has "
            "drained it of meaning. Here is what it changes, concretely, in the four "
            "places a general-population protocol misreads an AI/AN caller."
        ),
        body=body,
        reviewed=True,
        sources=[
            ("Schmitt-Thompson telephone triage protocols.",
             "https://www.stcc-triage.com/"),
            ("American Academy of Ambulatory Care Nursing, <em>Scope and Standards of Practice for Professional Telehealth Nursing</em>.",
             "https://www.aaacn.org/telehealth-nursing-practice"),
            ("Indian Health Service, quality and patient experience materials.",
             "https://www.ihs.gov/quality/"),
        ],
        disclaimer=(
            "Written from clinical and operational experience, not as a research "
            "finding. Communities differ; nothing here should be read as describing "
            "every AI/AN patient or every tribal nation."
        ),
    )


def post_er_diversion() -> Page:
    body = """    <p>Reducing avoidable emergency department use is a stated goal in a great many
    tribal health strategic plans, and a stated purpose in more than one recent IHS
    solicitation for nurse advice line services. It is worth being precise about what
    the data does and does not support.</p>

    <h2>What we can say with confidence</h2>

    <ul>
      <li><strong>Emergency department reliance is higher among AI/AN people living on
      tribal lands than off them.</strong> KFF's survey work has found a meaningfully
      higher share of AI/AN adults on tribal lands reporting a past-year emergency
      department visit compared with those living off tribal lands.</li>
      <li><strong>Emergency department visits are expensive.</strong> The Peterson-KFF
      Health System Tracker puts the average ED visit at roughly $2,453, of which about
      $1,134 is the evaluation-and-management portion. That figure is materially higher
      than the $1,200&ndash;$1,400 range that circulates in vendor marketing.</li>
      <li><strong>A share of ED volume is primary-care treatable.</strong> This is
      well established across the literature for the general population. The exact
      share depends heavily on how you define it, which is why the published estimates
      range so widely.</li>
      <li><strong>Access, not preference, drives much of it.</strong> When the clinic
      is closed and the alternative is nothing, the emergency department is not a
      choice among options.</li>
    </ul>

    <h2>What we should not claim</h2>

    <p>Vendors in this category routinely publish diversion percentages ("we
    reduce ED utilization by X%") drawn from a single client, a single year, and
    a population that looks nothing like a tribal service population.</p>

    <p>Those numbers are not transferable, and presenting them to a tribal health
    director as a forecast is a good way to lose credibility with someone who will
    check. The honest position is that nurse triage reliably diverts <em>some</em>
    avoidable volume, that the share depends on your baseline, and that the only way to
    know your number is to measure it.</p>

    <div class="callout">
      <div class="callout-head">A defensible way to frame it internally</div>
      <p>Start from your own PRC spend on outside emergency department visits. Apply a
      deliberately conservative assumption about what share was primary-care treatable.
      Apply a second conservative assumption about what share of those would have called
      a nurse line instead. The result is a floor rather than a projection, and a floor
      you can defend in a budget conversation is worth more than a vendor's ceiling.</p>
    </div>

    <h2>The compounding factors in Indian Country</h2>

    <p>Several features specific to AI/AN populations and geography push in the same
    direction:</p>

    <ul>
      <li><strong>Distance.</strong> Long travel to any facility means fewer
      intermediate options between home and the emergency department.</li>
      <li><strong>Chronic disease burden.</strong> Higher prevalence of diabetes and
      cardiovascular disease among AI/AN populations means more conditions that
      generate after-hours symptom questions.</li>
      <li><strong>Workforce shortages.</strong> Vacancy rates for clinical positions in
      the IHS system have been a subject of repeated federal oversight reporting, which
      constrains how much extended-hours coverage a facility can staff itself.</li>
      <li><strong>The PRC ceiling.</strong> Unlike a commercially insured population,
      the financial consequence of an avoidable visit is a hard reduction in what else
      the program can purchase this year.</li>
    </ul>

    <h2>Why the fix is a phone call</h2>

    <p>Most interventions aimed at emergency department use are hard: extend clinic
    hours, hire more clinicians, build urgent care capacity, run patient education
    campaigns. All of those require workforce that is difficult to recruit and retain in
    rural Indian Country.</p>

    <p>A nurse advice line is the exception. It requires no additional on-site staff, no
    new facility, and no change to clinic operations, and it can be procured as a
    service contract. That does not make it a substitute for the harder investments. It
    makes it the one that can be in place in months rather than years.</p>

    <p><a href="/resources/nurse-advice-line-prc-budget">The PRC budget mechanics are
    here</a>, and <a href="/for/tribal-health-ihs">what the service looks like in
    practice is here.</a></p>"""

    return _post(
        slug="reducing-avoidable-er-visits-indian-country",
        title="Reducing Avoidable ER Visits in Indian Country",
        description=(
            "What the data supports on AI/AN emergency department use, what vendors "
            "overclaim, and how to size ER diversion for a tribal health program "
            "honestly."
        ),
        eyebrow="Data &amp; access",
        h1="Avoidable ER visits <em>in Indian Country.</em>",
        deck=(
            "What the evidence actually supports, what the vendor marketing overstates, "
            "and how a tribal health program can size the opportunity in a way that "
            "survives scrutiny."
        ),
        body=body,
        reviewed=True,
        sources=[
            ("KFF research on racial equity and health policy, including AI/AN access and experience.",
             "https://www.kff.org/racial-equity-and-health-policy/"),
            ("Peterson-KFF Health System Tracker, emergency department cost analyses.",
             "https://www.healthsystemtracker.org/brief/emergency-department-visits-exceed-affordability-thresholds-for-many-consumers-with-private-insurance/"),
            ("Indian Health Service, <em>Purchased/Referred Care</em> program documentation.",
             "https://www.ihs.gov/prc/"),
            ("GAO-18-580, <em>Indian Health Service: Agency Faces Ongoing Challenges Filling Provider Vacancies</em>.",
             "https://www.gao.gov/products/gao-18-580"),
        ],
        disclaimer=(
            "Figures are drawn from published third-party research and are "
            "point-in-time. Verify current values before citing them externally, and "
            "treat any diversion estimate for your own program as a modelled range "
            "rather than a forecast."
        ),
    )


def post_uio() -> Page:
    body = """    <p>Roughly seven in ten American Indian and Alaska Native people live in urban
    areas. The health infrastructure serving them is a network of about forty Urban
    Indian Organizations, funded under Title V of the Indian Health Care Improvement
    Act, ranging from full-service clinics to referral and outreach programs.</p>

    <p>UIOs are part of the IHS system (the &ldquo;I&rdquo; in the I/T/U
    shorthand for IHS, Tribal, and Urban programs) and they are also, in several
    concrete ways, the part of it with the least margin.</p>

    <h2>The structural gap</h2>

    <p>The most consequential difference for after-hours planning is this: Urban Indian
    Organizations do not have Purchased/Referred Care.</p>

    <p>PRC operates through IHS-operated and tribally operated facilities and their
    defined delivery areas. A UIO patient who goes to an outside emergency department
    does not have a PRC allocation behind that visit. Depending on their coverage, the
    bill lands on Medicaid, on private insurance, or on the patient.</p>

    <div class="callout callout--amber">
      <div class="callout-head">What that changes about the business case</div>
      <p>For an IHS service unit or a 638 program, nurse triage has a budget argument:
      divert avoidable visits, protect the PRC allocation. For a UIO, that argument does
      not exist, so there is no allocation to protect. The case has to be made on
      access, continuity, and patient experience instead, which means it competes for a
      different pot of money and a different kind of justification.</p>
    </div>

    <h2>Why after-hours coverage is still hard to skip</h2>

    <p>A UIO's patient population is, by definition, living in a city with hospitals and
    urgent care. So why does a nurse line matter?</p>

    <ul>
      <li><strong>Continuity.</strong> An urban AI/AN patient who ends up in a general
      emergency department is outside the system that knows them. The UIO may not learn
      about the visit for weeks, if at all.</li>
      <li><strong>Cultural safety.</strong> Many patients choose a UIO precisely because
      it is a place where they do not have to explain themselves. After hours, that
      option disappears and the alternative is a system with no such orientation.</li>
      <li><strong>Coverage churn.</strong> UIO patient populations often have
      discontinuous Medicaid enrollment. An emergency department visit during a coverage
      gap becomes personal debt.</li>
      <li><strong>Small clinical staffs.</strong> Most UIOs are not large enough to put
      a clinician on call overnight without breaking the daytime schedule.</li>
    </ul>

    <h2>What funding it usually looks like</h2>

    <p>Without PRC, UIOs generally fund after-hours coverage from Title V grant funding,
    third-party revenue, or program-specific grants. That has two implications for how a
    service should be structured:</p>

    <ol>
      <li><strong>Pricing has to be predictable.</strong> A per-call model that spikes
      in flu season is hard to hold against a fixed grant. A flat monthly structure is
      easier to budget and easier to defend in a grant application.</li>
      <li><strong>Documentation has to support reporting.</strong> Grant-funded programs
      report on what they delivered. Encounter documentation that can feed those reports
      without manual reconstruction is worth more here than in a facility with a
      contracting office behind it.</li>
    </ol>

    <h2>The part that is worth saying plainly</h2>

    <p>Urban Indian Organizations serve the largest share of the AI/AN population and
    receive the smallest share of the attention, from federal funding
    conversations, from researchers, and from vendors. Nurse triage vendors marketing
    into Indian Country, to the extent any do, aim at IHS Area contracts because that is
    where the visible procurement is.</p>

    <p>The result is that a UIO evaluating after-hours coverage is usually starting from
    scratch, with no comparable to point to. If that is where you are, we are glad to be
    a useful conversation whether or not it ends in a contract.
    <a href="/contact">Reach us here.</a></p>"""

    return _post(
        slug="after-hours-coverage-urban-indian-organizations",
        title="After-Hours Coverage for Urban Indian Organizations",
        description=(
            "UIOs serve most of the AI/AN population but sit outside Purchased/Referred "
            "Care. What that changes about after-hours triage, and how it gets funded."
        ),
        eyebrow="Urban Indian health",
        h1="After-hours coverage <em>without a PRC backstop.</em>",
        deck=(
            "Urban Indian Organizations serve roughly seven in ten AI/AN people and have "
            "no Purchased/Referred Care allocation behind an outside emergency room "
            "visit. That changes the argument, not the need."
        ),
        body=body,
        reviewed=True,
        sources=[
            ("Indian Health Care Improvement Act, Title V, Urban Indian Health Program.",
             "https://www.ihs.gov/urban/"),
            ("Indian Health Service, Urban Indian Organizations directory.",
             "https://www.ihs.gov/urban/urban-indian-organizations/"),
            ("Indian Health Service, <em>Purchased/Referred Care</em> program documentation.",
             "https://www.ihs.gov/prc/"),
        ],
        disclaimer=(
            "The count of Urban Indian Organizations and the urban share of the AI/AN "
            "population are drawn from published IHS and census materials and change "
            "over time. Verify current figures before citing them."
        ),
    )


def posts() -> list[Page]:
    return [
        post_prc_budget(),
        post_what_is_prc(),
        post_isbee_vs_iee(),
        post_culturally_competent(),
        post_er_diversion(),
        post_uio(),
    ]


def resources_index() -> Page:
    page = Page(
        site=SITE,
        slug="resources/index",
        title="Resources: Tribal Health &amp; IHS Nurse Triage | TULQ",
        description=(
            "Plain-language explainers on Purchased/Referred Care, the Buy Indian Act, "
            "ER diversion in Indian Country, and culturally competent telephone triage."
        ),
        eyebrow="Resources",
        h1="Things worth <em>writing down.</em>",
        deck=(
            "Explainers on the parts of tribal health contracting and after-hours care "
            "that are badly documented elsewhere. Written from public sources, cited, "
            "and reviewed by our clinical director where the content is clinical."
        ),
        crumbs=[("Resources", "/resources/")],
        wide=True,
        priority="0.7",
        cta_title="Something we should write about?",
        cta_body=(
            "If there is a question your program keeps having to answer from scratch, "
            "tell us. The useful pieces here started as somebody's question."
        ),
    )

    page.body = f"""    <h2>Purchased/Referred Care</h2>

    {card_grid([
        ("PRC &amp; ER diversion", "How a nurse line protects your PRC budget",
         "PRC is appropriated annually and it runs out. What avoidable ER visits actually cost you, and how to size diversion honestly.",
         "/resources/nurse-advice-line-prc-budget"),
        ("PRC explained", "What is Purchased/Referred Care?",
         "Eligibility, payer of last resort, notification deadlines, and medical priority: the four conditions outsiders miss.",
         "/resources/what-is-purchased-referred-care"),
        ("Data &amp; access", "Reducing avoidable ER visits in Indian Country",
         "What the evidence supports, what vendor marketing overstates, and how to model it defensibly.",
         "/resources/reducing-avoidable-er-visits-indian-country"),
    ])}

    <h2>Federal contracting</h2>

    {card_grid([
        ("Set-asides", "ISBEE vs IEE: which applies?",
         "One test apart: whether you also meet the SBA size standard for the solicitation's NAICS code.",
         "/resources/isbee-vs-iee-set-asides"),
        ("Buy Indian Act", "The Buy Indian Act in plain language",
         "25 U.S.C. § 47, the 2022 IHS final rule, and how a requirement actually reaches the market.",
         "/buy-indian-act"),
        ("Procurement", "For contracting officers",
         "Capability summary, NAICS codes, and recent nurse advice line procurement by IHS Area.",
         "/for/contracting-officers"),
    ])}

    <h2>Clinical practice</h2>

    {card_grid([
        ("Clinical practice", "What culturally competent means on a triage call",
         "Household structure, understated pain, distance as a clinical variable, and how to evaluate a vendor's claim.",
         "/resources/culturally-competent-telephone-triage"),
        ("Urban Indian health", "After-hours coverage for UIOs",
         "Urban Indian Organizations serve most of the AI/AN population and have no PRC backstop. What that changes.",
         "/resources/after-hours-coverage-urban-indian-organizations"),
        ("Coverage", "Nurse advice line by IHS Area",
         "All twelve Areas, the states each covers, and where procurement has been active.",
         "/areas/"),
    ])}"""

    return page


# ══════════════════════════════════════════════════════════════════════
# Tribal-angle comparison
# ══════════════════════════════════════════════════════════════════════

def compare_tribal() -> Page:
    qa = [
        ("Are the national vendors bad at what they do?",
         "<p>No, and we would not suggest otherwise. IntellaTriage, Conduit Health "
         "Partners, and AccessNurse are established operators with real clinical "
         "infrastructure and long track records. The argument on this page is about "
         "fit for a specific buyer, not about competence.</p>"),
        ("What can TULQ not claim yet?",
         "<p>Operating history. TULQ is launching in 2026. We have no call volume "
         "statistics, no client references at scale, and no multi-year uptime record, "
         "and any comparison that pretended otherwise would be worthless to you. What "
         "we can be measured on today is corporate structure, clinical leadership "
         "credentials, licensure, protocol standard, and how the service is "
         "designed.</p>"),
        ("How should we actually run a comparison?",
         "<p>Ask every vendor the same questions and write the answers down: who "
         "answers the first call and what licensure do they hold; what protocol "
         "standard; how does escalation to our clinicians work; what does the "
         "documentation look like in our system; what is the pricing structure and "
         "does it move with volume; and, for a tribal buyer, what specifically about "
         "your service is built for this population. The last question is the one that "
         "separates the field.</p>"),
    ]

    body = """    <p>If you run a tribal health program and you are evaluating after-hours nurse
    coverage, you will find a short list of established national vendors and very
    little written about how any of them fit Indian Country. This page is our attempt
    at that comparison, written by an interested party, which you should weigh
    accordingly.</p>

    <h2>Who is actually in the market</h2>

    <p>The nurse triage category has a handful of serious operators, most of them
    fifteen to twenty-five years old:</p>

    <ul>
      <li><strong>IntellaTriage</strong>: the category leader, founded in 2008,
      built primarily around hospice and home health after-hours triage. Publishes
      substantial content on nurse-first triage, clinician burnout, and CAHPS.</li>
      <li><strong>Conduit Health Partners</strong>: nurse-first triage plus
      patient transfer, segmented by buyer: health systems, medical groups, health
      plans, and FQHCs. Publishes case studies with hard utilization numbers.</li>
      <li><strong>AccessNurse</strong>: in business since 1996, serving a large
      provider base with vertical landing pages by specialty, including community
      health centers.</li>
      <li><strong>TelemedRN</strong>: smaller, hospice and home-health focused,
      positioned on affordability.</li>
      <li><strong>Generic medical answering services</strong>: cheaper, and not
      clinical. A message taker is not a triage nurse, and the distinction matters more
      at 2 a.m. than it does on a price sheet.</li>
    </ul>

    <h2>The thing they have in common</h2>

    <p>Every one of them is built for mainstream healthcare. Read their sites: the
    buyers are hospices, home health agencies, physician groups, health systems, and
    health plans. The value propositions are clinician burnout, EMR documentation,
    CAHPS scores, and readmission penalties.</p>

    <p>None of them publishes content for tribal health programs, IHS beneficiaries,
    Purchased/Referred Care, Buy Indian Act contracting, or sovereignty-respecting
    care. Not because they are hostile to it, because it is not their
    market.</p>

    <div class="callout">
      <div class="callout-head">What that means in practice</div>
      <p>A vendor whose entire operating model is tuned to hospice after-hours volume
      can absolutely answer a phone for a tribal clinic. What they will not have is a
      protocol adaptation built around multigenerational households, a disposition
      logic that treats a two-hour drive as a clinical variable, or any structural
      standing under the Buy Indian Act.</p>
    </div>

    <h2>An honest comparison table</h2>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr>
            <th>&nbsp;</th>
            <th>Established national vendors</th>
            <th>TULQ</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Operating history</td>
            <td class="tick">15&ndash;25+ years, large call volumes, references at scale</td>
            <td class="cross">Launching 2026: no operating history</td>
          </tr>
          <tr>
            <td>Licensed RNs on first call</td>
            <td class="tick">Yes (the serious ones)</td>
            <td class="tick">Yes</td>
          </tr>
          <tr>
            <td>Schmitt-Thompson or equivalent protocols</td>
            <td class="tick">Yes</td>
            <td class="tick">Yes</td>
          </tr>
          <tr>
            <td>Published tribal / IHS content</td>
            <td class="cross">None found</td>
            <td class="tick">Yes</td>
          </tr>
          <tr>
            <td>Buy Indian Act standing (25 U.S.C. &sect; 47)</td>
            <td class="cross">Generally not eligible</td>
            <td class="tick">Indian Economic Enterprise</td>
          </tr>
          <tr>
            <td>PRC-aware value framing</td>
            <td class="cross">Built for commercial and Medicare economics</td>
            <td class="tick">Built around the PRC allocation</td>
          </tr>
          <tr>
            <td>Cultural adaptation at protocol level</td>
            <td class="cross">Not marketed</td>
            <td class="tick">Core design premise</td>
          </tr>
          <tr>
            <td>Scale for a very large multi-site contract</td>
            <td class="tick">Yes</td>
            <td class="cross">Not yet: teaming would be the honest answer</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>When you should pick one of them instead</h2>

    <p>We would rather say this than have you find out later. Choose an established
    national vendor if:</p>

    <ul>
      <li>You need a multi-year track record and client references at scale to satisfy
      an evaluation factor, and you need them now.</li>
      <li>Your requirement spans many sites at high volume and a proven capacity
      story is the deciding factor.</li>
      <li>Your program's after-hours need is essentially the mainstream one and the
      tribal-specific considerations on this page do not describe your population.</li>
    </ul>

    <p>Choose TULQ if the Buy Indian Act applies to your acquisition, if your service
    population is one where the four cultural-competency gaps
    <a href="/resources/culturally-competent-telephone-triage">described here</a> are
    real, or if you want a vendor whose economics are framed around your PRC allocation
    rather than a commercial utilization curve.</p>

    <h2>The FONEMED observation</h2>

    <p>It is worth noting what has actually been happening in IHS nurse advice line
    procurement. Several recent requirements were set aside under the Buy Indian Act,
    and awards have gone to firms that are not Indian Economic Enterprises, FONEMED LLC, a US/Canadian firm founded in 1996, among them.</p>

    <p>That is not a scandal and it is not anyone's fault. It is the documented,
    correct outcome when market research does not surface a capable Indian enterprise
    at a fair and reasonable price. It is also, precisely, the gap TULQ exists to
    close. <a href="/for/contracting-officers">The procurement record is summarized
    here.</a></p>"""

    page = Page(
        site=SITE,
        slug="compare/nurse-triage-for-tribal-health",
        title="Best Nurse Triage Company for Tribal Health | TULQ",
        description=(
            "Comparing nurse triage vendors for tribal health: what the national operators "
            "do well, where they don't fit Indian Country, and when to pick them."
        ),
        eyebrow="Comparison",
        h1="Choosing a nurse triage vendor <em>for tribal health.</em>",
        deck=(
            "A comparison written by an interested party, which you should weigh "
            "accordingly, including the part where we tell you when to pick "
            "somebody else."
        ),
        crumbs=[("Comparison", "/compare/nurse-triage-for-tribal-health")],
        priority="0.7",
        cta_title="Run the same questions past us.",
        cta_body=(
            "Ask us the six evaluation questions below and compare our answers against "
            "everyone else's. That is a more useful exercise than taking this page at "
            "face value."
        ),
    )
    page.body = f"""{body}

    {faq_block(qa)}

    {sources_block([
        "Competitor descriptions summarized from each company's own public website.",
        ("SAM.gov contract opportunities, Indian Health Service notices and awards.",
             "https://sam.gov/search/?index=opp"),
        ("Buy Indian Act, 25 U.S.C. &sect; 47, and the IHS Buy Indian Act final rule (2022).",
             "https://www.federalregister.gov/documents/2022/01/13/2021-28156/acquisition-regulations-buy-indian-act-procedures-for-contracting"),
    ], disclaimer=(
        "Competitor information is summarized from publicly available company "
        "materials and was accurate as reviewed; services and positioning change. "
        "This page is written by TULQ and is not independent analysis. Verify any "
        "claim that matters to your decision directly with the vendor."
    ))}"""
    page.schema = [faq_node(page, qa)]
    return page
