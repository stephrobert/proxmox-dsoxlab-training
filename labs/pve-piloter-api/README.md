# pve-piloter-api

Write and run a small API client that starts the prepared VM once, tracks the returned UPID to its final state with bounded polling, and resumes observing that same task after a client timeout. Keep the token out of reports and logs.

**Prerequisites / blocked conditions:** Creates only stopped VM 1736 with a 1 GiB empty disk. Create a least-privilege API token scoped to /vms/1736 yourself; keep its secret in a root-only file, never in the Terraform project or output.

```bash
dsoxlab run pve-piloter-api
dsoxlab check pve-piloter-api
dsoxlab clean pve-piloter-api
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
