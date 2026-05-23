import { IoClose } from "react-icons/io5";

export default function Toast({ message, type = "info", onClose }) {
  const typeMapping = {
    info: "alert-info",
    success: "alert-success",
    warning: "alert-warning",
    error: "alert-error",
  };
  return (
    <div className="toast toast-top toast-end">
      <div
        className={`min-w-min pe-8 py-4 alert ${typeMapping[type] || "alert-info"}`}
      >
        <span>{message}</span>
        <button
          className="btn btn-xs btn-rect btn-ghost absolute right-2 top-2 translate-y-2"
          onClick={onClose}
        >
          <IoClose className="text-lg" />
        </button>
      </div>
    </div>
  );
}
