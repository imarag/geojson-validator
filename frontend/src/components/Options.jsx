import Collapse from "./Collapse";
import { createPersistentConfig } from "../utils/storage";
import { storageConfigKey } from "../core/config";
import FormField from "./FormField";
import ToolTip from "./TootTip";
import { IoInformationCircleOutline } from "react-icons/io5";
import { MdOutlineCode } from "react-icons/md";
import { TbMap2 } from "react-icons/tb";
import { IoLayersOutline } from "react-icons/io5";
import { RiResetLeftLine } from "react-icons/ri";

function CollapseTitle({ title, icon: Icon }) {
  return (
    <span className="flex items-center gap-2">
      <Icon className="text-lg" />
      {title}
    </span>
  );
}

function ResetButton({ onClick }) {
  return (
    <button
      className="btn btn-ghost btn-xs flex items-center mb-4"
      onClick={onClick}
    >
      <RiResetLeftLine />
      <span>restore defaults</span>
    </button>
  );
}

export default function Options({ config, setConfig, configBackup }) {
  const configOptions = [
    {
      title: "JSON editor",
      icon: MdOutlineCode,
      configKey: "editor",
      description:
        "Change the editor appearance between light, dark, or high contrast mode.",
      data: Object.entries(config?.editor).map(([key, value]) => [key, value]),
    },
    {
      title: "GeoJSON Validation",
      icon: TbMap2,
      configKey: "geojson",
      description: "Configure the GeoJSON validation rules and constraints.",
      data: Object.entries(config?.geojson).map(([key, value]) => [key, value]),
    },
    {
      title: "Geometry Validation",
      icon: IoLayersOutline,
      configKey: "geometry",
      description: "Configure the geometry properties.",
      data: Object.entries(config?.geometry).map(([key, value]) => [
        key,
        value,
      ]),
    },
  ];

  return (
    <ul className="space-y-4">
      {configOptions.map((configOption) => (
        <li key={configOption.title}>
          <Collapse
            title={
              <CollapseTitle
                title={configOption.title}
                icon={configOption.icon}
              />
            }
          >
            <div>
              <div className="flex justify-end">
                <ResetButton
                  onClick={() =>
                    setConfig((prev) => {
                      const updated = { ...prev };
                      updated[configOption.configKey] =
                        configBackup[configOption.configKey];
                      createPersistentConfig(updated, storageConfigKey);
                      return updated;
                    })
                  }
                />
              </div>
              <div className="flex flex-col items-stretch gap-4">
                {configOption.data.map(([key, value]) => (
                  <div key={key} className="flex flex-col items-stretch gap-8">
                    <FormField
                      {...value}
                      label={
                        <div className="flex items-center justify-between gap-2">
                          <ToolTip message={value.description}>
                            <IoInformationCircleOutline className="inline ml-1 text-sm" />
                          </ToolTip>
                          <span>{value.label}</span>
                        </div>
                      }
                      onChange={(e) => {
                        const newValue =
                          e.target.type === "checkbox"
                            ? e.target.checked
                            : e.target.value;

                        setConfig((prev) => {
                          const updated = { ...prev };
                          updated[configOption.configKey] = {
                            ...prev[configOption.configKey],
                            [key]: {
                              ...prev[configOption.configKey][key],
                              value: newValue,
                            },
                          };
                          createPersistentConfig(updated, storageConfigKey);
                          return updated;
                        });
                      }}
                    />
                  </div>
                ))}
              </div>
            </div>
          </Collapse>
        </li>
      ))}
    </ul>
  );
}
