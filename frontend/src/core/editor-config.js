export const editorSettingsSchema = {
  theme: {
    label: "Theme",
    description:
      "Change the editor appearance between light, dark, or high contrast mode.",
    type: "select",
    value: "vs-dark",
    options: [
      { label: "Dark", value: "vs-dark" },
      { label: "Light", value: "vs-light" },
      { label: "High Contrast", value: "hc-black" },
    ],
  },

  fontSize: {
    label: "Font Size",
    description:
      "Adjust the size of the text inside the editor for better readability.",
    type: "number",
    value: 14,
    min: 10,
    max: 30,
    step: 1,
  },
  renderWhitespace: {
    label: "Render Whitespace",
    description: "Show spaces and tabs inside the editor.",
    type: "select",
    value: "selection",
    options: [
      { label: "None", value: "none" },
      { label: "Selection Only", value: "selection" },
      { label: "Trailing Only", value: "trailing" },
      { label: "All", value: "all" },
    ],
  },

  wordWrap: {
    label: "Word Wrap",
    description:
      "Wrap long lines onto the next line instead of using horizontal scrolling.",
    type: "select",
    value: "on",
    options: [
      { label: "On", value: "on" },
      { label: "Off", value: "off" },
    ],
  },

  lineNumbers: {
    label: "Line Numbers",
    description:
      "Show or hide line numbers to make debugging and navigation easier.",
    type: "select",
    value: "on",
    options: [
      { label: "On", value: "on" },
      { label: "Off", value: "off" },
      { label: "Relative", value: "relative" },
    ],
  },

  minimap: {
    label: "Minimap",
    description:
      "Display a small preview of the file on the right side for quick navigation.",
    type: "checkbox",
    value: false,
  },

  tabSize: {
    label: "Tab Size",
    description: "Number of spaces used when indenting code.",
    type: "number",
    value: 2,
    min: 2,
    max: 8,
    step: 1,
  },

  formatOnPaste: {
    label: "Format on Paste",
    description:
      "Automatically format code when pasting content into the editor.",
    type: "checkbox",
    value: true,
  },

  matchBrackets: {
    label: "Highlight Matching Brackets",
    description:
      "Highlight matching brackets to make nested structures easier to understand.",
    type: "select",
    value: "always",
    options: [
      { label: "Always", value: "always" },
      { label: "Never", value: "never" },
    ],
  },

  smoothScrolling: {
    label: "Smooth Scrolling",
    description:
      "Enable smoother scrolling for a more fluid reading experience.",
    type: "checkbox",
    value: true,
  },
};
