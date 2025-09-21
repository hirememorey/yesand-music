# Quality Assurance System

## Overview

YesAnd Music includes a comprehensive quality assurance system designed to maintain code quality, architectural integrity, and project consistency. The system consists of automated validation tools that enforce the project's architectural principles and coding standards.

## Quick Start

```bash
# Run the complete validation suite
./validate.sh
```

This single command runs all quality checks and provides a comprehensive report of the project's health.

## Validation Rules

### Rule 1: Code Quality & Style (Linting)
- **Tool**: Flake8 with custom configuration (`.flake8` file)
- **Critical Errors**: Syntax errors, undefined names, import errors (must pass)
- **Style Warnings**: Whitespace, line length, complexity (non-blocking)
- **Configuration**: 
  - Max line length: 120 characters
  - Ignores E501 (line length) and W503 (whitespace) warnings
  - Excludes: `.venv`, `__pycache__`, `build`, `dist`, `build_logs`

### Rule 2: Unit Tests Must Pass
- **Coverage**: 45+ comprehensive tests
- **Modules Tested**: 
  - `midi_io.py` - Universal note format and MIDI I/O
  - `analysis.py` - Pure functions for musical analysis
  - `project.py` - Project class functionality
  - `commands/` - Control plane components
- **Test Structure**: Organized in `tests/` directory with proper imports

### Rule 3: Architectural Purity Checks
- **Tool**: Custom Python script (`scripts/check_architecture.py`)
- **Enforces**:
  - **Separation of Concerns**: "Brain vs. Hands" architecture
    - `analysis.py` cannot import `mido` or `rtmidi` (MIDI I/O)
    - `midi_io.py` cannot import `analysis` (musical analysis)
  - **Pure Functions**: analysis.py contains only pure functions
    - No side effects, no global state modification
    - Functions cannot modify their input arguments
  - **No Heavy Dependencies**: Core modules avoid heavy libraries
  - **Universal Note Format**: Consistent MIDI data structure
  - **Command Pattern Consistency**: Proper command handling
  - **Real-Time Safety**: MIDI processing safety considerations
  - **Documentation Consistency**: Proper docstrings throughout

### Rule 4: Integration Tests
- **Main Entry Points**: `main.py`, `control_plane_cli.py`, `edit.py`
- **Help Commands**: All entry points respond to `--help`
- **Error Handling**: Graceful failure modes

### Rule 5: Documentation Consistency
- **Docstrings**: All Python files have proper module and function docstrings
- **Documentation**: Comprehensive markdown documentation
- **Code Comments**: Clear, helpful comments throughout

### Rule 6: Dependencies Check
- **Required Packages**: mido, python-rtmidi, python-osc
- **Availability**: All dependencies must be importable
- **Version Compatibility**: Ensures proper package versions

### Rule 7: File Structure Validation
- **Required Files**: main.py, requirements.txt, config.py, etc.
- **Directory Structure**: Proper organization of modules and tests
- **Project Integrity**: All essential components present

## Architectural Principles

### Brain vs. Hands Architecture
The project enforces a clear separation between:
- **The "Brain"**: Python intelligence (analysis, transformations)
- **The "Hands"**: DAW integration (MIDI I/O, real-time processing)

### Pure Functions
- `analysis.py` contains only pure functions
- No side effects, no global state modification
- Testable in isolation
- Deterministic output for given input

### Universal Note Format
Consistent MIDI data structure across all modules:
```python
{
    'pitch': int,           # MIDI note number (0-127)
    'velocity': int,        # MIDI velocity (0-127)
    'start_time_seconds': float,  # When the note starts
    'duration_seconds': float,    # How long the note lasts
    'track_index': int      # Which track the note belongs to
}
```

## Developer Workflow

### 1. Make Changes
```bash
# Edit your code
vim src/some_file.py
```

### 2. Validate Changes
```bash
# Run the complete validation suite
./validate.sh
```

### 3. Fix Issues
If validation fails:
- **Critical Errors**: Must be fixed before continuing
- **Style Warnings**: Can be addressed later (non-blocking)
- **Test Failures**: Must be fixed before committing
- **Architectural Violations**: Must be fixed before committing

### 4. Commit When Clean
```bash
# Only commit when all checks pass
git add .
git commit -m "Add new feature with validation passing"
```

## Continuous Integration

The validation system is designed to be CI/CD friendly:
- **Exit Codes**: Proper exit codes for automated systems
- **Colored Output**: Clear success/failure indicators
- **Detailed Reports**: Comprehensive error reporting
- **Fast Execution**: Optimized for quick feedback

## Customization

### Adding New Checks
1. Edit `scripts/check_architecture.py` to add new architectural rules
2. Update `validate.sh` to include new validation steps
3. Add corresponding tests in `tests/` directory

### Modifying Style Rules
Edit the `.flake8` configuration file:
```ini
[flake8]
ignore = E501, W503
max-line-length = 120
exclude = .venv,
          __pycache__,
          build,
          dist,
          build_logs
```

Or modify the flake8 commands in `validate.sh`:
```bash
# Adjust complexity threshold
--max-complexity=10

# Adjust line length
--max-line-length=127

# Add/remove exclusions
--exclude=.venv,__pycache__,build_logs
```

### Adding New Tests
1. Create new test file in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Import from parent directory: `sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))`
4. Run tests: `python -m unittest discover -s tests/`

## Troubleshooting

### Common Issues

**Virtual Environment Not Detected**
```bash
# Activate virtual environment first
source .venv/bin/activate
./validate.sh
```

**Missing Dependencies**
```bash
# Install required packages
pip install -r requirements.txt
```

**Test Failures**
```bash
# Run specific test for debugging
python -m unittest tests.test_analysis.TestAnalysis.test_apply_swing_valid_input
```

**Architectural Violations**
- Check `scripts/check_architecture.py` for specific rule violations
- Ensure proper separation of concerns
- Verify pure functions in analysis.py
- Check for forbidden imports

### Getting Help

1. **Read Error Messages**: The validation system provides detailed error messages
2. **Check Documentation**: Review this file and other docs for guidance
3. **Run Individual Checks**: Test specific components in isolation
4. **Review Architecture**: Ensure changes align with project principles

## Benefits

### For Developers
- **Immediate Feedback**: Know immediately if changes break the system
- **Consistent Quality**: Enforced standards across all contributions
- **Reduced Bugs**: Catch issues early in development
- **Clear Guidelines**: Understand project expectations

### For the Project
- **Maintainable Code**: Consistent structure and style
- **Reliable Architecture**: Enforced separation of concerns
- **Comprehensive Testing**: High confidence in code quality
- **Professional Standards**: Production-ready codebase

## Future Enhancements

### Planned Improvements
- **Coverage Reporting**: Add test coverage metrics
- **Performance Testing**: Add performance benchmarks
- **Security Scanning**: Add security vulnerability checks
- **Documentation Generation**: Auto-generate API documentation

### Integration Opportunities
- **Git Hooks**: Pre-commit validation
- **CI/CD Pipeline**: Automated validation on pull requests
- **IDE Integration**: Real-time validation in development environment
- **Code Metrics**: Track quality metrics over time

## Conclusion

The YesAnd Music quality assurance system ensures that the project maintains its high standards of code quality, architectural integrity, and professional development practices. By running `./validate.sh` before any commit, developers can be confident that their changes align with the project's principles and maintain the overall health of the codebase.
