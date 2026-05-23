// Fix single quotes → double quotes
export function fixSingleQuotes(rawText) {
  // Only replace quotes around keys and string values
  return rawText.replace(/'([^']*?)'/g, '"$1"');
}

// Remove trailing commas in objects or arrays
export function fixTrailingCommas(rawText) {
  return rawText.replace(/,\s*(?=[}\]])/g, "");
}

// Remove comments (//, /* */, #)
export function removeComments(rawText) {
  return rawText.replace(/\/\*[\s\S]*?\*\/|\/\/.*|#.*$/gm, "");
}

// Fix null literals: None → null
export function fixNullLiterals(rawText) {
  return rawText.replace(/\b(None|Non|Nul|Nan)\b/gi, "null");
}

// Fix boolean literals: True/False → true/false
export function fixBooleanLiterals(rawText) {
  return rawText.replace(/\bTrue\b/g, "true").replace(/\bFalse\b/g, "false");
}

// Remove leading zeros and + sign in numbers
export function fixNumberFormat(rawText) {
  let fixed = rawText.replace(/\b0+(\d+)/g, "$1"); // leading zeros
  fixed = fixed.replace(/\+(\d+)/g, "$1"); // + signs
  return fixed;
}

// Apply all fixes
export function fixGeoJSON(rawText) {
  let text = rawText;
  text = fixSingleQuotes(text);
  text = fixTrailingCommas(text);
  text = removeComments(text);
  text = fixNullLiterals(text);
  text = fixBooleanLiterals(text);
  text = fixNumberFormat(text);

  // Try parsing to ensure it's valid JSON
  try {
    const parsed = JSON.parse(text);
    return {
      ok: true,
      data: parsed,
      fixedText: JSON.stringify(parsed, null, 2),
    };
  } catch (err) {
    return { ok: false, error: "Cannot auto-fix JSON: " + err.message };
  }
}
