import { IoMdArrowDropdown } from "react-icons/io";

export default function DropDown({
  options,
  label,
  onClick,
  buttonSize = "medium",
  disabled,
}) {
  const buttonSizeMapping = {
    "extra-small": "btn-xs",
    small: "btn-sm",
    medium: "btn-md",
    large: "btn-lg",
  };
  return (
    <div className="dropdown">
      <div
        tabIndex={0}
        disabled={disabled}
        role="button"
        className={`btn btn-ghost ${buttonSizeMapping[buttonSize] || ""} m-1`}
      >
        {label}
        <IoMdArrowDropdown />
      </div>
      <ul
        tabIndex="-1"
        className="dropdown-content menu bg-base-200 rounded-box z-1 w-52 p-2 shadow-sm"
      >
        {options.map((option, index) => (
          <li key={index}>
            <a onClick={() => onClick(index)}>{option}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}
