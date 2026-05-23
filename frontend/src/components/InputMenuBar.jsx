import { FaRegCheckCircle } from "react-icons/fa";
import { FiUpload } from "react-icons/fi";
import { VscJson } from "react-icons/vsc";
import DropDown from "./DropDown";
import { geojsonSamples } from "../assets/sample-geojson";
import { useRef } from "react";
import { MdOutlineAutoFixHigh } from "react-icons/md";
import { VscTools } from "react-icons/vsc";
import { IoCloseCircleOutline } from "react-icons/io5";

function InputMenuBarButton({ text, icon: Icon, onClick, disabled }) {
  return (
    <button
      className="btn flex flex-row items-center gap-2 btn-ghost btn-sm"
      onClick={onClick}
      disabled={disabled}
    >
      <Icon />
      {text}
    </button>
  );
}

export default function InputMenuBar({
  handleUploadFile,
  handleAddSample,
  handleFormatInput,
  handleFixInput,
  JSONState,
  loading,
}) {
  const fileInputRef = useRef(null);
  const isJSONValid = JSONState === "valid";
  return (
    <div className="flex flex-row items-center py-1">
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        onChange={handleUploadFile}
      />
      <InputMenuBarButton
        text="upload file"
        icon={FiUpload}
        onClick={() => fileInputRef.current?.click()}
        disabled={loading}
      />
      <DropDown
        buttonSize="small"
        label={
          <span className="flex flex-row items-center gap-2">
            <VscJson /> add sample
          </span>
        }
        options={geojsonSamples.map((sample) => sample.title)}
        onClick={handleAddSample}
        disabled={loading}
      />
      <InputMenuBarButton
        text="prettify"
        icon={MdOutlineAutoFixHigh}
        onClick={handleFormatInput}
        disabled={JSONState !== "valid"}
      />
      <InputMenuBarButton
        text="Repair"
        icon={VscTools}
        onClick={handleFixInput}
        disabled={JSONState !== "invalid"}
      />
      {JSONState !== "idle" && (
        <p
          className={`flex items-center gap-2 text-sm ${isJSONValid ? "text-success" : "text-error"} ms-auto`}
        >
          <span>{isJSONValid ? "Valid JSON" : "Invalid JSON"}</span>
          {isJSONValid ? (
            <FaRegCheckCircle className="inline me-1" />
          ) : (
            <IoCloseCircleOutline className="inline me-1" />
          )}
        </p>
      )}
    </div>
  );
}
