# Counterparty Vetting

Checks whether an unfamiliar company, vendor or cold-email sender is what it claims to be, before you reply, pay or sign. Made by Smirnov Labs.

## Use it

Paste a URL, a company name or the cold email, and ask Claude whether it's legit. Casual questions work too, such as "is this real?" or "who are these guys?". The skill tells Claude to run six checks, even when you ask about only one of them:

1. Read the site, including its page markup, for leftovers from another company's site.
2. Look up when the domain was registered.
3. Check the domain's mail records: MX, SPF and DMARC.
4. Search for the site's distinctive text on other domains.
5. Search review sites, job boards, the press and business registries for an independent footprint.
6. Look for named people and a registered legal entity.

You get a verdict first. The evidence follows in three groups: confirmed, strongly indicated and unverified. Claude cites a URL for each piece of evidence, so you can check it yourself.

## Limits

The verdict rests on public evidence, which can be thin or misleading. A new or small business with no reviews is often legitimate, and a well-built front can pass some checks. Treat the verdict as research, not as legal or financial advice. Confirm anything important through a channel you trust.

The skill vets businesses. It looks at people only in their business role, and it tells Claude to stop if a request turns into profiling a private person.

## Requirements

Claude needs web search and web fetch. The domain and mail checks run two small Python scripts in Claude's code sandbox, so code execution must be on. The sandbox's network settings must also allow the hosts listed under Data. If a check can't run, Claude says so and marks that finding unverified instead of guessing.

## Data

The plugin has no connectors and stores nothing. Its two scripts, `rdap.py` and `dns.py`, use only Python's standard library. They contact only the RDAP and DNS servers below. While it works, Claude sends these:

- The domain name, to RDAP servers and to Cloudflare's DNS-over-HTTPS service at cloudflare-dns.com. The RDAP server is rdap.verisign.com for `.com` and `.net` domains. For other domains it is rdap.org, which redirects to the domain's registry.
- Search queries with the company's name, the names of people the site lists and short quotes from its pages, through Claude's web search.
- Requests for the site's pages and for related sites' pages, through Claude's web fetch.

Your conversation stays in your Claude account like any other chat.

## License

MIT. See `LICENSE`.
