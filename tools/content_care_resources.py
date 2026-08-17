#!/usr/bin/env python3
"""
The /resources and /compare tracks on tulqhealth.com.

The comparison pages describe competitors from their own public materials,
stick to structural facts, say plainly that TULQ is pre-launch, and tell
the reader when to choose the other vendor. That is both the honest way to
write them and the only version that survives a reader who checks.
"""

from __future__ import annotations

from pagekit import (
    CARE, Page, article_node, card_grid, faq_block, faq_node, sources_block,
)

SITE = CARE


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

def post_true_cost() -> Page:
    qa = [
        ("What does an ED visit actually cost?",
         "<p>The Peterson-KFF Health System Tracker puts the average emergency "
         "department visit at roughly $2,453, of which about $1,134 is the "
         "evaluation-and-management portion. That is notably higher than the "
         "$1,200&ndash;$1,400 range that circulates in vendor marketing, and it is the "
         "figure we would use because it is the better-sourced one.</p>"),
        ("Is per-call or flat monthly pricing better?",
         "<p>It depends on who should carry volume risk. Per-call looks cheaper in a "
         "quiet month and produces budget variances in a bad flu season. Flat monthly "
         "costs the vendor predictability and gives you a number you can put in a "
         "budget. For grant-funded and fixed-budget organizations, flat is usually "
         "worth more than the theoretical saving.</p>"),
        ("How do we measure whether it worked?",
         "<p>Pick your baselines before you start: after-hours call volume, how many "
         "reached a clinician, ED utilization among your census, and clinician turnover "
         "with a note on how many exit interviews mention call. Measure the same things "
         "at six and twelve months. Vendors will offer their own dashboards; your own "
         "numbers are the ones that will convince your board.</p>"),
    ]

    body = """    <p>Ask an agency what after-hours on-call costs and you will usually get the
    on-call differential. That number is real, and it is a fraction of the total. The
    rest is distributed across line items that live in different budgets and never get
    added up in the same place.</p>

    <h2>The four buckets</h2>

    <h3>1. Direct pay</h3>

    <p>On-call differentials, stipends, per-call rates, and any premium for holiday or
    weekend coverage. This is the number everyone quotes, and it is the easiest to
    pull.</p>

    <h3>2. Overtime and visit conversion</h3>

    <p>A share of after-hours calls become visits. Those are paid at overtime or
    premium rates, plus mileage, and they consume a clinician who then has a scheduled
    day in front of them.</p>

    <h3>3. Next-day productivity</h3>

    <p>The one nobody puts a number on. A clinician who took calls at one and three is
    not delivering a full schedule the following day, and the visits still have to
    happen, which means either they slip, or someone else absorbs them, or the
    clinician works longer to catch up. All three have a cost.</p>

    <h3>4. Turnover</h3>

    <p>The expensive one, by a wide margin. Replacing an experienced hospice or home
    health clinician costs a substantial multiple of the annual on-call differential
    you were paying them, once recruiting, onboarding, orientation, and reduced
    productivity during ramp-up are counted. Call burden is a well-documented
    contributor to clinical turnover in these settings.</p>

    <div class="callout callout--amber">
      <div class="callout-head">The arithmetic that changes the conversation</div>
      <p>If outsourcing after-hours triage retains <em>one</em> experienced clinician
      per year who would otherwise have left over call burden, the retention saving
      alone will typically exceed the annual cost of the service. That is the argument
      worth making to a board, not a diversion percentage.</p>
    </div>

    <h2>A worked example</h2>

    <p>Use your own numbers; this is a shape, not a benchmark. Consider a mid-sized
    agency running a rotation across eight clinicians:</p>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr><th>Line item</th><th>How to calculate it</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>On-call differential</td>
            <td>Nights covered per year &times; differential per night &times; number
            of clinicians on rotation</td>
          </tr>
          <tr>
            <td>Overtime on converted visits</td>
            <td>After-hours visits per year &times; average overtime hours per visit
            &times; loaded hourly rate</td>
          </tr>
          <tr>
            <td>Next-day productivity</td>
            <td>Disrupted nights per year &times; estimated lost visit capacity &times;
            revenue or cost per visit</td>
          </tr>
          <tr>
            <td>Turnover attributable to call</td>
            <td>Annual clinical departures &times; share citing call burden &times;
            full replacement cost</td>
          </tr>
          <tr>
            <td>Avoided ED visits</td>
            <td>Diverted visits &times; $2,453 average. Count this only if you
            carry the financial risk for it</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>That last row deserves care. If you are a hospice under a per-diem benefit, an
    avoided hospitalization has direct financial consequence for you. If you are a
    fee-for-service home health agency, the ED cost may fall on the payer rather than
    on you, and counting it as your saving will not survive scrutiny. Know which one
    you are before you put it in a model.</p>

    <h2>What the vendor's number is worth</h2>

    <p>Every vendor in this category, ourselves included, has an incentive to hand you
    a favourable calculation. Treat all of them as a starting structure rather than a
    result. The inputs that matter (your call volume, your turnover, your
    differential, your payment model) are yours, and substituting a vendor's
    assumptions for them produces a number you cannot defend in a budget meeting.</p>

    <p>The single most useful thing you can do before evaluating any vendor is spend
    an afternoon totalling the four buckets above from your own payroll and HR data. It
    is usually the first time anyone at the organization has seen the number in one
    place, and it tends to end the debate about whether the problem is worth
    solving.</p>"""

    return _post(
        slug="true-cost-of-after-hours-on-call",
        title="The True Cost of After-Hours On-Call Nursing",
        description=(
            "On-call differentials are a fraction of the total. The four buckets behind the "
            "real cost of after-hours coverage, and how to run the numbers yourself."
        ),
        eyebrow="Cost &amp; ROI",
        h1="What on-call <em>actually costs you.</em>",
        deck=(
            "Direct pay is the number everyone quotes and the smallest of the four. "
            "Here is the whole calculation, including the one line item that usually "
            "decides the answer."
        ),
        body=body,
        qa=qa,
        sources=[
            ("Peterson-KFF Health System Tracker, average emergency department visit cost.",
             "https://www.healthsystemtracker.org/brief/emergency-department-visits-exceed-affordability-thresholds-for-many-consumers-with-private-insurance/"),
            "Published research on clinical turnover and replacement cost in home health and hospice.",
            ("CMS Home Health Prospective Payment System, payment methodology.",
             "https://www.cms.gov/medicare/payment/prospective-payment-systems/home-health"),
        ],
        disclaimer=(
            "Cost figures are illustrative structure, not benchmarks. The ED cost "
            "figure is point-in-time from a third-party tracker; verify the "
            "current value before citing it externally. Run the calculation on your own "
            "payroll, HR, and utilization data."
        ),
        cta_title="Want help running it?",
        cta_body=(
            "We will walk through the four buckets with your finance staff using your "
            "numbers, without a proposal attached."
        ),
    )


def post_triage_vs_answering() -> Page:
    body = """    <p>The two services occupy the same slot in an operations diagram and do
    fundamentally different work. The confusion is understandable and it is expensive,
    because organizations buy the cheaper one, discover it did not solve the problem,
    and conclude that outsourcing after-hours does not work.</p>

    <h2>What an answering service does</h2>

    <p>A medical answering service employs trained, non-clinical operators. They answer
    the phone politely, take an accurate message, follow your routing rules, and reach
    your on-call clinician according to your escalation instructions.</p>

    <p>They are good at this. What they cannot do (legally and by training) is assess a symptom or make a care decision. So the operator's decision tree
    has two branches: is this obviously routine, or should I reach someone? Anything
    ambiguous goes to your clinician, because that is the safe choice when you are not
    qualified to judge.</p>

    <h2>What nurse triage does</h2>

    <p>A licensed registered nurse answers, works the caller through a physician-authored
    protocol, and reaches a documented disposition: home care with instructions, be seen
    in the clinic tomorrow, urgent care, or emergency department now.</p>

    <p>The nurse resolves the calls a nurse can resolve. Your clinician hears about the
    ones that need them, with the assessment already done.</p>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr><th>&nbsp;</th><th>Answering service</th><th>Nurse triage</th></tr>
        </thead>
        <tbody>
          <tr><td>Who picks up</td><td>Non-clinical operator</td><td class="tick">Licensed RN</td></tr>
          <tr><td>Symptom assessment</td><td class="cross">No</td><td class="tick">Yes, against protocol</td></tr>
          <tr><td>Care disposition</td><td class="cross">No</td><td class="tick">Yes</td></tr>
          <tr><td>Clinical documentation</td><td>Message log</td><td class="tick">Assessed encounter</td></tr>
          <tr><td>Calls reaching your clinician</td><td>Most</td><td class="tick">Only those protocol escalates</td></tr>
          <tr><td>Handles a genuine emergency</td><td>Routes it</td><td class="tick">Recognizes and directs it</td></tr>
          <tr><td>Relative cost</td><td>Lower</td><td>Higher</td></tr>
        </tbody>
      </table>
    </div>

    <h2>The number that decides it</h2>

    <p>Ask any vendor one question: <strong>what percentage of after-hours calls reach
    our clinician?</strong></p>

    <p>With an answering service the honest answer is most of them, because the operator
    cannot safely filter on clinical grounds. With nurse triage it should be a minority,
    because the nurse resolves what a nurse can resolve.</p>

    <p>That single figure is the whole value proposition. If a triage vendor cannot
    articulate it, or answers with a range so wide it is meaningless, you are being sold
    an answering service with better marketing.</p>

    <div class="callout">
      <div class="callout-head">Where an answering service is the right call</div>
      <p>If your after-hours volume is genuinely low, your calls are overwhelmingly
      administrative, and your clinicians are not experiencing call burden, an answering
      service may be exactly right and considerably cheaper. Not every organization has
      a clinical after-hours problem. Buy the thing that matches the problem you
      have.</p>
    </div>

    <h2>The hybrid that usually isn't one</h2>

    <p>Some vendors market a middle option: non-clinical first pick-up with a nurse
    available for escalation. Look closely at what triggers the escalation. If it is the
    operator's judgment about whether a call sounds clinical, you have an answering
    service with a nurse on standby, and the filtering decision, the one that
    determines whether your clinician's phone rings, is still being made by someone not
    qualified to make it.</p>

    <h2>Questions worth asking either way</h2>

    <ul>
      <li>Who answers the first call, and what licensure do they hold?</li>
      <li>What protocol standard do the nurses work from?</li>
      <li>What share of calls resolve without reaching our clinician?</li>
      <li>What does the documentation look like when it reaches us, and in what
      format?</li>
      <li>How does escalation work, and who defines the rules, you or us?</li>
      <li>Is pricing per-call or flat, and what happens in a bad respiratory
      season?</li>
    </ul>"""

    return _post(
        slug="nurse-triage-vs-answering-service",
        title="Nurse Triage vs Answering Service: The Difference",
        description=(
            "An answering service takes a message; nurse triage makes a clinical "
            "decision. The one question that tells you which you are actually being "
            "sold."
        ),
        eyebrow="Basics",
        h1="Nurse triage vs <em>answering service.</em>",
        deck=(
            "They occupy the same slot in an operations diagram and do different work. "
            "Here is the distinction, and the single question that exposes which one a "
            "vendor is really selling."
        ),
        body=body,
        reviewed=True,
        sources=[
            ("American Academy of Ambulatory Care Nursing, <em>Scope and Standards of Practice for Professional Telehealth Nursing</em>.",
             "https://www.aaacn.org/telehealth-nursing-practice"),
            ("Schmitt-Thompson telephone triage protocols.",
             "https://www.stcc-triage.com/"),
            ("NCSBN, state nurse practice acts governing nursing assessment and telephone triage.",
             "https://www.ncsbn.org/npa.htm"),
        ],
        disclaimer=(
            "Scope of practice for telephone triage is governed by state nurse practice "
            "acts and varies. Verify requirements for the states where your patients "
            "are located."
        ),
    )


def post_cahps() -> Page:
    body = """    <p>The CAHPS Hospice Survey is publicly reported and feeds the star ratings
    families see on Care Compare. Of the measures it captures, several are decided
    almost entirely by what happens when your office is closed.</p>

    <h2>Which measures after-hours access touches</h2>

    <p>The survey asks caregivers about their experience across several composites.
    Three of them are directly sensitive to after-hours responsiveness:</p>

    <ul>
      <li><strong>Getting timely help.</strong> Whether the family got help as soon as
      they needed it, including on evenings, weekends, and holidays. This is the most
      directly after-hours-dependent item on the survey.</li>
      <li><strong>Communication with the family.</strong> Whether the team kept the
      family informed and explained things understandably. A 2 a.m. call that reaches a
      voicemail box is a communication failure whether or not anyone calls back at
      seven.</li>
      <li><strong>Getting emotional and religious support / training the family.</strong>
      A caregiver managing a symptom crisis alone at night, without anyone to walk them
      through it, is the experience these items are trying to detect.</li>
    </ul>

    <h2>Which it does not</h2>

    <p>Being straight about the limits: after-hours coverage will not move the items
    about hospice team communication with the <em>patient</em> during scheduled visits,
    about help with pain and symptoms as assessed over the whole episode, or about
    whether the family would recommend the hospice for reasons unrelated to access. A
    nurse line does not fix a hospice with a staffing or quality problem during the
    day.</p>

    <div class="callout">
      <div class="callout-head">Why the timing matters more than the mechanism</div>
      <p>Survey respondents are family caregivers recalling an emotionally intense
      period. Their memory of &ldquo;did you get help when you needed it&rdquo; is
      formed disproportionately by the worst night, not by the average of all
      interactions. That asymmetry is why after-hours access has outsized influence on
      a score built from many more daytime touchpoints.</p>
    </div>

    <h2>What actually changes the answer</h2>

    <p>Three things, in order of effect:</p>

    <ol>
      <li><strong>Someone competent picks up immediately.</strong> Not a voicemail, not
      a queue, not a callback promise. The difference between a family reaching a nurse
      in twenty seconds and waiting eleven minutes for a callback is the difference
      between two different survey answers.</li>
      <li><strong>The person who picks up can help.</strong> An operator taking a
      message is a delay with a friendly voice attached. A nurse who can talk a
      caregiver through a symptom is help.</li>
      <li><strong>The escalation is real.</strong> When the call needs the agency's own
      clinician, it has to reach them, quickly, with the assessment done.</li>
    </ol>

    <h2>Measuring it without fooling yourself</h2>

    <p>CAHPS results lag, arrive quarterly, and are noisy at small volumes. If you are
    trying to establish whether an after-hours change moved anything, do not wait for
    the public report to tell you. Track the operational proxies:</p>

    <ul>
      <li>Time to reach a clinical person on after-hours calls</li>
      <li>Share of after-hours calls resolved without escalation</li>
      <li>Share escalated that reached your clinician within your target</li>
      <li>After-hours-originated ED transfers and hospital admissions</li>
      <li>Complaints and grievances originating from after-hours contacts</li>
    </ul>

    <p>Those move within weeks, and if they do not move, the survey result will not
    either.</p>

    <h2>A note on HOPE</h2>

    <p>The Hospice Outcomes &amp; Patient Evaluation instrument replaced the Hospice
    Item Set effective October 1, 2025, changing what is collected and at what points in
    the episode. It is a separate instrument from CAHPS (HOPE is completed by the
    hospice, CAHPS is completed by the family) but both sit inside the Hospice
    Quality Reporting Program, and both are worth understanding before assuming an
    operational change will show up somewhere specific.</p>"""

    return _post(
        slug="hospice-cahps-after-hours",
        title="How After-Hours Access Affects Hospice CAHPS Scores",
        description=(
            "Which CAHPS Hospice measures after-hours coverage actually moves, which it "
            "doesn't, and the operational proxies to track while you wait for the "
            "public report."
        ),
        eyebrow="CAHPS",
        h1="After-hours access and <em>your CAHPS scores.</em>",
        deck=(
            "Several CAHPS Hospice measures are decided by what happens at 2 a.m. Here "
            "is which ones, which ones aren't, and how to tell whether a change worked "
            "before the quarterly report arrives."
        ),
        body=body,
        reviewed=True,
        sources=[
            ("CMS, CAHPS Hospice Survey materials and quality measures.",
             "https://www.cms.gov/medicare/quality/hospice/cahpsr-hospice-survey"),
            ("CMS, Hospice Quality Reporting Program current measures.",
             "https://www.cms.gov/medicare/quality/hospice/current-measures"),
            ("CMS, Hospice Outcomes &amp; Patient Evaluation (HOPE) instrument guidance.",
             "https://www.cms.gov/medicare/quality/hospice/hope"),
            ("Medicare Care Compare, hospice ratings.",
             "https://www.medicare.gov/care-compare/"),
        ],
        disclaimer=(
            "Measure specifications, star rating methodology, and instrument effective "
            "dates change. Verify against current CMS guidance before relying on any of "
            "this operationally."
        ),
    )


def post_hhvbp() -> Page:
    body = """    <p>The expanded Home Health Value-Based Purchasing model adjusts Medicare
    payment for home health agencies against a set of quality measures. Acute-care
    utilization is one of the levers inside it, which is why after-hours coverage keeps
    coming up in HHVBP conversations.</p>

    <p>The connection is real. It is also frequently overstated by vendors, so it is
    worth separating what the model measures from what a phone line can influence.</p>

    <h2>What changed for CY2025</h2>

    <p>CMS moved the applicable acute-care utilization measure to a within-stay
    Potentially Preventable Hospitalization measure beginning with CY2025. The
    distinction matters: a within-stay measure looks at hospitalizations occurring
    during the home health episode, and &ldquo;potentially preventable&rdquo; narrows it
    to admissions for conditions considered manageable in an ambulatory or home
    setting.</p>

    <p>That narrowing is good news for the after-hours argument, because the
    hospitalizations the measure targets are disproportionately the ones that begin as
    an unmanaged symptom at an inconvenient hour.</p>

    <h2>The pathway a nurse line interrupts</h2>

    <p>A typical preventable admission from home health does not start at the hospital.
    It starts like this:</p>

    <ol>
      <li>A symptom changes in the evening: breathing, a wound, confusion, pain,
      a blood sugar.</li>
      <li>The patient or caregiver is uncertain and has no clinical person to ask.</li>
      <li>They wait, because calling feels like an overreaction.</li>
      <li>By early morning it is worse, and now the only available answer is the
      emergency department.</li>
      <li>The ED, seeing a deteriorated presentation with no interim clinical record,
      admits.</li>
    </ol>

    <p>Nurse triage intervenes at step two. Sometimes the answer is reassurance and a
    next-day visit. Sometimes it is an instruction that manages the symptom overnight.
    Sometimes it is an escalation to the agency's on-call clinician for a visit that
    prevents the deterioration entirely. All three change what happens at step five.</p>

    <div class="callout callout--teal">
      <div class="callout-head">The honest limit</div>
      <p>A phone line cannot prevent an admission that was going to happen regardless,
      and a meaningful share of them were. It also cannot fix an agency whose visit
      frequency or clinical management is the underlying problem. Triage addresses the
      subset of preventable admissions where the failure was access to a clinical
      opinion at the wrong hour. That subset is worth attacking; it is not the whole
      measure.</p>
    </div>

    <h2>How to model it before you buy</h2>

    <p>You have the data to do this properly, which puts you ahead of most vendor
    pitches:</p>

    <ul>
      <li>Pull your within-stay hospitalizations for the last twelve months.</li>
      <li>Flag which ones were preceded by an after-hours contact, or by no contact at
      all in the preceding 24 hours.</li>
      <li>Look at the admitting diagnoses against the potentially-preventable
      categories.</li>
      <li>Ask your clinical leadership, case by case for a sample: could a nurse
      reachable at 11 p.m. plausibly have changed this?</li>
    </ul>

    <p>That review takes a clinical manager a day or two and produces a defensible
    internal estimate. It will almost certainly be lower than a vendor's number and far
    more useful, because you can put it in front of your own board.</p>

    <h2>Where the payment adjustment actually lands</h2>

    <p>HHVBP adjusts payment based on performance relative to peers, on both achievement
    and improvement. Two implications worth holding onto:</p>

    <ul>
      <li><strong>You are graded on a curve.</strong> Improving matters even if your
      absolute rate is not best-in-class, and standing still while peers improve costs
      you.</li>
      <li><strong>The lag is long.</strong> Performance in one period adjusts payment in
      a later one. An operational change made today shows up in payment considerably
      later, which is an argument for tracking operational proxies rather than waiting
      for the adjustment to tell you whether it worked.</li>
    </ul>"""

    return _post(
        slug="hhvbp-ed-use",
        title="HHVBP and ED Use: How After-Hours Triage Moves It",
        description=(
            "CMS moved to a within-stay Potentially Preventable Hospitalization measure for "
            "CY2025. Where nurse triage interrupts that pathway, and how to model it."
        ),
        eyebrow="HHVBP",
        h1="HHVBP, ED use, and <em>the 11 p.m. call.</em>",
        deck=(
            "The CY2025 shift to a within-stay potentially preventable hospitalization "
            "measure sharpened the target. Here is the pathway a nurse line actually "
            "interrupts, and where it doesn't."
        ),
        body=body,
        reviewed=True,
        sources=[
            ("CMS, expanded Home Health Value-Based Purchasing model.",
             "https://www.cms.gov/priorities/innovation/innovation-models/expanded-home-health-value-based-purchasing-model"),
            ("CMS, Home Health Quality Reporting Program measure specifications.",
             "https://www.cms.gov/medicare/quality/home-health"),
            ("CMS Home Health Prospective Payment System final rules.",
             "https://www.cms.gov/medicare/payment/prospective-payment-systems/home-health"),
        ],
        disclaimer=(
            "Measure specifications, performance years, and payment adjustment "
            "methodology change annually. Verify against current CMS guidance before "
            "modelling financial impact."
        ),
    )


def post_apcm() -> Page:
    body = """    <p>Advanced Primary Care Management is the most consequential recent change to
    how primary care gets paid for care-management work, and it is directly relevant to
    any health center thinking about after-hours access, because 24/7 access is
    one of the service elements bundled into it.</p>

    <h2>What APCM is</h2>

    <p>CMS launched APCM on January 1, 2025 under the CY2025 Physician Fee Schedule. It
    replaces a stack of time-based care-management billing with a monthly per-patient
    payment, stratified into three tiers by patient complexity:</p>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr><th>Code</th><th>Tier</th><th>2025 national allowable (approx.)</th></tr>
        </thead>
        <tbody>
          <tr><td>G0556</td><td>Level 1: lower complexity</td><td>$15.20</td></tr>
          <tr><td>G0557</td><td>Level 2: two or more chronic conditions</td><td>$48.84</td></tr>
          <tr><td>G0558</td><td>Level 3: qualified Medicare beneficiary, higher complexity</td><td>$107.07</td></tr>
        </tbody>
      </table>
    </div>

    <p>NACHC's APCM guidance has listed distinct FQHC Medicare rates for the lower two
    tiers (roughly $16.37 for G0556 and $53.77 for G0557) and rates were
    adjusted upward across all three codes for 2026.</p>

    <div class="callout callout--amber">
      <div class="callout-head">Check these before you model on them</div>
      <p>Every figure above is a published rate for a specific program year and is
      subject to annual adjustment, geographic adjustment, and your MAC's guidance.
      Treat them as an order of magnitude for planning and confirm current values
      against the fee schedule before they reach a budget.</p>
    </div>

    <h2>Why it removed the time thresholds</h2>

    <p>The most significant structural change is not the money. Previous chronic care
    management billing required documented time thresholds per month, which meant staff
    tracking minutes and a lot of qualifying work going unbilled because nobody logged
    it.</p>

    <p>APCM pays for maintaining a defined set of care-management capabilities rather
    than for accumulated minutes. That shifts the compliance burden from time-tracking
    to demonstrating you actually provide the service elements.</p>

    <h2>Where after-hours access fits</h2>

    <p>Among those service elements is an expectation of 24/7 access to care and
    continuity with the care team, patients able to reach someone who can
    address urgent needs, at any hour.</p>

    <p>For a health center, there are three ways to satisfy that: put your own
    clinicians on call, extend hours, or arrange professional coverage. The first burns
    the staff you struggle to keep. The second requires hiring. The third is a service
    contract.</p>

    <p>Nurse triage is not the whole of an APCM program; there is care planning,
    care coordination, population health management, and performance measurement
    alongside it. But it is a concrete way to hold up the access element without adding
    a shift.</p>

    <h2>Who can bill it</h2>

    <p>FQHCs, RHCs, and critical access hospitals billing through an outpatient
    primary-care billing practitioner can all participate, alongside standard fee
    schedule billers. The mechanics differ by facility type, which is exactly where
    your MAC's guidance matters more than any general article.</p>

    <h2>The realistic view</h2>

    <p>APCM is not a windfall. At the lower tier the monthly amount is modest, and the
    administrative work of establishing and documenting the required elements is real.
    Where it becomes meaningful is at scale across an eligible panel, and where the
    capabilities you have to build are ones you wanted anyway.</p>

    <p>After-hours access is a good example of that overlap. If you were going to
    address it regardless (for patient safety, for ED diversion, for your own
    clinicians' sanity) then APCM changes the financial framing from pure cost
    to a supported capability. That is a different conversation to have with a
    board.</p>"""

    return _post(
        slug="apcm-billing-fqhc-rhc",
        title="APCM Billing at an FQHC or RHC: G0556-G0558",
        description=(
            "Advanced Primary Care Management explained for health centers: the three "
            "codes, why the time thresholds went away, and where 24/7 access coverage "
            "fits."
        ),
        eyebrow="Reimbursement",
        h1="APCM at a health center: <em>G0556 to G0558.</em>",
        deck=(
            "CMS launched Advanced Primary Care Management in January 2025, replacing "
            "time-threshold care management with a monthly per-patient payment. One of "
            "its required elements is 24/7 access."
        ),
        body=body,
        sources=[
            ("CMS Physician Fee Schedule, Advanced Primary Care Management (CY2025).",
             "https://www.cms.gov/medicare/payment/fee-schedules/physician"),
            ("National Association of Community Health Centers, APCM reimbursement tip sheet.",
             "https://www.nachc.org/wp-content/uploads/2025/03/APCM-Reimbursement-Tip-Sheet.pdf"),
            ("American Academy of Family Physicians, Advanced Primary Care Management coding.",
             "https://www.aafp.org/family-physician/practice-and-career/getting-paid/coding/advanced-primary-care-management.html"),
            ("HRSA Health Center Program Compliance Manual, Chapter 7: coverage for medical emergencies during and after hours.",
             "https://bphc.hrsa.gov/compliance/compliance-manual/chapter7"),
        ],
        disclaimer=(
            "Payment rates are published figures for the program year noted and are "
            "subject to annual, geographic, and MAC-specific adjustment. This is not "
            "billing or compliance advice. Confirm current rates and "
            "documentation requirements with your MAC before billing."
        ),
    )


def post_g0511_sunset() -> Page:
    """The G0511 sunset.

    The Aug 2026 research names this the highest-value authority topic TULQ
    has: it is fresh, genuinely confusing, under-covered by incumbents, and
    it lands squarely on the rural and health-center buyer. It is written
    from the January 2026 CMS RHC and FQHC booklets rather than from a
    vendor summary of them.

    It stays scoped to the *transition*: what replaced the bundle, what the
    coinsurance and cost-report treatment now are, and what the supervision
    rules allow. /resources/apcm-billing-fqhc-rhc owns the APCM code detail
    and this links across to it rather than restating it.
    """
    body = """    <p>For years a rural health clinic or federally qualified health center that
    did care-management work reported one bundled code, G0511, and received one
    bundled payment for it. That code was discontinued, and beginning in 2026 those
    organizations bill the individual care management codes at national non-facility
    Physician Fee Schedule rates, the same way a fee-for-service practice does.</p>

    <p>This is not a paperwork change. It changes what you report, how much you are
    paid, what the patient owes, where the cost lands on your cost report, and how much
    documentation you have to hold. It arrived at the same time as Advanced Primary Care
    Management, which is why so many health centers are working out two things at
    once.</p>

    <h2>What actually replaced the bundle</h2>

    <p>The single code became a table. CMS now lists these as the care coordination
    services an RHC or FQHC may bill, each with its own code set and its own
    documentation:</p>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr><th>Service</th><th>Base codes</th><th>Add-on codes</th></tr>
        </thead>
        <tbody>
          <tr><td>Chronic care management (CCM)</td><td>99487, 99490, 99491</td><td>99437, 99439, 99489</td></tr>
          <tr><td>Transitional care management (TCM)</td><td>99495, 99496</td><td>None</td></tr>
          <tr><td>Principal care management (PCM)</td><td>99424, 99426</td><td>99425, 99427</td></tr>
          <tr><td>Advanced primary care management (APCM)</td><td>G0556, G0557, G0558</td><td>G0568, G0569, G0570</td></tr>
          <tr><td>Chronic pain management (CPM)</td><td>G3002</td><td>G3003</td></tr>
          <tr><td>General behavioral health integration</td><td>99484, G0323</td><td>None</td></tr>
          <tr><td>Psychiatric collaborative care (CoCM)</td><td>99492, 99493, G2214</td><td>99494</td></tr>
        </tbody>
      </table>
    </div>

    <p>Remote physiologic and therapeutic monitoring, community health integration, and
    principal illness navigation sit in the same list. The practical consequence is that
    one line on a claim became a decision about which service a given patient is
    actually receiving this month, and that decision now has to be defensible.</p>

    <h2>Four things that changed with it</h2>

    <p><strong>You are paid the fee schedule rate, not a bundled one.</strong> CMS pays
    care coordination services and their add-on codes at the national, non-facility
    Physician Fee Schedule rate. For a health center that had grown used to one amount
    regardless of intensity, this cuts both ways: a complex patient managed properly is
    now worth materially more than the old bundle, and a thin month is worth less.</p>

    <p><strong>The patient owes coinsurance, calculated a specific way.</strong> The 20
    percent coinsurance is based on the lesser of the submitted charges or the
    individual code's national non-facility rate. That is a detail worth getting right
    before enrollment calls start, because a patient who is surprised by a statement
    disenrolls, and a disenrolled patient is a program that quietly stops.</p>

    <p><strong>The cost moves on your cost report.</strong> Care coordination costs are
    reported in the non-reimbursable section, and CMS does not consider them under the
    RHC all-inclusive rate or the FQHC prospective payment system. Administrative
    activities such as transcription and translation do not belong in there.</p>

    <p><strong>Nobody else can be billing the same period.</strong> An RHC or FQHC
    cannot bill care coordination services if another practitioner or facility bills
    them for that patient during the same period. Verification stops being a courtesy
    and becomes a monthly operational step.</p>

    <h2>The rule that makes outsourcing viable</h2>

    <p>Two lines in the 2026 booklets matter more than any of the payment detail, and
    they are easy to miss:</p>

    <p>CMS does not require face-to-face services to bill RHC or FQHC care coordination,
    and <strong>auxiliary personnel may provide them under general supervision.</strong>
    General supervision, not direct. The billing practitioner directs the service and
    remains responsible for it, but does not have to be physically present in the suite
    while the work happens.</p>

    <p>That is the legal basis on which a remote nurse can do this work at all. It is
    also the sharpest contrast with the annual wellness visit, which requires
    <em>direct</em> supervision, meaning the physician is immediately available throughout,
    whether in the office suite or virtually present on real-time audio and video. Care
    management and the wellness visit are frequently sold together and they do not sit
    under the same supervision rule. Anyone who tells you otherwise has not read both.</p>

    <h2>What to do about it</h2>

    <p>The honest sequence for a health center that has not moved yet:</p>

    <p><strong>Work out which service each patient is actually getting.</strong> Not
    which code pays best. APCM and CCM cannot both be billed for the same patient in the
    same month, and the choice turns on whether you already report quality measures,
    because APCM carries a reporting obligation and CCM does not.</p>

    <p><strong>Decide who is going to hold the time.</strong> The time-based codes need
    tracked minutes with a date, a staff member, and what was done, with no carryover
    between months. Insufficient time documentation is the most common denial in this
    benefit. If the answer is a medical assistant doing it between patients, the program
    will not survive review.</p>

    <p><strong>Price the coinsurance conversation.</strong> Screen for qualified Medicare
    beneficiary status before enrolling. Those patients owe nothing, and G0558 exists
    precisely for them.</p>

    <p><strong>Then decide whether to staff it or buy it.</strong> The arithmetic is
    usually a labour question rather than a software one. At 200 enrolled patients,
    twenty tracked minutes each is roughly 67 hours a month of licensed clinical time.</p>

    <p>The APCM code detail, including what each of the three tiers pays and where the
    24/7 access requirement fits, is covered separately in
    <a href="/resources/apcm-billing-fqhc-rhc">APCM billing at an FQHC or RHC</a>. If you
    are weighing running it in-house against outsourcing the clinical hours, that is
    <a href="/services/care-management">the care management service</a>.</p>
"""

    qa = [
        ("When exactly did G0511 go away?",
         "<p>The bundled general care management code was discontinued as part of the "
         "transition to individual code reporting, and the January 2026 CMS booklets for "
         "rural health clinics and federally qualified health centers no longer list it. "
         "Those booklets now enumerate the individual care coordination services and "
         "their codes instead. Check the current booklet for your organization type "
         "before assuming a code is still reportable.</p>"),

        ("What do RHCs and FQHCs bill now instead?",
         "<p>The individual care management codes: CCM, TCM, PCM, APCM, chronic pain "
         "management, general behavioral health integration, psychiatric collaborative "
         "care, and the remote monitoring family, each with its own base and add-on "
         "codes. CMS pays them at the national, non-facility Physician Fee Schedule "
         "rate.</p>"),

        ("Can our nurses do this remotely?",
         "<p>Yes, and this is the part most summaries skip. CMS does not require "
         "face-to-face services for RHC or FQHC care coordination, and auxiliary "
         "personnel may provide them under general supervision. General supervision "
         "means the billing practitioner directs the service without needing to be "
         "physically present while it happens. Note this is a different standard from "
         "the annual wellness visit, which requires direct supervision.</p>"),

        ("Does the patient get a bill now?",
         "<p>For the time-based codes, yes. The 20 percent coinsurance is based on the "
         "lesser of the submitted charges or the individual code's national non-facility "
         "rate. Patients with qualified Medicare beneficiary status owe nothing, which is "
         "what G0558 exists for. Screen for that status before enrolling and say the cost "
         "out loud during the consent call.</p>"),

        ("Where do the costs go on our cost report?",
         "<p>In the non-reimbursable section. CMS does not consider care coordination "
         "costs under the RHC all-inclusive rate or the FQHC prospective payment system. "
         "Administrative activities such as transcription and translation should not be "
         "included.</p>"),

        ("Can we bill APCM and CCM for the same patient?",
         "<p>Not in the same month. You choose one per patient per month, and only one "
         "practitioner or facility may bill care coordination for that patient in that "
         "period. The choice usually turns on quality reporting: APCM requires it, CCM "
         "does not, so a health center already reporting has a much easier time with "
         "APCM.</p>"),
    ]

    return _post(
        slug="g0511-sunset-rhc-fqhc-billing",
        title="G0511 Is Gone: RHC &amp; FQHC Care Management in 2026",
        description=(
            "G0511 is retired. How rural health clinics and FQHCs bill care management "
            "in 2026: the replacement codes, coinsurance, cost report, and supervision."
        ),
        eyebrow="Reimbursement",
        h1="G0511 is gone. <em>What health centers bill now.</em>",
        deck=(
            "The bundled care management code that rural health clinics and federally "
            "qualified health centers reported for years is retired. Here is what "
            "replaced it, and the four things that changed with it."
        ),
        body=body,
        reviewed=True,
        qa=qa,
        sources=[
            ("CMS, Information for Rural Health Clinics, MLN006398, January 2026.",
             "https://www.cms.gov/files/document/mln006398-information-rural-health-clinics.pdf"),
            ("CMS, Federally Qualified Health Center, MLN006397.",
             "https://www.cms.gov/files/document/mln006397-federally-qualified-health-center.pdf"),
            ("CMS, Care Management, Physician Fee Schedule.",
             "https://www.cms.gov/medicare/payment/fee-schedules/physician/care-management"),
            ("CMS, Advanced Primary Care Management services.",
             "https://www.cms.gov/medicare/payment/fee-schedules/physician-fee-schedule/advanced-primary-care-management-services"),
            ("CMS, Chronic Care Management Services booklet, MLN909188.",
             "https://www.cms.gov/files/document/chroniccaremanagement.pdf"),
            ("CMS, Physician Fee Schedule lookup.",
             "https://www.cms.gov/medicare/physician-fee-schedule/search"),
            ("National Association of Rural Health Clinics.",
             "https://narhc.org/"),
        ],
        disclaimer=(
            "Written against the January 2026 CMS booklets and reviewed August 2026. "
            "Payment rates are national averages adjusted by locality and updated each "
            "January. Code sets and program requirements change. This is not billing or "
            "compliance advice for your organization: confirm current codes, rates, and "
            "documentation requirements with your MAC before billing."
        ),
        cta_title="Thinking about who runs it?",
        cta_body=(
            "TULQ supplies the licensed nurses who do care management work inside your "
            "own record, under your supervising provider, with the documentation the "
            "individual codes now require. You keep the billing and the patient "
            "relationship."
        ),
    )


# ══════════════════════════════════════════════════════════════════════
# Quick-win cluster, from the Aug 2026 research.
#
# Four informational posts that feed the money pages. None of them tries
# to outrank CMS or AAFP on a head term; each targets the long-tail
# question and the AI-answer citation, which is the winnable ground for a
# domain with no authority.
# ══════════════════════════════════════════════════════════════════════

def post_compact_states() -> Page:
    body = """    <p>Nursing licensure follows the patient, not the nurse. A nurse sitting in
    Washington who telephones a patient in Montana is practising nursing in Montana, and
    needs to hold a licence that is valid there. That single rule decides whether a
    remote nursing model is lawful in your state, and it is the first thing you should
    ask any vendor.</p>

    <h2>What the compact does</h2>

    <p>The Nurse Licensure Compact lets a nurse hold one multistate licence, issued by
    their primary state of residence, and practise in every other member jurisdiction
    without applying for a separate licence in each. The official NLC site currently
    states that 43 jurisdictions are part of the compact.</p>

    <p>Read that number carefully, because it is the detail most summaries get wrong.
    Jurisdictions move through stages: legislation enacted, then a partial or full
    implementation date, and a state that has passed a law is not necessarily issuing or
    honouring multistate licences yet. The count that matters for your practice is
    whether your state is <em>implemented</em>, not whether it has been counted. Check
    the current map before relying on any figure, including this one.</p>

    <h2>Why it decides a remote nursing contract</h2>

    <p>Every service TULQ runs is delivered by telephone to a patient who is somewhere
    else, so licensure is not an administrative footnote:</p>

    <p><strong>After-hours triage.</strong> The nurse assessing a symptom at 2 a.m. is
    practising in the caller's state. Compact coverage is what makes national
    availability practical rather than a fifty-application project.</p>

    <p><strong>Care management.</strong> Monthly clinical outreach to an enrolled patient
    is nursing practice in that patient's state, every month, for as long as they are
    enrolled.</p>

    <p><strong>Annual wellness visits.</strong> Same rule, and the visit is a scheduled
    clinical encounter rather than an incidental call, so it deserves the same scrutiny.</p>

    <h2>What compact membership does not do</h2>

    <p>It does not override scope of practice. A nurse working under a multistate licence
    practises under the laws and scope rules of the state where the patient is, which can
    differ from their home state. It does not cover non-compact states, where a
    single-state licence is still required. And it does not answer the separate question
    of physician supervision, which for the annual wellness visit is a Medicare rule
    rather than a licensure one.</p>

    <h2>The question to ask a vendor</h2>

    <p>Not "are your nurses compact licensed," which every vendor will answer yes to.
    Ask: <strong>which of our patients' states are you licensed to practise in today, and
    what do you do about the ones you are not?</strong> An honest answer names the gaps
    and says how they are covered, usually with single-state licences held by named
    nurses. We will confirm coverage for your state before quoting, and tell you if we
    cannot cover it yet.</p>
"""
    qa = [
        ("How many states are in the nurse licensure compact?",
         "<p>The official NLC site currently states that 43 jurisdictions are part of the "
         "compact. That figure includes jurisdictions at different stages, some enacted "
         "but not yet implemented, so check the current map rather than relying on a "
         "count quoted anywhere, including here. Membership changes most years as "
         "legislatures act.</p>"),
        ("Which state's rules apply, the nurse's or the patient's?",
         "<p>The patient's. A nurse practising under a multistate licence works under the "
         "laws and scope of practice of the state where the patient is located. This is "
         "why licensure is the first compliance question in any remote nursing "
         "arrangement, and why a vendor that cannot name your state is a problem.</p>"),
        ("What happens if our state is not in the compact?",
         "<p>The nurse needs a single-state licence for your state. That is normal and "
         "workable; it just takes time and costs money, which is why some vendors quietly "
         "decline non-compact states. Ask directly rather than assuming national coverage "
         "means national licensure.</p>"),
        ("Does compact licensure cover the supervision rules too?",
         "<p>No, they are separate questions. Licensure decides whether a nurse may "
         "practise. Medicare supervision rules decide whether a service is payable and "
         "who must be available while it happens. Care management runs under general "
         'supervision; the annual wellness visit requires direct supervision. '
         '<a href="/services/medicare-annual-wellness-visits">That distinction is covered '
         "on the wellness visit page</a>.</p>"),
    ]
    return _post(
        slug="nurse-licensure-compact-states",
        title="Nurse Licensure Compact States: What It Means for You",
        description=(
            "How the Nurse Licensure Compact works, why nursing licensure follows the "
            "patient's state, and the question to ask any remote nursing vendor."
        ),
        eyebrow="Licensure",
        h1="The compact, and why <em>licensure follows the patient.</em>",
        deck=(
            "A nurse who telephones a patient in another state is practising nursing in "
            "that state. Here is what the Nurse Licensure Compact does about it, and what "
            "it does not."
        ),
        body=body,
        reviewed=True,
        qa=qa,
        sources=[
            ("Nurse Licensure Compact, official site.", "https://www.nursecompact.com/"),
            ("NCSBN, licensure compacts.", "https://www.ncsbn.org/compacts.page"),
            ("42 CFR 410.15, annual wellness visit.", "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-410/subpart-B/section-410.15"),
        ],
        disclaimer=(
            "Compact membership and implementation dates change; the counts here were "
            "checked in August 2026 against the official NLC site and should be "
            "re-checked against its current map. This is not legal advice on licensure "
            "for your organization."
        ),
        cta_title="Ask us about your state.",
        cta_body=(
            "We confirm licensure coverage for the states your patients are in before we "
            "quote you, and we will tell you plainly if we cannot cover one yet."
        ),
    )


def post_cm_small_practices() -> Page:
    body = """    <p>Care management is sold to large groups and bought by them. The independent
    practice with 400 Medicare patients, three providers, and one medical assistant who
    already does too much is the one leaving the most money on the table, and the one
    every national vendor quotes badly.</p>

    <h2>Why small practices stall</h2>

    <p>Not because anyone disagrees the work is worth doing. Three specific things stop
    it:</p>

    <p><strong>The hours do not exist.</strong> Twenty tracked minutes per patient per
    month is the arithmetic that kills it. At 200 enrolled patients that is roughly 67
    hours a month of licensed clinical time. There is no version of a busy medical
    assistant's week that absorbs 67 hours.</p>

    <p><strong>The documentation standard is higher than people expect.</strong>
    Insufficient time documentation is the most common denial in this benefit. Time
    logged with a date, a staff member, and what was done, with no carryover between
    months. A program run informally between patients will not survive review, and the
    repayment risk lands on the practice, not on whoever suggested it.</p>

    <p><strong>The quotes assume a panel you do not have.</strong> National vendors price
    for scale. A monthly floor built for 2,000 enrolled patients is not a proposal for a
    practice with 120.</p>

    <h2>What good looks like at small scale</h2>

    <p><strong>Start at fifty patients, not the whole panel.</strong> Ninety days, then
    look at what actually got billed and what the documentation looks like. Any vendor
    unwilling to start there is selling you a contract rather than a program.</p>

    <p><strong>Enrol during a wellness visit.</strong> An annual wellness visit is a
    qualifying visit, and it is the appointment where a nurse has twenty unhurried
    minutes with a patient who is not sick. Enrollment during a wellness visit converts
    at a materially different rate from cold outreach, which is why the two services
    belong together.</p>

    <p><strong>Pick the right instrument per patient.</strong> APCM has no time threshold
    at all but requires quality reporting. CCM requires tracked time but adds no
    reporting obligation. If you already report, APCM is usually the cleaner choice. You
    cannot bill both for the same patient in the same month.</p>

    <p><strong>Watch the fee structure, not just the fee.</strong> A vendor paid as a
    share of your collections is paid more when more gets coded. That is the arrangement
    auditors look at hardest, and a flat fee per enrolled patient avoids the question
    entirely.</p>

    <h2>Build or buy</h2>

    <p>Hiring is the right answer for some practices, and it is worth costing honestly:
    a care coordinator's loaded salary, the recruiting time, the training, the coverage
    when they are on leave, and the program stopping when they resign. Against that, a
    per-patient fee that scales down as easily as up.</p>

    <p>The arithmetic usually turns on whether you can keep one person's whole role
    filled. If you can, hire. If the honest answer is that this would be someone's fifth
    priority, buy it, or do not run the program at all. A half-run program that fails an
    audit is worse than no program.</p>

    <p>The full model, including which of the thirteen requirements sit with you, is on
    <a href="/services/care-management">the care management page</a>. If you are a health
    centre, the billing changed in 2026:
    <a href="/resources/g0511-sunset-rhc-fqhc-billing">G0511 is gone</a>.</p>
"""
    qa = [
        ("Is our practice too small for care management?",
         "<p>Rarely, but the vendor might be too large. The programme works down to "
         "surprisingly small panels because the payment is per patient per month, so the "
         "revenue scales with the enrollment rather than requiring a threshold. What does "
         "not scale down is a vendor contract with a monthly floor. Ask for a per-patient "
         "fee with no minimum and a fifty-patient pilot.</p>"),
        ("How many patients do we need to make it worth doing?",
         "<p>Run your own numbers rather than taking a benchmark. At 2026 national "
         "averages, Advanced Primary Care Management pays about $54 per patient per month "
         "at level two, where most enrolled patients sit. Multiply by a realistic "
         "enrollment, subtract the fee, and compare the remainder against the staff time "
         "you would otherwise spend. If the remainder is small, do not do it.</p>"),
        ("Can our medical assistant just do this?",
         "<p>They can do some of it, and the rules permit clinical staff to deliver the "
         "service under general supervision. The question is whether they can hold twenty "
         "tracked minutes per patient per month on top of their existing day, every "
         "month, and document it to an auditable standard. At 200 patients that is 67 "
         "hours. Most practices discover the answer six months in, when the program has "
         "quietly stopped.</p>"),
        ("What is the difference between CCM and APCM for a small practice?",
         "<p>CCM pays for tracked time and adds no reporting obligation. APCM pays a flat "
         "monthly amount by patient complexity with no time threshold, but requires "
         "quality reporting. A small practice already reporting quality measures usually "
         "prefers APCM because the stopwatch disappears. One that is not should look hard "
         "at whether the reporting obligation is worth taking on.</p>"),
    ]
    return _post(
        slug="care-management-outsourcing-small-practices",
        title="Care Management Outsourcing for Small Practices",
        description=(
            "Why small practices stall on CCM and APCM, what good looks like at small "
            "scale, and how to decide between hiring a coordinator and outsourcing."
        ),
        eyebrow="Care management",
        h1="Care management <em>at a small practice.</em>",
        deck=(
            "The independent practice with 400 Medicare patients is leaving the most on "
            "the table and getting quoted the worst. Here is the honest build-or-buy."
        ),
        body=body,
        reviewed=True,
        qa=qa,
        sources=[
            ("CMS, Chronic Care Management Services booklet, MLN909188.", "https://www.cms.gov/files/document/chroniccaremanagement.pdf"),
            ("CMS, Advanced Primary Care Management services.", "https://www.cms.gov/medicare/payment/fee-schedules/physician-fee-schedule/advanced-primary-care-management-services"),
            ("CMS, Care Management, Physician Fee Schedule.", "https://www.cms.gov/medicare/payment/fee-schedules/physician/care-management"),
            ("CMS, Physician Fee Schedule lookup.", "https://www.cms.gov/medicare/physician-fee-schedule/search"),
        ],
        disclaimer=(
            "Payment amounts are 2026 national averages under the Medicare Physician Fee "
            "Schedule, adjusted by locality and updated each January. Reviewed August "
            "2026. This is not billing or compliance advice for your practice."
        ),
        cta_title="Start with fifty patients.",
        cta_body=(
            "Bring your Medicare patient count and we will model the program against your "
            "own locality, then run ninety days on a small cohort before either of us "
            "commits to anything larger."
        ),
    )


def post_who_can_perform_awv() -> Page:
    body = """    <p>The short answer: more people than most practices think can perform it, and
    fewer than most vendors imply can bill it. Those are two different questions and
    conflating them is how a wellness visit program becomes a repayment.</p>

    <h2>Who may perform the visit</h2>

    <p>Medicare covers the annual wellness visit when it is furnished by a physician, by
    a qualified non-physician practitioner such as a physician assistant, nurse
    practitioner, or clinical nurse specialist, or by a medical professional or a team of
    medical professionals working under the <strong>direct supervision</strong> of a
    physician.</p>

    <p>That third route is the one that matters operationally. It is why a registered
    nurse, a health educator, or a licensed practical nurse can deliver the visit itself.
    Most of an annual wellness visit is a health risk assessment, history, a medication
    and provider list, screenings, and a written screening schedule. It is structured
    questioning rather than examination, which is exactly the work a nurse does well.</p>

    <h2>What direct supervision means</h2>

    <p>Direct supervision means the physician is immediately available to furnish
    assistance and direction throughout the performance of the service. Historically that
    meant present in the office suite, and not merely reachable by telephone.</p>

    <p>Since 1 January 2026 the presence it requires may be a virtual one, through
    real-time audio and video interactive telecommunications. Audio-only does not satisfy
    it, and it does not extend to services carrying a 010 or 090 global surgery indicator,
    which the wellness visit does not. CMS adopted this permanently in the CY2026
    Physician Fee Schedule final rule rather than extending it as a dated flexibility, and
    it is the single change that makes a standing telephone wellness visit programme
    practical to run. We have written the whole chain out in
    <a href="/awv">plain English</a>.</p>

    <p>It remains a stricter standard than care management, which runs under general
    supervision, where the billing practitioner directs the service without needing to be
    present at all. The two are frequently sold together and they do not share a
    supervision rule. If a vendor's pitch glosses that, press on it.</p>

    <h2>Who bills it</h2>

    <p>The billing practitioner, and the supervision obligation, sit with the practice.
    An outsourced nurse can perform the visit and produce the documentation. An
    outsourced nurse cannot make your practice's supervision requirement disappear, and
    no vendor can bill a Medicare annual wellness visit on your behalf as though it were
    theirs.</p>

    <p>Any vendor implying otherwise is describing something other than the benefit. We
    say this on <a href="/services/medicare-annual-wellness-visits">our own service
    page</a> rather than in a contract appendix, because it is the thing most likely to
    cause a practice trouble later.</p>

    <h2>Can it be done by telephone</h2>

    <p>For established patients, yes. The annual wellness visit sits on the Medicare
    telehealth list and audio-only delivery is permitted under the telehealth
    flexibilities, which the Consolidated Appropriations Act of 2026 extended through 31
    December 2027. New patients generally still need to be seen in person. Because these
    flexibilities have been extended repeatedly rather than made permanent, check the
    current CMS telehealth list rather than assuming the position holds.</p>

    <h2>Health centres</h2>

    <p>Federally qualified health centres and rural health clinics bill the bundled
    per-diem G0468 under their prospective payment system, with the standard G-codes
    reported on the claim for tracking. The clinical work is identical; the revenue
    arithmetic is not, and usually turns on visit volume rather than the per-visit rate.</p>
"""
    qa = [
        ("Can a registered nurse perform a Medicare annual wellness visit?",
         "<p>Yes, as part of a medical professional or team working under the direct "
         "supervision of a physician. The visit is largely history, structured screening, "
         "and a written prevention schedule rather than examination, which is why it is "
         "well suited to a nurse. The billing practitioner and the supervision obligation "
         "remain with the practice.</p>"),
        ("What exactly is direct supervision?",
         "<p>The physician must be immediately available to furnish assistance and "
         "direction throughout the performance of the service. Since 1 January 2026 that "
         "presence may be virtual, through real-time audio and video, rather than in the "
         "office suite; audio-only does not satisfy it. It remains a stricter standard "
         "than the general supervision that applies to care management, where the billing "
         "practitioner directs the service without needing to be present at all.</p>"),
        ("Can an outsourced company bill the AWV for us?",
         "<p>No. Your practice bills it, because the billing practitioner and the "
         "supervision requirement sit with you. A vendor can perform the visit and hand "
         "you finished documentation. If a vendor tells you it will bill Medicare for "
         "your patients' wellness visits, ask exactly what it means, because that is not "
         "how the benefit works.</p>"),
        ("Is an AWV the same as a physical?",
         "<p>No, and patients are often surprised. The annual wellness visit does not "
         "include a head-to-toe examination. It is a health risk assessment, medical and "
         "family history, a current provider and medication list, height, weight and "
         "blood pressure, cognitive impairment detection, depression screening, "
         "functional ability and safety review, a written screening schedule for the next "
         "five to ten years, and personalised advice with referrals.</p>"),
        ("What does it pay?",
         "<p>As 2026 national averages, roughly $174 for an initial visit (G0438) and "
         "roughly $138 for each subsequent one (G0439), both covered at 100 percent with "
         "no patient cost sharing. Amounts are adjusted by locality, so check the fee "
         'schedule lookup. You can model your own gap with our '
         '<a href="/tools/awv-revenue-calculator">AWV revenue calculator</a>.</p>'),
    ]
    return _post(
        slug="who-can-perform-annual-wellness-visit",
        title="Who Can Perform a Medicare Annual Wellness Visit?",
        description=(
            "Who may perform an AWV versus who may bill it, what direct supervision "
            "really requires, and whether a nurse can deliver the visit by telephone."
        ),
        eyebrow="Wellness visits",
        h1="Who can perform <em>an annual wellness visit?</em>",
        deck=(
            "More people can perform it than most practices think, and fewer can bill it "
            "than most vendors imply. Those are two different questions."
        ),
        body=body,
        reviewed=True,
        qa=qa,
        sources=[
            ("42 CFR 410.15, annual wellness visit.", "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-410/subpart-B/section-410.15"),
            ("42 CFR 410.32(b)(3)(ii), levels of supervision.", "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-410/subpart-B/section-410.32"),
            ("CMS, CY2026 Physician Fee Schedule final rule fact sheet, CMS-1832-F.", "https://www.cms.gov/newsroom/fact-sheets/calendar-year-cy-2026-medicare-physician-fee-schedule-final-rule-cms-1832-f"),
            ("CMS, Medicare Wellness Visits, MLN6775421.", "https://www.cms.gov/outreach-and-education/medicare-learning-network-mln/mlnproducts/mln-publications/mln6775421"),
            ("Medicare.gov, yearly wellness visits.", "https://www.medicare.gov/coverage/yearly-wellness-visits"),
            ("CMS, Medicare telehealth.", "https://www.cms.gov/medicare/coverage/telehealth"),
            ("CMS, Physician Fee Schedule lookup.", "https://www.cms.gov/medicare/physician-fee-schedule/search"),
        ],
        disclaimer=(
            "Reviewed August 2026. The virtual direct supervision definition was adopted "
            "permanently in the CY2026 Physician Fee Schedule final rule, but the "
            "patient-facing audio-only telehealth allowance carries a date; confirm the "
            "current position with CMS and your MAC. This is not billing or compliance "
            "advice."
        ),
        cta_title="Nurses who do the visit properly.",
        cta_body=(
            "TULQ supplies compact-licensed registered nurses who complete the visit by "
            "telephone and hand back finished documentation. Your practice supervises and "
            "bills, which is how the benefit is designed."
        ),
    )


def post_awv_completion() -> Page:
    body = """    <p>Every practice knows the annual wellness visit is worth doing. Most complete
    it for a minority of the eligible panel anyway. The gap is almost never a clinical
    disagreement, and it is almost never fixed by trying harder.</p>

    <h2>Why the visit loses</h2>

    <p>It competes for an examination room with sick visits, and sick visits always win.
    The wellness visit takes the better part of half an hour to do properly, generates no
    urgent complaint to anchor it, produces no immediate patient demand, and is therefore
    the easiest thing on the schedule to defer to a quarter that never arrives.</p>

    <p>Notice that none of those are motivation problems. They are scheduling and
    capacity problems, and they respond to structural fixes rather than to reminders.</p>

    <h2>Six things that actually move the rate</h2>

    <p><strong>Take it out of the examination room.</strong> The single largest lever.
    For established patients the visit can be delivered by telephone under the telehealth
    flexibilities extended through 31 December 2027. A visit that does not need a room is
    no longer competing for one.</p>

    <p><strong>Measure the real baseline first.</strong> Pull the actual count of G0438
    and G0439 claims from last year rather than estimating. Practices consistently guess
    high, and a programme that starts from a flattering baseline cannot show progress.</p>

    <p><strong>Work an eligibility list, not the whole panel.</strong> Sort by last visit
    date. Patients whose eligibility opens this month are a queue, not a mailing list,
    and the queue refreshes every month.</p>

    <p><strong>Say it costs nothing, early.</strong> The visit is covered at 100 percent
    with no coinsurance and no deductible. Patients decline because they assume a bill.
    Leading with the fact removes the most common objection before it is raised.</p>

    <p><strong>Attach the add-ons that belong.</strong> Advance care planning on the same
    day, and depression screening alongside a subsequent visit, are legitimately
    reportable and routinely left unbilled. Both have their own documentation
    requirements, so attach them when the work is genuinely done and not otherwise.</p>

    <p><strong>Use the visit to enrol.</strong> An annual wellness visit is a qualifying
    visit for care management. It is twenty unhurried minutes with a patient who is not
    sick, which is when chronic conditions surface honestly and consent can be explained
    properly. This is where the recurring revenue actually is.</p>

    <h2>Do the arithmetic before the programme</h2>

    <p>Multiply the number of additional completed visits by the blended rate, subtract
    the cost of whoever does them, and look at the remainder before committing. Our
    <a href="/tools/awv-revenue-calculator">AWV revenue calculator</a> will do it against
    your own panel and completion rate in about thirty seconds, and our
    <a href="/tools/annual-wellness-visit-worksheet">visit worksheet</a> is free if the
    problem is that the documentation takes too long.</p>

    <p>If the remainder is small, do not run the programme. That is a legitimate outcome
    and it is better discovered now.</p>
"""
    qa = [
        ("What is a realistic AWV completion rate?",
         "<p>Set your own target rather than chasing a benchmark, because the achievable "
         "rate depends far more on whether the visit has to occupy an examination room "
         "than on anything clinical. What matters is measuring the real baseline first: "
         "pull the actual count of G0438 and G0439 claims you billed last year, because "
         "practices consistently overestimate it.</p>"),
        ("Does moving the visit to the phone hurt quality?",
         "<p>It should not, and the reason is what the visit is. There is no head-to-toe "
         "examination in an annual wellness visit. It is a health risk assessment, "
         "history, screenings, and a written prevention schedule, which is structured "
         "questioning. What it does need is an unhurried twenty minutes, and a telephone "
         "visit is more likely to get that than a squeezed in-person slot.</p>"),
        ("Which add-on codes are legitimately billable on the same day?",
         "<p>Advance care planning is reportable on the same day as the wellness visit "
         "and the patient owes nothing for it when furnished that way. Depression "
         "screening is separately reportable alongside a subsequent visit. Both carry "
         "their own documentation requirements, and neither should be attached "
         "reflexively; bill them when the work was actually done.</p>"),
        ("How does the wellness visit connect to care management revenue?",
         "<p>It is the on-ramp. An AWV is a qualifying visit for care management "
         "enrollment, and it is the appointment where a nurse has time to discover the "
         "chronic conditions and explain a monthly programme properly. Enrollment during "
         "a wellness visit converts at a materially different rate from cold outreach, "
         'which is why <a href="/services/care-management">the two services belong '
         "together</a>.</p>"),
    ]
    return _post(
        slug="increase-awv-completion-rates",
        title="How to Increase Annual Wellness Visit Completion Rates",
        description=(
            "Six structural fixes that move AWV completion rates, why the visit loses to "
            "sick visits, and how to do the arithmetic before starting a program."
        ),
        eyebrow="Wellness visits",
        h1="Closing <em>the wellness visit gap.</em>",
        deck=(
            "The visit does not lose because anyone disagrees with it. It loses because "
            "it competes for an examination room with sick visits, and sick visits win."
        ),
        body=body,
        reviewed=True,
        qa=qa,
        sources=[
            ("42 CFR 410.15, annual wellness visit.", "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-410/subpart-B/section-410.15"),
            ("CMS, Medicare Wellness Visits, MLN6775421.", "https://www.cms.gov/outreach-and-education/medicare-learning-network-mln/mlnproducts/mln-publications/mln6775421"),
            ("Medicare.gov, yearly wellness visits.", "https://www.medicare.gov/coverage/yearly-wellness-visits"),
            ("CMS, Medicare telehealth.", "https://www.cms.gov/medicare/coverage/telehealth"),
            ("CMS, Physician Fee Schedule lookup.", "https://www.cms.gov/medicare/physician-fee-schedule/search"),
        ],
        disclaimer=(
            "Reviewed August 2026. Payment amounts are 2026 national averages adjusted by "
            "locality. Add-on codes carry their own coverage and documentation "
            "requirements. This is not billing or coding advice for your practice."
        ),
        cta_title="Model it against your own panel.",
        cta_body=(
            "Run the calculator, then bring the number to a fifteen minute call and we "
            "will redo it against your real locality rather than a national average."
        ),
    )


def post_cah() -> Page:
    body = """    <p>Critical access hospitals operate under a designation designed to keep small
    rural facilities viable, and under conditions of participation that come with it.
    One of those conditions concerns emergency care availability, which regularly gets
    read as covering the after-hours telephone. It does not.</p>

    <h2>What the designation requires</h2>

    <p>The CAH designation carries a set of structural limits and obligations:</p>

    <ul>
      <li>No more than 25 inpatient beds</li>
      <li>A location standard relative to other hospitals, with statutory exceptions</li>
      <li>An annual average inpatient length-of-stay limit</li>
      <li>24-hour emergency care services</li>
    </ul>

    <p>CMS conditions of participation also address the availability of a physician and
    notification when a physician is not on site around the clock. There were roughly
    1,377 critical access hospitals nationally as of early 2025.</p>

    <h2>What the requirement does not cover</h2>

    <p>Emergency care availability is about the emergency department: that it is
    open, that it is staffed, that a patient who arrives is seen. It says nothing about
    the patient at home at 11 p.m. who has not decided whether to come in.</p>

    <p>That patient has two options, and neither involves a clinician: guess, or drive
    in. A share of them drive in for something that did not need an emergency
    department. A different share guess wrong in the other direction and arrive the next
    day considerably worse.</p>

    <div class="callout">
      <div class="callout-head">The compliance point stated plainly</div>
      <p>Nurse triage does not satisfy your emergency services condition of
      participation and nobody should sell it to you as though it does. It addresses a
      gap the conditions do not speak to. Keep those two things separate in your own
      analysis, and be sceptical of any vendor who blurs them.</p>
    </div>

    <h2>Why the ED is the wrong first stop for some of this volume</h2>

    <p>For a small rural hospital, unnecessary ED volume is not primarily a revenue
    problem; it is a staffing one. A CAH emergency department may be covered by a
    single provider. Every low-acuity presentation consumes attention that is not
    infinitely divisible, and the cost lands on the next patient who walks in with
    something serious.</p>

    <p>There is also the attached clinic to consider: a majority of CAHs operate an
    associated rural health clinic, and many run swing-bed programs. Patients moving
    between those settings generate after-hours questions that have nowhere clinical to
    land.</p>

    <h2>The staffing arithmetic</h2>

    <p>The theoretically correct answer to all of this is to staff a nurse for the
    phone. Consider what that requires: around-the-clock coverage of a single seat needs
    roughly four to five full-time equivalents once shifts, relief, leave, and turnover
    are accounted for. For a facility that struggles to fill its existing clinical
    positions, that is not a plan.</p>

    <p>The realistic options are to leave the phone uncovered, push it onto providers
    already carrying too much, or contract the function. Contracting is the only one of
    the three that does not consume clinical staff you do not have.</p>

    <h2>What to specify if you contract it</h2>

    <ul>
      <li><strong>Licensure in your state</strong> for the nurses handling your calls,
      written into the agreement.</li>
      <li><strong>Escalation rules you define</strong>: which calls reach your
      ED, which reach the clinic provider, which reach nobody until morning.</li>
      <li><strong>Documentation format</strong> that your team can actually use at
      07:00 without re-keying it.</li>
      <li><strong>Flat pricing</strong> so that a bad respiratory season does not become
      a budget variance you have to explain to a board.</li>
      <li><strong>Swing-bed and attached-RHC call handling</strong>. If you run them, those calls have different escalation paths and are easy to leave out of
      a scope of work.</li>
    </ul>"""

    return _post(
        slug="critical-access-hospital-after-hours",
        title="After-Hours Coverage for Critical Access Hospitals",
        description=(
            "What the CAH conditions of participation require, what they leave uncovered, "
            "and why staffing a 24/7 phone seat rarely works for a small hospital."
        ),
        eyebrow="Rural hospitals",
        h1="The CAH phone line <em>nobody is required to answer.</em>",
        deck=(
            "Your emergency department is covered. The patient deciding at 11 p.m. "
            "whether to drive to it is not. That gap is not addressed by the conditions "
            "of participation, and it is where the avoidable volume comes from."
        ),
        body=body,
        reviewed=True,
        sources=[
            ("Conditions of participation for critical access hospitals, 42 CFR Part 485 Subpart F.",
             "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-G/part-485/subpart-F"),
            ("Rural Health Information Hub, critical access hospitals topic guide.",
             "https://www.ruralhealthinfo.org/topics/critical-access-hospitals"),
            ("Flex Monitoring Team, critical access hospital data and reporting.",
             "https://www.flexmonitoring.org/"),
        ],
        disclaimer=(
            "Conditions of participation and facility counts change. Nothing here is "
            "compliance advice. Verify against the current CFR and your state "
            "survey agency, and confirm any coverage arrangement with your compliance "
            "staff."
        ),
    )


def posts() -> list[Page]:
    return [
        post_true_cost(),
        post_triage_vs_answering(),
        post_cahps(),
        post_hhvbp(),
        post_apcm(),
        post_g0511_sunset(),
        post_compact_states(),
        post_cm_small_practices(),
        post_who_can_perform_awv(),
        post_awv_completion(),
        post_cah(),
    ]


def resources_index() -> Page:
    page = Page(
        site=SITE,
        slug="resources/index",
        title="Nurse Triage, Care Management &amp; AWV Resources | TULQ",
        description=(
            "Sourced explainers on after-hours coverage costs, CCM and APCM billing, the "
            "G0511 sunset, wellness visit rules, and two free tools. No signup."
        ),
        eyebrow="Resources",
        h1="The operational stuff, <em>written down.</em>",
        deck=(
            "Three tracks, one per service line: what after-hours coverage costs, how "
            "Medicare pays for managing chronic patients, and who may perform a wellness "
            "visit. Sourced to CMS and the CFR, and honest about the limits."
        ),
        crumbs=[("Resources", "/resources/")],
        wide=True,
        priority="0.7",
        cta_title="Something we should write about?",
        cta_body=(
            "If there is a question your team keeps answering from scratch, tell us. "
            "The useful pieces here started as somebody's question."
        ),
    )

    page.body = f"""    <p>Everything here is written from primary sources: CMS booklets, the Code of
    Federal Regulations, and the fee schedule, rather than from other vendors' summaries
    of them. Where a figure is a national average that your locality will change, it says
    so.</p>

    <h2>Free tools, no signup</h2>

    {card_grid([
        ("Calculator", "AWV revenue gap calculator",
         "Enter your Medicare panel and what you billed last year, and see the wellness visit revenue you are not collecting. Runs in your browser.",
         "/tools/awv-revenue-calculator"),
        ("Worksheet", "Annual wellness visit worksheet",
         "A charting worksheet built to the elements at 42 CFR 410.15, which generates a structured note. Nothing you type leaves the page.",
         "/tools/annual-wellness-visit-worksheet"),
        ("Compare", "Compare vendors",
         "IntellaTriage, ChartSpan, Signallamp, ThoroughCare and more: what each is built for, and when to pick them over us.",
         "/compare/"),
    ])}

    <h2>After-hours triage</h2>

    {card_grid([
        ("Cost &amp; ROI", "The true cost of after-hours on-call",
         "Direct pay is the smallest of four buckets. The whole calculation, including the line item that usually decides it.",
         "/resources/true-cost-of-after-hours-on-call"),
        ("Basics", "Nurse triage vs answering service",
         "They fill the same slot and do different work. The one question that exposes which you're being sold.",
         "/resources/nurse-triage-vs-answering-service"),
        ("CAHPS", "After-hours access and hospice CAHPS",
         "Which measures it moves, which it doesn't, and the operational proxies to track meanwhile.",
         "/resources/hospice-cahps-after-hours"),
        ("HHVBP", "HHVBP and ED use",
         "The CY2025 within-stay potentially preventable hospitalization measure, and the pathway triage interrupts.",
         "/resources/hhvbp-ed-use"),
        ("Rural hospitals", "After-hours coverage for critical access hospitals",
         "What the conditions of participation require, what they leave uncovered, and the staffing arithmetic.",
         "/resources/critical-access-hospital-after-hours"),
    ])}

    <h2>Care management</h2>

    {card_grid([
        ("Reimbursement", "G0511 is gone: what health centers bill now",
         "The bundled code is retired. The replacement codes, the coinsurance, the cost report, and the supervision rule that makes remote nursing possible.",
         "/resources/g0511-sunset-rhc-fqhc-billing"),
        ("Reimbursement", "APCM billing at an FQHC or RHC",
         "G0556, G0557, G0558: what changed, who can bill, and where 24/7 access fits.",
         "/resources/apcm-billing-fqhc-rhc"),
        ("Small practices", "Care management outsourcing for small practices",
         "Why small practices stall on CCM and APCM, what good looks like at small scale, and the honest build-or-buy.",
         "/resources/care-management-outsourcing-small-practices"),
    ])}

    <h2>Annual wellness visits</h2>

    {card_grid([
        ("Rules", "Who can perform an annual wellness visit?",
         "Who may perform it against who may bill it, what direct supervision actually requires, and whether a nurse can do it by phone.",
         "/resources/who-can-perform-annual-wellness-visit"),
        ("Playbook", "How to increase AWV completion rates",
         "Six structural fixes, why the visit loses to sick visits, and how to do the arithmetic before starting a program.",
         "/resources/increase-awv-completion-rates"),
        ("Licensure", "Nurse licensure compact states",
         "Licensure follows the patient, not the nurse. What the compact does, what it does not, and the question to ask a vendor.",
         "/resources/nurse-licensure-compact-states"),
    ])}

    <h2>By setting</h2>

    {card_grid([
        ("Hospice &amp; home health", "After-hours triage for hospice and home health",
         "Why on-call rotations break, and what changes when a nurse takes first call.",
         "/for/home-health"),
        ("Safety net", "FQHC, RHC and CAH coverage",
         "The segment with the same obligation as everyone else and the least room to staff it.",
         "/for/health-centers"),
        ("Services", "All three service lines",
         "After-hours triage, Medicare care management, and annual wellness visits, and how they fit together.",
         "/services/"),
    ])}"""

    return page


# ══════════════════════════════════════════════════════════════════════
# Comparison pages
# ══════════════════════════════════════════════════════════════════════

_COMPARE_DISCLAIMER = (
    "Competitor information is summarized from each company's own public website and "
    "was accurate as reviewed; services, pricing, and positioning change without "
    "notice. This page is written by TULQ and is not independent analysis. Verify "
    "anything that matters to your decision directly with the vendor."
)

_PRELAUNCH = """    <div class="callout callout--amber">
      <div class="callout-head">Where we are, stated plainly</div>
      <p>TULQ is launching in 2026. We do not have an operating history, call volume
      statistics, or client references at scale, and a comparison that implied
      otherwise would be worth nothing to you. What you can evaluate today is the
      clinical model, our director's credentials, licensure, protocol standard,
      escalation design, and pricing structure. If a multi-year track record is a
      hard requirement for your decision, the incumbent is the right answer and we
      would rather you knew that now.</p>
    </div>"""


TRIAGE_QUESTIONS = [
    "Who answers the first call, and what licensure do they hold?",
    "What protocol standard do your nurses work from?",
    "What share of calls resolve without reaching our clinician?",
    "What does encounter documentation look like when it reaches us, in what "
    "format, and how quickly?",
    "Who defines the escalation rules: us or you?",
    "Is pricing per-call or flat, and what happens in a bad respiratory season?",
]

# Care management turns on different things entirely: who employs the nurse,
# whose record the note lands in, and above all how the vendor is paid, since
# a vendor paid as a share of your Medicare reimbursement is the arrangement
# auditors look at hardest.
CARE_QUESTIONS = [
    "Who employs the people doing the clinical work, and what licensure do "
    "they hold in our patients' states?",
    "Does the documentation land in our record, or in yours?",
    "Are you paid a flat fee, or a share of what we collect?",
    "Are your staff compensated per enrollment?",
    "Who verifies each month that no other practice is billing that patient?",
    "What happens to our program, our data, and our patients if we leave you?",
]


def _compare(slug: str, competitor: str, title: str, description: str,
             h1: str, deck: str, profile: str, table_rows: str,
             when_them: list[str], when_us: list[str],
             qa: list, sources: list[str],
             questions: list[str] | None = None) -> Page:
    page = Page(
        site=SITE,
        slug=f"compare/{slug}",
        title=title,
        description=description,
        eyebrow="Comparison",
        h1=h1,
        deck=deck,
        body="",
        crumbs=[("Compare", "/compare/"), (competitor, f"/compare/{slug}")],
        priority="0.7",
        cta_title="Ask us the same questions.",
        cta_body=(
            "Put the same evaluation questions to us that you put to everyone else and "
            "compare the answers. That is more useful than taking any vendor's "
            "comparison page at face value."
        ),
    )

    them = "\n".join(f"      <li>{x}</li>" for x in when_them)
    us = "\n".join(f"      <li>{x}</li>" for x in when_us)
    decide = "\n".join(f"      <li>{x}</li>" for x in (questions or TRIAGE_QUESTIONS))

    page.body = f"""{profile}

{_PRELAUNCH}

    <h2>Side by side</h2>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr><th>&nbsp;</th><th>{competitor}</th><th>TULQ</th></tr>
        </thead>
        <tbody>
{table_rows}
        </tbody>
      </table>
    </div>

    <h2>Choose {competitor} if</h2>

    <ul>
{them}
    </ul>

    <h2>Choose TULQ if</h2>

    <ul>
{us}
    </ul>

    <h2>The questions that actually decide it</h2>

    <p>Ask every vendor the same six, write the answers down, and compare them
    side by side:</p>

    <ol>
{decide}
    </ol>

    {faq_block(qa)}

    {sources_block(sources, disclaimer=_COMPARE_DISCLAIMER)}"""

    page.schema = [faq_node(page, qa)]
    return page


def compare_intellatriage() -> Page:
    profile = """    <p>IntellaTriage is the category leader in outsourced nurse triage for hospice
    and home health, and any honest comparison should start there. Founded in 2008, it
    built the modern version of this service and most of the vocabulary the rest of the
    market uses.</p>

    <h2>What IntellaTriage is</h2>

    <p>Per its own published materials, IntellaTriage handled over 640,000 calls in
    2024, with an average speed to connect of around 37 seconds. Its architecture is a
    mature service-cluster model: dedicated pages and offerings for hospice and home
    health triage, after-hours nurse triage, a 24-hour nurse advice line, and patient
    engagement, alongside a substantial content operation covering nurse-first triage,
    clinician burnout, CAHPS, and revocation reduction.</p>

    <p>It is a serious operator with real clinical infrastructure. If you are a
    mid-sized or large hospice looking for a proven vendor with references in your
    segment, it belongs on your list.</p>"""

    rows = """          <tr><td>Founded</td><td>2008</td><td>Launching 2026</td></tr>
          <tr><td>Operating scale</td><td class="tick">640,000+ calls in 2024, per its own reporting</td><td class="cross">Pre-launch</td></tr>
          <tr><td>Licensed RNs on first call</td><td class="tick">Yes</td><td class="tick">Yes</td></tr>
          <tr><td>Protocol standard</td><td class="tick">Schmitt-Thompson</td><td class="tick">Schmitt-Thompson</td></tr>
          <tr><td>Primary segment</td><td>Hospice and home health</td><td>Hospice, home health, and the rural safety net</td></tr>
          <tr><td>Tribal / IHS specialization</td><td class="cross">None published</td><td class="tick">A dedicated site and practice</td></tr>
          <tr><td>Buy Indian Act standing</td><td class="cross">Not applicable</td><td class="tick">Indian Economic Enterprise</td></tr>
          <tr><td>Published pricing</td><td class="cross">Not published</td><td>Flat monthly, quoted on scope</td></tr>
          <tr><td>Client portal</td><td class="tick">IntellaHub</td><td>Documentation returned; portal at launch</td></tr>"""

    qa = [
        ("What does IntellaTriage cost?",
         "<p>IntellaTriage does not publish pricing; you get a quote scoped to your "
         "census and call volume. That is normal for the category. Our own approach is "
         "a flat monthly structure rather than per-call, so volume risk sits with us "
         "rather than with your budget, but you should get numbers from both and "
         "compare like for like.</p>"),
        ("Does IntellaTriage serve tribal health programs?",
         "<p>Not as a published specialization. We found no tribal, IHS, or "
         "Purchased/Referred Care content in its public materials. That is not a "
         "criticism; it is simply not the market it was built for. If you are a "
         "tribal health program, our tribal practice lives at "
         "<a href=\"https://tulq.health/for/tribal-health-ihs\">tulq.health</a>.</p>"),
        ("Is a newer vendor a risk?",
         "<p>Yes, and you should price that risk. The mitigations that actually work "
         "are contractual: service levels with teeth, a defined implementation and "
         "transition plan, termination provisions you can live with, and a pilot before "
         "a full cutover. Ask for all four from any vendor, incumbent or not.</p>"),
    ]

    return _compare(
        slug="intellatriage-alternative",
        competitor="IntellaTriage",
        title="IntellaTriage Alternative: An Honest Comparison | TULQ",
        description=(
            "How TULQ compares with IntellaTriage on protocols, segment focus, pricing "
            "structure, and operating history, including when to choose the incumbent."
        ),
        h1="Looking for an <em>IntellaTriage alternative.</em>",
        deck=(
            "IntellaTriage built this category and is good at it. Here is where we "
            "differ, where we don't, and the cases where you should pick them."
        ),
        profile=profile,
        table_rows=rows,
        when_them=[
            "You need a multi-year operating history and references at scale to satisfy "
            "an evaluation requirement.",
            "Your organization is large enough that proven capacity at high volume is "
            "the deciding factor.",
            "You want the vendor with the deepest hospice-specific content and the "
            "longest track record in that segment.",
        ],
        when_us=[
            "You are a tribal health program, IHS facility, or Urban Indian "
            "Organization: a segment with no incumbent specialization.",
            "You are a smaller agency or safety-net facility and want flat pricing that "
            "does not move with a bad respiratory season.",
            "The Buy Indian Act applies to your acquisition.",
            "You want a vendor small enough that your escalation rules are designed "
            "around your workflow rather than the other way round.",
        ],
        qa=qa,
        sources=[
            ("IntellaTriage public website and published materials.",
             "https://www.intellatriage.com/"),
            ("Schmitt-Thompson telephone triage protocols.",
             "https://www.stcc-triage.com/"),
        ],
    )


def compare_conduit() -> Page:
    profile = """    <p>Conduit Health Partners offers nurse-first triage alongside patient transfer
    services, with an architecture segmented by buyer type: health systems, medical
    groups, health plans, and FQHCs.</p>

    <h2>What Conduit is</h2>

    <p>Conduit's public materials lean heavily on measured outcomes. It publishes case
    studies with specific utilization numbers (including a client reaching
    roughly 90% ED avoidance, and specific groups seeing up to a 15% reduction in ED
    readmissions) and a data-driven news section covering call demand patterns,
    such as peak volume at 5 p.m. and on Saturdays, with overnight calls concentrating
    around pregnancy, fever, and vomiting.</p>

    <p>The patient-transfer capability is genuinely differentiating for health systems
    that need transfer coordination alongside triage. That is a different product than
    what we offer, and if that is your requirement, it is the more relevant one.</p>"""

    rows = """          <tr><td>Core offering</td><td>Nurse-first triage plus patient transfer coordination</td><td>Nurse-first triage</td></tr>
          <tr><td>Licensed RNs on first call</td><td class="tick">Yes</td><td class="tick">Yes</td></tr>
          <tr><td>Buyer segmentation</td><td class="tick">Health systems, medical groups, health plans, FQHCs</td><td>Hospice, home health, FQHC/RHC/CAH; tribal on a separate site</td></tr>
          <tr><td>Published outcome data</td><td class="tick">Case studies with specific utilization figures</td><td class="cross">Pre-launch: none to publish</td></tr>
          <tr><td>Patient transfer coordination</td><td class="tick">Yes</td><td class="cross">No</td></tr>
          <tr><td>Tribal / IHS specialization</td><td class="cross">None published</td><td class="tick">A dedicated site and practice</td></tr>
          <tr><td>Pricing structure</td><td>Quoted on scope</td><td>Flat monthly, quoted on scope</td></tr>"""

    qa = [
        ("Should we take Conduit's ED avoidance figures at face value?",
         "<p>Take them as real results for the clients described, not as a forecast for "
         "you. A figure like 90% ED avoidance depends entirely on the denominator: "
         "which calls were counted, over what period, for what population. Ask "
         "any vendor, us included, to define the denominator before you carry a "
         "percentage into your own model.</p>"),
        ("Do we need patient transfer coordination?",
         "<p>If you are a health system moving patients between facilities, quite "
         "possibly, and that is a genuine reason to choose Conduit over us. If you are "
         "a hospice, home health agency, or health center, it is likely solving a "
         "problem you do not have.</p>"),
        ("Which is better for an FQHC?",
         "<p>Both target the segment. Conduit has the operating history; we price flat "
         "for safety-net budgets and have written up the "
         "<a href=\"/resources/apcm-billing-fqhc-rhc\">APCM</a> and "
         "<a href=\"/for/health-centers\">rural coverage</a> angles specifically. Get "
         "quotes from both and compare the escalation design as closely as the "
         "price.</p>"),
    ]

    return _compare(
        slug="conduit-health-partners-alternative",
        competitor="Conduit Health Partners",
        title="Conduit Health Partners Alternative | TULQ",
        description=(
            "How TULQ compares with Conduit Health Partners on triage model, buyer "
            "focus, transfer services, and published outcome data, and when to choose "
            "Conduit."
        ),
        h1="A <em>Conduit Health Partners</em> alternative.",
        deck=(
            "Conduit pairs nurse-first triage with patient transfer coordination and "
            "publishes real outcome data. Here is where the two of us actually differ."
        ),
        profile=profile,
        table_rows=rows,
        when_them=[
            "You need patient transfer coordination alongside triage; we do not "
            "offer it.",
            "You are a health system or health plan, which is where their buyer "
            "segmentation is strongest.",
            "Published case-study outcome data is a required evaluation factor.",
        ],
        when_us=[
            "You are a tribal health program, IHS facility, or Urban Indian "
            "Organization.",
            "You are a hospice or home health agency and want a vendor whose whole "
            "focus is first-call triage rather than a broader service line.",
            "Flat monthly pricing matters more to you than a broader product suite.",
        ],
        qa=qa,
        sources=[
            ("Conduit Health Partners public website, case studies, and news materials.",
             "https://conduithp.com/"),
            ("Schmitt-Thompson telephone triage protocols.",
             "https://www.stcc-triage.com/"),
        ],
    )


def compare_accessnurse() -> Page:
    profile = """    <p>AccessNurse has been in business since 1996 and serves a large provider base
    (more than 20,000 providers by its own account), including health
    systems, universities, and community health centers.</p>

    <h2>What AccessNurse is</h2>

    <p>Its architecture is organized around vertical landing pages by specialty, with
    dedicated offerings for pediatrics, OB, community health centers, and physician
    practices. It reports licensure across all 50 states, which is a meaningful
    operational fact for any multi-state organization.</p>

    <p>Of the established vendors, AccessNurse is the closest analog to our
    safety-net positioning: it explicitly markets to community health centers. The
    difference is that its community health center offering is one vertical among many,
    while the rural safety net is one of two things we are built for.</p>"""

    rows = """          <tr><td>Founded</td><td>1996</td><td>Launching 2026</td></tr>
          <tr><td>Provider base</td><td class="tick">20,000+ providers, per its own reporting</td><td class="cross">Pre-launch</td></tr>
          <tr><td>Licensed RNs on first call</td><td class="tick">Yes</td><td class="tick">Yes</td></tr>
          <tr><td>Multi-state licensure</td><td class="tick">All 50 states</td><td>Scoped to each engagement's service area</td></tr>
          <tr><td>Specialty verticals</td><td class="tick">Pediatrics, OB, CHCs, physician practices</td><td>Hospice, home health, FQHC/RHC/CAH</td></tr>
          <tr><td>Community health center focus</td><td class="tick">One vertical among many</td><td class="tick">A core segment</td></tr>
          <tr><td>Tribal / IHS specialization</td><td class="cross">None published</td><td class="tick">A dedicated site and practice</td></tr>
          <tr><td>Pricing structure</td><td>Quoted on scope</td><td>Flat monthly, quoted on scope</td></tr>"""

    qa = [
        ("Is 50-state licensure a reason to choose AccessNurse?",
         "<p>If you operate across many states, it is a real advantage and a fair "
         "reason to pick them. We scope licensure to the service area of each "
         "engagement, which suits a single-state or regional organization and is a "
         "constraint for a national one. Ask us directly about your specific "
         "footprint.</p>"),
        ("We're an FQHC. Which is the better fit?",
         "<p>AccessNurse has the operating history and an established community health "
         "center vertical. We are betting on flat pricing built for safety-net budgets, "
         "and on writing seriously about the "
         "<a href=\"/resources/apcm-billing-fqhc-rhc\">reimbursement</a> and "
         "<a href=\"/for/health-centers\">rural coverage</a> questions that segment "
         "actually asks. Get both quotes.</p>"),
        ("Do you serve pediatric or OB practices?",
         "<p>Not as a dedicated vertical today. If you need a triage service built "
         "specifically around pediatric or OB protocols and call patterns, AccessNurse "
         "has a purpose-built offering and we would point you there.</p>"),
    ]

    return _compare(
        slug="accessnurse-alternative",
        competitor="AccessNurse",
        title="AccessNurse Alternative for Health Centers | TULQ",
        description=(
            "How TULQ compares with AccessNurse on licensure coverage, specialty "
            "verticals, community health center focus, and pricing, and when to choose "
            "AccessNurse."
        ),
        h1="An <em>AccessNurse</em> alternative.",
        deck=(
            "AccessNurse has served providers since 1996 and markets directly to "
            "community health centers, the closest analog to our safety-net "
            "positioning. Here is the honest difference."
        ),
        profile=profile,
        table_rows=rows,
        when_them=[
            "You operate across many states and need broad multi-state licensure "
            "already in place.",
            "You need a pediatric or OB-specific triage vertical.",
            "A long operating history and a large reference base are required "
            "evaluation factors.",
        ],
        when_us=[
            "You are a tribal health program, IHS facility, or Urban Indian "
            "Organization.",
            "You are a single-state or regional safety-net facility and want flat "
            "pricing built for that budget.",
            "You want a vendor for whom the rural safety net is a core segment rather "
            "than one vertical among many.",
        ],
        qa=qa,
        sources=[
            ("AccessNurse public website and published materials.",
             "https://www.accessnurse.com/"),
            ("Schmitt-Thompson telephone triage protocols.",
             "https://www.stcc-triage.com/"),
        ],
    )


def compare_pages() -> list[Page]:
    return [
        compare_intellatriage(),
        compare_conduit(),
        compare_accessnurse(),
        compare_chartspan(),
        compare_signallamp(),
        compare_thoroughcare(),
    ]


# ══════════════════════════════════════════════════════════════════════
# Care management comparisons.
#
# These three are a different competitive set from the triage comparisons
# above: ChartSpan and Signallamp sell nurse labour, ThoroughCare sells
# software. The research is explicit that "ChartSpan alternatives" and
# "chronic care management vendor comparison" are elite-intent, low-volume,
# near-zero-competition terms, and that a new domain wins on tightly-scoped
# intent match rather than on authority.
#
# House rule, and it matters most here: describe each competitor from its
# own public materials, and say plainly when the reader should pick them
# instead. Every one of these three is a better answer than TULQ for some
# real buyer, and the pages say so.
# ══════════════════════════════════════════════════════════════════════

def compare_chartspan() -> Page:
    profile = """    <p>ChartSpan describes itself as the largest full-service chronic care
    management organization in the United States, and on the evidence of its own
    published materials that is a fair claim. If you are shortlisting outsourced care
    management, it belongs on the list.</p>

    <h2>What ChartSpan is</h2>

    <p>Per its own site, ChartSpan runs a "proactive, full-service Chronic Care
    Management (CCM) program" in which it handles "patient enrollment, education, care
    plans, prescription refills, and more." The operating model is explicit: ChartSpan
    identifies eligible patients, the practice approves the eligibility list, and
    ChartSpan enrols and then contacts them monthly. Its RapidBill technology is
    described as letting a practice "review and bill under general supervision with
    ease."</p>

    <p>It publishes real proof: named client testimonials from billing managers, quality
    directors, and care coordinators, a figure of more than $100,000 generated annually
    at 300 enrolled patients, and average managed-program growth of 3 percent a month.
    It also bundles MIPS and quality improvement services and ten years of record
    archiving.</p>

    <p>That is a mature, well-resourced operation with a decade of references. Nothing
    on this page is an argument that it is not.</p>"""

    rows = """          <tr><td>Model</td><td>Full-service outsourced CCM at national scale</td><td>Nurse staffing for care management, triage, and wellness visits</td></tr>
          <tr><td>Operating history</td><td class="tick">Established, with named client references</td><td class="cross">Launching 2026, no references at scale</td></tr>
          <tr><td>Enrollment</td><td class="tick">ChartSpan identifies and enrols; you approve the list</td><td>We enrol against the list you approve, same shape</td></tr>
          <tr><td>Where the note lives</td><td>ChartSpan platform, with billing review tooling</td><td class="tick">Your own record, under a signed BAA</td></tr>
          <tr><td>Programs covered</td><td class="tick">CCM, APCM, wellness visits, quality programs</td><td>CCM, APCM, PCM, TCM, wellness visits, plus after-hours triage</td></tr>
          <tr><td>After-hours nurse triage</td><td>A 24/7 care team inside the CCM program</td><td class="tick">A standalone triage service on Schmitt-Thompson protocols</td></tr>
          <tr><td>Quality and MIPS support</td><td class="tick">Included</td><td class="cross">Not offered</td></tr>
          <tr><td>Typical customer</td><td>Practices and health systems of scale</td><td>Small, rural, and independent practices</td></tr>
          <tr><td>Published pricing</td><td class="cross">Not published</td><td>Flat fee per enrolled patient, quoted on scope</td></tr>"""

    qa = [
        ("Is TULQ cheaper than ChartSpan?",
         "<p>We do not know, and neither does anyone who has not seen both quotes. "
         "Neither company publishes pricing. What we will tell you is the structure: our "
         "fee is flat per enrolled patient per month, never a share of your collections, "
         "and our nurses are never paid per enrollment. Get numbers from both and compare "
         "the structure, not just the total.</p>"),
        ("ChartSpan has a decade of references and you have none. Why would we risk it?",
         "<p>Often you should not, and if a multi-year track record is a hard requirement "
         "then ChartSpan is the better answer and we would rather you knew that now. The "
         "risk is real and the mitigations are contractual: a fifty-patient pilot over "
         "ninety days, service levels with teeth, and termination provisions you can live "
         "with. Ask us for all three.</p>"),
        ("What can a smaller vendor actually do better?",
         "<p>Continuity, and scope. A full-service program at national scale means a "
         "larger pool of coordinators; that is what makes the enrollment volume possible "
         "and it is genuinely valuable. The trade is that a patient is less likely to "
         "hear the same voice each month. We staff a designated team per practice, which "
         "is one of the thirteen program requirements rather than a marketing "
         "preference. Separately, we are one vendor for care management, wellness visits, "
         "and the after-hours line, rather than a care management program plus a "
         "separate answering service.</p>"),
    ]

    return _compare(
        slug="chartspan-alternative",
        competitor="ChartSpan",
        title="ChartSpan Alternative: Nurse-Led Care Management | TULQ",
        description=(
            "An honest ChartSpan comparison for small and rural practices: full-service "
            "scale against a designated nurse team working inside your own record."
        ),
        h1="A ChartSpan alternative, <em>for the small practice.</em>",
        deck=(
            "ChartSpan is the largest full-service chronic care management organization "
            "in the country. Here is what it does well, where a smaller nurse-led model "
            "differs, and when you should pick them instead."
        ),
        profile=profile,
        table_rows=rows,
        when_them=[
            "You want a proven operator with a decade of named client references, and a "
            "track record is a hard requirement.",
            "You want MIPS and quality improvement services bundled with the care "
            "management program.",
            "You are large enough that enrollment volume matters more than a patient "
            "hearing the same nurse each month.",
            "You want one vendor to run enrollment at scale and are comfortable with the "
            "documentation living on their platform.",
        ],
        when_us=[
            "You are a small, rural, or independent practice and every national quote you "
            "have had assumed a panel you do not have.",
            "You want the note in your own record under a signed business associate "
            "agreement, not exported from somewhere else.",
            "You want the same nursing team covering care management, wellness visits, "
            "and the after-hours line rather than three arrangements.",
            "You want a flat fee per enrolled patient, never a percentage of your "
            "collections.",
        ],
        qa=qa,
        questions=CARE_QUESTIONS,
        sources=[
            ("ChartSpan, Chronic Care Management solution page.",
             "https://www.chartspan.com/chronic-care-management/"),
            ("ChartSpan homepage.", "https://www.chartspan.com/"),
            ("CMS, Advanced Primary Care Management services.",
             "https://www.cms.gov/medicare/payment/fee-schedules/physician-fee-schedule/advanced-primary-care-management-services"),
            ("CMS, Chronic Care Management Services booklet, MLN909188.",
             "https://www.cms.gov/files/document/chroniccaremanagement.pdf"),
        ],
    )


def compare_signallamp() -> Page:
    profile = """    <p>Signallamp Health is the closest thing to a direct analogue of the TULQ
    care management model that we are aware of: real nurses, embedded remotely, working
    inside the client's own electronic health record rather than selling a platform. If
    you like our model, you should look at theirs.</p>

    <h2>What Signallamp is</h2>

    <p>Per its own published materials, Signallamp describes "remotely-embedded care
    management" delivered by nurses who are "100% U.S.-based and licensed in the same
    state as your patients," with the emphatic addition: "No call centers!" It
    highlights nurses who "operate directly in your own EHR," with no additional
    software, integrations, or workflow changes, and a four to six week launch.</p>

    <p>Its published client list leans to health systems and large groups, including
    UPMC, Temple Health, and Tampa General Hospital, and it publishes outcome figures
    including a 63 percent reduction in emergency department utilization and better than
    90 percent patient retention.</p>

    <p>One thing a buyer should know before shortlisting: Signallamp Health has become
    part of Tellihealth, and its chronic care management service now runs as signalCCM,
    powered by Tellihealth. That is not a criticism, but continuity of team and contract
    through a transition is a fair question to ask, and you should ask it.</p>"""

    rows = """          <tr><td>Model</td><td>Remotely-embedded nurses, no software sold</td><td class="tick">The same model</td></tr>
          <tr><td>Nurses work in your EHR</td><td class="tick">Yes</td><td class="tick">Yes</td></tr>
          <tr><td>State-licensed to the patient</td><td class="tick">Yes</td><td class="tick">Yes, compact plus single-state where needed</td></tr>
          <tr><td>How the vendor is paid</td><td>Described as a revenue-share against existing CPT codes</td><td class="tick">Flat fee per enrolled patient, never a percentage</td></tr>
          <tr><td>Typical customer</td><td>Health systems and large groups</td><td class="tick">Small, rural, and independent practices</td></tr>
          <tr><td>Operating history</td><td class="tick">Established, with published outcome data</td><td class="cross">Launching 2026</td></tr>
          <tr><td>Corporate status</td><td>Now part of Tellihealth; CCM runs as signalCCM</td><td>Independent, nurse-led</td></tr>
          <tr><td>After-hours nurse triage</td><td class="cross">Not the core offering</td><td class="tick">A standalone service on Schmitt-Thompson protocols</td></tr>
          <tr><td>Annual wellness visits</td><td class="cross">Not published as a service line</td><td class="tick">Telephone AWVs, priced per completed visit</td></tr>"""

    qa = [
        ("What is actually different, if the model is the same?",
         "<p>Two things. Size of customer, and how the vendor gets paid.</p>"
         "<p>Signallamp's published references are health systems and large groups. We "
         "are built for the practice with a few hundred Medicare patients that every "
         "national quote has treated as too small to bother with.</p>"
         "<p>The second is the one worth arguing about. A revenue-share ties the vendor's "
         "pay to your Medicare reimbursement. We charge a flat fee per enrolled patient "
         "instead, and our nurses are never paid per enrollment, because tying vendor "
         "compensation to the volume or value of federal healthcare business is precisely "
         "the arrangement that draws scrutiny. Reasonable people structure this "
         "differently and a revenue-share is not unlawful, but you should understand "
         "which one you are signing.</p>"),
        ("Does a revenue-share not align our incentives better?",
         "<p>It aligns them toward enrollment, which is not always the same as toward the "
         "patient. Our answer is to be month to month after an initial term: if patients "
         "are not actually enrolled and actually managed, you stop paying us. That gives "
         "you the same alignment without tying our fee to your Medicare receipts.</p>"),
        ("They publish a 63 percent reduction in ED utilization. What do you publish?",
         "<p>Nothing, because we have nothing yet. TULQ is launching in 2026, and "
         "borrowing an industry figure to imply it is ours would be the first dishonest "
         "thing on this site. If published outcome data is what decides your evaluation, "
         "that is a real point in their favour and you should weigh it.</p>"),
    ]

    return _compare(
        slug="signallamp-alternative",
        competitor="Signallamp",
        title="Signallamp Alternative: Flat-Fee Care Management | TULQ",
        description=(
            "Signallamp and TULQ run the same embedded-nurse model. The differences are "
            "customer size and how the vendor gets paid: revenue share against flat fee."
        ),
        h1="A Signallamp alternative, <em>on a flat fee.</em>",
        deck=(
            "Signallamp Health, now part of Tellihealth, runs the closest model to ours: "
            "real nurses, embedded remotely, working in your own record. Two things "
            "differ, and one of them is how the vendor gets paid."
        ),
        profile=profile,
        table_rows=rows,
        when_them=[
            "You are a health system or a large group, which is where their published "
            "references sit.",
            "Published outcome data matters to your evaluation, and a vendor with none is "
            "disqualifying.",
            "A revenue-share suits your finance team better than a per-patient fee, and "
            "you have taken your own view on the compliance posture.",
            "You want remote patient monitoring devices alongside care management, which "
            "the Tellihealth platform offers and we do not.",
        ],
        when_us=[
            "You are small, rural, or independent, and national vendors have quoted you a "
            "floor you will never reach.",
            "You want a flat fee per enrolled patient rather than a share of your "
            "Medicare collections.",
            "You want after-hours triage and annual wellness visits from the same nursing "
            "team, not just care management.",
            "You would rather contract with an independent nurse-led company than with a "
            "brand mid-transition.",
        ],
        qa=qa,
        questions=CARE_QUESTIONS,
        sources=[
            ("Signallamp Health.", "https://www.signallamphealth.com/"),
            ("Tellihealth.", "https://www.tellihealth.com/"),
            ("CMS, Care Management, Physician Fee Schedule.",
             "https://www.cms.gov/medicare/payment/fee-schedules/physician/care-management"),
        ],
    )


def compare_thoroughcare() -> Page:
    profile = """    <p>ThoroughCare is the comparison most likely to be a category error, and it
    is worth resolving early: ThoroughCare principally sells software, and TULQ sells
    nurses. If your problem is that your care coordinators lack a good tool, we are not
    the answer. If your problem is that you have no care coordinators, a tool will not
    fix it.</p>

    <h2>What ThoroughCare is</h2>

    <p>Per its own materials, ThoroughCare is "a platform built by clinicians, helping
    providers engage patients," covering chronic care management, remote patient
    monitoring, annual wellness visits, behavioral health integration, principal care
    management, transitional care management, advanced primary care management, and
    advance care planning. It states that its platform is "NCQA Prevalidated for
    Population Health Management in Health Plan Accreditation."</p>

    <p>It is not purely software: it offers a clinical advisory team for workflow design,
    training, documentation review, and compliance support, and it has built AI features
    and a patient education integration. Its content library on CPT and reimbursement is
    among the deepest in the category and is genuinely useful reading, whoever you end up
    buying from.</p>

    <p>If you already employ the staff, ThoroughCare is a strong choice and this page is
    not an argument otherwise.</p>"""

    rows = """          <tr><td>What you are buying</td><td>A care coordination platform, plus advisory services</td><td class="tick">Licensed nurses who do the clinical work</td></tr>
          <tr><td>Who makes the calls</td><td class="cross">Your staff</td><td class="tick">Our nurses</td></tr>
          <tr><td>Who documents the time</td><td>Your staff, in the platform</td><td class="tick">Our nurses, in your record</td></tr>
          <tr><td>Programs supported</td><td class="tick">CCM, RPM, AWV, BHI, PCM, TCM, APCM, ACP</td><td>CCM, APCM, PCM, TCM, AWV, plus after-hours triage</td></tr>
          <tr><td>Remote patient monitoring</td><td class="tick">Supported</td><td class="cross">Not offered</td></tr>
          <tr><td>NCQA prevalidation</td><td class="tick">Stated for population health management</td><td class="cross">Not applicable, we are not a platform</td></tr>
          <tr><td>Software to buy</td><td>Yes, that is the product</td><td class="tick">None</td></tr>
          <tr><td>Solves a staffing shortage</td><td class="cross">No</td><td class="tick">Yes, that is the product</td></tr>
          <tr><td>Works alongside the other</td><td class="tick">Yes</td><td class="tick">Yes, our nurses will work in a platform you own</td></tr>"""

    qa = [
        ("Do we need both?",
         "<p>Sometimes, and there is no conflict. If you have already bought "
         "ThoroughCare and the problem is that nobody has time to use it, our nurses will "
         "work inside it. We do not require you to abandon a platform you have paid for "
         "and trained on, and we do not sell a competing one.</p>"),
        ("Which one is cheaper?",
         "<p>Software is almost always the cheaper line item, because it is not paying "
         "anybody's salary. The comparison only becomes fair when you add the loaded cost "
         "of the clinical staff time the platform assumes you have. At 200 enrolled "
         "patients, twenty tracked minutes each is roughly 67 hours a month. Price the "
         "software against the software, and the nurse against the nurse.</p>"),
        ("Is a platform better for audit defence?",
         "<p>A good platform makes time-logging consistent, which genuinely helps. But "
         "insufficient time documentation is the most common denial in this benefit, and "
         "the failure is nearly always that the work did not happen or was not recorded "
         "at the time, not that the recording tool was inadequate. A tool cannot document "
         "a call nobody made.</p>"),
    ]

    return _compare(
        slug="thoroughcare-alternative",
        competitor="ThoroughCare",
        title="ThoroughCare Alternative: Nurses, Not Software | TULQ",
        description=(
            "ThoroughCare sells a care coordination platform. TULQ sells the nurses. "
            "Which one you need depends on whether you have the staff or only the tool."
        ),
        h1="A ThoroughCare alternative, <em>if the gap is staff.</em>",
        deck=(
            "ThoroughCare sells a care coordination platform and TULQ sells licensed "
            "nurses. They are not really substitutes, and knowing which problem you have "
            "decides it in about a minute."
        ),
        profile=profile,
        table_rows=rows,
        when_them=[
            "You already employ care coordinators and what they lack is a good tool.",
            "You want remote patient monitoring in the same system as care management.",
            "NCQA prevalidation for population health management matters to your "
            "accreditation work.",
            "You want to own the workflow and keep the clinical work in-house.",
        ],
        when_us=[
            "Your care management program keeps stalling because nobody has the hours, "
            "not because the software is bad.",
            "You would rather buy the clinical time than hire, train, and cover for a "
            "care coordinator.",
            "You want the same nurses covering after-hours triage and wellness visits.",
            "You already own a platform and simply need somebody to work inside it.",
        ],
        qa=qa,
        questions=CARE_QUESTIONS,
        sources=[
            ("ThoroughCare.", "https://www.thoroughcare.net/"),
            ("CMS, Chronic Care Management Services booklet, MLN909188.",
             "https://www.cms.gov/files/document/chroniccaremanagement.pdf"),
            ("CMS, Care Management, Physician Fee Schedule.",
             "https://www.cms.gov/medicare/payment/fee-schedules/physician/care-management"),
        ],
    )


def compare_index() -> Page:
    page = Page(
        site=SITE,
        slug="compare/index",
        title="Compare Nurse Triage &amp; Care Management Vendors | TULQ",
        description=(
            "Honest comparisons of the nurse triage and care management vendors: "
            "IntellaTriage, ChartSpan, Signallamp, ThoroughCare and more, including "
            "when to choose them."
        ),
        eyebrow="Compare",
        h1="Comparing <em>the vendors you are shortlisting.</em>",
        deck=(
            "Written by an interested party, which you should weigh accordingly. We "
            "have tried to make these useful by being specific about where the "
            "incumbents are the better choice."
        ),
        crumbs=[("Compare", "/compare/")],
        wide=True,
        priority="0.7",
        cta_title="Ask us the same six questions.",
        cta_body=(
            "Put the evaluation questions on these pages to every vendor on your list, "
            "including us, and compare the answers side by side."
        ),
    )

    page.body = f"""    <p>Two different markets are compared below, because TULQ sells into both.
    Outsourced nurse triage has perhaps five serious operators, most of them fifteen to
    thirty years old, plus a large field of medical answering services that are not
    clinical and should not be evaluated in the same category. Care management is a
    more crowded field of well-funded software platforms and full-service vendors.</p>

    <p>We are new. That is a real disadvantage on any comparison that weights operating
    history, and we have said so on every page below rather than burying it. What
    follows is our attempt at comparisons that are actually useful, which means
    telling you when to pick somebody else.</p>

    {card_grid([
        ("Category leader", "IntellaTriage alternative",
         "Founded 2008, 640,000+ calls in 2024. Where we differ, where we don't, and when to choose them.",
         "/compare/intellatriage-alternative"),
        ("Transfer services", "Conduit Health Partners alternative",
         "Nurse-first triage plus patient transfer coordination, with published outcome data.",
         "/compare/conduit-health-partners-alternative"),
        ("Health centers", "AccessNurse alternative",
         "In business since 1996, 50-state licensure, explicit community health center vertical.",
         "/compare/accessnurse-alternative"),
    ])}

    <h2>Care management vendors</h2>

    {card_grid([
        ("Full-service scale", "ChartSpan alternative",
         "The largest full-service CCM organization in the country. Scale and named references against a designated nurse team in your own record.",
         "/compare/chartspan-alternative"),
        ("The same model", "Signallamp alternative",
         "The closest analogue to how we work: embedded nurses, no software. The differences are customer size and revenue share against flat fee.",
         "/compare/signallamp-alternative"),
        ("Software, not staff", "ThoroughCare alternative",
         "A care coordination platform rather than a staffing company. Which you need depends on whether you have the people or only the tool.",
         "/compare/thoroughcare-alternative"),
    ])}

    <h2>Before you compare anyone</h2>

    <p>Two distinctions do more work than any vendor comparison. First, whether you are
    buying <a href="/resources/nurse-triage-vs-answering-service">nurse triage or an
    answering service</a>, they occupy the same slot and do different work.
    Second, what your current arrangement
    <a href="/resources/true-cost-of-after-hours-on-call">actually costs</a>, which
    most organizations have never totalled in one place.</p>

    <p>Sort those out and the vendor comparison gets considerably easier.</p>

    <h2>The six questions</h2>

    <ol>
      <li>Who answers the first call, and what licensure do they hold?</li>
      <li>What protocol standard do your nurses work from?</li>
      <li>What share of calls resolve without reaching our clinician?</li>
      <li>What does encounter documentation look like when it reaches us, in what
      format, and how quickly?</li>
      <li>Who defines the escalation rules: us or you?</li>
      <li>Is pricing per-call or flat, and what happens in a bad respiratory
      season?</li>
    </ol>

    {sources_block([
        "Vendor descriptions summarized from each company's own public website.",
    ], disclaimer=_COMPARE_DISCLAIMER)}"""

    return page
