# UI Contract: Local File Mover Application

**Phase**: 1 - Design & Contracts  
**Date**: 2026-05-21  
**Framework**: Streamlit

## Overview

This document defines the Streamlit UI component structure, layout, interaction flows, and state management for the Local File Mover application.

---

## Component Hierarchy

```
📦 StreamlitFileMovApp (main.py)
├── 🎨 Page Header
│   ├── Title: "Local File Mover"
│   └── Instructions: "Move files from one folder to another"
│
├── 📊 Session Status (visible at all times)
│   └── Display: Last operation status or "Ready"
│
├── 📝 Input Section (always visible, editable)
│   ├── Source Path Input (text input)
│   ├── Source Path Status (✓ valid / ✗ error)
│   ├── Destination Path Input (text input)
│   ├── Destination Path Status (✓ valid / ✗ error)
│   └── "Move Files" Button (enabled/disabled based on validation)
│
├── ⏳ Progress Section (visible during IN_PROGRESS)
│   ├── Status Container
│   │   ├── Progress Bar (percentage)
│   │   ├── Metrics: "Files moved: X / Total: Y"
│   │   ├── Current File Display: "[filename] ..."
│   │   └── Elapsed Time
│   └── Cancel Button
│
├── ✅ Results Section (visible after COMPLETED/FAILED/CANCELLED)
│   ├── Result Alert (success or error styling)
│   ├── Summary Metrics
│   │   ├── "✓ Successfully moved: X files"
│   │   └── "✗ Failed: Y files"
│   ├── Results Table (if any failures)
│   │   ├── Filename
│   │   ├── Error Reason
│   │   └── Suggested Action
│   └── Action Buttons
│       ├── "Retry" (if failures)
│       ├── "Clear & Start Over"
│       └── [Optional] "View Log"
│
└── 📋 Expandable Log Section (debug/advanced)
    └── Operation log (timestamp, file, status)
```

---

## Page States & Layouts

### State 1: Initial (PENDING)

**When**: App loaded with no operation in progress

**Visible Components**:
- Header
- Session Status: "Ready to transfer"
- Input Section (fully interactive)
- Progress Section: Hidden
- Results Section: Hidden

**User Actions**: Enter paths, click "Move Files"

```
┌─────────────────────────────────────────┐
│ Local File Mover                        │
│ Move files from one folder to another   │
├─────────────────────────────────────────┤
│ Ready to transfer                       │
├─────────────────────────────────────────┤
│ Source Folder Path                      │
│ [____________________________________________] ✓
│ Destination Folder Path                 │
│ [____________________________________________] ✗ (not found)
├─────────────────────────────────────────┤
│ [Move Files] (disabled)                 │
└─────────────────────────────────────────┘
```

---

### State 2: In Progress (IN_PROGRESS)

**When**: User clicked "Move Files"; transfer is running

**Visible Components**:
- Header
- Session Status: "Moving files..."
- Input Section: Disabled (read-only)
- Progress Section: Visible
- Results Section: Hidden

**User Actions**: Watch progress, optionally cancel

```
┌─────────────────────────────────────────┐
│ Local File Mover                        │
│ Move files from one folder to another   │
├─────────────────────────────────────────┤
│ Moving files...                         │
├─────────────────────────────────────────┤
│ Source Folder Path                      │
│ [C:/Users/alice/Downloads       ] (readonly)
│ Destination Folder Path                 │
│ [C:/Users/alice/Archive         ] (readonly)
├─────────────────────────────────────────┤
│ ✓ Moving files                          │
│   Progress: ████████░░░░░░░░░ 58%       │
│   Files moved: 4 / 7                    │
│   Current: document.pdf ...             │
│   Elapsed: 0m 3s                        │
│ [Cancel]                                │
└─────────────────────────────────────────┘
```

---

### State 3: Completed (COMPLETED)

**When**: All files moved successfully

**Visible Components**:
- Header
- Session Status: "Completed successfully"
- Input Section: Editable (user can run again)
- Progress Section: Hidden
- Results Section: Visible (success variant)

**User Actions**: Run again, clear and start over

```
┌─────────────────────────────────────────┐
│ Local File Mover                        │
├─────────────────────────────────────────┤
│ ✓ Completed successfully                │
├─────────────────────────────────────────┤
│ Source Folder Path                      │
│ [C:/Users/alice/Downloads       ]       │
│ Destination Folder Path                 │
│ [C:/Users/alice/Archive         ]       │
├─────────────────────────────────────────┤
│ [Move Files]                            │
├─────────────────────────────────────────┤
│ ✓ Successfully moved 7 files            │
│ All files transferred without errors.   │
│ [Move Again] [Clear & Start Over]       │
└─────────────────────────────────────────┘
```

---

### State 4: Failed with Errors (COMPLETED_WITH_ERRORS)

**When**: Some files failed to move

**Visible Components**:
- Header
- Session Status: "Completed with errors"
- Input Section: Editable
- Progress Section: Hidden
- Results Section: Visible (error variant + failed files table)

**User Actions**: Retry failed files, modify paths and retry, or start over

```
┌─────────────────────────────────────────┐
│ Local File Mover                        │
├─────────────────────────────────────────┤
│ ⚠ Completed with errors                 │
├─────────────────────────────────────────┤
│ Source: C:/Users/alice/Downloads        │
│ Destination: C:/Users/alice/Archive     │
│ [Move Again] [Clear]                    │
├─────────────────────────────────────────┤
│ ✓ Successfully moved: 5 files           │
│ ✗ Failed: 2 files                       │
│ Reason: Some files are locked           │
│                                         │
│ Failed Files:                           │
│ ┌─────────────────────────────────────┐ │
│ │ Filename | Error | Suggestion      │ │
│ ├─────────────────────────────────────┤ │
│ │ config.ini | File locked | Close... │ │
│ │ app.exe    | File locked | Close... │ │
│ └─────────────────────────────────────┘ │
│ [Retry Failed] [Retry All]              │
└─────────────────────────────────────────┘
```

---

### State 5: Validation Error (PENDING with errors)

**When**: User entered invalid paths; validation failed

**Visible Components**:
- Header
- Session Status: "Validation error"
- Input Section: Interactive with error indicators
- Progress/Results: Hidden

**User Actions**: Correct paths and retry

```
┌─────────────────────────────────────────┐
│ Local File Mover                        │
├─────────────────────────────────────────┤
│ ✗ Validation error                      │
├─────────────────────────────────────────┤
│ Source Folder Path                      │
│ [C:/nonexistent/path           ] ✗     │
│ ✗ Folder not found. Check path spelling │
│ Destination Folder Path                 │
│ [C:/Users/alice/Archive        ] ✓     │
├─────────────────────────────────────────┤
│ [Move Files] (disabled)                 │
│ Fix the error above to proceed.         │
└─────────────────────────────────────────┘
```

---

## Input Validation UI Feedback

### Path Input Validation

**Trigger**: On text change (debounced 500ms) or on blur

**Validation Flow**:

```
User types path
      ↓
After 500ms debounce:
  - Check path exists
  - Check is directory
  - Check readable (for source) / writable (for dest)
      ↓
If valid:
  - Show ✓ checkmark in green
  - Enable "Move Files" button (if both paths valid)
      ↓
If invalid:
  - Show ✗ with error message
  - Disable "Move Files" button
  - Display actionable message (e.g., "Check path spelling")
```

**Example: Valid Source Path**

```
Source Folder Path
[C:/Users/alice/Downloads              ] ✓
(green checkmark, path found and readable)
```

**Example: Invalid Destination Path**

```
Destination Folder Path
[/mnt/invalid/network/share            ] ✗
✗ Cannot write to this folder. Check permissions or choose different destination.
```

---

## Button States

### "Move Files" Button

| Condition | State | Action |
|-----------|-------|--------|
| Both paths valid, no operation running | Enabled | Click to start transfer |
| Source or destination invalid | Disabled | Show tooltip: "Fix validation errors above" |
| Operation in progress | Hidden | Replaced by "Cancel" |
| Operation completed | Re-enabled | Click to move again |

---

## Progress Feedback During Transfer

### Progress Container (st.status)

```
Status: ✓ Moving files

Inside container:
  - Progress bar: ████████░░░░░░░░░ 58%
  - Metrics:
    - Files moved: 4 / 7
    - Current file: document.pdf
    - Elapsed time: 0m 3s
  - [Cancel] button
```

**Update Frequency**: Every 100ms or per file (whichever is slower)

**Cancellation**: User clicks [Cancel] button
- Sets `operation.user_cancelled = True`
- Stops processing additional files
- Completes current file if possible
- Transitions to CANCELLED state
- Displays: "Operation cancelled by user. 4 of 7 files moved."

---

## Results Display

### Success Results

```
✓ Successfully moved 7 files

All files transferred without errors.
No further action needed.

[Move Again] [Clear & Start Over]
```

### Failed Results (Table)

| Column | Content | Example |
|--------|---------|---------|
| Filename | Name of file that failed | `config.ini` |
| Error | Category of error | "File Locked" |
| Suggestion | User action to resolve | "Close programs using this file and retry" |

**Table is sortable**: User can click column header to sort

---

## Keyboard Shortcuts & Accessibility

| Action | Shortcut | Notes |
|--------|----------|-------|
| Focus source path | Tab | Default focus on page load |
| Focus destination | Tab | |
| Submit (Move Files) | Enter | When "Move Files" button focused |
| Cancel operation | Escape | During transfer |
| Clear form | Ctrl+L | Clear both paths |

---

## Session State Integration

Streamlit `st.session_state` keys used:

```python
st.session_state.source_path        # str: current source input
st.session_state.destination_path   # str: current destination input
st.session_state.current_operation  # FileOperation: active operation
st.session_state.validation_errors  # List[str]: errors to display
st.session_state.show_results       # bool: show results section
st.session_state.last_success_count # int: for UX feedback
```

---

## Error Messages Reference

| Scenario | Message | Styling |
|----------|---------|---------|
| Path not found | "Folder not found at [path]. Check spelling." | ✗ Red |
| Permission error | "Cannot access [path]. Check permissions." | ✗ Red |
| Same source/dest | "Source and destination are the same." | ⚠ Yellow |
| Operation failed | "[N] files failed to move." | ⚠ Yellow |
| Success | "All files moved successfully." | ✓ Green |
| Cancelled | "Operation cancelled. [N] files moved." | ⓘ Blue |

---

## Next Steps

✅ UI Contract defined with component hierarchy, states, and interactions.

→ Proceed to Phase 1 Quickstart Guide (quickstart.md)
