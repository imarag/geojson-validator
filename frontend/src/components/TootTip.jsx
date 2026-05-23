export default function ToolTip({ message, children }) {
  return (
    <div className="tooltip z-50 tooltip-right">
      <div className="tooltip-content">
        <div className="max-w-50">{message}</div>
      </div>
      {children}
    </div>
  );
}
