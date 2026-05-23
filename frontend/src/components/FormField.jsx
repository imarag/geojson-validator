import { useId } from "react";

export default function FormField({
  type = "text",
  value,
  onChange,
  label = null,
  size = "medium",
  options = [],
  labelCenter = false,
  labelTagDirection = "column",
  ...inputProps
}) {
  const generatedId = useId();

  const inputId = inputProps.id ?? generatedId;
  const inputName = inputProps.name ?? inputId;

  // Size mappings grouped by element type
  const sizeMapping = {
    input: {
      extraSmall: "input-xs",
      small: "input-sm",
      medium: "input-md",
      large: "input-lg",
      extraLarge: "input-xl",
    },
    select: {
      extraSmall: "select-xs",
      small: "select-sm",
      medium: "select-md",
      large: "select-lg",
      extraLarge: "select-xl",
    },
    textarea: {
      extraSmall: "textarea-xs",
      small: "textarea-sm",
      medium: "textarea-md",
      large: "textarea-lg",
      extraLarge: "textarea-xl",
    },
    radio: {
      extraSmall: "radio-xs",
      small: "radio-sm",
      medium: "radio-md",
      large: "radio-lg",
      extraLarge: "radio-xl",
    },
    checkbox: {
      extraSmall: "checkbox-xs",
      small: "checkbox-sm",
      medium: "checkbox-md",
      large: "checkbox-lg",
      extraLarge: "checkbox-xl",
    },
  };

  const globalClass = "w-full";

  const sizeClass = sizeMapping[type]?.[size] ?? sizeMapping[type]?.medium;

  // =============================
  // Render element
  // =============================

  let fieldElement;

  if (type === "select") {
    fieldElement = (
      <select
        {...inputProps}
        id={inputId}
        name={inputName}
        value={value}
        onChange={onChange}
        className={`select ${sizeClass} ${globalClass}`}
      >
        {(options ?? []).map((opt) => (
          <option key={String(opt.value)} value={opt.value}>
            {String(opt.label)}
          </option>
        ))}
      </select>
    );
  } else if (type === "textarea") {
    fieldElement = (
      <textarea
        {...inputProps}
        id={inputId}
        name={inputName}
        value={value}
        onChange={onChange}
        className={`textarea ${sizeClass} ${globalClass}`}
      />
    );
  } else if (type === "checkbox") {
    fieldElement = (
      <input
        {...inputProps}
        id={inputId}
        name={inputName}
        type="checkbox"
        checked={Boolean(value)}
        onChange={onChange}
        className={`checkbox ${sizeClass}`}
      />
    );
  } else if (type === "radio") {
    fieldElement = (
      <input
        {...inputProps}
        id={inputId}
        name={inputName}
        type="radio"
        value={value}
        onChange={onChange}
        className={`radio ${sizeClass}`}
      />
    );
  } else {
    fieldElement = (
      <input
        {...inputProps}
        id={inputId}
        name={inputName}
        type={type}
        value={value}
        onChange={onChange}
        className={`input ${sizeClass} ${globalClass}`}
      />
    );
  }

  // =============================
  // Layout
  // =============================

  return (
    <div
      className={`flex ${
        labelTagDirection === "column" ? "flex-col" : "flex-row"
      } ${
        labelTagDirection === "column" ? "items-stretch" : "items-center"
      } gap-2`}
    >
      {label && (
        <label
          htmlFor={inputId}
          className={`label ${labelCenter ? "mx-auto" : ""}`}
        >
          {label}
        </label>
      )}

      <div>{fieldElement}</div>
    </div>
  );
}
