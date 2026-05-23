import { useState, useRef, useEffect } from "react";
import GeoJSONOutput from "./components/GeoJSONOutput";
import GeoJSONInput from "./components/GeoJSONInput";
import Toast from "./components/Toast";
import Sidebar from "./components/Sidebar";
import { RiMenuUnfoldLine } from "react-icons/ri";
import Options from "./components/Options";
import { editorSettingsSchema } from "./core/editor-config";
import { storageConfigKey, storageThemeKey } from "./core/config";
import { endpoints } from "./core/urls";
import "leaflet/dist/leaflet.css";
import { appThemes } from "./core/config";
import ThemeController from "./components/ThemeController";

function App() {
  const [pipelineOutput, setPipelineOutput] = useState(null);
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem(storageThemeKey);
    return stored ? stored : appThemes["dark"];
  });
  const [showSettingsSidebar, setShowSettingsSidebar] = useState(false);
  const [inputGeoJSON, setInputGeoJSON] = useState(null);
  const [config, setConfig] = useState(() => {
    const stored = localStorage.getItem(storageConfigKey);
    return stored ? JSON.parse(stored) : null;
  });
  const [configBackup, setConfigBackup] = useState(() => config);
  const [toast, setToast] = useState({
    message: "",
    type: "info",
    visible: false,
  });
  const sidebarRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      // If sidebar is closed, do nothing
      if (!showSettingsSidebar) return;

      // If ref exists and click target is NOT inside sidebar
      if (sidebarRef.current && !sidebarRef.current.contains(event.target)) {
        setShowSettingsSidebar(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showSettingsSidebar]);

  useEffect(() => {
    async function fetchSchemas() {
      try {
        const [geojsonRes, geometryRes] = await Promise.all([
          fetch(endpoints.GET_GEOJSON_CONFIG_SCHEMA),
          fetch(endpoints.GET_GEOMETRY_CONFIG_SCHEMA),
        ]);

        const [geojsonSchema, geometrySchema] = await Promise.all([
          geojsonRes.json(),
          geometryRes.json(),
        ]);

        const combinedSchema = {
          editor: editorSettingsSchema,
          geojson: geojsonSchema,
          geometry: geometrySchema,
        };

        setConfig(combinedSchema);
        setConfigBackup(combinedSchema);
        localStorage.setItem(storageConfigKey, JSON.stringify(combinedSchema));
      } catch (error) {
        console.error("Failed to fetch schemas:", error);
      }
    }
    if (config !== null) return; // already loaded from storage
    fetchSchemas();
  }, [config]);

  return (
    <div
      className="h-screen flex gap-4 xl:gap-8 p-4 xl:p-8 box-border"
      data-theme={theme}
    >
      {!showSettingsSidebar && (
        <button
          className="btn btn-ghost absolute top-8 left-8"
          onClick={() => setShowSettingsSidebar(true)}
        >
          <RiMenuUnfoldLine className="text-xl" />
        </button>
      )}
      {toast.visible && (
        <div className="absolute top-4 right-4 z-50">
          <Toast
            message={toast.message}
            type={toast.type}
            onClose={() => setToast({ ...toast, visible: false })}
          />
        </div>
      )}
      {showSettingsSidebar && (
        <Sidebar onClose={() => setShowSettingsSidebar(false)} ref={sidebarRef}>
          <div className="h-full flex flex-col gap-4">
            <div className="flex-1 overflow-scroll">
              <Options
                config={config}
                setConfig={setConfig}
                configBackup={configBackup}
              />
            </div>
            <div className="flex items-center justify-center">
              <ThemeController theme={theme} setTheme={setTheme} />
            </div>
          </div>
        </Sidebar>
      )}

      <div className="flex-1">
        <GeoJSONInput
          setPipelineOutput={setPipelineOutput}
          setToast={setToast}
          inputGeoJSON={inputGeoJSON}
          setInputGeoJSON={setInputGeoJSON}
          showSettingsSidebar={showSettingsSidebar}
          setShowSettingsSidebar={setShowSettingsSidebar}
          config={config}
        />
      </div>
      <div className="flex-1">
        <GeoJSONOutput
          pipelineOutput={pipelineOutput}
          toast={toast}
          inputGeoJSON={inputGeoJSON}
        />
      </div>
    </div>
  );
}

export default App;
