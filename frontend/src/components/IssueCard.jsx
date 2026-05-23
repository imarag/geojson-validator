import Collapse from "./Collapse";

export default function IssueCard({ issue }) {
  const filterFields = ["message", "issue_code", "repair_context"];

  return (
    <Collapse title={issue.message} titleClassName="py-2 px-4 text-sm">
      <div className="space-y-2">
        {Object.keys(issue)
          .filter((key) => !filterFields.includes(key))
          .map((key) => {
            const value = issue[key];

            const renderValue = (val) => {
              if (typeof val === "boolean") {
                return val ? "Yes" : "No";
              }
              return String(val);
            };

            return (
              <div>
                <h3 className="font-semibold text-base-content/80">{key}</h3>
                {value && typeof value === "object" && !Array.isArray(value) ? (
                  <ul>
                    {Object.entries(value).map(([k, v]) => (
                      <li key={k}>
                        <span className="text-base-content/50">{k}</span>:{" "}
                        <span className="text-base-content/50">
                          {renderValue(v)}
                        </span>
                      </li>
                    ))}
                  </ul>
                ) : /* Array → stringify */
                Array.isArray(value) ? (
                  <p className="text-base-content/50">
                    {JSON.stringify(value)}
                  </p>
                ) : (
                  /* Primitive */
                  <p className="text-base-content/50">{renderValue(value)}</p>
                )}
              </div>
            );
          })}
      </div>
    </Collapse>
  );
}
