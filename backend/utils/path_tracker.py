from contextlib import contextmanager


class PathTracker:
    def __init__(self, root_part: str = "$"):
        self.root_part = root_part
        self.separator = "."
        self._parts: list[str] = []

    def __str__(self):
        return self.current()

    def __repr__(self):
        return f"PathTracker({self.current()})"

    @contextmanager
    def track(self, part: str | int):
        """Context manager: automatically push/pop path parts."""
        self.push(part)
        try:
            yield
        finally:
            self.pop()

    def push(self, part: str | int):
        if isinstance(part, int):
            part = f"[{part}]"
        else:
            part = self.separator + part
        self._parts.append(part)

    def pop(self):
        if not self._parts:
            print("Path underflow")
            return
        self._parts.pop()

    def current(self) -> str:
        return self.root_part + "".join(self._parts)

    def set_parts(self, parts: list[str]):
        """Set the tracker to a specific list of parts."""
        self._parts = parts.copy()

    def get_parts(self) -> list[str]:
        """Return a copy of the current parts list."""
        return self._parts.copy()

    def copy(self) -> "PathTracker":
        p = PathTracker()
        p.root_part = self.root_part
        p._parts = self._parts.copy()
        return p
