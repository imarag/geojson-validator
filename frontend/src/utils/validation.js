import JSON5 from "json5";

export function getJSONValidationState(value) {
  if (!value || !value.trim()) return "idle";

  try {
    JSON.parse(value);
    return "valid";
  } catch {
    return "invalid";
  }
}

export function fixAndValidateJSON(input) {
  if (!input || !input.trim()) {
    return {
      valid: false,
      empty: true,
      error: "Input is empty",
    };
  }
  try {
    // Step 1 — normalize common invalid tokens
    const pre = input
      .replace(/\bNone\b/gi, "null")
      .replace(/\bTrue\b/gi, "true")
      .replace(/\bFalse\b/gi, "false")
      .replace(/\bNaN\b/gi, "null")
      .replace(/\bInfinity\b/gi, "1e999")
      .replace(/\b-Infinity\b/gi, "-1e999");

    // Step 2 — parse using JSON5 (tolerant)
    const parsed = JSON5.parse(pre);

    // Step 3 — serialize to strict JSON
    return {
      valid: true,
      fixedJSON: JSON.stringify(parsed, null, 2),
      data: parsed,
    };
  } catch (err) {
    return {
      valid: false,
      error: err.message,
    };
  }
}
