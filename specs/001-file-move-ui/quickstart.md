# Quick Start Guide: Local File Mover

**Phase**: 1 - Design & Contracts  
**Date**: 2026-05-21  
**Purpose**: Setup, first run, and testing guide

---

## Development Environment Setup

### Prerequisites

- Python 3.9 or later
- pip or conda package manager
- Git (for version control)

### Step 1: Clone/Navigate to Repository

```bash
cd path/to/my_project
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected dependencies** (in `requirements.txt`):
- `streamlit>=1.28.0` - Web framework
- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Code coverage

### Step 4: Verify Installation

```bash
streamlit --version
pytest --version
```

---

## Running the Application

### Start the Streamlit App

```bash
streamlit run src/main.py
```

**Expected Output**:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

The app will open in your default browser. If not, navigate to `http://localhost:8501`.

### Initial App State

- Title: "Local File Mover"
- Status: "Ready to transfer"
- Source and Destination path inputs: empty
- Move Files button: disabled (greyed out)

---

## First Run: Simple Test

### Test Scenario 1: Move 3 Files Successfully

**Setup**:
1. Create a test source folder: `C:\temp\test_source` (Windows) or `/tmp/test_source` (Unix)
2. Create 3 test files in source:
   - `file1.txt` (create with text content)
   - `file2.txt`
   - `file3.txt`
3. Create a destination folder: `C:\temp\test_destination` (Windows) or `/tmp/test_destination` (Unix)

**Steps**:
1. Open the app (http://localhost:8501)
2. In "Source Folder Path" input, enter: `C:\temp\test_source` (adjust for your OS)
3. Observe: ✓ checkmark appears (green, "Source folder found")
4. In "Destination Folder Path" input, enter: `C:\temp\test_destination`
5. Observe: ✓ checkmark appears; [Move Files] button becomes enabled
6. Click [Move Files]
7. Observe:
   - Progress section appears with status container
   - Progress bar fills from 0% to 100%
   - Metric shows: "Files moved: 3 / 3"
   - After completion: "✓ Successfully moved 3 files"
8. Verify:
   - Source folder is now empty (all files moved)
   - Destination folder contains: file1.txt, file2.txt, file3.txt

**Expected Result**: ✅ PASS

---

### Test Scenario 2: Handle Invalid Source Path

**Setup**:
1. Use the same app session

**Steps**:
1. In "Source Folder Path", clear and enter: `/nonexistent/path`
2. Observe: ✗ checkmark (red) appears with message: "Folder not found. Check spelling."
3. [Move Files] button becomes disabled
4. Correct the path to an existing folder
5. Observe: ✗ becomes ✓; button re-enables

**Expected Result**: ✅ PASS - Validation works in real-time

---

### Test Scenario 3: Permission Error (Optional, Requires Admin Access)

**Setup** (if permission testing desired):
1. Create a folder with read-only/no-write permissions
2. Set destination to that folder

**Steps**:
1. Enter destination path and observer validation
2. Observe: ✗ with message "Cannot write to [path]. Check permissions."

**Expected Result**: ✅ PASS - Permission validation working

---

## Running Tests

### Run All Unit Tests

```bash
pytest tests/unit/ -v
```

**Expected Output**:
```
tests/unit/test_file_mover.py::test_move_single_file PASSED
tests/unit/test_validators.py::test_validate_source_path PASSED
...
```

### Run Integration Tests

```bash
pytest tests/integration/ -v
```

**Expected Output** (tests real file operations with temp folders):
```
tests/integration/test_file_operations_e2e.py::test_move_multiple_files_successfully PASSED
...
```

### Run Tests with Coverage

```bash
pytest --cov=src tests/ --cov-report=html
```

This generates a coverage report in `htmlcov/index.html`.

---

## Development Workflow

### Modifying Code

1. **Edit files** in `src/` directory
2. **Save changes**
3. **Streamlit auto-reloads**: App will refresh in browser when you save
4. **Test with manual scenarios** above
5. **Run tests** to verify no regressions:
   ```bash
   pytest tests/unit/ -v
   ```

### Adding Features

1. Define feature in spec.md (already done for v1)
2. Add corresponding data model in `src/models/`
3. Implement logic in `src/services/`
4. Add UI components in `src/ui/`
5. Write unit tests in `tests/unit/`
6. Write integration tests in `tests/integration/` if file operations involved
7. Run full test suite:
   ```bash
   pytest tests/ -v --cov=src
   ```

---

## Logging & Debugging

### View Application Logs

Logs are output to:
- **Console**: Visible in terminal running Streamlit
- **File**: `file_mover.log` (in project root, if configured)

**Log Level**: DEBUG (verbose) or INFO (standard)

To increase verbosity, edit `src/utils/logging_config.py` and change log level.

### Debug Mode

Run Streamlit with debug output:

```bash
streamlit run src/main.py --logger.level=debug
```

---

## Troubleshooting

### Issue: "Port 8501 already in use"

**Solution**: Use a different port:
```bash
streamlit run src/main.py --server.port 8502
```

### Issue: "Module not found: streamlit"

**Solution**: Activate virtual environment and reinstall:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Files not moving (permissions)

**Solution**: Run Streamlit as admin (Windows) or check file permissions (Unix):
```bash
# Windows: Right-click terminal, "Run as Administrator"
streamlit run src/main.py

# Unix: Check permissions
ls -la /path/to/source
chmod 755 /path/to/destination
```

---

## Testing Checklist

Use this checklist to validate the app before each release:

### Basic Functionality

- [ ] Source path input accepts valid paths
- [ ] Destination path input accepts valid paths
- [ ] Move button is disabled when paths invalid
- [ ] Move button is enabled when both paths valid
- [ ] Click "Move Files" starts transfer
- [ ] Progress bar updates during transfer
- [ ] Transfer completes and shows success message
- [ ] Files appear in destination after transfer
- [ ] Files are removed from source after transfer

### Error Handling

- [ ] Invalid source path shows ✗ with message
- [ ] Invalid destination path shows ✗ with message
- [ ] Permission error displays actionable message
- [ ] User can correct path and retry
- [ ] Locked file error displays with suggestion
- [ ] Cancel button stops operation cleanly
- [ ] Partial success shows "X of Y files moved"

### Session State

- [ ] Paths persist when page is refreshed
- [ ] Operation history is retained
- [ ] Can run multiple operations in one session
- [ ] Paths clear when user clicks "Clear & Start Over"

### UI/UX

- [ ] App layout is clean and readable
- [ ] All text is properly formatted
- [ ] Error messages are non-technical and helpful
- [ ] Buttons are appropriately enabled/disabled
- [ ] Status indicators (✓, ✗) are clear
- [ ] Progress indication is visible for long operations

---

## Next Steps

✅ Setup and first run completed.

→ Ready for Phase 2 Task Generation (use `/speckit-tasks`)

---

## Support & Questions

- **Documentation**: See `data-model.md` and `ui-contract.md` for technical details
- **Tests**: Check `tests/` directory for example usage patterns
- **Constitution**: Refer to `.specify/memory/constitution.md` for design principles
