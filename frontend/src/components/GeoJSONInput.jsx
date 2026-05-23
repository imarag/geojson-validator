import { useState, useRef } from "react";
import MainTitle from "./MainTitle";
import { geojsonSamples } from "../assets/sample-geojson";
import { endpoints } from "../core/urls";
import GeoJSONEditor from "./GeoJSONEditor";
import InputMenuBar from "./InputMenuBar";
import ValidateButton from "./ValidateButton";
import {
  fixAndValidateJSON,
  getJSONValidationState,
} from "../utils/validation";
import { apiRequest } from "../utils/io";

export default function GeoJSONInput({
  setPipelineOutput,
  setToast,
  inputGeoJSON,
  setInputGeoJSON,
  showSettingsSidebar,
  setShowSettingsSidebar,
  config,
}) {
  const [loading, setLoading] = useState(false);
  const editorRef = useRef(null);
  const JSONState = getJSONValidationState(inputGeoJSON);

  function handleFixInput() {
    const currentText = editorRef.current?.getValue();
    if (!currentText) return;
    const fixed = fixAndValidateJSON(currentText);
    if (fixed.valid) {
      editorRef.current?.setValue(fixed.fixedJSON);
    } else {
      setToast({
        message:
          "Could not fix the JSON. Please check the syntax and try again.",
        type: "error",
        visible: true,
      });
    }
  }

  async function handleUploadFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);

      const validationResult = await apiRequest(
        endpoints.VALIDATE_GEOJSON_FILE,
        { method: "POST", body: formData },
        setToast,
        "GeoJSON loaded successfully.",
      );

      const fileRawInput = validationResult["raw_geojson"];
      editorRef.current?.setValue(fileRawInput);
    } catch (err) {
      editorRef.current?.setValue("");
      console.error("Validation error:", err);
    } finally {
      setLoading(false);
    }
  }

  function handleAddSample(index) {
    setInputGeoJSON(geojsonSamples[index].geojson);
    setPipelineOutput(null);
    editorRef.current.focus();
  }

  function handleEditorChange(value) {
    setInputGeoJSON(value.trim());
    setPipelineOutput(null);
  }

  function handleOpenOptions() {
    setShowSettingsSidebar(!showSettingsSidebar);
  }

  function extractConfigValue(obj) {
    const result = {};
    for (const [key, val] of Object.entries(obj)) {
      result[key] = val.value;
    }
    return result;
  }

  async function uploadGeoJSON() {
    try {
      setLoading(true);

      const geojsonObject = editorRef.current?.getValue();
      const geojsonConfig = config?.geojson || {};
      const geometryConfig = config?.geometry || {};

      const result = {
        ...extractConfigValue(geojsonConfig),
        geometry: extractConfigValue(geometryConfig),
      };

      const payload = {
        geojson: geojsonObject,
        config: result,
      };

      // Use apiRequest helper
      const pipelineResult = await apiRequest(
        endpoints.VALIDATE_GEOJSON_TEXT,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        },
        setToast,
      );

      setPipelineOutput(pipelineResult);
    } catch (err) {
      console.error("Validation error:", err);
      setPipelineOutput(null); // keep UI state clean on error
    } finally {
      setLoading(false);
    }
  }

  function handleFormatInput() {
    if (!editorRef.current) return;
    editorRef.current.getAction("editor.action.formatDocument").run();
  }

  return (
    <div className="h-full min-h-0 flex flex-col gap-4 xl:gap-8 box-border">
      <MainTitle />
      <div className="flex-1 flex flex-col gap-0">
        <div>
          <InputMenuBar
            handleUploadFile={handleUploadFile}
            handleAddSample={handleAddSample}
            handleFormatInput={handleFormatInput}
            handleFixInput={handleFixInput}
            settingsSidebarOpen={showSettingsSidebar}
            handleOpenOptions={handleOpenOptions}
            JSONState={JSONState}
            loading={loading}
          />
        </div>
        <div className="flex-1">
          <GeoJSONEditor
            editorConfig={config?.editor}
            editorRef={editorRef}
            value={inputGeoJSON}
            onChange={handleEditorChange}
          />
        </div>
      </div>
      <ValidateButton
        onClick={uploadGeoJSON}
        disabled={JSONState !== "valid" || loading}
        loading={loading}
      />
    </div>
  );
}
