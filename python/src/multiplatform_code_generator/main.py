#!/usr/bin/env python3
"""
Main entry point for the Multiplatform Code Generator MCP server.
"""

import asyncio
import sys
from typing import Optional

from .server import MultiplatformCodeGeneratorServer


async def main(args: Optional[list[str]] = None) -> None:
    """Main entry point for the MCP server."""
    if args is None:
        args = sys.argv[1:]
    
    # Create and run the MCP server
    server = MultiplatformCodeGeneratorServer()
    await server.run()


def cli_main() -> None:
    """CLI entry point."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
