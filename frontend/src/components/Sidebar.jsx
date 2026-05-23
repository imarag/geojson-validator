import { IoClose } from "react-icons/io5";

export default function Sidebar({ onClose, ref, children }) {
  return (
    <div
      ref={ref}
      className="fixed top-0 bottom-0 start-0 flex flex-col overflow-x-visible bg-base-200 p-4 rounded-md w-88 shadow border border-white/10 z-50"
    >
      <div className="flex justify-between mb-8 items-center">
        <h2 className="text-start text-xl">Settings</h2>
        <button className="btn btn-rect btn-ghost" onClick={onClose}>
          <IoClose className="text-xl" />
        </button>
      </div>
      <div className="grow min-h-0">{children}</div>
    </div>
  );
}
