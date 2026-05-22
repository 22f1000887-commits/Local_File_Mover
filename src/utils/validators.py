from pathlib import Path
import os

SYSTEM_BLOCKLIST = [
    "C:\\Windows",
    "/usr/bin",
    "/bin",
    "/etc",
    "/System",
]

def is_system_path(path: Path) -> bool:
    try:
        p = str(path)
        for blocked in SYSTEM_BLOCKLIST:
            if p.startswith(blocked):
                return True
    except Exception:
        return False
    return False

def validate_source_path(path_str: str):
    p = Path(path_str)
    if not p.exists():
        return False, "Source folder not found"
    if not p.is_dir():
        return False, "Source path is not a directory"
    if is_system_path(p):
        return False, "System directories are not allowed"
    if not os.access(p, os.R_OK):
        return False, "Source folder is not readable"
    return True, "OK"

def validate_destination_path(path_str: str, allow_create: bool = True):
    p = Path(path_str)
    if p.exists():
        if not p.is_dir():
            return False, "Destination exists and is not a directory"
        if is_system_path(p):
            return False, "System directories are not allowed"
        if not os.access(p, os.W_OK):
            return False, "Destination folder is not writable"
        return True, "OK"
    else:
        parent = p.parent
        if not parent.exists():
            return False, "Destination parent does not exist"
        if not os.access(parent, os.W_OK):
            return False, "Cannot create destination: parent not writable"
        if allow_create:
            return True, "OK (will create)"
        return False, "Destination does not exist"
