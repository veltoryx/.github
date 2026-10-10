# Cloudflare setup for veltoryxtech.com

Last updated: 2026-10-10 (email routing added)

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
| MX | `@` | `route1.mx.cloudflare.net` (17), `route2` (69), `route3` (58) | No | Email Routing: receive mail for the domain |
| TXT | `@` | `v=spf1 include:_spf.mx.cloudflare.net ~all` | No | SPF |
| TXT | `cf2024-1._domainkey` | Cloudflare DKIM public key | No | DKIM for forwarded mail |
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:contact@veltoryxtech.com; adkim=r; aspf=r` | No | DMARC, monitoring mode |

Records for the apex and `mediatlas` are added automatically when each Worker gets its custom domain. Don't remove the MX, SPF or DKIM records, or email stops working.

## Email

| Address | Goes to | Set up in |
|---|---|---|
| `contact@veltoryxtech.com` | Owner's personal inbox (forwarded) | Email → Email Routing → Routing rules |
| Catch-all (any other address) | Dropped (disabled) | Same page; can forward later if aliases like `hello@` are needed |

Cloudflare Email Routing only receives and forwards. Sending as `contact@veltoryxtech.com` needs an outgoing mail service; see #10. When that's set up, its SPF include and DKIM records go here, and DMARC can move from `p=none` to `p=quarantine`.

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
