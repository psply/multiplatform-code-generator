#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { CppInterfaceParser } from "./parsers/cpp-parser.js";
import { AndroidJniGenerator } from "./generators/android-jni.js";
import { IosOcGenerator } from "./generators/ios-oc.js";
import { HarmonyNapiGenerator } from "./generators/harmony-napi.js";
import { FileManager } from "./utils/file-manager.js";

const server = new Server(
  {
    name: "multiplatform-code-generator",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 工具列表
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "generate_multiplatform_code",
        description: "Generate cross-platform code from C++ interface",
        inputSchema: {
          type: "object",
          properties: {
            cpp_interface: {
              type: "string",
              description: "C++ interface function code"
            },
            output_directory: {
              type: "string",
              description: "Base output directory for generated files"
            },
            platforms: {
              type: "array",
              items: {
                type: "string",
                enum: ["android", "ios", "harmony"]
              },
              description: "Target platforms to generate code for"
            },
            android_config: {
              type: "object",
              properties: {
                package_name: {
                  type: "string",
                  description: "Java/Kotlin package name for Android"
                },
                class_name: {
                  type: "string",
                  description: "Java/Kotlin class name for Android"
                },
                language: {
                  type: "string",
                  enum: ["java", "kotlin"],
                  description: "Programming language for Android wrapper"
                }
              },
              description: "Android-specific configuration"
            },
            ios_config: {
              type: "object",
              properties: {
                class_prefix: {
                  type: "string",
                  description: "Objective-C class prefix"
                },
                framework_name: {
                  type: "string",
                  description: "iOS framework name"
                }
              },
              description: "iOS-specific configuration"
            },
            harmony_config: {
              type: "object",
              properties: {
                module_name: {
                  type: "string",
                  description: "HarmonyOS module name"
                },
                namespace: {
                  type: "string",
                  description: "NAPI namespace"
                }
              },
              description: "HarmonyOS-specific configuration"
            }
          },
          required: ["cpp_interface", "output_directory", "platforms"]
        }
      },
      {
        name: "parse_cpp_interface",
        description: "Parse C++ interface and extract function information",
        inputSchema: {
          type: "object",
          properties: {
            cpp_interface: {
              type: "string",
              description: "C++ interface function code to parse"
            }
          },
          required: ["cpp_interface"]
        }
      },
      {
        name: "list_supported_platforms",
        description: "List all supported target platforms",
        inputSchema: {
          type: "object",
          properties: {},
          required: []
        }
      }
    ]
  };
});

// 工具调用处理
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "generate_multiplatform_code":
        return await generateMultiplatformCode(args);
      
      case "parse_cpp_interface":
        return await parseCppInterface(args);
      
      case "list_supported_platforms":
        return await listSupportedPlatforms();
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`
        }
      ]
    };
  }
});

async function generateMultiplatformCode(args) {
  const {
    cpp_interface,
    output_directory,
    platforms,
    android_config,
    ios_config,
    harmony_config
  } = args;

  // 解析C++接口
  const parser = new CppInterfaceParser();
  const parsedInterface = parser.parse(cpp_interface);

  const results = [];
  const fileManager = new FileManager(output_directory);

  // 为每个平台生成代码
  for (const platform of platforms) {
    switch (platform) {
      case "android":
        if (!android_config?.package_name || !android_config?.class_name) {
          throw new Error("Android platform requires package_name and class_name in android_config");
        }
        const androidGenerator = new AndroidJniGenerator(android_config);
        const androidFiles = await androidGenerator.generate(parsedInterface, fileManager);
        results.push({
          platform: "android",
          files: androidFiles
        });
        break;

      case "ios":
        const iosGenerator = new IosOcGenerator(ios_config || {});
        const iosFiles = await iosGenerator.generate(parsedInterface, fileManager);
        results.push({
          platform: "ios",
          files: iosFiles
        });
        break;

      case "harmony":
        const harmonyGenerator = new HarmonyNapiGenerator(harmony_config || {});
        const harmonyFiles = await harmonyGenerator.generate(parsedInterface, fileManager);
        results.push({
          platform: "harmony",
          files: harmonyFiles
        });
        break;

      default:
        throw new Error(`Unsupported platform: ${platform}`);
    }
  }

  return {
    content: [
      {
        type: "text",
        text: `Successfully generated cross-platform code for ${platforms.join(", ")}!\n\nGenerated files:\n${results.map(r => 
          `\n${r.platform.toUpperCase()}:\n${r.files.map(f => `  - ${f}`).join('\n')}`
        ).join('\n')}`
      }
    ]
  };
}

async function parseCppInterface(args) {
  const { cpp_interface } = args;
  
  const parser = new CppInterfaceParser();
  const parsedInterface = parser.parse(cpp_interface);

  return {
    content: [
      {
        type: "text",
        text: `Parsed C++ interface:\n\nFunction: ${parsedInterface.functionName}\nReturn Type: ${parsedInterface.returnType}\nParameters:\n${parsedInterface.parameters.map(p => `  - ${p.type} ${p.name}`).join('\n')}\n\nNamespace: ${parsedInterface.namespace || 'global'}`
      }
    ]
  };
}

async function listSupportedPlatforms() {
  const platforms = [
    { name: "android", description: "Android JNI bindings (Java/Kotlin)" },
    { name: "ios", description: "iOS Objective-C bindings" },
    { name: "harmony", description: "HarmonyOS NAPI bindings" }
  ];

  return {
    content: [
      {
        type: "text",
        text: `Supported platforms:\n${platforms.map(p => `- ${p.name}: ${p.description}`).join('\n')}`
      }
    ]
  };
}

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Multiplatform Code Generator MCP server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
