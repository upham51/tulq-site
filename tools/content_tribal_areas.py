#!/usr/bin/env python3
"""
The twelve IHS Area pages on tulq.health, plus their index.

The research called for templated geo pages: low competition, high buyer
intent, cheap to produce from public IHS data. Five Areas (Albuquerque,
Phoenix, Navajo, Great Plains, Portland) have had recent public nurse
advice line procurement activity and get an extra section.

Facility lists are illustrative rather than exhaustive, and every page
says so. The authoritative list is the IHS Area directory, which we link.
"""

from __future__ import annotations

from pagekit import TRIBAL, Page, card_grid, faq_block, faq_node, service_node, sources_block

SITE = TRIBAL


# name, slug, states blurb, character paragraph, illustrative facilities
AREAS = [
    {
        "name": "Alaska",
        "slug": "alaska-area",
        "states": "Alaska",
        "character": (
            "The Alaska Area is unlike any other in the IHS system. Care is delivered "
            "almost entirely through a tribally managed network under self-governance "
            "compacts, across a service area with more roadless communities than road-"
            "connected ones. For a village accessible only by air or river, the phrase "
            "&ldquo;go to the emergency department&rdquo; can mean a medevac decision "
            "rather than a drive."
        ),
        "facilities": [
            "Alaska Native Medical Center, Anchorage",
            "Regional tribal health corporations across the state",
            "Village and sub-regional clinics",
        ],
        "active": None,
    },
    {
        "name": "Albuquerque",
        "slug": "albuquerque-area",
        "states": "New Mexico, Colorado, and west Texas",
        "character": (
            "The Albuquerque Area serves Pueblo, Apache, and Navajo communities across "
            "a wide stretch of the Southwest, mixing IHS-operated facilities with "
            "tribally operated 638 programs. It has been among the most consistent "
            "users of the Buy Indian Act preference in the system."
        ),
        "facilities": [
            "Santa Fe Indian Health Center",
            "Acoma-Ca&ntilde;oncito-Laguna Indian Health Center",
            "Albuquerque Indian Health Center",
            "Zuni, Mescalero, and Jicarilla service units",
        ],
        "active": (
            "<p>Albuquerque has been one of the most active Areas for nurse advice line "
            "procurement. RFQ <strong>75H70725Q00103</strong> for the Santa Fe Indian "
            "Health Center was awarded in August 2025. Separately, "
            "Acoma-Ca&ntilde;oncito-Laguna posted a Sources Sought notice for 24/7 "
            "nurse phone triage as an ISBEE set-aside under NAICS 541990.</p>"
            "<p>The Area has publicly described procuring from Small Business Indian "
            "Firms as its standard practice, which makes it a natural fit for an "
            "Indian Economic Enterprise offering clinical services.</p>"
        ),
    },
    {
        "name": "Bemidji",
        "slug": "bemidji-area",
        "states": "Minnesota, Wisconsin, Michigan, Indiana, and Illinois",
        "character": (
            "The Bemidji Area covers Ojibwe, Potawatomi, Ho-Chunk, Menominee, and other "
            "nations across the upper Midwest. Most care is delivered through tribally "
            "operated programs, and winter travel distance is a real clinical variable "
            "in after-hours decisions."
        ),
        "facilities": [
            "Red Lake Indian Health Service Hospital",
            "Cass Lake Indian Health Service Hospital",
            "White Earth and Leech Lake tribal health programs",
            "Tribal clinics across Wisconsin and Michigan",
        ],
        "active": None,
    },
    {
        "name": "Billings",
        "slug": "billings-area",
        "states": "Montana and Wyoming",
        "character": (
            "The Billings Area serves the Crow, Northern Cheyenne, Blackfeet, "
            "Assiniboine, Gros Ventre, Sioux, Chippewa-Cree, Eastern Shoshone, and "
            "Northern Arapaho nations. Service populations are spread across some of "
            "the largest and least densely populated reservations in the country, where "
            "the nearest emergency department is frequently an hour or more away."
        ),
        "facilities": [
            "Crow and Northern Cheyenne service units",
            "Blackfeet Community Hospital",
            "Fort Belknap and Fort Peck service units",
            "Wind River service unit",
        ],
        "active": None,
    },
    {
        "name": "California",
        "slug": "california-area",
        "states": "California",
        "character": (
            "The California Area is highly decentralized: care runs almost entirely "
            "through tribally operated health programs and urban Indian health "
            "organizations serving more than a hundred federally recognized tribes and "
            "a large urban AI/AN population. Programs here are typically small, "
            "independently governed, and procuring on their own authority rather than "
            "through an Area-wide contract."
        ),
        "facilities": [
            "Tribal health programs and consortia statewide",
            "Urban Indian health organizations in the major metropolitan areas",
            "Rancheria and reservation clinics",
        ],
        "active": None,
    },
    {
        "name": "Great Plains",
        "slug": "great-plains-area",
        "states": "North Dakota, South Dakota, Nebraska, and Iowa",
        "character": (
            "The Great Plains Area serves Lakota, Dakota, Nakota, and other nations "
            "across four states, and carries some of the most documented access "
            "challenges in the IHS system. Distance, weather, and workforce shortages "
            "compound each other, and after-hours coverage is a recurring subject of "
            "both procurement and oversight attention."
        ),
        "facilities": [
            "Woodrow Wilson Keeble Memorial Health Care Center, Sisseton SD",
            "Pine Ridge and Rosebud service units",
            "Rapid City Indian Health Center",
            "Standing Rock and Winnebago service units",
        ],
        "active": (
            "<p>The Great Plains Area has posted repeated market research for exactly "
            "this service. Sources Sought <strong>IHS1520417</strong>, published in "
            "December 2025 for the Woodrow Wilson Keeble Memorial Health Care Center in "
            "Sisseton, followed an earlier notice (<strong>IHS1507826</strong>) in early "
            "2025. Both were ISBEE/IEE set-asides under NAICS 621111.</p>"
            "<p>The stated purpose was a toll-free nurse advice and medical library "
            "line intended to reduce emergency room use near the Lake Traverse "
            "Reservation &mdash; which is, precisely, the case for nurse triage in a "
            "Purchased/Referred Care environment.</p>"
        ),
    },
    {
        "name": "Nashville",
        "slug": "nashville-area",
        "states": "the eastern United States, from Maine to Florida and west to Texas",
        "character": (
            "The Nashville Area has the widest geographic footprint of any IHS Area, "
            "serving tribes across more than twenty states. Its programs are mostly "
            "tribally operated and vary enormously in size, from large tribal health "
            "systems to small clinics serving a few hundred people."
        ),
        "facilities": [
            "Cherokee Indian Hospital, North Carolina",
            "Choctaw Health Center, Mississippi",
            "Seminole and Miccosukee tribal health programs, Florida",
            "Tribal clinics across the Northeast and Gulf states",
        ],
        "active": None,
    },
    {
        "name": "Navajo",
        "slug": "navajo-area",
        "states": "Arizona, New Mexico, and Utah",
        "character": (
            "The Navajo Area serves the Navajo Nation, the largest reservation in the "
            "United States at roughly the size of West Virginia. Households without "
            "reliable telephone or broadband service, long distances between "
            "communities, and a service population concentrated across three states "
            "make after-hours access a persistent structural problem rather than an "
            "occasional one."
        ),
        "facilities": [
            "Gallup Indian Medical Center",
            "Chinle Comprehensive Health Care Facility",
            "Northern Navajo Medical Center, Shiprock",
            "Tuba City, Crownpoint, and Kayenta service units",
        ],
        "active": (
            "<p>The Gallup Service Unit published a Sources Sought notice for nurse "
            "advice line services in January 2025, with a five-year period of "
            "performance and a Buy Indian Act preference under NAICS 621399.</p>"
            "<p>Gallup Indian Medical Center is one of the highest-volume facilities in "
            "the IHS system, which makes the after-hours telephone load correspondingly "
            "large.</p>"
        ),
    },
    {
        "name": "Oklahoma City",
        "slug": "oklahoma-city-area",
        "states": "Oklahoma, Kansas, and parts of Texas",
        "character": (
            "The Oklahoma City Area serves the largest AI/AN service population of any "
            "IHS Area, across dozens of nations. Many of the largest tribal health "
            "systems in the country operate here under self-governance compacts, "
            "procuring independently and at meaningful scale."
        ),
        "facilities": [
            "W.W. Hastings Hospital, Tahlequah",
            "Claremore Indian Hospital",
            "Lawton Indian Hospital",
            "Large tribally operated health systems statewide",
        ],
        "active": None,
    },
    {
        "name": "Phoenix",
        "slug": "phoenix-area",
        "states": "Arizona, Nevada, and Utah",
        "character": (
            "The Phoenix Area spans a mix of urban and deeply rural service units "
            "across three states, from a major medical center in metropolitan Phoenix "
            "to small clinics serving a few hundred patients. That range means "
            "after-hours call volume varies by more than an order of magnitude between "
            "facilities in the same Area."
        ),
        "facilities": [
            "Phoenix Indian Medical Center",
            "Colorado River Service Unit",
            "Uintah &amp; Ouray Service Unit",
            "Southern Bands Health Center",
        ],
        "active": (
            "<p>Phoenix has run recent market research on both ends of the volume "
            "range. RFQ <strong>RFQ-26-PHX-046</strong> covered the Colorado River, "
            "Uintah &amp; Ouray, and Southern Bands service units together &mdash; "
            "facilities whose published call estimates ranged from roughly ten to a "
            "couple hundred calls a month. Separately, Sources Sought "
            "<strong>SS-25-PHX-002</strong> addressed the Phoenix Indian Medical Center "
            "under NAICS 621399, as Buy Indian competitive.</p>"
            "<p>The multi-site structure of RFQ-26-PHX-046 is worth noting: small "
            "facilities are cheaper to cover when they are bundled, because the fixed "
            "cost of standing up coverage is spread across them.</p>"
        ),
    },
    {
        "name": "Portland",
        "slug": "portland-area",
        "states": "Washington, Oregon, and Idaho",
        "character": (
            "The Portland Area serves more than forty federally recognized tribes "
            "across the Pacific Northwest, most of them operating their own health "
            "programs under 638 contracts or compacts. It is also where TULQ's own name "
            "comes from &mdash; <span class=\"lush\">tultx&#695;</span>, the Lushootseed "
            "word for the confluence of the Tolt and Snoqualmie rivers, in western "
            "Washington."
        ),
        "facilities": [
            "Yakama Indian Health Center, Toppenish WA",
            "Warm Springs Health &amp; Wellness Center, Oregon",
            "Colville and Nez Perce tribal health programs",
            "Puget Sound and coastal tribal clinics",
        ],
        "active": (
            "<p>The Yakama Indian Health Center in Toppenish, Washington solicited a "
            "&ldquo;24 Hour Nurse Advice Line&rdquo; under RFQ "
            "<strong>75H71325Q00030</strong>, structured as a base year plus four "
            "option years.</p>"
            "<p>Notably, that requirement was set aside for Women-Owned Small Business "
            "rather than under the Buy Indian Act, under NAICS 621111 &mdash; a useful "
            "reminder that the Buy Indian preference is applied acquisition by "
            "acquisition, not automatically across an Area.</p>"
        ),
    },
    {
        "name": "Tucson",
        "slug": "tucson-area",
        "states": "southern Arizona",
        "character": (
            "The Tucson Area is the smallest IHS Area, serving the Tohono O'odham "
            "Nation and the Pascua Yaqui Tribe along the southern Arizona border. Its "
            "compactness is relative: the Tohono O'odham Nation alone covers an area "
            "larger than Connecticut, much of it desert, with long distances between "
            "communities and definitive care."
        ),
        "facilities": [
            "Sells Indian Hospital",
            "San Xavier Health Center",
            "Pascua Yaqui tribal health programs",
        ],
        "active": None,
    },
]


def _area_page(area: dict) -> Page:
    name = area["name"]
    slug = area["slug"]
    facilities = "\n".join(f"      <li>{f}</li>" for f in area["facilities"])

    active_section = ""
    if area["active"]:
        active_section = f"""
    <h2>Recent procurement activity</h2>

    <div class="callout callout--amber">
      <div class="callout-head">Public record &middot; SAM.gov</div>
      {area["active"]}
    </div>

    <p>These notices are matters of public record and are summarized here as context.
    A Sources Sought notice is market research, not a commitment to solicit or award,
    and notices are routinely amended or superseded. Work from the current posting.
    <a href="/for/contracting-officers">More for contracting officers.</a></p>
"""

    page = Page(
        site=SITE,
        slug=f"areas/{slug}",
        title=f"{name} Area IHS Nurse Advice Line | TULQ",
        description=(
            f"Nurse advice line coverage for IHS facilities and tribal health programs "
            f"in the {name} Area. Native-owned, RN-answered, 24/7. Talk to our team."
        ),
        eyebrow=f"{name} Area",
        h1=f"Nurse advice line coverage in the <em>{name} Area.</em>",
        deck=(
            f"The {name} Area covers {area['states']}. TULQ provides 24/7 telephone "
            f"nurse triage for the IHS service units, 638 tribal health programs, and "
            f"Urban Indian Organizations that serve it."
        ),
        crumbs=[("IHS Areas", "/areas/"), (f"{name} Area", f"/areas/{slug}")],
        priority="0.6",
        cta_title=f"Coverage for the {name} Area.",
        cta_body=(
            "Tell us which facility or program you are scoping and we will walk through "
            "what after-hours coverage would look like for that service population."
        ),
    )

    page.body = f"""    <p>{area["character"]}</p>

    <h2>Facilities and programs in this Area</h2>

    <p>The {name} Area includes IHS-operated service units alongside tribally operated
    638 programs and compacts. Illustrative facilities:</p>

    <ul>
{facilities}
    </ul>

    <p>This is not a complete list. The Indian Health Service maintains the
    authoritative directory of Area facilities and service units, and tribally
    operated programs change hands between IHS and tribal operation over time.</p>
{active_section}
    <h2>What coverage looks like here</h2>

    <p>The service is the same everywhere: one number, answered any hour by a U.S.
    state-licensed registered nurse working Schmitt-Thompson telephone triage
    protocols, with the encounter documented and returned to the facility. What
    changes by Area is the context around it &mdash; how far the nearest emergency
    department is, what the winter looks like, whether the caller has reliable
    cellular service, and how the program is funded.</p>

    <p>For IHS-operated service units, after-hours coverage is typically procured
    through the Area office and appears publicly on SAM.gov. For 638 programs and
    compacts, it is procured directly by the tribe or tribal organization, with no
    IHS solicitation required. <a href="/for/tribal-health-ihs">Both paths are
    covered on our tribal health page.</a></p>

    <h2>Elsewhere in the system</h2>

    {card_grid([
        ("Overview", "All twelve IHS Areas",
         "The full map: which states each Area covers and where nurse advice line procurement has been active.",
         "/areas/"),
        ("Tribal health", "Built for Indian Country",
         "Why a tribal health program's after-hours problem is not the same problem the mainstream vendors solve.",
         "/for/tribal-health-ihs"),
        ("PRC", "Protecting the PRC budget",
         "How avoidable emergency department use draws against a finite Purchased/Referred Care allocation.",
         "/resources/nurse-advice-line-prc-budget"),
    ])}

    {sources_block([
        "Indian Health Service Area office and facility directories.",
        "SAM.gov contract opportunities &mdash; Indian Health Service notices.",
        "Indian Self-Determination and Education Assistance Act of 1975, P.L. 93-638.",
    ], disclaimer=(
        "Facility lists are illustrative, drawn from public IHS materials, and change "
        "over time as programs move between IHS and tribal operation. TULQ is launching "
        "in 2026; this page describes intended coverage, not past contract performance."
    ))}"""

    page.schema = [
        service_node(
            page,
            name=f"24/7 nurse advice line for the {name} IHS Area",
            service_type="Telephone nurse triage",
            description=(
                f"24/7 telephone nurse triage for Indian Health Service service units, "
                f"638 tribal health programs, and Urban Indian Organizations in the "
                f"{name} IHS Area, covering {area['states']}."
            ),
            audience=f"IHS facilities and tribal health programs in the {name} Area",
        ),
    ]
    return page


def area_pages() -> list[Page]:
    return [_area_page(a) for a in AREAS]


def areas_index() -> Page:
    page = Page(
        site=SITE,
        slug="areas/index",
        title="IHS Areas: Nurse Advice Line Coverage | TULQ",
        description=(
            "All twelve Indian Health Service Areas, the states each covers, and where "
            "nurse advice line procurement has recently been active. See the map."
        ),
        eyebrow="IHS Areas",
        h1="Twelve Areas. <em>One line.</em>",
        deck=(
            "The Indian Health Service organizes its system into twelve Areas. They "
            "differ enormously &mdash; in geography, in how much care is tribally "
            "operated, and in how after-hours coverage gets bought. Here is the map."
        ),
        crumbs=[("IHS Areas", "/areas/")],
        wide=True,
        priority="0.7",
        cta_title="Not sure which Area you fall under?",
        cta_body=(
            "Tell us the facility or program and we will sort it out, along with what "
            "after-hours coverage would look like for that service population."
        ),
    )

    active = [a for a in AREAS if a["active"]]
    rows = []
    for a in AREAS:
        flag = ('<span class="tick">Recent activity</span>' if a["active"]
                else '<span class="cross">None surfaced</span>')
        rows.append(f"""          <tr>
            <td><a href="/areas/{a['slug']}">{a['name']} Area</a></td>
            <td>{a['states'].capitalize() if a['states'][0].islower() else a['states']}</td>
            <td>{flag}</td>
          </tr>""")

    cards = [("", f"{a['name']} Area", a["states"].capitalize() if a["states"][0].islower()
              else a["states"], f"/areas/{a['slug']}") for a in AREAS]

    page.body = f"""    <p>An IHS Area is an administrative region, not a clinical one. What it
    determines, for our purposes, is who does the contracting: an IHS-operated service
    unit generally procures after-hours coverage through its Area office, while a
    tribally operated 638 program or compact procures on its own authority.</p>

    <p>Areas also differ in how much recent procurement activity they have shown for
    nurse advice line services. Five have posted public notices in the last two years;
    the others have not, which usually means coverage is handled inside tribal
    programs rather than through Area contracting.</p>

    <div class="table-scroll">
      <table class="data">
        <thead>
          <tr>
            <th>IHS Area</th>
            <th>States served</th>
            <th>Recent public nurse-line procurement</th>
          </tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>

    <div class="callout">
      <div class="callout-head">Reading that last column</div>
      <p>&ldquo;None surfaced&rdquo; means we found no public SAM.gov nurse-advice-line
      notice for that Area in the recent record. It does not mean those facilities have
      coverage, and it does not mean they are not buying it &mdash; tribally operated
      programs procure directly and never appear on SAM.gov at all.</p>
    </div>

    <h2>Where procurement has been active</h2>

    <p>{len(active)} of the twelve Areas have had recent public activity:
    {", ".join(a["name"] for a in active[:-1])}, and {active[-1]["name"]}. Each of
    those Area pages summarizes the notices on record.</p>

    <h2>Every Area</h2>

    {card_grid(cards)}

    {sources_block([
        "Indian Health Service Area office directories.",
        "SAM.gov contract opportunities &mdash; Indian Health Service.",
    ], disclaimer=(
        "Area descriptions are drawn from public IHS materials. Procurement summaries "
        "reflect public SAM.gov postings as recorded; notices are amended and "
        "superseded, so work from the current posting."
    ))}"""

    return page
