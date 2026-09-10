# Launch audit reports and next steps

This index identifies the current launch-audit deliverables. Other files in this directory include older component reviews and historical claims; use the reports below for the tested remediation and its limits.

| Report | Contents |
| --- | --- |
| [Final audit report](FINAL_AUDIT_REPORT_2026-09-10.md) | Findings, fixes, 882-test consolidated run, supplementary checks, real OCR/PDF results and verification limits |
| [PRD and scope alignment](SCOPE_ALIGNMENT_2026-09-09.md) | Requirement-by-requirement status and unmet acceptance criteria |
| [PDF/report validation](REPORT_VALIDATION_2026-09-10.md) | Report injection defenses, notes/images, rendering checks and unsigned-draft limitations |
| [Current API contract](API_LAUNCH_CONTRACT.md) | Access requirements, supported routes, limits and deliberately unavailable operations |
| [Security finding draft](SECURITY_SCAN_DRAFT_2026-09-10.json) | Eight consolidated baseline findings with source evidence; partial coverage, native scan unsealed |

The original audit used branch `codex/launch-audit`, based on `c436e3a7055b8f048018727df3ee3b34d0311bf1`. The user authorized publication to `main` after the local checks. Local-only wording within the security draft describes validation at audit time, not the current Git branch or deployment state. Use Git history for the publication commit. A successful Git push is not proof of a successful Netlify deployment or a working hosted Python API.

## Recommended sequence

1. **Confirm the release.** Check the [GitHub Actions run](https://github.com/kunal-raj-dev/MetroLens/actions) for the pushed commit. In Netlify, confirm the production branch and deployed commit, then inspect its build result. Configured continuous deployment can publish a push automatically; see [Netlify's deployment documentation](https://docs.netlify.com/deploy/create-deploys/).
2. **Choose demonstration or live inspection deliberately.** For a demonstration, keep `NEXT_PUBLIC_API_URL` empty. For live inspection, deploy the Python API separately over HTTPS, provide a strong private `METROLENS_API_KEY`, explicit trusted origins and private bounded storage, and use one API worker. Never place the service key in `NEXT_PUBLIC_*` variables.
3. **Connect and verify the hosted flow.** Set `NEXT_PUBLIC_API_URL` to the actual HTTPS API URL and rebuild the web deployment; [Netlify environment-variable changes require a build/deploy](https://docs.netlify.com/build/environment-variables/get-started/). Check authorized/unauthorized access, a real image, unreadable/oversized images, manual-review states, PDF download, reset, and mobile/keyboard interaction. This closes the outstanding production-browser acceptance gap.
4. **Validate rules and measurements before operational reliance.** Resolve partially verified statutory sources, historical applicability and conflicting citations. Collect representative real packages with physical ground truth and measure OCR quality, calibration error and latency. Do not turn blocked dataset/benchmark statuses into verified claims without evidence.
5. **Complete the missing PRD work in separate milestones.** Prioritize durable inspections and officer review history with individual access control, guided multi-panel assessment, measured PDP/glyph geometry, and a complete evidence graph. Add real signing only with verified identity and custody requirements. The scope matrix describes each gap; government integration remains deferred.

The first three steps establish what actually runs after publication. The remaining steps establish whether the product is suitable beyond a clearly labelled prototype or trusted-group pilot.
