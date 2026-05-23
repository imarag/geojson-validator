import Spinner from "./Spinner";

export default function ValidateButton({ onClick, disabled, loading }) {
  return (
    <div className="text-center flex justify-center items-center">
      <button
        type="button"
        className="btn btn-primary btn-lg btn-block"
        onClick={onClick}
        disabled={disabled}
      >
        {loading && <Spinner />}
        {loading ? "validating..." : "Validate"}
      </button>
    </div>
  );
}
