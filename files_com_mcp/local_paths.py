import os
from pathlib import Path


class LocalPathError(ValueError):
    pass


def configured_local_root() -> Path | None:
    value = os.getenv("FILES_COM_LOCAL_ROOT")
    if not value:
        return None

    try:
        root = Path(value).expanduser()
        if not root.is_absolute():
            raise ValueError("expected an absolute directory path")
        root = root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("expected a directory")
    except (OSError, RuntimeError, ValueError) as error:
        raise LocalPathError(
            f"Invalid FILES_COM_LOCAL_ROOT: {error}"
        ) from error
    return root


def resolve_local_path(local_path: str, root: Path | None) -> str:
    if root is None:
        return local_path

    try:
        # The destination file may not exist yet when downloading.
        path = Path(local_path).resolve()
    except (OSError, RuntimeError, ValueError) as error:
        raise LocalPathError(f"Cannot resolve local path: {error}") from error

    if not path.is_relative_to(root):
        raise LocalPathError(
            f"Local path must be within FILES_COM_LOCAL_ROOT ({root})."
        )

    # Windows path comparisons can equate distinct directory names. Check
    # the filesystem identity of the matching ancestor before allowing it.
    ancestor = path
    for _ in path.relative_to(root).parts:
        ancestor = ancestor.parent
    try:
        same_root = ancestor.samefile(root)
    except OSError as error:
        raise LocalPathError(
            f"Cannot validate local directory: {error}"
        ) from error
    if not same_root:
        raise LocalPathError(
            f"Local path must be within FILES_COM_LOCAL_ROOT ({root})."
        )
    return str(path)
