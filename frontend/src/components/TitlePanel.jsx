import { BsArrowsExpand } from "react-icons/bs";
import { BsArrowsCollapse } from "react-icons/bs";

export default function TitlePanel({
  text,
  className,
  icon: Icon,
  handleTogglePanel,
  open,
}) {
  return (
    <div className="flex flex-row items-center justify-between px-4 py-1 xl:py-2 xl:px-8 border-b border-white/5">
      <h2 className={`font-bold ${className || ""} flex gap-2 items-center`}>
        <Icon />
        <span>{text}</span>
      </h2>
      <button className="btn btn-ghost" onClick={handleTogglePanel}>
        {open ? (
          <BsArrowsCollapse className="text-xl" />
        ) : (
          <BsArrowsExpand className="text-xl" />
        )}
      </button>
    </div>
  );
}
