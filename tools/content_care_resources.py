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
        post_cah(),
    ]


def resources_index() -> Page:
    page = Page(
        site=SITE,
        slug="resources/index",
        title="Resources: After-Hours Nurse Triage | TULQ",
        description=(
            "Explainers on what on-call really costs, nurse triage vs answering "
            "services, hospice CAHPS, HHVBP, APCM billing, and critical access hospital "
            "coverage."
        ),
        eyebrow="Resources",
        h1="The operational stuff, <em>written down.</em>",
        deck=(
            "What after-hours coverage costs, what it touches in your quality and "
            "reimbursement programs, and how to evaluate a vendor. Sourced, and honest "
            "about the limits."
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

    page.body = f"""    <h2>Cost and evaluation</h2>

    {card_grid([
        ("Cost &amp; ROI", "The true cost of after-hours on-call",
         "Direct pay is the smallest of four buckets. The whole calculation, including the line item that usually decides it.",
         "/resources/true-cost-of-after-hours-on-call"),
        ("Basics", "Nurse triage vs answering service",
         "They fill the same slot and do different work. The one question that exposes which you're being sold.",
         "/resources/nurse-triage-vs-answering-service"),
        ("Compare", "Comparing triage vendors",
         "IntellaTriage, Conduit, and AccessNurse: what each is built for, and when to pick them over us.",
         "/compare/"),
    ])}

    <h2>Quality programs and reimbursement</h2>

    {card_grid([
        ("CAHPS", "After-hours access and hospice CAHPS",
         "Which measures it moves, which it doesn't, and the operational proxies to track meanwhile.",
         "/resources/hospice-cahps-after-hours"),
        ("HHVBP", "HHVBP and ED use",
         "The CY2025 within-stay potentially preventable hospitalization measure, and the pathway triage interrupts.",
         "/resources/hhvbp-ed-use"),
        ("Reimbursement", "APCM billing at an FQHC or RHC",
         "G0556, G0557, G0558: what changed, who can bill, and where 24/7 access fits.",
         "/resources/apcm-billing-fqhc-rhc"),
    ])}

    <h2>By setting</h2>

    {card_grid([
        ("Rural hospitals", "After-hours coverage for critical access hospitals",
         "What the conditions of participation require, what they leave uncovered, and the staffing arithmetic.",
         "/resources/critical-access-hospital-after-hours"),
        ("Hospice &amp; home health", "After-hours triage for hospice and home health",
         "Why on-call rotations break, and what changes when a nurse takes first call.",
         "/for/home-health"),
        ("Safety net", "FQHC, RHC and CAH coverage",
         "The segment with the same obligation as everyone else and the least room to staff it.",
         "/for/health-centers"),
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


def _compare(slug: str, competitor: str, title: str, description: str,
             h1: str, deck: str, profile: str, table_rows: str,
             when_them: list[str], when_us: list[str],
             qa: list, sources: list[str]) -> Page:
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
      <li>Who answers the first call, and what licensure do they hold?</li>
      <li>What protocol standard do your nurses work from?</li>
      <li>What share of calls resolve without reaching our clinician?</li>
      <li>What does encounter documentation look like when it reaches us, in what
      format, and how quickly?</li>
      <li>Who defines the escalation rules: us or you?</li>
      <li>Is pricing per-call or flat, and what happens in a bad respiratory
      season?</li>
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
    return [compare_intellatriage(), compare_conduit(), compare_accessnurse()]


def compare_index() -> Page:
    page = Page(
        site=SITE,
        slug="compare/index",
        title="Compare Nurse Triage Companies | TULQ",
        description=(
            "Honest comparisons of the established nurse triage vendors ("
            "IntellaTriage, Conduit Health Partners, AccessNurse), including when to "
            "choose them over us."
        ),
        eyebrow="Compare",
        h1="Comparing <em>nurse triage vendors.</em>",
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

    page.body = f"""    <p>There are perhaps five serious operators in outsourced nurse triage, most of
    them fifteen to thirty years old, plus a large field of medical answering services
    that are not clinical and should not be evaluated in the same category.</p>

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
