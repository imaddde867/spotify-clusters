#!/usr/bin/env python3
"""
Development utility script for code quality checks.

This script runs all code quality tools in sequence:
- Black (code formatting)
- isort (import sorting) 
- flake8 (linting)
- mypy (type checking)
- pytest (tests)

Usage: python scripts/dev/quality_check.py [--fix] [--fast]
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, description: str, fix_mode: bool = False) -> bool:
    """
    Run a command and return success status.
    
    Args:
        cmd: Command to run as list of strings
        description: Description of what the command does
        fix_mode: Whether we're in fix mode (affects exit behavior)
        
    Returns:
        True if command succeeded, False otherwise
    """
    print(f"\n🔍 {description}...")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} passed")
            if result.stdout.strip():
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} failed")
            if result.stdout.strip():
                print("STDOUT:", result.stdout)
            if result.stderr.strip():
                print("STDERR:", result.stderr)
            return False
            
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run code quality checks")
    parser.add_argument(
        "--fix", 
        action="store_true", 
        help="Automatically fix issues where possible"
    )
    parser.add_argument(
        "--fast", 
        action="store_true", 
        help="Skip slower checks (mypy, full test suite)"
    )
    
    args = parser.parse_args()
    
    # Get project root
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src"
    tests_dir = project_root / "tests"
    
    print(f"🎯 Running code quality checks for: {project_root}")
    print(f"📁 Source directory: {src_dir}")
    print(f"🧪 Tests directory: {tests_dir}")
    
    success_count = 0
    total_checks = 0
    
    # 1. Black (code formatting)
    total_checks += 1
    black_cmd = ["black"]
    if not args.fix:
        black_cmd.append("--check")
    black_cmd.extend(["src/", "tests/"])
    
    if run_command(black_cmd, "Black code formatting", args.fix):
        success_count += 1
    
    # 2. isort (import sorting)
    total_checks += 1
    isort_cmd = ["isort"]
    if not args.fix:
        isort_cmd.append("--check-only")
    isort_cmd.extend(["src/", "tests/"])
    
    if run_command(isort_cmd, "isort import sorting", args.fix):
        success_count += 1
    
    # 3. flake8 (linting)
    total_checks += 1
    flake8_cmd = ["flake8", "src/", "tests/"]
    
    if run_command(flake8_cmd, "flake8 linting", False):
        success_count += 1
    
    # 4. mypy (type checking) - unless fast mode
    if not args.fast:
        total_checks += 1
        mypy_cmd = ["mypy", "src/"]
        
        if run_command(mypy_cmd, "mypy type checking", False):
            success_count += 1
    
    # 5. pytest (tests) - basic tests only in fast mode
    total_checks += 1
    pytest_cmd = ["python", "-m", "pytest"]
    
    if args.fast:
        pytest_cmd.extend(["tests/test_basic_functionality.py", "-v"])
        test_description = "pytest basic tests"
    else:
        pytest_cmd.extend(["tests/", "-v", "--tb=short"])
        test_description = "pytest full test suite"
    
    if run_command(pytest_cmd, test_description, False):
        success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Quality Check Summary: {success_count}/{total_checks} passed")
    
    if success_count == total_checks:
        print("🎉 All checks passed! Code quality is excellent.")
        sys.exit(0)
    else:
        failed_count = total_checks - success_count
        print(f"⚠️  {failed_count} check(s) failed. Please fix the issues above.")
        
        if not args.fix:
            print("\n💡 Tip: Run with --fix to automatically fix formatting issues")
        
        sys.exit(1)


if __name__ == "__main__":
    main()