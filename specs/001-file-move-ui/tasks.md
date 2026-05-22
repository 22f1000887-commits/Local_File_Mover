---

description: "Task list for Local File Mover UI feature implementation"
---

# Tasks: Local File Mover UI

**Input**: Design documents from `/specs/001-file-move-ui/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/, research.md

**Tests**: Integration tests included for end-to-end validation; manual Streamlit UI testing via quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- `src/` - Main application source code (repository root)
- `tests/` - Test files
- Paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure with src/, tests/unit/, tests/integration/, tests/fixtures/ directories
- [ ] T002 Create requirements.txt with dependencies: streamlit>=1.28.0, pytest>=7.0, pytest-cov>=4.0
- [ ] T003 Create .streamlit/config.toml with Streamlit configuration (logger level, client maxMessageSize, etc.)
- [ ] T004 Create src/main.py as Streamlit app entry point with placeholder "Local File Mover" title
- [ ] T005 Create README.md with project description, setup instructions, and usage guide
- [ ] T006 Create .gitignore for Python projects (venv, __pycache__, *.pyc, .streamlit/secrets.toml, etc.)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [P] Create src/models/file_operation.py with FileOperation class (operation_id, source_path, destination_path, status, timestamps, success_count, failure_count, moved_files, failed_files)
- [ ] T008 [P] Create src/models/file_operation.py with FileTransferResult class (filename, source_full_path, destination_full_path, success, error_code, error_reason, user_message, timestamps)
- [ ] T009 [P] Create src/utils/validators.py with validate_source_path() function that checks: exists, is_directory, readable, not_system_critical
- [ ] T010 [P] Create src/utils/validators.py with validate_destination_path() function that checks: writable_or_creatable, not_system_critical, not_same_as_source
- [ ] T011 [P] Create src/utils/validators.py with validate_paths_not_collision() function for source != destination and no subdirectory collision checks
- [ ] T012 [P] Create src/services/error_handler.py with error classification mapping (FileNotFoundError → "Source folder not found", PermissionError → "Cannot write to folder", etc.)
- [ ] T013 [P] Create src/services/error_handler.py with format_error_message() function that returns user-friendly, actionable error messages per error category
- [ ] T014 [P] Create src/ui/session_manager.py with init_session_state() function to initialize st.session_state keys (source_path, destination_path, current_operation, validation_errors, show_results)
- [ ] T015 [P] Create src/utils/logging_config.py with setup_logging() function that configures Python logging with context (file path, operation, timestamp) to file_mover.log
- [ ] T016 Create src/__init__.py as package marker
- [ ] T017 Create src/models/__init__.py as package marker
- [ ] T018 Create src/services/__init__.py as package marker
- [ ] T019 Create src/ui/__init__.py as package marker
- [ ] T020 Create src/utils/__init__.py as package marker

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic File Transfer (Priority: P1) 🎯 MVP

**Goal**: Enable users to move all files from source to destination with visual feedback

**Independent Test**: Create test_source folder with 5 test files, set test_destination, execute move, verify files transferred and source empty

### Tests for User Story 1 (OPTIONAL - provided for reference)

- [ ] T021 [P] [US1] Create tests/unit/test_validators.py with test cases for validate_source_path (exists, not exists, not directory, permission)
- [ ] T022 [P] [US1] Create tests/unit/test_validators.py with test cases for validate_destination_path (writable, not writable, collision detection)
- [ ] T023 [P] [US1] Create tests/unit/test_file_mover.py with test case test_move_single_file that uses tempfile.TemporaryDirectory
- [ ] T024 [P] [US1] Create tests/unit/test_file_mover.py with test case test_move_multiple_files that verifies success count and all files present in destination
- [ ] T025 [P] [US1] Create tests/unit/test_error_handler.py with test cases for each error category (FileNotFoundError, PermissionError, etc.)
- [ ] T026 [US1] Create tests/fixtures/test_files/ directory with sample test files (file1.txt, file2.txt, file3.txt, large_file.bin)
- [ ] T027 [US1] Create tests/integration/test_file_operations_e2e.py with test case test_move_files_end_to_end (full workflow: validate → discover → move → results)

### Implementation for User Story 1

- [ ] T028 [P] [US1] Create src/services/file_mover.py with discover_files(source_path) function that returns list of regular files (not directories) from source
- [ ] T029 [P] [US1] Create src/services/file_mover.py with move_file(source_file_path, destination_folder_path) function that uses shutil.move() and returns FileTransferResult with success/error info
- [ ] T030 [US1] Create src/services/file_mover.py with move_files(source_path, destination_path, callback=None) that iterates files and calls callback(filename, progress_percent) for UI updates
- [ ] T031 [P] [US1] Create src/ui/components.py with render_input_section() that displays source and destination text inputs with validation status indicators (✓/✗)
- [ ] T032 [P] [US1] Create src/ui/components.py with render_move_button(enabled: bool) that shows "Move Files" button (enabled/disabled based on validation)
- [ ] T033 [US1] Create src/ui/app.py with main Streamlit app structure: header, input section, button, (progress placeholder), (results placeholder)
- [ ] T034 [US1] Create src/ui/app.py with path input handlers that call validators.validate_source_path() and validators.validate_destination_path() on text input blur
- [ ] T035 [US1] Create src/ui/app.py with "Move Files" button click handler that validates paths and calls file_mover.move_files()
- [ ] T036 [US1] Create src/ui/app.py with result display that shows "Successfully moved X files" message and file count after operation completes
- [ ] T037 [US1] Update src/main.py to import and run ui/app.py as main Streamlit entrypoint

**Checkpoint**: At this point, User Story 1 (basic file transfer) should be fully functional and testable independently

---

## Phase 4: User Story 2 - Error Handling & Status Feedback (Priority: P1)

**Goal**: Handle errors gracefully and provide real-time progress feedback during file transfer

**Independent Test**: Trigger error scenarios (invalid path, permission denied, locked file), verify error messages are clear and actionable, verify partial success reports

### Tests for User Story 2 (OPTIONAL - provided for reference)

- [ ] T038 [P] [US2] Create tests/unit/test_error_handler.py with test case for each error type (path not found, permission denied, file locked, no space, same source/dest, system directory, invalid path)
- [ ] T039 [US2] Create tests/integration/test_file_operations_e2e.py with test case test_handle_locked_file (simulate locked file, verify continues with others and reports failed file)
- [ ] T040 [US2] Create tests/integration/test_file_operations_e2e.py with test case test_handle_partial_failure (5 files total, 2 fail, verify "Moved 3 of 5" message and failed file list)

### Implementation for User Story 2

- [ ] T041 [P] [US2] Create src/ui/components.py with render_progress_container(current_file, files_moved, total_files, elapsed_seconds) that displays st.status() with progress metrics
- [ ] T042 [P] [US2] Create src/ui/components.py with render_results_section(operation_result) that displays success/error alert, moved/failed counts, and failed files table with reasons
- [ ] T043 [US2] Create src/ui/components.py with render_retry_button() and render_clear_button() for result actions
- [ ] T044 [US2] Create src/services/file_mover.py with error handling: wrap file operations in try/except, classify errors, log failed file details (file path, error code, user message)
- [ ] T045 [US2] Create src/services/file_mover.py with handle_file_move_failure(filename, exception) that determines error category and returns user-friendly message from error_handler
- [ ] T046 [US2] Update src/ui/app.py with progress section display during IN_PROGRESS operation (show progress_container with live updates)
- [ ] T047 [US2] Update src/ui/app.py with results section display after operation completes (show results_section with success/error variant, failed files table, retry button)
- [ ] T048 [US2] Update src/ui/app.py with error recovery workflow: allow user to correct paths and retry failed files after partial failure
- [ ] T049 [US2] Update src/services/file_mover.py to call logging_config.setup_logging() and log all operations (operation start, file move attempts, failures, completion)

**Checkpoint**: At this point, User Story 2 error handling and progress feedback should be fully functional

---

## Phase 5: User Story 3 - Session Persistence (Priority: P2)

**Goal**: Persist user's path selections within session for repeated operations

**Independent Test**: Set source/destination paths, refresh page, verify paths are restored, perform another transfer with same paths

### Tests for User Story 3 (OPTIONAL - provided for reference)

- [ ] T050 [US3] Create tests/integration/test_file_operations_e2e.py with test case test_session_state_persistence (set paths, verify st.session_state contains paths, refresh simulation)

### Implementation for User Story 3

- [ ] T051 [P] [US3] Create src/ui/session_manager.py with persist_path(path_type: str, path_value: str) that saves source_path or destination_path to st.session_state
- [ ] T052 [P] [US3] Create src/ui/session_manager.py with get_persisted_path(path_type: str) function that retrieves path from st.session_state if available
- [ ] T053 [US3] Create src/ui/session_manager.py with clear_paths() function that resets both paths in st.session_state
- [ ] T054 [US3] Update src/ui/app.py to call persist_path() whenever user changes path input
- [ ] T055 [US3] Update src/ui/app.py to call get_persisted_path() on app load to restore previous paths if session exists
- [ ] T056 [US3] Update src/ui/components.py with initial_value parameter in render_input_section() to populate text inputs with persisted paths

**Checkpoint**: At this point, User Story 3 (session persistence) should be fully functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Testing, documentation, and final refinement

- [ ] T057 Run all unit tests: `pytest tests/unit/ -v` and verify 100% pass
- [ ] T058 Run all integration tests: `pytest tests/integration/ -v` and verify 100% pass
- [ ] T059 Run tests with coverage: `pytest --cov=src tests/ --cov-report=html` and verify ≥80% code coverage
- [ ] T060 [P] Create manual testing checklist in quickstart.md with test scenarios for happy path, error cases, and edge cases
- [ ] T061 [P] Verify app follows Constitution principles: UI first (FR-006 progress feedback), file safety (FR-004 validation), error resilience (FR-009 messages), session state (FR-010 persistence), simplicity (focused scope)
- [ ] T062 Perform end-to-end manual test: create test folders, transfer files, verify success/failure feedback, test error recovery
- [ ] T063 Test with edge case: same source and destination (should error)
- [ ] T064 Test with edge case: locked file (should report failed and continue)
- [ ] T065 Test with edge case: destination doesn't exist (should handle gracefully per spec)
- [ ] T066 Test with edge case: user cancels mid-transfer (should stop and report partial results)
- [ ] T067 Run `streamlit run src/main.py` and verify UI loads without errors
- [ ] T068 Update README.md with final implementation notes and troubleshooting guide
- [ ] T069 Create or update CHANGELOG.md documenting v1.0.0 features (P1: basic transfer + error handling, P2: session persistence)

---

## Dependency Graph & Execution Order

```
Phase 1: Setup (T001-T006) ✓ Foundation
    ↓
Phase 2: Foundational (T007-T020) ✓ Core Infrastructure
    ↓
┌─── Phase 3: User Story 1 (T021-T037) - Basic File Transfer (P1)
│        ├─ Unit Tests (T021-T026)
│        └─ Implementation (T028-T037)
│
├─── Phase 4: User Story 2 (T038-T049) - Error Handling (P1)
│        ├─ Unit Tests (T038-T040)
│        └─ Implementation (T041-T049)
│        (Depends on: Phase 3 complete for base functionality)
│
└─── Phase 5: User Story 3 (T050-T056) - Session Persistence (P2)
         ├─ Unit Tests (T050)
         └─ Implementation (T051-T056)
         (Depends on: Phase 3 complete for base UI)

    ↓
Phase 6: Polish & Testing (T057-T069) ✓ Validation & Documentation
```

---

## Parallel Execution Opportunities

### Within Phase 2: Foundational
All tasks T007-T020 (except T016-T020) can run in parallel:
- **Batch 1 (Models)**: T007, T008 - FileOperation and FileTransferResult entities
- **Batch 2 (Validators)**: T009, T010, T011 - Path validation functions
- **Batch 3 (Services)**: T012, T013, T015 - Error handler and logging
- **Batch 4 (UI Infrastructure)**: T014 - Session manager

### Within Phase 3: User Story 1
- **T021-T026 (Tests)**: Can run in parallel (different test files)
- **T028-T032 (Models & Components)**: Can run in parallel (different files)
- **T033-T037 (App Integration)**: Sequential (depend on components)

### Within Phase 4: User Story 2
- **T038-T040 (Tests)**: Can run in parallel
- **T041-T043 (UI Components)**: Can run in parallel
- **T044-T049 (Service & App updates)**: Sequential (integrate error handling)

### Within Phase 5: User Story 3
- **T051-T053 (Session Manager)**: Can run in parallel
- **T054-T056 (App Integration)**: Sequential (depend on session manager)

---

## Implementation Strategy

### MVP Scope (Ready for v1.0.0 Release)
- ✅ **P1 Complete**: User Story 1 (Basic File Transfer) + User Story 2 (Error Handling)
- ⏱️ **P2 Optional**: User Story 3 (Session Persistence) can be pushed to v1.1 if time-constrained

### Suggested Delivery Increments
1. **Sprint 1**: Phase 1 Setup + Phase 2 Foundational (T001-T020)
2. **Sprint 2**: Phase 3 User Story 1 (T021-T037) - MVP core feature
3. **Sprint 3**: Phase 4 User Story 2 (T038-T049) - Production-ready error handling
4. **Sprint 4**: Phase 5 User Story 3 (T050-T056) - Enhanced UX
5. **Sprint 5**: Phase 6 Polish (T057-T069) - Testing, docs, final QA

### Independent Testing per Story

**User Story 1 Independent Test**:
- Create `test_source/` with files (file1.txt, file2.txt, file3.txt)
- Create empty `test_destination/` folder
- Run app, enter paths, click "Move Files"
- ✅ Verify: files in destination, source empty, success message shown

**User Story 2 Independent Test**:
- Set source to invalid path (e.g., `/nonexistent`)
- ✅ Verify: error message "Source folder not found"
- Fix path and retry
- ✅ Verify: operation proceeds

**User Story 3 Independent Test**:
- Set source and destination paths
- ✅ Verify: paths visible in text inputs
- Refresh page (simulated by `st.rerun()` or browser refresh)
- ✅ Verify: paths still populated from session state

---

## Task Summary

**Total Tasks**: 69  
**Phase 1 (Setup)**: 6 tasks  
**Phase 2 (Foundational)**: 14 tasks  
**Phase 3 (User Story 1)**: 17 tasks (7 tests + 10 implementation)  
**Phase 4 (User Story 2)**: 12 tasks (3 tests + 9 implementation)  
**Phase 5 (User Story 3)**: 7 tasks (1 test + 6 implementation)  
**Phase 6 (Polish)**: 13 tasks  

**Parallel Opportunities**: 40+ tasks can execute in parallel (marked with [P])  
**Critical Path**: T001 → T020 → T028/T041 → T033 → T046 → T050-T056 → T057+ (~13 sequential task clusters)  
**Estimated Timeline (with parallelization)**: 4-5 weeks for full implementation and testing