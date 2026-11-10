#!/usr/bin/env python3
"""Print a domain's mail-related DNS records over DNS over HTTPS.

Usage: python3 dns.py example.com

Asks Cloudflare's public resolver (cloudflare-dns.com) through its JSON
API, so it works where dig is missing. Queries MX, TXT and A for the
domain, then TXT for _dmarc.<domain>, where DMARC lives. "(none)" means
the resolver answered with no records. "lookup failed" means the query
got no answer. Uses only the Python standard library.
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{0,62}$"
)
QUERIES = [("MX", "{d}"), ("TXT", "{d}"), ("A", "{d}"), ("TXT", "_dmarc.{d}")]
RCODES = {1: "FORMERR", 2: "SERVFAIL", 3: "NXDOMAIN (name does not exist)", 5: "REFUSED"}


def clean_domain(raw):
    domain = raw.strip().lower().rstrip(".")
    try:
        domain = domain.encode("idna").decode("ascii")
    except UnicodeError:
        pass
    if not DOMAIN_RE.match(domain):
        sys.exit(f"not a domain name: {raw!r}")
    return domain


def lookup(name, rtype):
    query = urllib.parse.urlencode({"name": name, "type": rtype})
    request = urllib.request.Request(
        "https://cloudflare-dns.com/dns-query?" + query,
        headers={"Accept": "application/dns-json", "User-Agent": "vet-counterparty-skill/1.0"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: dns.py <domain>")
    domain = clean_domain(sys.argv[1])
    failures = 0
    for rtype, pattern in QUERIES:
        name = pattern.format(d=domain)
        print(f"=== {rtype} {name} ===")
        try:
            result = lookup(name, rtype)
        except (OSError, ValueError) as err:
            failures += 1
            print(f"  lookup failed: {err}")
            continue
        if result.get("Status", 0) != 0:
            print("  " + RCODES.get(result["Status"], f"DNS error {result['Status']}"))
            continue
        answers = result.get("Answer", [])
        if not answers:
            print("  (none)")
        for answer in answers:
            print(" ", str(answer.get("data", ""))[:200])
    if failures == len(QUERIES):
        sys.exit("every DNS-over-HTTPS lookup failed: report the mail records as unchecked")


if __name__ == "__main__":
    main()
