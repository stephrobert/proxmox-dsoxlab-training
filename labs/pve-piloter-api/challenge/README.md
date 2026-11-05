# Challenge: Pilot the API and wait for real results

Write and run a small API client that starts the prepared VM once, tracks the returned UPID to its final state with bounded polling, and resumes observing that same task after a client timeout. Keep the token out of reports and logs.

## What the tests observe

- The reported UPID resolves to a real completed Proxmox task for the target VM.
- The VM is actually running and there is exactly one VM with the lab identity.
- The client report and its logs do not contain the API secret.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
