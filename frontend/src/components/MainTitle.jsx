import { FaLinkedin } from "react-icons/fa";

export default function MainTitle() {
  return (
    <div>
      <h2 className="text-4xl font-bold mb-2 text-center">GeoJSON validator</h2>
      <p className="text-base-content/50 text-xl mb-2 text-center">
        Input a GeoJSON string or upload a file and validate it.
      </p>
      <p className="text-center text-sm text-base-content/50 mb-4">
        By <span className="font-bold">Ioannis Maragkakis</span>
        <a
          className="link link-hover"
          href="https://www.linkedin.com/in/ioannis-maragkakis-1ba2851a9"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaLinkedin className="inline ms-2 text-xl" />
        </a>
      </p>
    </div>
  );
}
