export default function OutputMessage({
  icon: Icon = null,
  message,
  direction = "col",
  className,
}) {
  return (
    <p
      className={`flex flex-${direction} items-center gap-4 p-8 ${className || ""}`}
    >
      {Icon && <Icon className="text-4xl" />}
      <span>{message}</span>
    </p>
  );
}
