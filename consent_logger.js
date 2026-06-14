/*
 * consent_logger.js
 *
 * Frontend logger for Terms click-wrap acceptance.
 * Call `handleAcceptButtonClick(...)` from your modal's "I Accept" button.
 */

function collectFingerprintBase() {
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "unknown";
  return {
    language: navigator.language || "unknown",
    languages: (navigator.languages || []).join(","),
    platform: navigator.platform || "unknown",
    userAgent: navigator.userAgent || "unknown",
    screen: `${window.screen.width}x${window.screen.height}x${window.screen.colorDepth}`,
    timezone: tz,
    hardwareConcurrency: navigator.hardwareConcurrency || 0,
    deviceMemory: navigator.deviceMemory || 0,
    touchPoints: navigator.maxTouchPoints || 0,
  };
}

async function sha256Hex(input) {
  const data = new TextEncoder().encode(input);
  const digest = await crypto.subtle.digest("SHA-256", data);
  const bytes = new Uint8Array(digest);
  return [...bytes].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export async function logLegalConsent({
  tosVersion,
  endpoint = "/api/v1/consent",
  consentAction = "click_wrap_accept",
  manualOptOut = null,
}) {
  if (!tosVersion) {
    throw new Error("tosVersion is required.");
  }

  const fpBase = collectFingerprintBase();
  const fingerprintHash = await sha256Hex(JSON.stringify(fpBase));

  const payload = {
    tos_version: tosVersion,
    fingerprint_hash: fingerprintHash,
    consent_action: consentAction,
    user_agent: navigator.userAgent || "unknown",
    timezone_name: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC",
    // JS returns opposite sign; negate so CDT is -300 as requested.
    timezone_offset: -new Date().getTimezoneOffset(),
    manual_opt_out: manualOptOut === null ? null : Boolean(manualOptOut),
  };

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
    credentials: "omit",
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Consent logging failed (${response.status}): ${text}`);
  }

  return response.json();
}

export async function handleAcceptButtonClick({
  tosVersion,
  endpoint = "/api/v1/consent",
  onAccepted,
}) {
  try {
    await logLegalConsent({ tosVersion, endpoint, consentAction: "click_wrap_accept" });
  } finally {
    // Always allow normal accept flow so UX is not blocked by logging outages.
    if (typeof onAccepted === "function") {
      onAccepted();
    }
  }
}

