#!/usr/bin/env python3
"""Print a domain's registration record from RDAP.

Usage: python3 rdap.py example.com

Asks Verisign's RDAP server about .com and .net domains, and rdap.org,
which redirects to the right registry, about every other domain. Prints
the domain name, registrar, registration events, nameservers and status.
Uses only the Python standard library.
"""
import json
import re
import sys
import urllib.error
import urllib.request

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{0,62}$"
)
# rdap.org refuses Python's default User-Agent with HTTP 403.
HEADERS = {"Accept": "application/rdap+json", "User-Agent": "vet-counterparty-skill/1.0"}


def clean_domain(raw):
    domain = raw.strip().lower().rstrip(".")
    try:
        domain = domain.encode("idna").decode("ascii")
    except UnicodeError:
        pass
    if not DOMAIN_RE.match(domain):
        sys.exit(f"not a domain name: {raw!r}")
    return domain


def rdap_url(domain):
    tld = domain.rsplit(".", 1)[-1]
    if tld in ("com", "net"):
        return f"https://rdap.verisign.com/{tld}/v1/domain/{domain}"
    return f"https://rdap.org/domain/{domain}"


def registrar_name(record):
    for entity in record.get("entities", []):
        if "registrar" not in entity.get("roles", []):
            continue
        vcard = entity.get("vcardArray") or []
        for item in vcard[1] if len(vcard) > 1 else []:
            if isinstance(item, list) and len(item) > 3 and item[0] == "fn":
                return item[3]
    return None


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: rdap.py <domain>")
    domain = clean_domain(sys.argv[1])
    url = rdap_url(domain)
    request = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            record = json.load(response)
    except urllib.error.HTTPError as err:
        if err.code == 404 and "rdap.verisign.com" in url:
            sys.exit(f"RDAP: Verisign has no record of {domain}, so it is probably not registered.")
        if err.code == 404:
            sys.exit(
                f"RDAP: rdap.org has no record of {domain}. Either the domain is not "
                "registered, or its registry offers no RDAP service that rdap.org knows. "
                "Treat the domain's age as unverified."
            )
        sys.exit(f"RDAP lookup failed: HTTP {err.code} from {url}")
    except OSError as err:
        sys.exit(f"RDAP lookup failed: {err} ({url})")
    except ValueError:
        sys.exit(f"RDAP lookup failed: {url} did not return JSON")

    print("name:", record.get("ldhName"))
    print("registrar:", registrar_name(record))
    for event in record.get("events", []):
        print(" ", event.get("eventAction"), event.get("eventDate"))
    for server in record.get("nameservers", []):
        print("  NS:", server.get("ldhName"))
    print("status:", record.get("status"))


if __name__ == "__main__":
    main()
