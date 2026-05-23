import { useMemo } from "react";
import { TbMapSearch } from "react-icons/tb";
import MapViewer from "./MapViewer";
import OutputMessage from "./OutputMessage";
import Container from "./Container";
import TitlePanel from "./TitlePanel";
import { LiaMapMarkedAltSolid } from "react-icons/lia";

export default function GeoJSONMap({
  initialRender,
  isNotSuccess,
  isSuccessWithIssues,
  inputGeoJSON,
  showPanels,
  setShowPanels,
}) {
  const parsedGeoJSON = useMemo(() => {
    if (!inputGeoJSON) return null;

    try {
      return JSON.parse(inputGeoJSON);
    } catch (err) {
      return null;
    }
  }, [inputGeoJSON]);

  return (
    <div className="flex flex-col h-full">
      <div>
        <TitlePanel
          text="Map Preview"
          icon={LiaMapMarkedAltSolid}
          handleTogglePanel={() =>
            setShowPanels((prev) => ({ ...prev, bottom: !prev.bottom }))
          }
          open={showPanels.bottom}
        />
      </div>
      <div className="flex-1">
        {showPanels.bottom && (
          <>
            {initialRender ? (
              <Container>
                <OutputMessage
                  icon={TbMapSearch}
                  message="No GeoJSON to display the map preview."
                  direction="col"
                />
              </Container>
            ) : isNotSuccess ? (
              <Container>
                <OutputMessage
                  message="Error validating GeoJSON. Please check your input to see the map
          preview."
                  direction="col"
                  className="text-error"
                />
              </Container>
            ) : isSuccessWithIssues ? (
              <Container>
                <OutputMessage
                  message="GeoJSON has issues and cannot be displayed. Please fix the issues to
          see the map preview."
                  direction="col"
                  className="text-error"
                />
              </Container>
            ) : (
              <div className="h-full">
                <MapViewer geojson={parsedGeoJSON} />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
