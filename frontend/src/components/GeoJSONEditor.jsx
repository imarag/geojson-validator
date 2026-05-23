import Editor from "@monaco-editor/react";

export default function GeoJSONEditor({
  editorConfig,
  editorRef,
  value,
  onChange,
}) {
  // Store editor instance for manual actions
  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
    editor.focus();
  }

  // Update state on typing
  function handleEditorChange(value) {
    onChange && onChange(value);
  }

  function handleValidate(markers) {
    console.log(markers);
  }

  return (
    <Editor
      height="100%"
      loading="Loading GeoJSON editor..."
      defaultLanguage="json"
      value={value}
      onChange={handleEditorChange}
      onMount={handleEditorDidMount}
      onValidate={handleValidate}
      theme={editorConfig?.theme?.value}
      options={{
        fontSize: editorConfig?.fontSize?.value,

        // Layout
        automaticLayout: true,
        wordWrap: editorConfig?.wordWrap?.value,
        smoothScrolling: editorConfig?.smoothScrolling?.value,

        // Formatting
        tabSize: editorConfig?.tabSize.value,
        insertSpaces: true,
        formatOnPaste: editorConfig?.formatOnPaste?.value,
        renderWhitespace: editorConfig?.renderWhitespace?.value,
        formatOnType: true,

        // Navigation
        lineNumbers: editorConfig?.lineNumbers?.value,
        minimap: { enabled: editorConfig?.minimap?.value },

        // Structure visibility
        matchBrackets: editorConfig?.matchBrackets?.value,
        bracketPairColorization: { enabled: true },

        // Clean UX
        scrollBeyondLastLine: false,
      }}
    />
  );
}
