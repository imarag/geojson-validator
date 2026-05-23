export function createPersistentConfig(config, storageKey) {
  try {
    const configString = JSON.stringify(config);
    localStorage.setItem(storageKey, configString);
  } catch (err) {
    console.error("Failed to save config to localStorage:", err);
  }
}
