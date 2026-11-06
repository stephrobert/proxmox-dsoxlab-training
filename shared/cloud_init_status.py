"""Recognize completed cloud-init, including one measured PVE compatibility warning."""

# Measured on PVE 9.2.25, 2026-11-06. Its generated user-data still emits
# scalar `user`. Do not waive any other warning or any failed stage.
PVE_USER_DEPRECATION = (
    "'user' of type string is deprecated in 22.2 and scheduled to be removed in 27.2. "
    "Use 'users' list instead."
)


def cloud_init_complete(report, exitcode):
    if not isinstance(report, dict) or report.get("status") != "done" or type(exitcode) is not int or exitcode not in (0, 2):
        return False
    scopes = [report]
    for stage in ("init-local", "init", "modules-config", "modules-final"):
        if stage in report:
            if not isinstance(report[stage], dict):
                return False
            scopes.append(report[stage])
    found_compatibility_warning = False
    for scope in scopes:
        if scope.get("errors") != []:
            return False
        recoverable = scope.get("recoverable_errors", {})
        if not isinstance(recoverable, dict):
            return False
        for kind, warnings in recoverable.items():
            if kind != "DEPRECATED" or not isinstance(warnings, list) or not warnings:
                return False
            if any(warning != PVE_USER_DEPRECATION for warning in warnings):
                return False
            found_compatibility_warning = True
    return exitcode == 0 or found_compatibility_warning
