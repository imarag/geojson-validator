export default function Collapse({ title, titleClassName = null, children }) {
  return (
    <div className="collapse collapse-arrow bg-base-100  overflow-visible">
      <input type="checkbox" />
      <div className={`collapse-title ${titleClassName || ""}`}>{title}</div>
      <div className="collapse-content text-sm overflow-hidden">{children}</div>
    </div>
  );
}
