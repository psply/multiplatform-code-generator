"""
MCP Server implementation for the Multiplatform Code Generator.
"""

import logging
from typing import Any, Dict, List, Optional

from .mcp_types import SimpleMCPServer, Tool, TextContent, CallToolResult
from pydantic import BaseModel, Field

from .parsers.cpp_parser import CppInterfaceParser
from .generators.android_jni import AndroidJniGenerator
from .generators.ios_oc import IosOcGenerator  
from .generators.harmony_napi import HarmonyNapiGenerator
from .utils.file_manager import FileManager


# Request/Response models
class GenerateMultiplatformCodeRequest(BaseModel):
    """Request model for generate_multiplatform_code tool."""
    cpp_interface: str = Field(description="C++ interface function code")
    output_directory: str = Field(description="Base output directory for generated files")
    platforms: List[str] = Field(description="Target platforms to generate code for")
    android_config: Optional[Dict[str, Any]] = Field(
        default=None, description="Android-specific configuration"
    )
    ios_config: Optional[Dict[str, Any]] = Field(
        default=None, description="iOS-specific configuration"
    )
    harmony_config: Optional[Dict[str, Any]] = Field(
        default=None, description="HarmonyOS-specific configuration"
    )


class ParseCppInterfaceRequest(BaseModel):
    """Request model for parse_cpp_interface tool."""
    cpp_interface: str = Field(description="C++ interface function code to parse")


class MultiplatformCodeGeneratorServer:
    """MCP Server for the Multiplatform Code Generator."""

    def __init__(self):
        """Initialize the server."""
        self.logger = logging.getLogger(__name__)
        self.server = SimpleMCPServer("multiplatform-code-generator")
        self._setup_tools()

    def _setup_tools(self) -> None:
        """Set up the MCP tools."""
        # Define tools
        generate_tool = Tool(
            name="generate_multiplatform_code",
            description="Generate cross-platform code from C++ interface",
            inputSchema={
                "type": "object",
                "properties": {
                    "cpp_interface": {
                        "type": "string",
                        "description": "C++ interface function code"
                    },
                    "output_directory": {
                        "type": "string", 
                        "description": "Base output directory for generated files"
                    },
                    "platforms": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["android", "ios", "harmony"]
                        },
                        "description": "Target platforms to generate code for"
                    },
                    "android_config": {
                        "type": "object",
                        "properties": {
                            "package_name": {
                                "type": "string",
                                "description": "Java/Kotlin package name for Android"
                            },
                            "class_name": {
                                "type": "string", 
                                "description": "Java/Kotlin class name for Android"
                            },
                            "language": {
                                "type": "string",
                                "enum": ["java", "kotlin"],
                                "description": "Programming language for Android wrapper"
                            }
                        },
                        "description": "Android-specific configuration"
                    },
                    "ios_config": {
                        "type": "object",
                        "properties": {
                            "class_prefix": {
                                "type": "string",
                                "description": "Objective-C class prefix"
                            },
                            "framework_name": {
                                "type": "string",
                                "description": "iOS framework name"
                            }
                        },
                        "description": "iOS-specific configuration"
                    },
                    "harmony_config": {
                        "type": "object",
                        "properties": {
                            "module_name": {
                                "type": "string",
                                "description": "HarmonyOS module name"
                            },
                            "namespace": {
                                "type": "string",
                                "description": "NAPI namespace"
                            }
                        },
                        "description": "HarmonyOS-specific configuration"
                    }
                },
                "required": ["cpp_interface", "output_directory", "platforms"]
            }
        )
        
        parse_tool = Tool(
            name="parse_cpp_interface",
            description="Parse C++ interface and extract function information",
            inputSchema={
                "type": "object",
                "properties": {
                    "cpp_interface": {
                        "type": "string",
                        "description": "C++ interface function code to parse"
                    }
                },
                "required": ["cpp_interface"]
            }
        )
        
        list_platforms_tool = Tool(
            name="list_supported_platforms",
            description="List all supported target platforms",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        
        # Register tools with handlers
        self.server.add_tool(generate_tool, self._generate_multiplatform_code)
        self.server.add_tool(parse_tool, self._parse_cpp_interface)
        self.server.add_tool(list_platforms_tool, self._list_supported_platforms)

    async def _generate_multiplatform_code(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Generate multiplatform code."""
        try:
            request = GenerateMultiplatformCodeRequest(**arguments)
            
            # Parse C++ interface
            parser = CppInterfaceParser()
            parsed_interface = parser.parse(request.cpp_interface)
            
            results = []
            file_manager = FileManager(request.output_directory)
            
            # Generate code for each platform
            for platform in request.platforms:
                if platform == "android":
                    if not request.android_config or not all(
                        k in request.android_config for k in ["package_name", "class_name"]
                    ):
                        raise ValueError(
                            "Android platform requires package_name and class_name in android_config"
                        )
                    generator = AndroidJniGenerator(request.android_config)
                    files = await generator.generate(parsed_interface, file_manager)
                    results.append({"platform": "android", "files": files})
                    
                elif platform == "ios":
                    generator = IosOcGenerator(request.ios_config or {})
                    files = await generator.generate(parsed_interface, file_manager)
                    results.append({"platform": "ios", "files": files})
                    
                elif platform == "harmony":
                    generator = HarmonyNapiGenerator(request.harmony_config or {})
                    files = await generator.generate(parsed_interface, file_manager)
                    results.append({"platform": "harmony", "files": files})
                    
                else:
                    raise ValueError(f"Unsupported platform: {platform}")
            
            # Format results
            platforms_str = ", ".join(request.platforms)
            files_summary = []
            for result in results:
                platform_files = "\n".join(f"  - {f}" for f in result["files"])
                files_summary.append(f"\n{result['platform'].upper()}:\n{platform_files}")
            
            message = (
                f"Successfully generated cross-platform code for {platforms_str}!\n\n"
                f"Generated files:{''.join(files_summary)}"
            )
            
            return CallToolResult(content=[TextContent(type="text", text=message)])
            
        except Exception as e:
            self.logger.error(f"Error in generate_multiplatform_code: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    async def _parse_cpp_interface(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Parse C++ interface."""
        try:
            request = ParseCppInterfaceRequest(**arguments)
            
            parser = CppInterfaceParser()
            parsed = parser.parse(request.cpp_interface)
            
            params_str = "\n".join(f"  - {p.type} {p.name}" for p in parsed.parameters)
            
            message = (
                f"Parsed C++ interface:\n\n"
                f"Function: {parsed.function_name}\n"
                f"Return Type: {parsed.return_type}\n"
                f"Parameters:\n{params_str}\n\n"
                f"Namespace: {parsed.namespace or 'global'}"
            )
            
            return CallToolResult(content=[TextContent(type="text", text=message)])
            
        except Exception as e:
            self.logger.error(f"Error in parse_cpp_interface: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    async def _list_supported_platforms(self, arguments: Dict[str, Any]) -> CallToolResult:
        """List supported platforms."""
        try:
            platforms = [
                {"name": "android", "description": "Android JNI bindings (Java/Kotlin)"},
                {"name": "ios", "description": "iOS Objective-C bindings"},
                {"name": "harmony", "description": "HarmonyOS NAPI bindings"}
            ]
            
            platforms_str = "\n".join(
                f"- {p['name']}: {p['description']}" for p in platforms
            )
            
            message = f"Supported platforms:\n{platforms_str}"
            
            return CallToolResult(content=[TextContent(type="text", text=message)])
            
        except Exception as e:
            self.logger.error(f"Error in list_supported_platforms: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    async def run(self) -> None:
        """Run the MCP server."""
        await self.server.run_stdio()