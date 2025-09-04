# 跨平台代码生成器 MCP 工具

一个强大的 MCP (Model Context Protocol) 工具，能够从 C++ 接口函数自动生成 Android、iOS 和鸿蒙等不同平台的调用代码。

## 功能特性

- 🔄 **跨平台支持**: 支持 Android (JNI)、iOS (Objective-C) 和鸿蒙 (NAPI)
- 🧠 **智能解析**: 自动解析 C++ 函数签名和参数类型
- 📦 **完整生成**: 生成包装类、构建文件和配置文件
- 🛠️ **MCP 兼容**: 与大模型无缝集成，支持 Claude、GPT 等
- ⚡ **即用型代码**: 生成的代码可直接编译运行

## 支持平台

| 平台 | 输出格式 | 描述 |
|------|----------|------|
| Android | JNI + Java/Kotlin | 生成 JNI C++ 代码和 Java/Kotlin 包装类 |
| iOS | Objective-C | 生成 Objective-C 桥接代码和 Swift 包装 |
| 鸿蒙 | NAPI + ArkTS | 生成 NAPI C++ 代码和 TypeScript/ArkTS 包装 |

## 安装

### 前置要求

- Node.js 18+ 
- npm 或 yarn

### 安装步骤

1. 克隆仓库:
```bash
git clone <repository-url>
cd multiplatform_code
```

2. 安装依赖:
```bash
npm install
```

3. 启动 MCP 服务器:
```bash
npm start
```

## 配置 MCP 客户端

### Claude Desktop 配置

在 Claude Desktop 的 `claude_desktop_config.json` 文件中添加:

```json
{
  "mcpServers": {
    "multiplatform-code-generator": {
      "command": "node",
      "args": ["/path/to/multiplatform_code/src/index.js"],
      "env": {}
    }
  }
}
```

### 其他 MCP 客户端

参考您使用的 MCP 客户端文档进行配置。

## 使用方法

### 基本用法

1. 在 MCP 客户端中调用工具
2. 提供 C++ 接口函数代码
3. 指定输出目录和目标平台
4. 配置平台特定参数

### 示例

#### 生成跨平台代码

```javascript
// C++ 接口示例
const cppInterface = `
namespace MathUtils {
    int add(int a, int b);
    std::string formatNumber(double value, int precision);
}
`;

// 调用生成工具
generate_multiplatform_code({
  cpp_interface: cppInterface,
  output_directory: "/path/to/output",
  platforms: ["android", "ios", "harmony"],
  android_config: {
    package_name: "com.example.mathutils",
    class_name: "MathUtils",
    language: "kotlin"
  },
  ios_config: {
    class_prefix: "MU",
    framework_name: "MathUtils"
  },
  harmony_config: {
    module_name: "MathUtils",
    namespace: "mathutils"
  }
});
```

#### 解析 C++ 接口

```javascript
parse_cpp_interface({
  cpp_interface: "int multiply(int x, int y);"
});
```

## 可用工具

### 1. generate_multiplatform_code

生成跨平台代码的主要工具。

**参数:**
- `cpp_interface` (必需): C++ 接口函数代码
- `output_directory` (必需): 输出目录路径
- `platforms` (必需): 目标平台数组 (`["android", "ios", "harmony"]`)
- `android_config` (可选): Android 配置
  - `package_name`: Java/Kotlin 包名
  - `class_name`: 类名
  - `language`: "java" 或 "kotlin"
- `ios_config` (可选): iOS 配置
  - `class_prefix`: Objective-C 类前缀
  - `framework_name`: 框架名称
- `harmony_config` (可选): 鸿蒙配置
  - `module_name`: 模块名称
  - `namespace`: NAPI 命名空间

### 2. parse_cpp_interface

解析 C++ 接口函数并提取信息。

**参数:**
- `cpp_interface` (必需): C++ 接口函数代码

### 3. list_supported_platforms

列出所有支持的目标平台。

## 生成的文件结构

### Android (JNI)
```
android/
├── jni/
│   ├── function_name_jni.cpp
│   ├── function_name_jni.h
│   └── CMakeLists.txt
├── src/main/java/com/package/ClassName.java
└── build.gradle.jni
```

### iOS (Objective-C)
```
ios/
├── ClassName.h
├── ClassName.m
├── ClassNameBridge.hpp
├── ClassNameBridge.cpp
├── ClassNameSwift.swift
├── FrameworkName.podspec
└── Config.xcconfig
```

### 鸿蒙 (NAPI)
```
harmony/
├── src/main/
│   ├── cpp/
│   │   ├── napi/
│   │   │   ├── function_name_napi.cpp
│   │   │   ├── function_name_napi.h
│   │   │   └── napi_init.cpp
│   │   └── CMakeLists.txt
│   └── ets/
│       ├── ModuleName.ets
│       └── types/ModuleName.d.ts
├── oh-package.json5
└── build-profile.json5
```

## 高级用法

### 支持的 C++ 类型

| C++ 类型 | Android (Java/Kotlin) | iOS (Objective-C) | 鸿蒙 (TypeScript) |
|----------|----------------------|-------------------|-------------------|
| `void` | `void`/`Unit` | `void` | `void` |
| `bool` | `boolean`/`Boolean` | `BOOL` | `boolean` |
| `int` | `int`/`Int` | `int` | `number` |
| `long` | `long`/`Long` | `long` | `number` |
| `float` | `float`/`Float` | `float` | `number` |
| `double` | `double`/`Double` | `double` | `number` |
| `std::string` | `String` | `NSString*` | `string` |

### 错误处理

生成的代码包含适当的错误处理:
- **Android**: Java 异常
- **iOS**: Objective-C 异常
- **鸿蒙**: Promise 拒绝

### 内存管理

- **Android**: 自动处理 JNI 字符串释放
- **iOS**: 使用 ARC (Automatic Reference Counting)
- **鸿蒙**: 自动处理 NAPI 内存

## 故障排除

### 常见问题

1. **解析失败**: 确保 C++ 代码语法正确
2. **类型不支持**: 检查类型映射表
3. **文件权限**: 确保输出目录有写权限

### 调试技巧

1. 使用 `parse_cpp_interface` 验证解析结果
2. 检查生成的代码语法
3. 查看 MCP 服务器日志

## 贡献

欢迎贡献代码！请遵循以下步骤:

1. Fork 仓库
2. 创建特性分支
3. 提交更改
4. 创建 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 支持

如有问题或建议，请:
- 创建 GitHub Issue
- 发送邮件至 support@example.com
- 查看文档和示例

---

**注意**: 此工具生成的代码需要您在项目中包含相应的 C++ 源文件和头文件。
