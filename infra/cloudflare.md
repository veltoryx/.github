# Cloudflare setup for veltoryxtech.com

Last updated: 2026-10-10

## Domain

| Item | Value |
|---|---|
| Domain | veltoryxtech.com |
| Registrar | Cloudflare Registrar |
| Registered | 2026-10-08 |
| Expires | 2027-10-08 (auto-renew should be on) |
| Name servers | `boyd.ns.cloudflare.com`, `rita.ns.cloudflare.com` |
| Plan | Free |
| DNSSEC | Enabled (DS record managed automatically by Cloudflare Registrar) |

## Hosting

Both Next.js sites run on **Cloudflare Workers** using the OpenNext adapter (`@opennextjs/cloudflare`). See #6 for the decision.

| Hostname | Serves | How the DNS record is created |
|---|---|---|
| `veltoryxtech.com` | Main website (`veltoryx-web`) | Automatically, by adding it as a Worker custom domain |
| `www.veltoryxtech.com` | Redirect to `veltoryxtech.com` | Placeholder record plus a redirect rule (below) |
| `mediatlas.veltoryxtech.com` | MediAtlas (`mediatlas-ui`) | Automatically, by adding it as a Worker custom domain |

Future products get their own subdomain the same way: `<product>.veltoryxtech.com` as a Worker custom domain.

## DNS records

| Type | Name | Content | Proxied | Purpose |
|---|---|---|---|---|
| AAAA | `www` | `100::` | Yes | Placeholder so Cloudflare can catch `www` traffic and redirect it. Do not remove. |

Records for the apex and `mediatlas` are added automatically when each Worker gets its custom domain. Email routing records (MX, SPF, DKIM, DMARC) will be added in #5.

## Redirect rules

| Rule | Matches | Sends to | Status |
|---|---|---|---|
| Redirect www to apex | `http.host eq "www.veltoryxtech.com"` | `https://veltoryxtech.com` + original path, query string kept | 301 |

## SSL/TLS and security settings

| Setting | Value |
|---|---|
| SSL/TLS encryption mode | Full (strict) |
| Always Use HTTPS | On |
| Minimum TLS version | 1.2 |
| TLS 1.3 | On |
| Automatic HTTPS Rewrites | On |

## API access

A Cloudflare API token named **veltoryx-dns** is limited to the `veltoryxtech.com` zone with these permissions: Zone Settings Edit, DNS Edit, Zone Read, Single Redirect Edit. It's stored outside any repository. **Never commit API tokens.** Deploying Workers will need a separate token with Workers permissions.
