# Security policy and implemented boundaries

MetroLens is a prototype for trusted, limited use. A source audit and regression tests do not establish that it is free of all vulnerabilities.

## Report a vulnerability

Avoid posting exploitable details or private evidence in a public issue. Contact a repository maintainer through an existing private channel. A dedicated security contact and response SLA have not yet been designated.

## Current controls

- Operational inspection, report, audit, and metrics requests require `Authorization: Bearer <METROLENS_API_KEY>`. Configuration fails closed when the key is absent or shorter than 32 bytes. Use a randomly generated secret, HTTPS, and explicit trusted CORS origins.
- The key represents one trusted service group, not a verified individual officer. Public role selection and affidavit issuance are disabled. Individual RBAC, account recovery, and identity certification are not implemented.
- Uploads use JPEG/PNG/WebP signatures, a 16 MiB request-body cap, a 15 MiB file cap, a 40 MP/8000-pixel-side limit, raster validation, and metadata sanitization. One OCR job runs at a time; limits are local to one process. Client bypass and forwarded-IP headers do not override application rate limits. Run the ASGI server with `--no-proxy-headers` unless a separately verified proxy configuration is provided.
- Spool IDs are restricted portable identifiers. Every spool read/write/delete validates containment and rejects symlinks and Windows reparse points. The directory must be private to the service OS account. A hostile process with the same filesystem rights is outside this boundary.
- Original and sanitized image hashes are separate. Reports and integrity checks require a genuine retained inspection and recompute retained image hashes. A hash comparison is not a digital signature, identity proof, legal admissibility certificate, or full chain of custody.
- Dynamic PDF text is escaped before ReportLab markup parsing. The API does not issue legal affidavits or self-certified government records.
- Browser service keys live only in tab memory. Production builds do not silently send images to localhost or turn live failures into demo successes.

## Retention and limitations

Up to 128 canonical inspection records are kept in memory for one hour. They are lost on restart and can be evicted earlier. Temporary images are cleaned periodically; disk pressure can remove them earlier. Original photos may contain sensitive EXIF data. Application-managed disk encryption, durable signed audit graphs, distributed rate limiting, and full officer-level authorization are not provided. Unused legacy cache/forensics modules must not be treated as production encryption controls.

Use a dedicated private temporary directory on an encrypted volume if sensitive images are permitted by your deployment policy. Do not upload personal or confidential evidence to an unverified public deployment. Dependencies and deployment configuration need ongoing review; never commit service keys, images from private inspections, or environment files.
