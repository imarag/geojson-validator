import { useState } from "react";
import { BsCheckCircleFill } from "react-icons/bs";
import { VscJson } from "react-icons/vsc";
import OutputMessage from "./OutputMessage";
import IssueCard from "./IssueCard";
import Container from "./Container";
import TitlePanel from "./TitlePanel";
import { LuClipboardList } from "react-icons/lu";

function IssuesList({ issues, currentStatus }) {
  return (
    <>
      {issues.length > 0 ? (
        issues.map((issue, index) => <IssueCard key={index} issue={issue} />)
      ) : (
        <OutputMessage
          message={`No ${currentStatus} issues to display.`}
          className="mt-8"
        />
      )}
    </>
  );
}

function StatusBar({ totalIssues, issueStatus, setIssueStatus }) {
  return (
    <div className="flex justify-between items-center mb-4">
      <div className="flex flex-wrap gap-2">
        {["all", "warning", "error", "critical"].map((status) => (
          <button
            key={status}
            className={`btn btn-xs btn-secondary ${issueStatus === status ? "btn-secondary" : "btn-ghost"}`}
            onClick={() => setIssueStatus(status)}
          >
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </button>
        ))}
      </div>
      <span className="text-sm">total: {totalIssues}</span>
    </div>
  );
}

export default function GeoJSONIssues({
  pipelineOutput,
  initialRender,
  isNotSuccess,
  isSuccessWithIssues,
  showPanels,
  setShowPanels,
}) {
  const issues = pipelineOutput?.result || [];
  const [issueStatus, setIssueStatus] = useState("all");

  const filteredIssues =
    issueStatus === "all"
      ? issues
      : issues.filter((issue) => issue.severity.toLowerCase() === issueStatus);
  const totalIssues = issues.length;

  // Success: no issues
  return (
    <div className="flex flex-col h-full">
      <TitlePanel
        text="Validation Issues"
        icon={LuClipboardList}
        handleTogglePanel={() =>
          setShowPanels((prev) => ({ ...prev, top: !prev.top }))
        }
        open={showPanels.top}
      />
      <div className="flex-1 min-h-0">
        {showPanels.top && (
          <div className="h-full">
            {initialRender ? (
              <Container>
                <OutputMessage
                  icon={VscJson}
                  message="No GeoJSON to validate."
                  direction="col"
                />
              </Container>
            ) : isNotSuccess ? (
              <Container>
                <OutputMessage
                  message="Error validating GeoJSON. Please check your input or try again."
                  direction="col"
                  className="text-error"
                />
              </Container>
            ) : isSuccessWithIssues ? (
              <div className="flex flex-col h-full p-4 xl:p-8">
                <StatusBar
                  totalIssues={totalIssues}
                  issueStatus={issueStatus}
                  setIssueStatus={setIssueStatus}
                />
                <div className="h-full flex-1 overflow-scroll space-y-4">
                  <IssuesList
                    issues={filteredIssues}
                    currentStatus={issueStatus}
                  />
                </div>
              </div>
            ) : (
              <Container>
                <OutputMessage
                  icon={BsCheckCircleFill}
                  message="GeoJSON is valid. No issues found."
                  direction="col"
                  className="text-success"
                />
              </Container>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
