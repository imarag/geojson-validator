export default function Container({ children }) {
  return (
    <div className="h-full flex flex-col items-center justify-center">
      {children}
    </div>
  );
}
