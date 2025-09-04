#!/usr/bin/env python3
"""
Start script for the Multiplatform Code Generator MCP server (Python version).
"""

import argparse
import sys
import asyncio
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from multiplatform_code_generator.main import main as mcp_main


def print_header():
    """Print the header."""
    print("=" * 50)
    print("  Multiplatform Code Generator MCP Server (Python)")
    print("=" * 50)


def print_usage():
    """Print usage information."""
    print("""
Usage: python start_mcp.py [options]

Options:
  -h, --help     Show this help message
  -t, --test     Run tests before starting server
  -v, --version  Show version information

Examples:
  python start_mcp.py              # Start server directly
  python start_mcp.py --test       # Run tests then start server
""")


def print_version():
    """Print version information."""
    try:
        from multiplatform_code_generator import __version__
        print(f"Multiplatform Code Generator (Python) v{__version__}")
    except ImportError:
        print("Version information not available")


async def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    try:
        # Import and run test
        from test_generator import main as test_main
        result = await test_main()
        if result == 0:
            print("✅ All tests passed!\n")
            return True
        else:
            print("❌ Some tests failed!\n")
            return False
    except Exception as e:
        print(f"❌ Test execution failed: {e}\n")
        return False


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Multiplatform Code Generator MCP Server",
        add_help=False
    )
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-t", "--test", action="store_true", help="Run tests")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    
    args = parser.parse_args()
    
    print_header()
    
    if args.help:
        print_usage()
        return 0
    
    if args.version:
        print_version()
        return 0
    
    if args.test:
        test_success = await run_tests()
        if not test_success:
            print("⚠️  Tests failed, but continuing to start server...")
    
    print("🚀 Starting MCP server...")
    print("📡 Transport: stdio (standard input/output)")
    print("🛑 Use Ctrl+C to stop the server\n")
    
    try:
        await mcp_main()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)
