from pathlib import Path
import shutil
import time
from typing import List, Callable, Dict

def discover_files(source_path: str) -> List[Path]:
    p = Path(source_path)
    return [f for f in p.iterdir() if f.is_file()]

def move_file(source_file: Path, destination_folder: str) -> Dict:
    destination_folder_path = Path(destination_folder)
    destination_folder_path.mkdir(parents=True, exist_ok=True)
    dest = destination_folder_path / source_file.name
    result = {"filename": source_file.name, "success": False, "skipped": False, "error": None}

    if dest.exists():
        result["skipped"] = True
        result["error"] = "Destination file already exists"
        return result

    try:
        shutil.move(str(source_file), str(dest))
        result["success"] = True
    except Exception as e:
        result["error"] = str(e)
    return result

def move_files(source_path: str, destination_path: str, callback: Callable = None) -> Dict:
    start = time.time()
    files = discover_files(source_path)
    total = len(files)
    moved = []
    skipped = []
    failed = []
    for idx, f in enumerate(files, start=1):
        res = move_file(f, destination_path)
        if res["success"]:
            moved.append(res["filename"])
        elif res["skipped"]:
            skipped.append(res["filename"])
        else:
            failed.append({"filename": res["filename"], "reason": res["error"]})
        if callback:
            try:
                callback(res["filename"], idx, total)
            except Exception:
                pass
    end = time.time()
    return {
        "total": total,
        "moved_count": len(moved),
        "skipped_count": len(skipped),
        "failed_count": len(failed),
        "moved": moved,
        "skipped": skipped,
        "failed": failed,
        "duration_seconds": end - start,
    }
