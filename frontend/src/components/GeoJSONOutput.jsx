import { useState } from "react";
import GeoJSONIssues from "./GeoJSONIssues";
import GeoJSONMap from "./GeoJSONMap";

export default function GeoJSONOutput({ pipelineOutput, inputGeoJSON }) {
  const [showPanels, setShowPanels] = useState({ top: true, bottom: true });
  const isSuccess = pipelineOutput?.success === true;
  const issues = pipelineOutput?.result || [];

  const initialRender = pipelineOutput === null;
  const isSuccessWithIssues = isSuccess && issues.length > 0;
  // const isSuccessNoIssues = isSuccess && issues.length === 0;
  const isNotSuccess = !isSuccess && !initialRender;

  return (
    <div className="h-full">
      <div className="h-full flex flex-col gap-4 xl:gap-8">
        <div
          className={`${showPanels.top && "flex-1"} min-h-0 rounded-md bg-base-300`}
        >
          <GeoJSONIssues
            pipelineOutput={pipelineOutput}
            initialRender={initialRender}
            isNotSuccess={isNotSuccess}
            isSuccessWithIssues={isSuccessWithIssues}
            showPanels={showPanels}
            setShowPanels={setShowPanels}
          />
        </div>
        <div
          className={`${showPanels.bottom && "flex-1"} min-h-0 rounded-md bg-base-300 `}
        >
          <GeoJSONMap
            initialRender={initialRender}
            isNotSuccess={isNotSuccess}
            isSuccessWithIssues={isSuccessWithIssues}
            inputGeoJSON={inputGeoJSON}
            showPanels={showPanels}
            setShowPanels={setShowPanels}
          />
        </div>
      </div>
    </div>
  );
}
