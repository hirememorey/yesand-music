#!/usr/bin/env python3
"""
Architectural purity checker for YesAnd Music.

This script enforces the project's architectural principles:
1. Separation of concerns (Brain vs. Hands)
2. Pure functions in analysis.py
3. No heavy dependencies in core modules
4. Real-time safety in MIDI processing
5. Universal note format compliance
6. Command pattern consistency
"""

import os
import ast
import sys
import re
from pathlib import Path
from typing import List, Dict, Set

class ArchitectureChecker:
    """Checks architectural compliance for YesAnd Music project."""
    
    def __init__(self):
        self.violations: List[str] = []
        self.core_modules = ['midi_io.py', 'analysis.py', 'project.py']
        self.forbidden_heavy_deps = {
            'numpy', 'scipy', 'pandas', 'tensorflow', 'torch', 'sklearn',
            'matplotlib', 'seaborn', 'plotly', 'dash', 'flask', 'django'
        }
        self.allowed_core_imports = {
            'mido', 'pathlib', 'typing', 'json', 'time', 'threading',
            'unittest', 'unittest.mock', 'logging', 'math', 'random'
        }
    
    def check_file_imports(self, filepath: str, is_core_module: bool = False) -> List[str]:
        """Check if a file follows import restrictions."""
        violations = []
        
        # Define specific forbidden imports for Brain vs. Hands architecture
        forbidden_imports = {
            'analysis.py': ['mido', 'rtmidi'],  # Rule: analysis should NOT do MIDI I/O
            'midi_io.py': ['analysis']  # Rule: MIDI I/O should NOT know about analysis
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            
            # Check for specific forbidden imports
            filename = os.path.basename(filepath)
            if filename in forbidden_imports:
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name in forbidden_imports[filename]:
                                violations.append(f"❌ ARCHITECTURE VIOLATION in {filepath}: Found forbidden import '{alias.name}' on line {node.lineno}")
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and node.module in forbidden_imports[filename]:
                            violations.append(f"❌ ARCHITECTURE VIOLATION in {filepath}: Found forbidden import from '{node.module}' on line {node.lineno}")
            
            # Check for heavy dependencies in core modules
            if is_core_module:
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name in self.forbidden_heavy_deps:
                                violations.append(f"Forbidden heavy dependency '{alias.name}' in core module {filepath}")
                            elif alias.name not in self.allowed_core_imports:
                                violations.append(f"Unexpected import '{alias.name}' in core module {filepath}")
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            if node.module in self.forbidden_heavy_deps:
                                violations.append(f"Forbidden heavy dependency '{node.module}' in core module {filepath}")
                            elif node.module not in self.allowed_core_imports:
                                violations.append(f"Unexpected import '{node.module}' in core module {filepath}")
        
        except Exception as e:
            violations.append(f"Error parsing {filepath}: {e}")
        
        return violations
    
    def check_pure_functions(self, filepath: str) -> List[str]:
        """Check that analysis.py contains only pure functions."""
        violations = []
        
        if not os.path.exists(filepath) or not filepath.endswith('analysis.py'):
            return violations
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            
            # Check for global variables (should be minimal in pure functions)
            if 'global ' in content:
                violations.append(f"analysis.py should not use global variables (pure functions) in {filepath}")
            
            # Check for print statements (should use logging or return values)
            if 'print(' in content:
                violations.append(f"analysis.py should not use print statements (pure functions) in {filepath}")
            
            # Check for file I/O (should be handled by other modules)
            if 'open(' in content or 'with open(' in content:
                violations.append(f"analysis.py should not perform file I/O (pure functions) in {filepath}")
            
            # More advanced check: parse analysis.py and ensure functions don't
            # modify their input arguments directly
            print("Checking for pure functions in analysis.py...")
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if function modifies its input arguments
                    for child in ast.walk(node):
                        if isinstance(child, ast.Assign):
                            for target in child.targets:
                                if isinstance(target, ast.Name):
                                    # Check if this is modifying a parameter
                                    for arg in node.args.args:
                                        if arg.arg == target.id:
                                            violations.append(f"Function '{node.name}' modifies input argument '{target.id}' (not pure) in {filepath}")
        
        except Exception as e:
            violations.append(f"Error checking pure functions in {filepath}: {e}")
        
        return violations
    
    def check_separation_of_concerns(self) -> List[str]:
        """Check that modules maintain proper separation of concerns."""
        violations = []
        
        # Control plane should not contain musical analysis logic
        if os.path.exists('commands/control_plane.py'):
            try:
                with open('commands/control_plane.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for analysis functions
                analysis_functions = ['apply_swing', 'filter_notes', 'parse_midi_file', 'save_midi_file']
                for func in analysis_functions:
                    if f'def {func}' in content:
                        violations.append(f"control_plane.py should not contain musical analysis function '{func}'")
                
                # Check for direct MIDI file operations
                if 'parse_midi_file' in content or 'save_midi_file' in content:
                    violations.append("control_plane.py should not directly perform MIDI file I/O")
            
            except Exception as e:
                violations.append(f"Error checking control_plane.py: {e}")
        
        # MIDI I/O should not contain musical analysis
        if os.path.exists('midi_io.py'):
            try:
                with open('midi_io.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                analysis_functions = ['apply_swing', 'filter_notes']
                for func in analysis_functions:
                    if f'def {func}' in content:
                        violations.append(f"midi_io.py should not contain musical analysis function '{func}'")
            
            except Exception as e:
                violations.append(f"Error checking midi_io.py: {e}")
        
        return violations
    
    def check_universal_note_format(self) -> List[str]:
        """Check that the universal note format is used consistently."""
        violations = []
        
        # Check midi_io.py for universal note format
        if os.path.exists('midi_io.py'):
            try:
                with open('midi_io.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for universal note format documentation
                if 'pitch.*int.*velocity.*int.*start_time_seconds.*float.*duration_seconds.*float.*track_index.*int' not in content.replace('\n', ' ').replace(' ', ''):
                    violations.append("midi_io.py should document the universal note format")
                
                # Check that functions use the correct format
                if 'parse_midi_file' in content:
                    if 'track_index' not in content:
                        violations.append("parse_midi_file should include track_index in universal note format")
            
            except Exception as e:
                violations.append(f"Error checking universal note format in midi_io.py: {e}")
        
        return violations
    
    def check_command_pattern_consistency(self) -> List[str]:
        """Check that command patterns are consistent across the system."""
        violations = []
        
        # Check that all command types are handled in control_plane.py
        if os.path.exists('commands/types.py') and os.path.exists('commands/control_plane.py'):
            try:
                # Extract command types from types.py
                with open('commands/types.py', 'r', encoding='utf-8') as f:
                    types_content = f.read()
                
                command_types = re.findall(r'(\w+) = "(\w+)"', types_content)
                
                # Check that control_plane.py handles all command types
                with open('commands/control_plane.py', 'r', encoding='utf-8') as f:
                    control_content = f.read()
                
                for cmd_type, cmd_value in command_types:
                    if cmd_type not in control_content:
                        violations.append(f"Command type {cmd_type} not handled in control_plane.py")
            
            except Exception as e:
                violations.append(f"Error checking command pattern consistency: {e}")
        
        return violations
    
    def check_real_time_safety(self) -> List[str]:
        """Check for real-time safety violations in MIDI processing."""
        violations = []
        
        # Check sequencer.py for real-time safety
        if os.path.exists('sequencer.py'):
            try:
                with open('sequencer.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for blocking operations
                blocking_ops = ['time.sleep', 'input(', 'raw_input(']
                for op in blocking_ops:
                    if op in content:
                        violations.append(f"sequencer.py contains blocking operation '{op}' which violates real-time safety")
                
                # Check for memory allocation in hot paths
                if 'list(' in content or 'dict(' in content or 'set(' in content:
                    if 'def play' in content or 'def add_note' in content:
                        violations.append("sequencer.py may allocate memory in real-time critical paths")
            
            except Exception as e:
                violations.append(f"Error checking real-time safety in sequencer.py: {e}")
        
        return violations
    
    def check_documentation_consistency(self) -> List[str]:
        """Check that documentation is consistent with implementation."""
        violations = []
        
        # Check that all Python files have proper docstrings
        for py_file in Path('.').rglob('*.py'):
            if '__pycache__' in str(py_file) or 'build_logs' in str(py_file) or '.venv' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for module docstring
                if not content.strip().startswith('"""') and not content.strip().startswith("'''"):
                    if py_file.name != '__init__.py':
                        violations.append(f"Missing module docstring in {py_file}")
                
                # Check for function docstrings in public functions
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('def ') and not line.strip().startswith('def _'):
                        # Check if next non-empty line is a docstring
                        j = i + 1
                        while j < len(lines) and lines[j].strip() == '':
                            j += 1
                        
                        if j < len(lines) and not (lines[j].strip().startswith('"""') or lines[j].strip().startswith("'''")):
                            violations.append(f"Missing docstring for function at line {i+1} in {py_file}")
            
            except Exception as e:
                violations.append(f"Error checking documentation in {py_file}: {e}")
        
        return violations
    
    def run_all_checks(self) -> List[str]:
        """Run all architectural checks."""
        all_violations = []
        
        # Check core modules for heavy dependencies
        for module in self.core_modules:
            if os.path.exists(module):
                violations = self.check_file_imports(module, is_core_module=True)
                all_violations.extend(violations)
        
        # Check pure functions in analysis.py
        violations = self.check_pure_functions('analysis.py')
        all_violations.extend(violations)
        
        # Check separation of concerns
        violations = self.check_separation_of_concerns()
        all_violations.extend(violations)
        
        # Check universal note format
        violations = self.check_universal_note_format()
        all_violations.extend(violations)
        
        # Check command pattern consistency
        violations = self.check_command_pattern_consistency()
        all_violations.extend(violations)
        
        # Check real-time safety
        violations = self.check_real_time_safety()
        all_violations.extend(violations)
        
        # Check documentation consistency
        violations = self.check_documentation_consistency()
        all_violations.extend(violations)
        
        return all_violations

def main():
    """Main function."""
    print("🔍 Checking architectural purity...")
    print("=" * 40)
    
    checker = ArchitectureChecker()
    violations = checker.run_all_checks()
    
    if violations:
        print("❌ Architectural violations found:")
        print()
        for i, violation in enumerate(violations, 1):
            print(f"  {i}. {violation}")
        print()
        print(f"Total violations: {len(violations)}")
        print()
        print("Please fix these violations before continuing.")
        return False
    else:
        print("✅ All architectural checks passed!")
        print()
        print("Architectural principles verified:")
        print("  ✅ Separation of concerns (Brain vs. Hands)")
        print("  ✅ Pure functions in analysis.py")
        print("  ✅ No heavy dependencies in core modules")
        print("  ✅ Universal note format compliance")
        print("  ✅ Command pattern consistency")
        print("  ✅ Real-time safety considerations")
        print("  ✅ Documentation consistency")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
