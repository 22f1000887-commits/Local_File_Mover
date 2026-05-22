# Research: Local File Mover UI

**Phase**: 0 - Research & Analysis  
**Date**: 2026-05-21  
**Status**: Complete

## Design Areas Investigated

### 1. Streamlit UI Patterns for File Operations

#### Decision: Text Input Fields for Path Entry

**What was chosen**: Use `st.text_input()` for both source and destination paths. Allow users to manually type or paste folder paths.

**Rationale**:
- More flexible than file picker widgets (users can use relative paths, network paths, UNC paths)
- Enables batch processing scripts and programmatic workflows
- Works consistently across all platforms (Windows, macOS, Linux)
- Allows copy-paste of recent paths without re-browsing

**Alternatives Considered**:
- Native file picker (`st.file_uploader`) - Limited to single files in web context; no folder selection
- Dropdown of recent paths - Less flexible; requires predefined paths
- Hybrid approach (picker + text) - Added complexity without proportional benefit

---

#### Decision: Session State Management with `st.session_state`

**What was chosen**: Use Streamlit's `st.session_state` dictionary to persist source/destination paths and operation history across page reruns.

**Rationale**:
- Native Streamlit feature; no external dependencies
- Aligns with Constitution Principle IV (Session State Awareness)
- Automatic cleanup when browser session ends (no disk clutter)
- Simple key-value interface

**Alternatives Considered**:
- Browser localStorage via JavaScript - Added complexity; security concerns; not needed for v1
- Client-side cookie storage - Limited size; unnecessary complexity
- File-based session store (JSON) - Overkill for single-user desktop app; disk I/O overhead

---

#### Decision: Progress Indication with `st.status()` Container

**What was chosen**: Use Streamlit's `st.status()` context manager to display operation progress. Update progress metrics dynamically within the container.

**Rationale**:
- Native Streamlit feature designed exactly for this use case
- Provides visual status indicator (running, completed, error) automatically
- Allows nested metrics/progress bar updates
- Clean UI without custom CSS/JavaScript

**Alternatives Considered**:
- Progress bar only (`st.progress()`) - Less information; hard to show which file is being processed
- Custom HTML/CSS - Violates Streamlit philosophy; maintenance burden
- Polling external API - Unnecessary; single-process execution

---

### 2. Python File Operations Best Practices

#### Decision: `pathlib.Path` + `shutil.move()` for File Movement

**What was chosen**: Use `pathlib.Path` for all path manipulation and `shutil.move()` for atomic file movement.

**Rationale**:
- `pathlib.Path` handles Windows/Unix path differences automatically; more readable than `os.path`
- `shutil.move()` is atomic (file removed from source after successful destination write)
- Works across filesystems (unlike `os.rename()`)
- Handles edge cases (overwrite behavior, directory moves) well-defined

**Alternatives Considered**:
- `os.rename()` - Not cross-filesystem; less portable
- Custom copy + delete - Error-prone; may abandon files on failure; violates atomic principle
- `os.replace()` - Similar to rename; not cross-filesystem safe

---

#### Decision: Validate Paths Before Transfer; Handle Errors Per-File

**What was chosen**: 
1. Validate both paths upfront (exist, accessible, no collisions)
2. Discover list of files to move
3. Move files one-by-one; log failures per file
4. Report partial success (e.g., "Moved 5 of 7 files") rather than all-or-nothing

**Rationale**:
- Fail-fast validation prevents corrupted state
- Per-file error handling allows partial success (user isn't blocked by one locked file)
- User feedback shows exactly which files succeeded/failed
- Aligns with Constitution Principle III (Error Resilience)

**Alternatives Considered**:
- All-or-nothing transaction - Too strict; single locked file blocks entire operation
- Rollback failed files - Complex, violates simplicity; users prefer to retry and fix issues
- Skip locked files silently - Poor UX; user doesn't know what happened

---

### 3. Error Handling & User Messaging

#### Decision: Error Categorization with Actionable Messages

**What was chosen**: Map Python exceptions and OS errors to user-friendly, actionable messages.

**Rationale**:
- Reduces support burden; users can self-serve
- Aligns with Spec FR-009 (descriptive error messages) and Constitution Principle III
- Meets success criterion SC-003 (95% error cases have actionable messages)

**Error Categories & Messages**:

| Scenario | Exception Type | User Message |
|----------|----------------|--------------|
| Source folder missing | `FileNotFoundError` | "Source folder not found at [path]. Check the folder name and try again." |
| Destination not writable | `PermissionError` | "Cannot write to [path]. Check folder permissions or choose a different destination." |
| File locked | `PermissionError` (during move) | "[filename] is in use by another program. Close the program and retry." |
| No disk space | `OSError` (ENOSPC) | "Not enough disk space at [path]. Free up space and retry." |
| Source = Destination | Custom validation | "Source and destination folders are the same. Choose different folders." |
| System directory | Custom validation | "System directories cannot be used. Choose a regular folder." |
| Invalid path characters | `ValueError` | "Path contains invalid characters. Check for <, >, ?, *, etc." |

**Alternatives Considered**:
- Raw Python exceptions - Users won't understand `FileNotFoundError`; violates UX principle
- Generic "Operation failed" - Users can't recover; poor experience
- Per-exception custom UI - Code smell; maintenance burden

---

### 4. Testing Strategies

#### Decision: Unit Tests with Mocked Paths + Integration Tests with Real Temp Directories

**What was chosen**:
- **Unit tests**: Mock path validation, error classification using `unittest.mock`
- **Integration tests**: Use `tempfile.TemporaryDirectory()` to create real file scenarios and verify behavior

**Rationale**:
- Unit tests are fast and isolated; good for logic testing
- Integration tests verify actual file system behavior (permissions, locks, errors)
- Temp directories are cleaned up automatically; no test pollution
- Covers both happy path and error scenarios

**Alternatives Considered**:
- Full mocking with pyfakefs - Adds dependency; benefits don't justify complexity
- Manual test folder management - Error-prone; slow cleanup
- No integration tests - Risky for file operations; must verify real behavior

---

#### Decision: Streamlit UI Testing via Manual Scripts

**What was chosen**: Provide manual testing checklist and example test data in quickstart.md; no automated UI tests (Streamlit testing framework is immature).

**Rationale**:
- Streamlit testing is still evolving; `streamlit.testing.v1` is limited
- Manual testing is sufficient for v1 scope (simple UI, few workflows)
- Example test scenarios and data provided for QA

**Alternatives Considered**:
- Selenium/Playwright automation - Heavy for simple UI; maintenance burden
- streamlit.testing.v1 framework - Limited capabilities; not suitable for interactive progress tracking

---

## Design Decisions Summary

| Area | Decision | Justification |
|------|----------|---------------|
| Path Input | Text fields | Flexible, copy-paste friendly, cross-platform |
| State Persistence | Streamlit session_state | Native, simple, auto-cleanup |
| Progress Feedback | st.status() container | Purpose-built, native UI |
| File Movement | pathlib + shutil.move() | Atomic, cross-filesystem, portable |
| Error Handling | Per-file + actionable messages | Partial success UX, supports recovery |
| Testing | Unit + Integration | Fast feedback + Real behavior verification |

---

## Next Steps

✅ Phase 0 Research complete. All design decisions documented with rationale and alternatives.

→ Proceed to Phase 1 (Design Artifacts: data-model.md, contracts, quickstart.md)
