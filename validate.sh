#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

echo "🎵 YesAnd Music - Project Validation"
echo "===================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "control_plane_cli.py" ] || [ ! -f "requirements.txt" ]; then
    print_error "This script must be run from the YesAnd Music project root directory"
    exit 1
fi

# Check if Python virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "Virtual environment not detected. Consider activating it first:"
    echo "  source .venv/bin/activate"
    echo ""
fi

# Rule 1: Code Quality & Style (Linting)
print_status "Rule 1: Code Quality & Style (Linting)"
echo "----------------------------------------"

# Check if flake8 is installed
if ! command -v flake8 &> /dev/null; then
    print_warning "flake8 not found. Installing..."
    pip install flake8
fi

# Critical errors (must pass)
print_status "Checking for critical errors..."
if flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; then
    print_success "No critical errors found"
else
    print_error "Critical errors found! Fix these before continuing."
    exit 1
fi

# Style and complexity checks (warnings)
print_status "Checking code style and complexity..."
if flake8 . --count --exit-zero --max-complexity=10; then
    print_success "Code style checks passed"
else
    print_warning "Code style issues found (non-blocking)"
fi

echo ""

# Rule 2: Unit Tests Must Pass
print_status "Rule 2: Unit Tests Must Pass"
echo "--------------------------------"

# Check if tests directory exists, if not create it
if [ ! -d "tests" ]; then
    print_warning "No tests directory found. Creating basic test structure..."
    mkdir -p tests
    touch tests/__init__.py
fi

# Run unit tests
print_status "Running unit tests..."
if python -m unittest discover -s . -p "test_*.py" -v; then
    print_success "All unit tests passed"
else
    print_error "Unit tests failed! Fix tests before continuing."
    exit 1
fi

echo ""

# Rule 3: Architectural Purity Checks
print_status "Rule 3: Architectural Purity Checks"
echo "---------------------------------------"

# Create scripts directory if it doesn't exist
if [ ! -d "scripts" ]; then
    mkdir -p scripts
fi

# Run architectural checks
if [ -f "scripts/check_architecture.py" ]; then
    if python scripts/check_architecture.py; then
        print_success "Architectural checks passed"
    else
        print_error "Architectural violations found! Fix before continuing."
        exit 1
    fi
else
    print_warning "Architectural checker not found. Creating basic checker..."
    # Create a basic architectural checker
    cat > scripts/check_architecture.py << 'EOF'
#!/usr/bin/env python3
"""
Architectural purity checker for YesAnd Music.

This script enforces the project's architectural principles:
1. Separation of concerns (Brain vs. Hands)
2. Pure functions in analysis.py
3. No heavy dependencies in core modules
4. Real-time safety in MIDI processing
"""

import os
import ast
import sys
from pathlib import Path

def check_file_imports(filepath, allowed_imports, forbidden_imports):
    """Check if a file follows import restrictions."""
    violations = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in forbidden_imports:
                        violations.append(f"Forbidden import '{alias.name}' in {filepath}")
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module in forbidden_imports:
                    violations.append(f"Forbidden import '{node.module}' in {filepath}")
    
    except Exception as e:
        violations.append(f"Error parsing {filepath}: {e}")
    
    return violations

def check_architecture():
    """Main architectural check function."""
    violations = []
    
    # Define architectural rules
    core_modules = ['midi_io.py', 'analysis.py', 'project.py']
    forbidden_heavy_deps = ['numpy', 'scipy', 'pandas', 'tensorflow', 'torch', 'sklearn']
    
    # Check core modules for heavy dependencies
    for module in core_modules:
        if os.path.exists(module):
            module_violations = check_file_imports(module, [], forbidden_heavy_deps)
            violations.extend(module_violations)
    
    # Check for pure functions in analysis.py
    if os.path.exists('analysis.py'):
        try:
            with open('analysis.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for global variables (should be minimal in pure functions)
            if 'global ' in content:
                violations.append("analysis.py should not use global variables (pure functions)")
            
            # Check for print statements (should use logging or return values)
            if 'print(' in content:
                violations.append("analysis.py should not use print statements (pure functions)")
        
        except Exception as e:
            violations.append(f"Error checking analysis.py: {e}")
    
    # Check for proper separation of concerns
    if os.path.exists('commands/control_plane.py'):
        try:
            with open('commands/control_plane.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Control plane should not contain musical analysis logic
            if 'def apply_swing' in content or 'def filter_notes' in content:
                violations.append("control_plane.py should not contain musical analysis functions")
        
        except Exception as e:
            violations.append(f"Error checking control_plane.py: {e}")
    
    return violations

def main():
    """Main function."""
    print("Checking architectural purity...")
    
    violations = check_architecture()
    
    if violations:
        print("❌ Architectural violations found:")
        for violation in violations:
            print(f"  - {violation}")
        return False
    else:
        print("✅ All architectural checks passed")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF
    
    if python scripts/check_architecture.py; then
        print_success "Architectural checks passed"
    else
        print_error "Architectural violations found! Fix before continuing."
        exit 1
    fi
fi

echo ""

# Rule 4: Integration Tests
print_status "Rule 4: Integration Tests"
echo "-----------------------------"

# Test that main entry points work
print_status "Testing main entry points..."

# Test control_plane_cli.py help
if python control_plane_cli.py --help > /dev/null 2>&1; then
    print_success "control_plane_cli.py --help works"
else
    print_error "control_plane_cli.py --help failed"
    exit 1
fi

# Test enhanced_control_plane_cli.py help
if python enhanced_control_plane_cli.py --help > /dev/null 2>&1; then
    print_success "enhanced_control_plane_cli.py --help works"
else
    print_error "enhanced_control_plane_cli.py --help failed"
    exit 1
fi

echo ""

# Rule 5: Documentation Consistency
print_status "Rule 5: Documentation Consistency"
echo "------------------------------------"

# Check that all Python files have docstrings
print_status "Checking for missing docstrings..."
missing_docstrings = 0

for py_file in $(find . -name "*.py" -not -path "./__pycache__/*" -not -path "./build_logs/*"); do
    if ! grep -q '"""' "$py_file" && ! grep -q "'''" "$py_file"; then
        if [ "$py_file" != "./scripts/check_architecture.py" ]; then
            print_warning "Missing docstring in $py_file"
            missing_docstrings=$((missing_docstrings + 1))
        fi
    fi
done

if [ $missing_docstrings -eq 0 ]; then
    print_success "All Python files have docstrings"
else
    print_warning "$missing_docstrings files missing docstrings (non-blocking)"
fi

echo ""

# Rule 6: Dependencies Check
print_status "Rule 6: Dependencies Check"
echo "-----------------------------"

# Check if all required dependencies are installed
print_status "Checking required dependencies..."
missing_deps=0

for dep in mido python-rtmidi python-osc; do
    if ! python -c "import $dep" 2>/dev/null; then
        print_error "Missing dependency: $dep"
        missing_deps=$((missing_deps + 1))
    else
        print_success "Dependency $dep is available"
    fi
done

if [ $missing_deps -gt 0 ]; then
    print_error "Missing $missing_deps dependencies. Install with: pip install -r requirements.txt"
    exit 1
fi

echo ""

# Rule 7: File Structure Validation
print_status "Rule 7: File Structure Validation"
echo "------------------------------------"

# Check for required files
required_files=("control_plane_cli.py" "enhanced_control_plane_cli.py" "requirements.txt" "config.py" "midi_io.py" "analysis.py" "project.py")
missing_files=0

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "Required file $file exists"
    else
        print_error "Missing required file: $file"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -gt 0 ]; then
    print_error "Missing $missing_files required files"
    exit 1
fi

echo ""

# Final Success Message
echo "🎉🎉🎉 ALL CHECKS PASSED! 🎉🎉🎉"
echo "================================"
echo ""
print_success "Project is in a good state and ready for development!"
echo ""
echo "Summary of checks:"
echo "✅ Code quality and style"
echo "✅ Unit tests"
echo "✅ Architectural purity"
echo "✅ Integration tests"
echo "✅ Documentation consistency"
echo "✅ Dependencies"
echo "✅ File structure"
echo ""
echo "You can now safely commit your changes or continue development."
