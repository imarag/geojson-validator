export async function apiRequest(
  url,
  options = {},
  setToast,
  successMessage = null,
) {
  try {
    const response = await fetch(url, options);

    // Attempt to parse JSON
    let data;
    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    // Throw if status not OK
    if (!response.ok) {
      const errorMessage =
        data?.detail || data || `Server error ${response.status}`;
      throw new Error(errorMessage);
    }

    if (successMessage) {
      setToast({
        message: successMessage,
        type: "success",
        visible: true,
      });
    }
    return data;
  } catch (err) {
    console.error("API request error:", err);
    setToast({
      message: err.message || "Something went wrong. Please try again.",
      type: "error",
      visible: true,
    });
    throw err; // rethrow so caller can handle if needed
  }
}
