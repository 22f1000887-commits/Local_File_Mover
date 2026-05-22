# Data Model: Local File Mover UI

**Phase**: 1 - Design & Contracts  
**Date**: 2026-05-21  
**Status**: Complete

## Core Entities

### FileOperation

Represents a single file movement operation instance.

**Fields**:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `operation_id` | str (UUID) | Unique identifier for this operation | Generated at operation start |
| `source_path` | str (absolute path) | Source folder path | Must exist, must be readable |
| `destination_path` | str (absolute path) | Destination folder path | Must be writable or creatable |
| `timestamp` | datetime | Operation start time | Auto-set on creation |
| `status` | Enum | Current operation state | See State Transitions below |
| `files_to_move` | List[Path] | Files discovered in source | Populated after discovery phase |
| `started_at` | datetime | Timestamp when transfer began | Null until transfer starts |
| `completed_at` | datetime | Timestamp when transfer ended | Null until transfer completes |
| `success_count` | int | Number of files successfully moved | Default: 0 |
| `failure_count` | int | Number of files that failed to move | Default: 0 |
| `moved_files` | List[str (filename)] | Files that were successfully moved | Populated during transfer |
| `failed_files` | List[{filename: str, reason: str, error_code: str}] | Files that failed with reasons | Populated during transfer |
| `user_cancelled` | bool | Whether user initiated cancellation | Default: false |

**Relationships**:

- One FileOperation contains many file transfer attempts
- Each FileOperation is independent; no parent-child relationships
- Session stores current and historical FileOperations

---

### FileTransferResult

Represents the outcome of moving a single file.

**Fields**:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `filename` | str | Name of the file (with extension) | Non-empty |
| `source_full_path` | Path | Full path in source folder | |
| `destination_full_path` | Path | Full path in destination folder | |
| `success` | bool | Whether transfer succeeded | true if file exists at destination |
| `error_code` | str | OS/app error code if failed | Null if success |
| `error_reason` | str | Human-readable error reason | See Error Classification section |
| `user_message` | str | User-facing action message | Actionable next step for user |
| `attempted_at` | datetime | When transfer was attempted | |
| `completed_at` | datetime | When transfer finished or failed | |

---

## Validation Rules

### Path Validation

**Source Path**:
- [ ] Must exist and be a directory (not a file)
- [ ] Must be readable (user has read permission)
- [ ] Must not be a system-critical directory (block: `C:\Windows\*`, `/System*`, `/usr/bin`, `/bin`, `/etc`)
- [ ] Must not be empty or null

**Destination Path**:
- [ ] Must exist as a directory OR be creatable (parent directory exists and is writable)
- [ ] Must be writable (user has write permission or parent has)
- [ ] Must not be a system-critical directory (same blocklist as source)
- [ ] Must not be null or empty

**Collision Prevention**:
- [ ] Source and destination must not be identical (case-insensitive on Windows, case-sensitive on Unix)
- [ ] Destination must not be a subdirectory of source (prevents data loss)

**Path Format**:
- [ ] Paths can be absolute or relative
- [ ] Relative paths resolved from current working directory
- [ ] No invalid path characters (< > : " / \ | ? *)

---

### File-Level Validation

Before moving each file:
- [ ] File exists in source
- [ ] File is a regular file (not directory, not symlink)
- [ ] File is readable
- [ ] Destination is writable
- [ ] If file exists in destination with same name:
  - [ ] Notify user and skip (or optionally allow overwrite with confirmation)
- [ ] If file is locked (in use):
  - [ ] Attempt move; if fails with permission error, report as locked

---

### Operation State Validation

| Current State | Allowed Next States | Validation |
|---------------|-------------------|-----------|
| `PENDING` | `IN_PROGRESS` | User clicked "Move"; paths valid |
| `IN_PROGRESS` | `COMPLETED`, `FAILED`, `CANCELLED` | Transfer ends or user cancels |
| `COMPLETED` | `PENDING` (new operation) | User clicks "Move" again |
| `FAILED` | `PENDING` (retry) | User clicks "Retry" |
| `CANCELLED` | `PENDING` (retry) | User clicks "Retry" |

---

## State Transitions & Workflows

### File Movement Workflow

```
User Provides Paths
        ↓
Validate Paths (FR-004)
        ↓
    [If valid]  [If invalid]
        ↓            ↓
    PENDING      Display Error
                   ↓
              User Corrects Path
                   ↓
              Retry validation
                   
[Back to User Provides Paths]
        ↓
User Clicks "Move Files"
        ↓
    IN_PROGRESS (start timer, show progress)
        ↓
    Discover files in source (FR-005: files only, no dirs)
        ↓
    For each file:
      - Attempt move (FR-003)
      - If success: add to moved_files
      - If fail (locked, permission): log error, continue
    
    [User may cancel at any time]
      ↓
COMPLETED or CANCELLED
      ↓
Display Results (FR-007)
      - Files moved: [count]
      - Files failed: [count]
      - Retry option if any failed
```

### Error Recovery Workflow

```
Operation Completes with Errors
      ↓
User Reviews Failed Files
      ↓
[Options]
  - Retry: Move PENDING → IN_PROGRESS with same paths
  - Cancel: Clear paths, start over
  - New paths: Update source/destination, retry
      ↓
User Clicks "Retry"
      ↓
Re-validate paths
      ↓
Attempt to move only failed files from previous attempt
      ↓
Display new results
```

---

## Error Classification

All file system errors are classified into user-facing categories:

| Error Category | OS Exceptions | User Message Template | Next Step Suggestion |
|---|---|---|---|
| **Path Not Found** | `FileNotFoundError`, `OSError(ENOENT)` | "Source folder not found at [PATH]. Check the folder name and try again." | Verify path spelling |
| **Permission Denied** | `PermissionError`, `OSError(EACCES)` | "Cannot write to [PATH]. Check folder permissions or choose a different destination." | Run as admin or change folder |
| **File Locked** | `PermissionError`, `OSError` during move | "[FILENAME] is in use. Close the program using this file and retry." | Close programs using file |
| **No Space** | `OSError(ENOSPC)` | "Not enough disk space at [PATH]. Free up space and retry." | Delete files or choose different destination |
| **Invalid Path** | `ValueError`, `OSError(EINVAL)` | "Path contains invalid characters. Check for <, >, ?, *, etc." | Fix path format |
| **Same Source/Dest** | Custom validation | "Source and destination are the same. Choose different folders." | Change destination |
| **System Directory** | Custom validation | "System directories cannot be used. Choose a regular folder." | Select user folder |
| **Not a Directory** | Custom validation | "[PATH] is not a folder. Select a folder path." | Provide folder path |

---

## Session State Structure

Streamlit `st.session_state` keys:

```python
{
    "source_path": str or None,           # Current source path input
    "destination_path": str or None,      # Current destination path input
    "last_operation": FileOperation,      # Last completed operation
    "operation_history": List[FileOperation],  # All operations in session
    "current_errors": List[str],          # Validation errors to display
    "show_results": bool,                 # Whether to display results section
}
```

---

## Logging & Audit Trail

All operations logged with context:

```
[2026-05-21 14:30:45] OPERATION_START
  operation_id: uuid-xxx
  source: /Users/alice/Downloads
  destination: /Users/alice/Archive
  files_found: 7

[2026-05-21 14:30:46] FILE_MOVED
  filename: document.pdf
  duration_ms: 45

[2026-05-21 14:30:47] FILE_FAILED
  filename: readonly.txt
  error: PermissionError
  reason: File locked
  
[2026-05-21 14:30:48] OPERATION_COMPLETE
  status: COMPLETED_WITH_ERRORS
  success: 6, failed: 1
  duration_ms: 3000
```

---

## Next Steps

✅ Data model defined with validation rules and state transitions.

→ Proceed to Phase 1 Contracts (ui-contract.md)
