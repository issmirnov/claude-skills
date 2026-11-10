---
name: vet-counterparty
description: "Due-diligence workflow for vetting an unfamiliar company, domain, agency, vendor, subcontractor or cold-outreach sender. It checks domain age through RDAP and the domain's mail records, then searches for marketing copy reused on other sites, for independent reviews, and for real people and a registered entity behind the business. Use it when someone asks whether a company is legit or a scam. Use it when they paste a URL or company name from an unsolicited email, LinkedIn message or DM and ask for research. Use it when they evaluate a vendor, agency, subcontractor or partner they have no history with, or ask how old a domain is, who is behind a site, or whether reviews exist. Trigger on casual phrasing too ('is this real?', 'should I reply to this?', 'who are these guys?'). If they ask for only one piece, such as domain age, still run the full sequence: each signal is weak alone, and together they usually settle the question."
---

# Vetting a counterparty

The goal is a defensible verdict on whether an unfamiliar business is what it claims to be. Deliver it fast enough to help before the person replies to an email or takes a call.

The core idea of this skill: **any single signal is weak, and the combination usually settles the question**. A new domain proves nothing, because every legitimate business was new once. Copied text proves nothing on its own, because agencies buy templates. No reviews proves nothing, because plenty of good small firms have no Clutch profile. But a five-month-old domain, copy that appears word for word on eight other domains, no MX record and zero named people are not ambiguous together. Run every step, even when an early one looks clean. Reason about the pattern at the end instead of concluding from the first finding.

All company names in this skill's examples are made up.

## Scope

This is due diligence on **businesses and their public commercial presence**: companies, domains, agencies, vendors and the entity behind a cold email. It covers individuals only as business counterparties, through their professional footprint. Does this person exist, do they hold the role they claim, and is their firm real?

It is not for building a profile of a private individual. This skill verifies business claims. If a request drifts toward locating someone, assembling a personal history or investigating a private person's life, say so plainly and stop. That is a different activity wearing this one's clothes.

## Step 1: Capture the artifact

Fetch the site. Start with the page the person cited, then the homepage, About, Services or Pricing, and Privacy or Terms.

On claude.ai, the web fetch tool accepts only a URL that already appeared in a search result or in the person's message. If it rejects a URL, search for the domain first, then fetch the page from the result.

Read the returned markup, not just the prose. In a fabricated site, the best evidence is almost always mechanical debris the operator never saw:

- **Anchor links and slugs that contain a different brand name.** A footer link to `#acme-consulting-process-title` on a site called Example Growth Co means the page belonged to Acme Consulting first. This is the most reliable tell in the whole workflow.
- **Leftover names in the prose.** A failed find-and-replace leaves fragments such as "Thank you Acme Example Growth Co!", with the old name stranded mid-sentence.
- **Truncated template variables.** A sentence that stops mid-thought, such as "We Are the Top X Lead Generation Service for", is an unfilled placeholder.
- **Booking-link slugs** that end in `-clone`, `-copy` or `-v2`.
- **A privacy policy dated before the domain was registered.** The operator copied the boilerplate whole.
- **Missing CAN-SPAM requirements** on a site that sends cold email: no physical address, no working contact method, no entity name.
- **Typos in navigation paths** such as `/consutants/`. Nobody proofreads a disposable site.
- **Site-builder fingerprints** in meta tags, such as Leadpages, Squarespace or GoHighLevel. This is not damning alone. Still, a real agency with a decade of clients rarely runs its whole presence on a landing-page builder.

## Step 2: Domain age and registration

`whois` on port 43 is often blocked or times out in Claude's code sandbox. Use RDAP over HTTPS instead, because it is faster and returns structured data. Run the script in this skill's `scripts/` folder:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/rdap.py EXAMPLE.com
```

The script asks Verisign's RDAP server about `.com` and `.net` domains, and rdap.org about all others. rdap.org redirects to the right registry. The script prints the registrar, the registration events, the nameservers and the status.

If the script reports a failure, or says that rdap.org has no record, search the web for the domain's registration record. Cite the source you used. If that fails too, report the domain's age as unverified and say why. Don't estimate it.

What to read from the result:

- **Registration date.** Compare it with the tenure the site claims. "Decades of experience" on a domain registered in February is the whole story.
- **Expiration date.** A new domain registered for one year fits a disposable site. Many legitimate owners also renew every year, so this is weak alone. A multi-year registration is a modest positive.
- **Nameservers** point to the registrar or DNS host, and help you link related domains.
- **Last-changed date** far after registration can mean that a new operator re-registered a dropped domain. That matters, because the domain's age then overstates the business's age.

Run RDAP on every related domain you find in Step 4. Registration dates in a tight cluster, or a series a few months apart, show how often the operator rotates domains.

## Step 3: Mail infrastructure

Query DNS over HTTPS, because the sandbox often lacks `dig`. The script in this skill's `scripts/` folder asks Cloudflare's public resolver for the MX, TXT and A records. It then asks for the TXT record at `_dmarc.EXAMPLE.com`, where DMARC lives:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/dns.py EXAMPLE.com
```

The domain's own TXT answer shows SPF. `(none)` means the resolver answered with no records. `lookup failed` means the query got no answer, so report those records as unchecked. An MX record of `0 .` is a null MX: the domain states that it accepts no mail.

Interpretation:

- **No MX records** on a domain that just cold-emailed the person is significant. Mail servers then fall back to the domain's A record, which on a landing-page host almost never accepts mail. The message came from a separate sending domain. Disposable cold-outreach setups work this way: burner sending domains get dropped as they hit blocklists, while the destination site stays put. It also means replies and unsubscribe requests can go nowhere.
- **No SPF or DMARC records** means nobody manages mail deliverability for this domain. That fits a landing page better than a place of business.
- **A shared A record** with another suspect domain is suggestive but weak alone, because site builders put thousands of customers behind one IP. Treat a shared IP as support for a link you established another way, never as proof by itself.

## Step 4: Copy provenance (highest yield)

This step breaks most of these cases open. Take two or three **distinctive, specific strings** from the site and search for them. Good candidates are named case-study clients, unusual combinations of metrics and oddly worded testimonials.

Distinctiveness is what matters, because generic marketing language returns noise. In contrast, "Example Vision Labs" plus "Sample Retail Group" plus "average monthly appointments" can return a whole clone network in one query.

Prefer client names, proper nouns and specific numbers. Combine two or three in one query instead of quoting a long passage.

When the same copy comes back on several domains:

1. **List the network.** Each hit is another domain that runs the same template with the name swapped. List them all.
2. **Find the original.** The set usually includes a real firm with a genuine history whose site someone copied. A real track record, real reviews, named staff and a much older domain identify it. Name it if you can establish it. If you are inferring instead of confirming, say so and give your confidence.
3. **Date the network** with RDAP on each domain.

Be careful with the inference here. Several sites that share copy can mean any of these:

- one operator running many brands
- several unrelated buyers of the same white-label template
- one firm rebranding over time

Leftover slugs that name a specific earlier brand (Step 1) separate a rebrand or a single operator from coincidence. State which conclusion the evidence supports, and go no further.

## Step 5: Independent footprint

Search for the exact company name in the places where a real B2B firm leaves third-party traces. Check Clutch, G2, Trustpilot, BBB, Glassdoor, Indeed and LinkedIn company pages. Also check industry press, conference listings, job postings and state business registries.

**Missing reviews matter only in proportion to the size the firm claims.** A two-person consultancy with no Clutch profile is unremarkable. Now take a firm that claims Fortune 500 clients, decades of history and thousands of engagements, with no third-party trace anywhere. Its claims don't fit its own footprint. Frame the finding that way, not as "no reviews, therefore fake."

Watch for **name collisions**. A search for a generic name turns up unrelated real companies. It is easy to credit the subject with a legitimate firm's record, or to blame it for another firm's scam reports. Point out near-name collisions to the person. A name confusingly close to an established firm's is worth knowing about in itself.

## Step 6: People and legal entity

Look for at least one **named person** with a verifiable professional presence. Real service businesses put founders and account leads on the About page, because people sell the service. A site that sells senior sales expertise but names no one who has it describes a capability nobody has claimed.

Also check these:

- the registered entity name and jurisdiction
- a physical address and a phone number
- LinkedIn profiles that claim the company, and whether they predate the domain

For a named individual, verify only the narrow business claim: they exist, they hold the stated role, and the company is real. Stop there.

## Evidence tiering

Separate what you established from what you inferred. Present findings in three tiers, and keep the tiers visibly distinct in the output:

- **Confirmed:** RDAP dates, DNS records, strings in fetched HTML, and identical copy retrieved from several named URLs. Anyone can reproduce these.
- **Strongly indicated:** conclusions that follow from confirmed facts through a judgment step, such as "the same operator runs these domains" or "this copy originated with firm X".
- **Unverified:** anything not checked, plus what the absence of evidence does and doesn't support.

Say plainly when you couldn't determine something. "No registry filing found" is a finding. "No registry filing exists" is usually more than the search established.

## Output format

Lead with the verdict. The person is deciding whether to reply to an email, not reading a report. Put the answer first and the evidence after it.

```
## Verdict
[One or two sentences. Direct.]

## Domain
[Table: registered, expires, registrar/NS, host, MX, SPF, DMARC]

## [Findings sections, strongest first]
[Copy provenance, forensic artifacts, footprint, people/entity.
 Include only what you actually found; skip empty sections.]

## Pricing
[What's published, or that nothing is. Note if the only path is a booking link.]

## Recommendation
[What to actually do. Reply, ignore, block, ask specific questions, proceed with terms.]
```

Quote the mechanical artifacts exactly: the stranded brand name, the anchor slug, the truncated sentence. They are the most convincing part of the case. Anyone can check them in seconds, and the analysis could not have made them up.

## Calibration

The failure to guard against is treating thin-but-honest as fraudulent. A new consultancy with a Squarespace site, no reviews and a template it paid for is common and fine. What separates it from a fabricated front is **claims that don't fit the footprint**, for example:

- decades of claimed history on a months-old domain
- named Fortune 500 clients with no support anywhere
- case studies that belong to someone else

Don't soften a clear finding either. If the copy is demonstrably stolen and the infrastructure is disposable, say so directly and let the person decide.

When the evidence is mixed, say so. Then give the specific questions that can resolve it, for example:

- Can you share references from named clients?
- What is your registered entity name?
- Who will actually staff the work?

Those questions help more than a confident verdict the evidence doesn't carry.

## Practical notes

- Unsubscribing from confirmed spam confirms a live address. With no MX record, the unsubscribe path might not reach anything real. Blocking the sending domain is usually the better move. Mention this when the trigger was a cold email.
- Note when the person is the obvious ideal customer for the pitch, for example when their industry has its own landing page on the site. Expect follow-ups from rotated domains with identical copy.
- Cite the URL where each piece of evidence lives, so the person can spot-check any claim without redoing the work.
