#!/usr/bin/env python3
"""
The three tulqhealth.com service lines, plus the hub that holds them.

Architecture note, because this is the change that reshaped the site.

tulqhealth.com used to be one product: a 24/7 nurse triage line, argued on
the homepage, with four practice-type segment pages hanging off it. TULQ now
sells three things, and the Aug 2026 keyword research is unambiguous that
they need three separate money pages rather than one combined page: the
buyers differ, the SERPs differ, and the keyword sets barely overlap. Google
needs a distinct URL to rank for each intent.

    /services/                                  hub
    /services/after-hours-nurse-triage          Page A, best intent-to-difficulty
    /services/care-management                   Page C, biggest contract value
    /services/medicare-annual-wellness-visits   Page B, thinnest SERP, on-ramp to C

Build order in the research is triage, then care management, then AWV, on
the reasoning that triage has the most winnable SERP (owned by commercial
vendors, not CMS or associations) while "chronic care management companies"
is a mature listicle battlefield a new domain will not crack inside a year.

How this relates to the pages that already existed:

  * The homepage keeps the triage argument but its sub-head now covers all
    three lines. It routes to the hub instead of being the triage page.
  * The four segment pages (/nurse-triage-for-hospice, /for/home-health,
    /nurse-triage-for-rural-health-clinics, /for/health-centers) are
    practice-type modifiers on the triage service and are unchanged. Page A
    targets the unmodified head term and links down to them. It must not
    start covering hospice or RHC specifics, or it will cannibalise them.
  * /resources/apcm-billing-fqhc-rhc already owns the RHC and FQHC APCM
    billing query. Page C links across to it rather than re-arguing it.

Reimbursement figures. Every dollar amount here is a 2026 national average
under the Medicare Physician Fee Schedule and is adjusted by locality, so
each one is labelled as such on-page and sits next to a link to the CMS fee
schedule lookup. TULQ is pre-launch: no page claims a call volume, an answer
time, an uptime figure, or a client reference, because it does not have one
yet. The comparison sections name competitors from their own public
materials and say plainly when a reader should pick them instead.
"""

from __future__ import annotations

from landing import (
    LandingPage, band, breadcrumb_node, compare_table, contact_close, crumbs,
    faq, faq_node, ledger, note, numbers, pillars, prose, routes,
    section_links, serve_cards, service_node, source_link, sources, split,
)
from pagekit import CARE

SITE = CARE

# ── Shared source URLs. Every one of these has been requested and returns
#    200; see the house rule in CLAUDE.md. Prefer the primary document over
#    a summary of it, which is why these are CMS, eCFR, and NCSBN rather
#    than vendor blogs, even where a vendor blog explains it more nicely.
PFS_LOOKUP = "https://www.cms.gov/medicare/physician-fee-schedule/search"
CMS_APCM = ("https://www.cms.gov/medicare/payment/fee-schedules/"
            "physician-fee-schedule/advanced-primary-care-management-services")
CMS_APCM_FAQ = ("https://www.cms.gov/files/document/"
                "advanced-primary-care-management-apcm-services-faq.pdf")
CMS_CARE_MGMT = "https://www.cms.gov/medicare/payment/fee-schedules/physician/care-management"
CMS_CCM_BOOKLET = "https://www.cms.gov/files/document/chroniccaremanagement.pdf"
CMS_RHC_MLN = "https://www.cms.gov/files/document/mln006398-information-rural-health-clinics.pdf"
CMS_AWV_MLN = ("https://www.cms.gov/outreach-and-education/medicare-learning-network-mln/"
               "mlnproducts/mln-publications/mln6775421")
CMS_TELEHEALTH = "https://www.cms.gov/medicare/coverage/telehealth"
ECFR_AWV = ("https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/"
            "part-410/subpart-B/section-410.15")
MEDICARE_AWV = "https://www.medicare.gov/coverage/yearly-wellness-visits"
NCSBN_NLC = "https://www.ncsbn.org/nurse-licensure-compact.htm"
AAACN = "https://www.aaacn.org/telehealth-nursing-practice"
KFF_ED = ("https://www.healthsystemtracker.org/brief/emergency-department-visits-"
          "exceed-affordability-thresholds-for-many-consumers-with-private-insurance/")

RATES_NOTE = (
    "Payment amounts on this page are 2026 national averages under the Medicare "
    "Physician Fee Schedule. They are adjusted by locality and updated each January, "
    'so check the <a href="' + PFS_LOOKUP + '" target="_blank" rel="noopener">CMS fee '
    "schedule lookup</a> for your own carrier before modelling on them. Nothing here "
    "is billing, coding, or legal advice for your practice."
)


# ══════════════════════════════════════════════════════════════════════
# HUB  /services/
# ══════════════════════════════════════════════════════════════════════

def services_hub() -> LandingPage:
    page = LandingPage(
        site=SITE,
        slug="services/index",
        title="Nurse-Led Clinical Services for Practices | TULQ",
        description=(
            "Licensed RNs who run your after-hours triage line, your Medicare care "
            "management program, and your annual wellness visits. See what each costs."
        ),
        h1="Three services. <em>One nursing team.</em>",
        hero_sub=(
            "TULQ supplies licensed registered nurses to independent practices, health "
            "centers, and agencies: after-hours triage, Medicare care management, and "
            "annual wellness visits."
        ),
        hero_eyebrow="What we do",
        hero_facts=("Licensed RNs", "Compact-licensed, national coverage", "Flat monthly pricing"),
        hero_scene="pines",
        hero_ctas=(
            '<a class="btn btn-primary" href="/contact" data-magnetic>Book a 15 minute call'
            '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">'
            '<path d="M3 7h8m0 0L7.5 3.5M11 7l-3.5 3.5" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
            '<a class="btn btn-ghost" href="#lines">See the three lines</a>'
        ),
        priority="0.9",
        reviewed=True,
    )
    trail = [("Services", "/services/")]

    page.sections = [
        crumbs(trail),

        band(
            prose(
                "      <p>Every one of these services is the same underlying thing: a licensed "
                "registered nurse doing clinical work your practice cannot staff, documented "
                "well enough to bill or to survive a survey. What changes between them is who "
                "pays and what the documentation has to prove.</p>\n"
                "      <p>We sell nurse labour, not software. There is no platform to buy, no "
                "per-seat licence, and no percentage of your collections. You keep the billing, "
                "the chart, and the patient relationship in every one of the three.</p>"
            ),
            eyebrow="The premise",
            h2="We are the staffing, not the software.",
            scene="premise",
        ),

        band(
            serve_cards([
                {
                    "title": "After-hours nurse triage.",
                    "body": "A licensed RN answers the after-hours call, assesses against "
                            "Schmitt-Thompson protocols, makes a disposition, and documents it "
                            "back to you. Replaces the provider's personal cell phone and the "
                            "answering service that only takes a message.",
                    "tag": "Flat monthly subscription",
                    "href": "/services/after-hours-nurse-triage",
                    "link_label": "See how triage works",
                },
                {
                    "title": "Medicare care management.",
                    "body": "CCM, APCM, PCM, and TCM run by remote RNs inside your chart. "
                            "Medicare pays your practice every month for work your staff is "
                            "probably already doing for free. We supply the clinical hours and "
                            "the documentation that makes it billable.",
                    "tag": "Per enrolled patient, per month",
                    "href": "/services/care-management",
                    "link_label": "See the care management model",
                },
                {
                    "title": "Medicare annual wellness visits.",
                    "body": "Compact-licensed RNs complete the AWV by phone and return finished "
                            "documentation to your clinic. Priced per completed visit, which "
                            "closes the completion gap without adding a room or a shift.",
                    "tag": "Per completed visit",
                    "href": "/services/medicare-annual-wellness-visits",
                    "link_label": "See the AWV model",
                },
            ]),
            dark=True,
            anchor="lines",
            eyebrow="The three lines",
            h2="Pick the one that is <em>costing you the most.</em>",
            deck="Most practices start with one and add the second within a year, because the "
                 "same nurses do all three and the wellness visit is what makes a patient "
                 "eligible for care management in the first place.",
            scene="totem",
        ),

        band(
            prose(
                "      <p>They compound, and the order matters. An annual wellness visit is a "
                "qualifying visit for care management enrolment, so the AWV is the on-ramp: it "
                "is the appointment where a nurse has twenty unhurried minutes, discovers the "
                "chronic conditions, and gets consent while the patient is already engaged.</p>\n"
                "      <p>Care management then requires 24 hour access to a care team member "
                "for urgent needs. That is a triage requirement, and it is one of the thirteen "
                "obligations that quietly kills care management programs run on a physician's "
                "cell phone. If you already have the triage line, you have already satisfied "
                "it.</p>\n"
                "      <p>Run all three and the same nurses who know your protocols at 2 a.m. "
                "are the ones calling your diabetic patients on the fifteenth of the month. "
                "That continuity is the part a call center cannot sell you.</p>"
            ),
            eyebrow="How they fit together",
            h2="The wellness visit enrolls. Care management retains. Triage covers the night.",
            scene="why",
        ),

        band(
            routes(
                "Read the page written for <em>your organization.</em>",
                "The triage service has four practice-type pages under it, each covering the "
                "rule you are actually held to and what a surveyor asks for.",
                [
                    {"tag": "42 CFR 418.100(c)", "title": "Hospice",
                     "desc": "The 24-hour nurse Condition of Participation, and how after-hours "
                             "calls get documented back to the IDG.",
                     "href": "/nurse-triage-for-hospice"},
                    {"tag": "42 CFR 484 · HHVBP", "title": "Home health",
                     "desc": "Keeping the on-call field nurse asleep, and what triage does to "
                             "the acute-care utilization measure your HHVBP score rides on.",
                     "href": "/for/home-health"},
                    {"tag": "HRSA Chapter 7", "title": "FQHC &amp; health centers",
                     "desc": "Demonstrating after-hours coverage for Health Center Program "
                             "compliance, with documentation that lands in your EHR.",
                     "href": "/for/health-centers"},
                    {"tag": "42 CFR 491 · 42 CFR 485 F", "title": "Rural health clinics",
                     "desc": "RHCs and critical access hospitals carrying a 24/7 obligation "
                             "without a clinician on-site overnight.",
                     "href": "/nurse-triage-for-rural-health-clinics"},
                ],
            ) + "\n" + section_links([
                ("Run the AWV revenue numbers", "/tools/awv-revenue-calculator"),
                ("Compare triage vendors", "/compare/"),
                ("Resources and reimbursement guides", "/resources/"),
            ]),
            dark=True,
            eyebrow="By organization",
            h2="Four practice types, four pages.",
            scene="pines",
        ),

        contact_close(
            "Fifteen minutes, your real numbers.",
            "Bring your Medicare patient count and your after-hours call volume. We will tell "
            "you what each line is worth at your locality, what it costs, and which of the "
            "three to start with. Sometimes the answer is none of them yet.",
            cap_title="Capability &amp; compliance",
            cap_body="Service scope, supervision model, and sample documentation on request.",
        ),
    ]

    page.schema = [
        breadcrumb_node(page, trail),
        service_node(
            page,
            "Nurse-led outsourced clinical services",
            "Clinical staffing",
            "Licensed registered nurses supplied to physician practices, health centers, and "
            "agencies for after-hours nurse triage, Medicare care management, and annual "
            "wellness visits.",
            audience="Physician practices, federally qualified health centers, rural health "
                     "clinics, hospices, and home health agencies",
            offers=[
                {"name": "After-hours nurse triage",
                 "description": "24/7 licensed-RN telephone triage on Schmitt-Thompson protocols."},
                {"name": "Medicare care management",
                 "description": "CCM, APCM, PCM, and TCM delivered by remote registered nurses."},
                {"name": "Medicare annual wellness visits",
                 "description": "Telephone AWVs completed by compact-licensed registered nurses."},
            ],
        ),
    ]
    return page


# ══════════════════════════════════════════════════════════════════════
# PAGE A  /services/after-hours-nurse-triage
# Primary: after hours nurse triage service
# ══════════════════════════════════════════════════════════════════════

def page_triage() -> LandingPage:
    qa = [
        ("How much does an after-hours nurse triage service cost?",
         "<p>Most services price one of two ways. Per-call pricing looks cheap until a bad "
         "night, and medical answering services commonly quote per minute, which means a long "
         "clinical call costs you more precisely when it mattered most. TULQ prices a flat "
         "monthly subscription based on your call volume band and coverage window, so the "
         "number does not move when a patient has a hard week.</p>"
         "<p>The figure worth putting next to it is the avoided cost. The Peterson-KFF Health "
         "System Tracker puts the average emergency department visit at roughly "
         "<strong>$2,453</strong>. A single avoided, genuinely unnecessary ED visit covers a "
         "meaningful share of a month of coverage.</p>"
         + source_link("Peterson-KFF Health System Tracker", KFF_ED)),

        ("What is the difference between a nurse triage line and an answering service?",
         "<p>An answering service takes a message. The person on the phone is not a clinician, "
         "cannot assess a symptom, and cannot make a care decision, so every call that matters "
         "gets forwarded to whoever is on call, at whatever hour it arrives.</p>"
         "<p>Nurse triage puts a licensed registered nurse on the first call. The nurse assesses "
         "the caller against physician-authored protocols, reaches a disposition, documents the "
         "encounter, and escalates to your on-call clinician only when the protocol calls for "
         "it. The clinical difference is the disposition. The operational difference is how "
         "many times your staff gets woken up.</p>"
         + source_link("AAACN telehealth nursing standards", AAACN)),

        ("Who answers the calls, a nurse or an operator?",
         "<p>A licensed registered nurse owns every disposition. If we ever put a clerical "
         "front door in front of the queue to collect a name and a callback number, it is "
         "clerical only: it does not assess, it does not advise, and it does not decide. No "
         "automated system and no non-clinical operator triages a TULQ call.</p>"),

        ("What protocols do your nurses use?",
         "<p>Schmitt-Thompson, the physician-authored protocol framework used by the large "
         "majority of medical call centers in the United States. Your medical director reviews "
         "and signs off on the protocol set before we take a call, and can adjust dispositions "
         "where your practice has a standing preference.</p>"),

        ("How do you document each call back to our EHR?",
         "<p>Every call produces a dated encounter note: who called, what was assessed, which "
         "protocol was used, the disposition reached, the advice given, and any escalation. "
         "Where you can grant delegated access we document directly in your record under a "
         "signed business associate agreement. Where you cannot, the note is returned to you "
         "on an agreed schedule with a morning report waiting when you open.</p>"),

        ("Can one service cover a very low call volume practice affordably?",
         "<p>That is the case most vendors handle badly, and it is the one we were built for. "
         "A small practice may take four calls a month and still be obligated to have a nurse "
         "reachable for all seven hundred and thirty hours of it. Because our nurses cover a "
         "pool of practices rather than sitting idle on yours, low volume is priced as low "
         "volume instead of as an enterprise contract with a floor you will never reach.</p>"),

        ("Are your nurses licensed in our state?",
         "<p>Nursing licensure follows the patient's location, not the nurse's. Our nurses hold "
         "multistate licenses under the Nurse Licensure Compact, plus single-state licenses "
         "where a state is not a compact member. We confirm coverage for your state before we "
         "quote you, and we will tell you if we cannot cover it yet.</p>"
         + source_link("NCSBN Nurse Licensure Compact", NCSBN_NLC)),

        ("Can nurse triage be billed to Medicare?",
         "<p>No, and you should be sceptical of anyone who says otherwise. Telephone triage "
         "calls have no separately payable code in traditional Medicare, so the line is a "
         "practice expense, not a revenue line. It is worth paying for because it satisfies a "
         "requirement you already carry, it keeps your providers asleep, and every avoided "
         "emergency visit protects your shared savings. Care management, which does pay, is "
         'the revenue line: <a href="/services/care-management">that is covered here</a>.</p>'),
    ]

    page = LandingPage(
        site=SITE,
        slug="services/after-hours-nurse-triage",
        title="After-Hours Nurse Triage Service | RN on Every Call",
        description=(
            "RN-owned 24/7 nurse triage on Schmitt-Thompson protocols. A licensed nurse owns "
            "every disposition. Built for small, low-call-volume practices. See pricing."
        ),
        h1="After-hours nurse triage, <em>an RN on every call.</em>",
        hero_sub=(
            "A 24/7 telephone triage service for medical practices, staffed by licensed "
            "registered nurses working from Schmitt-Thompson protocols your medical director "
            "signs off on."
        ),
        hero_eyebrow="Service 01 · After-hours nurse triage",
        hero_facts=("Licensed RNs", "Schmitt-Thompson protocols", "Flat monthly, never per minute"),
        hero_scene="pines",
        priority="1.0",
        reviewed=True,
    )
    trail = [("Services", "/services/"), ("After-hours nurse triage", "/services/after-hours-nurse-triage")]

    page.sections = [
        crumbs(trail),

        band(
            prose(
                "      <p>Most small practices cover nights the same way: the calls forward to "
                "a physician's personal mobile. It works, in the sense that the phone gets "
                "answered. What it costs is invisible until someone leaves.</p>\n"
                "      <p>The clinician who took three calls between eleven and four is still "
                "seeing a full panel the next morning. The cost turns up as a stipend, as "
                "overtime when a night call runs long, as the next-day productivity nobody "
                "measures, and eventually as the recruiting bill for replacing a provider who "
                "left over call burden. None of those line items are labelled after-hours "
                "coverage, which is exactly why the total never gets added up.</p>\n"
                "      <p>The alternative most practices try next is an answering service. That "
                "moves the ringing off the physician's nightstand but not the deciding: the "
                "operator takes a message and pages the same clinician anyway, having added a "
                "delay and no clinical judgement.</p>"
            ),
            eyebrow="The problem",
            h2="Your after-hours plan is <em>a physician's personal cell phone.</em>",
            scene="premise",
        ),

        band(
            split(
                {"label": "An answering service",
                 "body": "        <p>A non-clinical operator answers, takes a name and a "
                         "number, and pages whoever is on call. Commonly billed per minute, so "
                         "the longest and most worrying calls cost you the most.</p>\n"
                         "        <p>No assessment. No disposition. No clinical documentation. "
                         "Your on-call clinician is still woken for the calls that a nurse "
                         "could have closed, because nobody in the chain was licensed to "
                         "close them.</p>"},
                {"label": "TULQ nurse triage",
                 "body": "        <p>A licensed registered nurse answers, assesses the caller "
                         "against Schmitt-Thompson protocols, reaches a disposition, gives the "
                         "advice, and documents the encounter to your chart.</p>\n"
                         "        <p><strong>Your clinician is paged when the protocol says to "
                         "page them, and not otherwise.</strong> Flat monthly pricing, so a bad "
                         "night is not an invoice event.</p>"},
            ),
            dark=True,
            anchor="how",
            eyebrow="Nurse triage versus an answering service",
            h2="The difference is <em>who is allowed to decide.</em>",
            deck="Both answer the phone. Only one of them can end a call safely without waking "
                 "your on-call clinician.",
            scene="totem",
        ),

        band(
            serve_cards([
                {"title": "The call reaches a nurse.",
                 "body": "Answer-on-connect rather than queue-and-callback. If a clerical front "
                         "door collects the callback number first, it is clerical only and never "
                         "triages.",
                 "tag": "Licensed RN"},
                {"title": "Assessment against protocol.",
                 "body": "The nurse works the Schmitt-Thompson protocol set your medical director "
                         "approved, adjusted where your practice has a standing preference.",
                 "tag": "Schmitt-Thompson"},
                {"title": "Disposition and advice.",
                 "body": "Home care, appointment next day, urgent care, emergency department, or "
                         "escalate to your on-call clinician. The disposition is the product.",
                 "tag": "RN owns the call"},
                {"title": "Documented back to you.",
                 "body": "A dated encounter note with the protocol used, the disposition, and any "
                         "escalation. In your chart under a signed BAA where access allows.",
                 "tag": "Audit-ready note"},
            ]),
            eyebrow="How the line works",
            h2="Four steps, and a nurse owns all of them.",
            scene="why",
        ),

        band(
            prose(
                "      <p>A practice taking four after-hours calls a month still has to be "
                "reachable for every one of the roughly 730 hours in it. That arithmetic is why "
                "low-volume practices get quoted badly: an enterprise contract with a monthly "
                "floor assumes a call volume you will never produce, and per-call pricing "
                "punishes you on the one night that matters.</p>\n"
                "      <p>Our nurses cover a pool of practices rather than sitting idle on "
                "yours, so low volume is priced as low volume. Direct primary care, pediatric, "
                "and OB practices are the clearest fit: all three promised after-hours access "
                "to patients, and all three are trying to honour it on a physician's mobile.</p>",
                wide=True,
            )
            + "\n" + note(
                "<p><strong>What we will not tell you.</strong> TULQ is launching in 2026. We do "
                "not have an average speed to answer, a call resolution rate, or a client list "
                "to quote you, and we are not going to borrow an industry figure and imply it is "
                "ours. What we will do is write a service level into the contract and be held "
                "to it.</p>",
                kind="caution",
            ),
            dark=True,
            eyebrow="Built for small practices",
            h2="Four calls a month, <em>730 hours of obligation.</em>",
            scene="pines",
        ),

        band(
            faq(qa),
            eyebrow="Common questions",
            h2="What practice managers ask first.",
            extra_class="faq-section",
            scene="cave",
        ),

        band(
            routes(
                "The rule <em>your organization</em> is held to.",
                "Triage obligations differ by organization type. These four pages cover the "
                "specific regulation, what a surveyor asks for, and what coverage costs.",
                [
                    {"tag": "42 CFR 418.100(c)", "title": "Hospice",
                     "desc": "24-hour nurse availability as a Medicare Condition of "
                             "Participation, and how calls document back to the IDG.",
                     "href": "/nurse-triage-for-hospice"},
                    {"tag": "42 CFR 484 · HHVBP", "title": "Home health",
                     "desc": "The on-call field nurse, and the acute-care utilization measure "
                             "your HHVBP payment adjustment rides on.",
                     "href": "/for/home-health"},
                    {"tag": "HRSA Chapter 7", "title": "FQHC &amp; health centers",
                     "desc": "Demonstrating after-hours coverage for Health Center Program "
                             "compliance on a safety-net budget.",
                     "href": "/for/health-centers"},
                    {"tag": "42 CFR 491 · 42 CFR 485 F", "title": "RHCs &amp; critical access",
                     "desc": "A 24/7 obligation carried without a clinician on-site overnight.",
                     "href": "/nurse-triage-for-rural-health-clinics"},
                ],
            ) + "\n" + section_links([
                ("Triage versus answering service, in depth", "/resources/nurse-triage-vs-answering-service"),
                ("What on-call really costs", "/resources/true-cost-of-after-hours-on-call"),
                ("Compare triage vendors honestly", "/compare/"),
            ]) + "\n" + sources(
                [
                    ("AAACN telehealth nursing practice standards", AAACN),
                    ("Peterson-KFF Health System Tracker, emergency department visit costs", KFF_ED),
                    ("NCSBN Nurse Licensure Compact", NCSBN_NLC),
                ],
                disclaimer="Reviewed August 2026. TULQ is pre-launch and does not publish call "
                           "volumes, answer times, or client references, because it does not "
                           "have them yet.",
            ),
            dark=True,
            eyebrow="By organization",
            h2="Four practice types, four pages.",
            scene="totem",
        ),

        contact_close(
            "See the line before you commit to it.",
            "Bring your after-hours call volume and your current arrangement. We will tell you "
            "what coverage would cost, and whether your existing on-call setup already meets "
            "the requirement you are trying to satisfy.",
            cap_title="Capability &amp; compliance",
            cap_body="Protocol scope, coverage model, and sample triage documentation on request.",
        ),
    ]

    page.schema = [
        breadcrumb_node(page, trail),
        service_node(
            page,
            "After-hours nurse triage service",
            "Telephone nurse triage",
            "24/7 after-hours telephone triage for medical practices, staffed by licensed "
            "registered nurses working from Schmitt-Thompson protocols, with documented "
            "encounter notes returned to the practice record.",
            audience="Physician practices, direct primary care, pediatric and OB practices, "
                     "health centers, hospices, and home health agencies",
        ),
        faq_node(page, qa),
    ]
    return page


# ══════════════════════════════════════════════════════════════════════
# PAGE C  /services/care-management
# Primary: care management outsourcing for small practices
# ══════════════════════════════════════════════════════════════════════

def page_care_management() -> LandingPage:
    qa = [
        ("What is the difference between CCM and APCM?",
         "<p>Chronic Care Management pays for time. You bill 99490 after at least twenty "
         "minutes of clinical staff time in a calendar month, and the time has to be logged "
         "with a date, a staff member, and what was done. Advanced Primary Care Management "
         "pays a flat monthly amount by patient complexity with no time threshold at all, "
         "which removes the single most common denial risk in the benefit.</p>"
         "<p>The trade is quality reporting. APCM requires you to report the Value in Primary "
         "Care MIPS Value Pathway or participate in an ACO or primary care model. If you "
         "already report, APCM is usually the better instrument. If you do not, that obligation "
         "is a real cost and CCM may be the cleaner choice.</p>"
         + source_link("CMS Advanced Primary Care Management services", CMS_APCM)),

        ("Can you bill CCM and TCM in the same month?",
         "<p>Not for the same patient in the same service period. Only one practitioner may "
         "bill care management for a given patient in a given calendar month, the same minute "
         "cannot be counted twice, and CCM and TCM cannot overlap inside the 30 day "
         "post-discharge window. APCM likewise cannot be billed with CCM, PCM, or TCM for the "
         "same patient in the same month.</p>"
         "<p>We verify all of this before enrolling a patient, every month, and flag a conflict "
         "to you rather than submitting and hoping.</p>"
         + source_link("CMS Chronic Care Management Services booklet", CMS_CCM_BOOKLET)),

        ("What is the 2026 reimbursement for 99490 and the APCM codes?",
         "<p>As 2026 national averages: 99490 pays about <strong>$66</strong> for the first "
         "twenty minutes of staff-directed CCM, with 99439 adding roughly <strong>$50</strong> "
         "per additional twenty minutes up to two units. The three APCM codes pay about "
         "<strong>$16</strong> (G0556, one chronic condition), <strong>$54</strong> (G0557, two "
         "or more), and <strong>$117</strong> (G0558, two or more plus Qualified Medicare "
         "Beneficiary status) per patient per month.</p>"
         "<p>All of those are national averages adjusted by locality and updated each January. "
         "Run your own carrier before modelling on them.</p>"
         + source_link("CMS Physician Fee Schedule lookup", PFS_LOOKUP)),

        ("How do RHCs and FQHCs bill care management in 2026 now that G0511 is gone?",
         "<p>G0511, the bundled general care management code, sunset on 30 September 2025. "
         "Beginning in 2026 RHCs and FQHCs bill the individual care management CPT and HCPCS "
         "codes at national non-facility fee schedule rates, which means tracking time and "
         "documentation separately the way a fee-for-service practice does rather than "
         "reporting one bundled line.</p>"
         "<p>That is a real operational change and it is the single most common reason a health "
         "center calls us. We have written it up in full: "
         '<a href="/resources/g0511-sunset-rhc-fqhc-billing">G0511 is gone, what health '
         'centers bill now</a>.</p>'
         + source_link("CMS Information for Rural Health Clinics, January 2026", CMS_RHC_MLN)),

        ("Do we need to buy software?",
         "<p>No. We are not a software company and we do not resell one. Software vendors sell "
         "eligibility flags, consent capture, care plan templates, and batch claim generation, "
         "all of which remove clicks and none of which make the twenty phone calls. What stops "
         "practices billing this benefit is a labour wall, not a software wall.</p>"
         "<p>If you already own a care management platform, our nurses will work inside it.</p>"),

        ("Who owns the patient relationship?",
         "<p>You do, and the rules require it. Care management runs under general supervision, "
         "so you direct the care without needing to be present while we work. Our nurses "
         "introduce themselves as your care team, because under the benefit that is exactly "
         "what they are. There is no vendor branding, no separate phone number, and no "
         "offshore handoff. You review and sign the care plan, and anything clinical routes "
         "back to you the same day.</p>"),

        ("Do my patients get a bill?",
         "<p>Under CCM, yes: roughly $13 a month in coinsurance at the standard twenty minute "
         "code. Most patients have secondary coverage or Medigap that absorbs it, and patients "
         "with Qualified Medicare Beneficiary status owe nothing. We screen for QMB status "
         "before enrolling and we say the cost out loud during the consent call, rather than "
         "letting a patient discover it on a statement and disenrol in anger.</p>"),

        ("Will this survive an audit?",
         "<p>That is the actual product. Insufficient time documentation is the most common "
         "denial in this benefit, and a program run casually by front desk staff between "
         "patients will not withstand review. Documented consent, a care plan in your certified "
         "record, time logged with date and staff member and activity, monthly eligibility "
         "verification, and no carryover minutes between months. We would rather bill you for "
         "fewer patients than hand you a claim you cannot defend.</p>"),
    ]

    page = LandingPage(
        site=SITE,
        slug="services/care-management",
        title="Outsourced Care Management: CCM, APCM &amp; TCM | TULQ",
        description=(
            "Remote RNs run your CCM, APCM, PCM, and TCM programs and return audit-ready "
            "documentation. Built for small and rural practices. No software to buy."
        ),
        h1="Your care management program, <em>run by nurses.</em>",
        hero_sub=(
            "Medicare pays your practice every month to manage chronic patients between "
            "visits. TULQ supplies the licensed nurses who do the work. You keep the billing, "
            "the chart, and the patient relationship."
        ),
        hero_eyebrow="Service 02 · Medicare care management",
        hero_facts=("CCM · APCM · PCM · TCM", "Flat fee per enrolled patient", "No software to buy"),
        hero_scene="pines",
        priority="1.0",
        reviewed=True,
    )
    trail = [("Services", "/services/"), ("Care management", "/services/care-management")]

    page.sections = [
        crumbs(trail),

        band(
            prose(
                "      <p>Every practice we talk to already does this work. You call the "
                "patient who just got out of the hospital. You sort out the medication the "
                "cardiologist changed. You chase the mammogram. You do it for free, between "
                "patients, at six in the evening.</p>\n"
                "      <p>Medicare will pay you for that work every single month. What it wants "
                "in return is proof: documented consent, a care plan in the chart, tracked "
                "clinical time, and someone reachable around the clock. That is the wall "
                "practices hit, and it is a labour wall rather than a software wall.</p>\n"
                "      <p>At two hundred enrolled patients, twenty minutes each comes to "
                "roughly <strong>67 hours a month</strong> of licensed clinical time. That is "
                "most of a full-time employee you do not have.</p>"
            ),
            eyebrow="Why it does not get done",
            h2="The program is not complicated. <em>Staffing it is.</em>",
            scene="premise",
        ),

        band(
            numbers([
                {"tag": "APCM, level 1", "value": "$16", "count": "16", "prefix": "$",
                 "label": "G0556, per patient per month, for a patient with one chronic "
                          "condition. 2026 national average."},
                {"tag": "APCM, level 2", "value": "$54", "count": "54", "prefix": "$",
                 "label": "G0557, per patient per month, two or more chronic conditions. Where "
                          "most enrolled patients land."},
                {"tag": "APCM, level 3", "value": "$117", "count": "117", "prefix": "$",
                 "label": "G0558, two or more conditions plus Qualified Medicare Beneficiary "
                          "status. These patients owe nothing out of pocket."},
                {"tag": "CCM, first 20 min", "value": "$66", "count": "66", "prefix": "$",
                 "label": "99490, per patient per month, for staff-directed chronic care "
                          "management. 99439 adds about $50 per further 20 minutes."},
                {"tag": "Staff time absorbed", "value": "67", "count": "67", "suffix": "hrs",
                 "label": "Licensed clinical hours a month at 200 enrolled patients and twenty "
                          "minutes each. Most of a full-time employee."},
                {"tag": "Who submits the claim", "value": "You",
                 "label": "TULQ never bills Medicare. We invoice your practice a flat fee per "
                          "enrolled patient per month."},
            ], source="Sources · CMS Physician Fee Schedule, 2026 national averages · CMS "
                      "Advanced Primary Care Management services · adjusted by locality"),
            dark=True,
            eyebrow="The numbers worth knowing",
            h2="What the benefit actually pays.",
            deck="2026 national averages under the Medicare Physician Fee Schedule. Your "
                 "locality will differ, and these update every January.",
            scene="pines",
        ),

        band(
            split(
                {"label": "What software vendors sell",
                 "body": "        <p>Eligibility flags, consent capture, care plan templates, "
                         "batch claim generation, dashboards. Real value, and it removes "
                         "clicks.</p>\n"
                         "        <p>Then someone on your team still has to pick up the phone "
                         "twenty times a day, do the clinical work, and be reachable at 2 a.m. "
                         "The software does not do that. Your medical assistant does, on top of "
                         "everything else, until the program quietly dies.</p>"},
                {"label": "What TULQ sells",
                 "body": "        <p>Licensed registered nurses who make the calls, do the "
                         "clinical work, document it in your chart, log the time, and answer "
                         "the phone at night.</p>\n"
                         "        <p><strong>We work inside your system under your supervising "
                         "provider.</strong> Your patients experience your practice, not a "
                         "vendor. You bill it. We invoice a flat fee per enrolled patient per "
                         "month.</p>"},
            ),
            anchor="how",
            eyebrow="What we actually are",
            h2="A software wall and a labour wall are <em>not the same wall.</em>",
            scene="why",
        ),

        band(
            ledger([
                {"title": "Set up once, at your practice",
                 "items": [
                     ("<strong>A certified electronic health record.</strong> You almost "
                      "certainly already have one.", "you"),
                     ("<strong>24 hour access to a care team member</strong> for urgent needs.",
                      "tulq"),
                     ("<strong>A designated care team</strong> so patients get continuity "
                      "rather than a stranger each month.", "tulq"),
                     ("<strong>A way to track time</strong> per patient per calendar month.",
                      "tulq"),
                 ]},
                {"title": "Once per patient, at enrollment",
                 "items": [
                     ("<strong>Two or more chronic conditions</strong> expected to last twelve "
                      "months or until death, placing the patient at significant risk.", "you"),
                     ("<strong>A qualifying visit first</strong> if the patient is new or "
                      "unseen in twelve months. A wellness visit satisfies this.", "you"),
                     ("<strong>Documented consent</strong> covering cost sharing, one practice "
                      "per month, and the right to stop at any time.", "tulq"),
                     ("<strong>A written care plan</strong> in the record, shared with the "
                      "patient.", "tulq"),
                 ]},
                {"title": "Every month, forever. This is where programs die.",
                 "wide": True,
                 "note": "Insufficient time documentation is the most common denial in this "
                         "benefit. Five of the thirteen requirements recur every single month, "
                         "and all five are ours.",
                 "items": [
                     ("<strong>At least twenty minutes</strong> of clinical staff time, for the "
                      "time-based codes.", "tulq"),
                     ("<strong>Time logged</strong> with date, patient, staff member, and what "
                      "was done. No carryover between months.", "tulq"),
                     ("<strong>The actual clinical work.</strong> Check-ins, medication "
                      "reconciliation, gap closure, specialist and discharge coordination.",
                      "tulq"),
                     ("<strong>The care plan kept current</strong> as things change.", "tulq"),
                     ("<strong>One practice billing</strong> that patient that month. We verify "
                      "before enrolling.", "tulq"),
                 ]},
            ])
            + "\n" + note(
                "<p>Most vendors hide this list. We lead with it, because its length is the "
                "reason you are not billing this today. If a program is run casually by front "
                "desk staff between patients, it will fail an audit. That is the risk we are "
                "hired to remove, and it is why we log every minute in your chart rather than "
                "in ours.</p>",
                kind="caution",
            ),
            dark=True,
            eyebrow="Every requirement, and who owns it",
            h2="Thirteen requirements. <em>We own nine.</em>",
            deck="The ones marked for your practice are the ones only a billing provider can "
                 "hold. Everything else is ours.",
            scene="totem",
        ),

        band(
            compare_table(
                "Which program fits your practice",
                ("Chronic Care Management", "Advanced Primary Care Management"),
                [
                    ("How it pays",
                     "About $66 for the first twenty minutes, stacking upward with additional "
                     "tracked time.",
                     "A flat monthly amount by patient complexity: about $16, $54, or $117."),
                    ("Time tracking",
                     "Required every calendar month. The main denial risk in the benefit.",
                     "None. No time threshold at all."),
                    ("Quality reporting",
                     "None attached to the code itself.",
                     "Required. Straightforward if you already report, a real cost if you "
                     "do not."),
                    ("Best fit",
                     "Independent practices that want no new reporting obligations.",
                     "Practices already in an accountable care or shared savings arrangement."),
                ],
                foot="You cannot bill both for the same patient in the same month. We help you "
                     "choose patient by patient, and we are indifferent to which you pick "
                     "because our fee is identical either way.",
            ),
            eyebrow="CCM or APCM",
            h2="Two instruments for <em>the same clinical work.</em>",
            scene="why",
        ),

        band(
            serve_cards([
                {"title": "You stay the doctor.",
                 "body": "Care management runs under general supervision, so you direct care "
                         "without having to be available while we work. You review and sign the "
                         "care plan. Anything clinical routes back to you the same day.",
                 "tag": "General supervision"},
                {"title": "We work in your chart.",
                 "body": "Delegated access under a signed business associate agreement. Nothing "
                         "lives on our side. Your billing team sees a complete, dated, "
                         "defensible note every month.",
                 "tag": "Signed BAA"},
                {"title": "Your patients hear your practice.",
                 "body": "We introduce ourselves as your care team, because under the rules that "
                         "is exactly what we are. No call center script, no vendor branding, no "
                         "offshore handoff.",
                 "tag": "No vendor branding"},
                {"title": "Flat fee, never a percentage.",
                 "body": "Never a share of your collections, and our nurses are never paid per "
                         "enrollment. Tying a vendor's pay to your Medicare reimbursement is the "
                         "arrangement auditors look at hardest.",
                 "tag": "Deliberate compliance choice"},
            ]),
            dark=True,
            eyebrow="How it actually runs",
            h2="Inside your practice, <em>under your supervision.</em>",
            scene="pines",
        ),

        band(
            prose(
                "      <p>G0511, the bundled general care management code that rural health "
                "clinics and federally qualified health centers reported for years, sunset on "
                "30 September 2025. From 2026 those organizations bill the individual care "
                "management codes at national non-facility fee schedule rates, tracking time "
                "and documentation separately the way a fee-for-service practice does.</p>\n"
                "      <p>For a health center that had one bundled line and now has several "
                "coded ones, that is a genuine operational change rather than a paperwork "
                "tweak, and it arrived alongside the APCM codes. It is the single most common "
                "reason a health center calls us.</p>\n"
                '      <p>We have written the whole thing up. The transition itself, the '
                'replacement codes, the coinsurance, and the supervision rule that makes '
                'remote nursing possible: '
                '<a href="/resources/g0511-sunset-rhc-fqhc-billing">G0511 is gone, what '
                'health centers bill now</a>. The APCM code detail on its own: '
                '<a href="/resources/apcm-billing-fqhc-rhc">APCM billing at an FQHC or '
                'RHC</a>.</p>',
                wide=True,
            ),
            eyebrow="RHCs and FQHCs in 2026",
            h2="The G0511 sunset changed how <em>health centers bill this.</em>",
            scene="bio",
        ),

        band(
            faq(qa),
            eyebrow="Common questions",
            h2="The questions you are going to ask.",
            extra_class="faq-section",
            scene="cave",
        ),

        band(
            section_links([
                ("APCM billing at an FQHC or RHC", "/resources/apcm-billing-fqhc-rhc"),
                ("Annual wellness visits, the enrollment on-ramp", "/services/medicare-annual-wellness-visits"),
                ("The 24/7 access requirement", "/services/after-hours-nurse-triage"),
            ]) + "\n" + sources(
                [
                    ("CMS Advanced Primary Care Management services", CMS_APCM),
                    ("CMS Advanced Primary Care Management services FAQ", CMS_APCM_FAQ),
                    ("CMS Chronic Care Management Services booklet, MLN909188", CMS_CCM_BOOKLET),
                    ("CMS Care Management, Physician Fee Schedule", CMS_CARE_MGMT),
                    ("CMS Information for Rural Health Clinics, MLN006398, January 2026", CMS_RHC_MLN),
                    ("CMS Physician Fee Schedule lookup", PFS_LOOKUP),
                ],
                disclaimer=RATES_NOTE + " Reviewed August 2026.",
            ),
            dark=True,
            eyebrow="Read further",
            h2="Where to go next.",
            scene="totem",
        ),

        contact_close(
            "Fifteen minutes, your real panel, honest numbers.",
            "Bring your Medicare patient count. We will tell you what the program is worth at "
            "your locality, what it will cost you, and whether it is worth doing at all. "
            "Sometimes the answer is no.",
            cap_title="Program design &amp; compliance",
            cap_body="Requirement matrix, supervision model, and sample monthly documentation.",
        ),
    ]

    page.schema = [
        breadcrumb_node(page, trail),
        service_node(
            page,
            "Outsourced Medicare care management",
            "Chronic care management",
            "Licensed registered nurses who deliver Chronic Care Management, Advanced Primary "
            "Care Management, Principal Care Management, and Transitional Care Management "
            "inside a practice's own electronic health record, under the practice's supervising "
            "provider, with audit-ready monthly documentation.",
            audience="Independent physician practices, rural health clinics, and federally "
                     "qualified health centers",
            offers=[
                {"name": "Chronic Care Management (CCM)",
                 "description": "99490 and 99439, twenty minutes or more of clinical staff time "
                                "per calendar month with time logged per patient."},
                {"name": "Advanced Primary Care Management (APCM)",
                 "description": "G0556, G0557, and G0558, paid monthly by patient complexity "
                                "with no time-based threshold."},
                {"name": "Transitional Care Management (TCM)",
                 "description": "99495 and 99496, post-discharge outreach and coordination "
                                "inside the 30 day window."},
            ],
        ),
        faq_node(page, qa),
    ]
    return page


# ══════════════════════════════════════════════════════════════════════
# PAGE B  /services/medicare-annual-wellness-visits
# Primary: annual wellness visit outsourcing
# ══════════════════════════════════════════════════════════════════════

def page_awv() -> LandingPage:
    qa = [
        ("Can an annual wellness visit be done by phone?",
         "<p>For established patients, yes. The AWV is on the Medicare telehealth list and "
         "audio-only delivery is permitted under the telehealth flexibilities, which the "
         "Consolidated Appropriations Act of 2026 extended through 31 December 2027. That is "
         "what makes a telephone AWV programme possible at all, and it is also why it is worth "
         "checking the current CMS telehealth list rather than assuming the position is "
         "permanent.</p>"
         "<p>New patients are a different matter and generally still need to be seen in "
         "person.</p>"
         + source_link("CMS Medicare telehealth", CMS_TELEHEALTH)),

        ("Who can perform and who can bill a Medicare AWV?",
         "<p>This is the compliance nuance that matters most in our model, so we will be exact "
         "about it. Medicare covers the AWV when it is furnished by a physician, a qualified "
         "non-physician practitioner, or by a medical professional or team working under the "
         "direct supervision of a physician.</p>"
         "<p><strong>The billing and supervision obligations sit with your practice, not with "
         "us.</strong> TULQ's registered nurses perform the visit and produce the "
         "documentation; your practice supervises and bills. Any vendor that tells you an "
         "outsourced nurse can simply bill a Medicare AWV on your behalf is describing "
         "something other than the benefit.</p>"
         '<p>The full chain, rule by rule, is written out on our <a href="/awv">plain '
         "English guide to how the visit gets paid</a>.</p>"
         + source_link("42 CFR 410.15", ECFR_AWV)),

        ("What is the 2026 reimbursement for G0438 and G0439?",
         "<p>As 2026 national averages, the initial AWV (G0438) pays roughly "
         "<strong>$174</strong> and each subsequent annual visit (G0439) roughly "
         "<strong>$138</strong>. Both are covered at 100 percent with no patient cost sharing "
         "and no deductible, which is why they are one of the few Medicare touchpoints a "
         "patient never gets a bill for.</p>"
         "<p>FQHCs and RHCs bill the bundled per-diem G0468 under their prospective payment "
         "system, with the standard G-codes reported on the claim for tracking.</p>"
         + source_link("CMS Physician Fee Schedule lookup", PFS_LOOKUP)),

        ("How does an AWV differ from a physical?",
         "<p>An AWV is not a physical and does not include a head-to-toe examination. It is a "
         "structured prevention and risk assessment: a health risk assessment, a review of "
         "medical and family history, a current provider and medication list, height, weight "
         "and blood pressure, cognitive impairment detection, depression screening, functional "
         "ability and safety review, a written screening schedule for the next five to ten "
         "years, and personalised health advice with referrals.</p>"
         "<p>Because most of that is history and structured questioning rather than "
         "examination, it is well suited to a nurse working by telephone. That is the whole "
         "reason this service exists.</p>"
         + source_link("Medicare.gov yearly wellness visits", MEDICARE_AWV)),

        ("How do you return documentation to our EHR?",
         "<p>Where you can grant delegated access, our nurses document directly in your record "
         "under a signed business associate agreement, so the note is already where your "
         "biller looks. Where you cannot, we return a completed, structured note on an agreed "
         "schedule for your team to file. Either way you receive a finished note with every "
         "required element evidenced, not a transcript for someone else to convert.</p>"),

        ("How does this work for a rural health clinic or FQHC?",
         "<p>The clinical work is identical. The billing is not: RHCs and FQHCs report the "
         "bundled per-diem rather than the fee schedule amount, so the revenue arithmetic is "
         "different and usually turns on visit volume and completion rate rather than on the "
         "per-visit rate. We will model it against your own numbers before quoting.</p>"
         + source_link("CMS Information for Rural Health Clinics, January 2026", CMS_RHC_MLN)),

        ("Why do so few of our eligible patients get one?",
         "<p>Because it competes for the same appointment slot as sick visits, and sick visits "
         "always win. The visit takes a clinician the better part of half an hour to do "
         "properly, generates no urgent complaint to anchor it, and is easy to defer to a "
         "quarter that never arrives.</p>"
         "<p>Moving it to a nurse working by telephone takes it out of that competition "
         "entirely. The room is not the constraint any more, and neither is the clinician's "
         "calendar.</p>"),

        ("What does it cost, and how do we know it is worth it?",
         "<p>Priced per completed visit, not per attempt and not per enrolled patient, so we "
         'are paid when you have something to bill. Our <a href="/tools/awv-revenue-calculator">'
         "AWV revenue gap calculator</a> will show you the arithmetic against your own panel "
         "and completion rate in about thirty seconds. Bring the result to the call and we "
         "will run it against your actual locality.</p>"),
    ]

    page = LandingPage(
        site=SITE,
        slug="services/medicare-annual-wellness-visits",
        title="Outsource Medicare Annual Wellness Visits | TULQ",
        description=(
            "Compact-licensed RNs complete Medicare AWVs by phone and return finished "
            "documentation to your clinic. Priced per completed visit. Raise completion rates."
        ),
        h1="Annual wellness visits, <em>completed by nurses.</em>",
        hero_sub=(
            "Compact-licensed registered nurses complete the Medicare annual wellness visit by "
            "telephone and return finished documentation to your clinic. Your practice "
            "supervises and bills."
        ),
        hero_eyebrow="Service 03 · Medicare annual wellness visits",
        hero_facts=("Priced per completed visit", "Audio-only, established patients",
                    "Finished note, not a transcript"),
        hero_scene="pines",
        priority="1.0",
        reviewed=True,
    )
    trail = [("Services", "/services/"),
             ("Medicare annual wellness visits", "/services/medicare-annual-wellness-visits")]

    page.sections = [
        crumbs(trail),

        band(
            prose(
                "      <p>The annual wellness visit is the most reliably ignored money in "
                "primary care. It pays well, it costs the patient nothing, and it is the "
                "qualifying visit that makes chronic care management enrollment possible. Most "
                "practices still complete it for a minority of their eligible panel.</p>\n"
                "      <p>The reason is not that anyone disagrees it is worthwhile. It is that "
                "the visit competes for the same appointment slot as sick visits, and sick "
                "visits always win. It takes the better part of half an hour to do properly, "
                "there is no urgent complaint to anchor it, and it is the easiest thing on the "
                "schedule to defer.</p>\n"
                "      <p>A nurse working by telephone does not compete for that slot. The "
                "examination room stops being the constraint, and so does the clinician's "
                "calendar.</p>"
            ),
            eyebrow="The gap",
            h2="The visit that pays well and <em>never gets scheduled.</em>",
            scene="premise",
        ),

        band(
            numbers([
                {"tag": "Initial AWV", "value": "$174", "count": "174", "prefix": "$",
                 "label": "G0438, the first annual wellness visit. 2026 national average under "
                          "the Physician Fee Schedule, adjusted by locality."},
                {"tag": "Subsequent AWV", "value": "$138", "count": "138", "prefix": "$",
                 "label": "G0439, each subsequent year. The recurring one, and the one most "
                          "practices leave on the table."},
                {"tag": "Patient cost", "value": "$0", "count": "0", "prefix": "$",
                 "label": "Covered at 100 percent with no coinsurance and no deductible. There "
                          "is no bill for the patient to be surprised by."},
                {"tag": "Health centers", "value": "G0468",
                 "label": "FQHCs and RHCs bill the bundled per-diem under the prospective "
                          "payment system, with the G-codes reported for tracking."},
                {"tag": "Audio-only", "value": "2027",
                 "label": "Telehealth flexibilities permitting audio-only delivery for "
                          "established patients run through 31 December 2027."},
                {"tag": "Enrollment on-ramp", "value": "CCM",
                 "label": "An AWV is a qualifying visit for care management enrollment, which "
                          "is where the recurring revenue actually is."},
            ], source="Sources · CMS Physician Fee Schedule, 2026 national averages · "
                      "42 CFR 410.15 · CMS Medicare telehealth · adjusted by locality"),
            dark=True,
            eyebrow="The numbers worth knowing",
            h2="What a completed visit is worth.",
            deck="2026 national averages under the Medicare Physician Fee Schedule. Your "
                 "locality will differ, and these update every January.",
            scene="pines",
        ),

        band(
            serve_cards([
                {"title": "You send us the list.",
                 "body": "Eligible established patients, by last AWV date. We screen for "
                         "eligibility, check nobody else has billed the visit this year, and "
                         "put the outreach in a queue.",
                 "tag": "Eligibility screened"},
                {"title": "A nurse calls the patient.",
                 "body": "Health risk assessment, history, medication and provider list, "
                         "cognitive and depression screening, functional and safety review, and "
                         "the five to ten year screening schedule.",
                 "tag": "Every required element"},
                {"title": "You get the finished note.",
                 "body": "Structured, complete, and evidenced against each required element. In "
                         "your chart under a signed BAA where access allows, returned on an "
                         "agreed schedule where it does not.",
                 "tag": "Ready to bill"},
                {"title": "Your practice bills it.",
                 "body": "The billing practitioner and supervision requirements sit with you, "
                         "because that is what the benefit requires. We are paid per completed "
                         "visit, not per attempt.",
                 "tag": "Per completed visit"},
            ]),
            anchor="how",
            eyebrow="How it works",
            h2="Four steps, and <em>none of them use your rooms.</em>",
            scene="why",
        ),

        band(
            note(
                "<p><strong>The supervision nuance, stated plainly.</strong> Medicare covers "
                "the AWV when it is furnished by a physician, a qualified non-physician "
                "practitioner, or by a medical professional or team working under the direct "
                "supervision of a physician. Direct supervision means the physician is "
                "immediately available to furnish assistance and direction throughout, and "
                "since 1 January 2026 that presence may be a virtual one, through real-time "
                "audio and video rather than in the office suite.</p>"
                "<p>TULQ's nurses perform the visit and produce the documentation. Your "
                "practice holds the supervision obligation and submits the claim. We are "
                "telling you this on the money page rather than in a contract appendix because "
                "any vendor who implies an outsourced nurse can simply bill a Medicare AWV for "
                'you is describing something other than the benefit. See '
                f'<a href="{ECFR_AWV}" target="_blank" rel="noopener">42 CFR 410.15</a>, or '
                '<a href="/awv">the whole chain of rules written out</a>.</p>',
                kind="info",
            ),
            dark=True,
            eyebrow="Who performs, who bills",
            h2="The part <em>we will not blur.</em>",
            deck="The remote-nurse model intersects real supervision and billing rules. Getting "
                 "this wrong is how a program becomes a repayment.",
            scene="totem",
        ),

        band(
            prose(
                "      <p>The visit itself is worth having. What makes it strategically "
                "important is what it unlocks: an AWV is a qualifying visit for chronic care "
                "management enrollment, and it is the appointment where a nurse has twenty "
                "unhurried minutes with a patient who is not sick and not rushed.</p>\n"
                "      <p>That is the moment the chronic conditions surface, the medication "
                "list gets reconciled honestly, and consent for a monthly programme can be "
                "explained properly rather than squeezed into the end of a sick visit. "
                "Enrollment during a wellness visit converts at a materially different rate "
                "from cold outreach, which is why we treat the two services as one "
                "pipeline.</p>\n"
                '      <p>The recurring revenue is in <a href="/services/care-management">care '
                "management</a>. The wellness visit is how patients get there.</p>",
                wide=True,
            )
            + "\n" + section_links([
                ("Run your own numbers, AWV revenue gap calculator", "/tools/awv-revenue-calculator"),
                ("The AWV documentation worksheet", "/tools/annual-wellness-visit-worksheet"),
                ("Care management, where the recurring revenue is", "/services/care-management"),
            ]),
            eyebrow="Why it matters more than it pays",
            h2="The wellness visit is <em>the on-ramp.</em>",
            scene="bio",
        ),

        band(
            faq(qa),
            eyebrow="Common questions",
            h2="What practices ask about outsourced AWVs.",
            extra_class="faq-section",
            scene="cave",
        ),

        band(
            sources(
                [
                    ("42 CFR 410.15, annual wellness visit", ECFR_AWV),
                    ("CMS Medicare Wellness Visits, MLN6775421", CMS_AWV_MLN),
                    ("Medicare.gov yearly wellness visits", MEDICARE_AWV),
                    ("CMS Medicare telehealth", CMS_TELEHEALTH),
                    ("CMS Information for Rural Health Clinics, MLN006398, January 2026", CMS_RHC_MLN),
                    ("CMS Physician Fee Schedule lookup", PFS_LOOKUP),
                ],
                disclaimer=RATES_NOTE + " Reviewed August 2026.",
            ),
            dark=True,
            eyebrow="Sources",
            h2="Where these figures come from.",
            scene="totem",
        ),

        contact_close(
            "Bring your panel, we will bring the arithmetic.",
            "Tell us how many Medicare patients you have and roughly what share got a wellness "
            "visit last year. We will show you the gap in dollars at your own locality, and "
            "what closing it would cost.",
            cap_title="Program design &amp; compliance",
            cap_body="Visit workflow, supervision model, and a sample completed AWV note.",
        ),
    ]

    page.schema = [
        breadcrumb_node(page, trail),
        service_node(
            page,
            "Outsourced Medicare annual wellness visits",
            "Preventive care services",
            "Compact-licensed registered nurses who complete the Medicare annual wellness visit "
            "by telephone for established patients and return finished, structured "
            "documentation to the practice, which supervises and submits the claim.",
            audience="Physician practices, rural health clinics, and federally qualified "
                     "health centers",
        ),
        faq_node(page, qa),
    ]
    return page


def pages() -> list[LandingPage]:
    return [services_hub(), page_triage(), page_care_management(), page_awv()]
