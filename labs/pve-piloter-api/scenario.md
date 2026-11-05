# Mission: Pilot the API and wait for real results

Write and run a small API client that starts the prepared VM once, tracks the returned UPID to its final state with bounded polling, and resumes observing that same task after a client timeout. Keep the token out of reports and logs.

## Acceptance criteria

1. The reported UPID resolves to a real completed Proxmox task for the target VM.
2. The VM is actually running and there is exactly one VM with the lab identity.
3. The client report and its logs do not contain the API secret.

## Prerequisites

Creates only stopped VM 1736 with a 1 GiB empty disk. Create a least-privilege API token scoped to /vms/1736 yourself; keep its secret in a root-only file, never in the Terraform project or output.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
