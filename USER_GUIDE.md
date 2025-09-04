# 跨平台代码生成器使用指南

这是一个详细的用户使用指南，帮助您快速上手跨平台代码生成器 MCP 工具。

## 🎯 工具简介

这是一个 MCP (Model Context Protocol) 工具，可以从 C++ 接口函数自动生成 Android、iOS 和鸿蒙等平台的调用代码。支持：

- **Android**: JNI C++ + Java/Kotlin 包装类
- **iOS**: Objective-C 桥接 + Swift 包装类
- **鸿蒙**: NAPI C++ + TypeScript/ArkTS 包装类

## 📋 系统要求

### 选项 1: Node.js 版本
- Node.js 18.0+ 
- npm 或 yarn
- 支持的系统: Windows, macOS, Linux

### 选项 2: Python 版本
- Python 3.8+
- pip 包管理器
- 支持的系统: Windows, macOS, Linux

## 🚀 快速开始

### 步骤 1: 下载和安装

```bash
# 下载项目
git clone <项目地址>
cd multiplatform_code

# 选择版本并安装依赖
```

#### Node.js 版本
```bash
# 安装依赖
npm install

# 验证安装
npm test
```

#### Python 版本
```bash
cd python

# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 验证安装
python test_generator.py
```

### 步骤 2: 配置 MCP 客户端

#### 配置 Claude Desktop

1. **找到配置文件位置**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **添加配置** (选择一个版本):

**Node.js 版本配置**:
```json
{
  "mcpServers": {
    "multiplatform-code-generator": {
      "command": "node",
      "args": ["/绝对路径/到/multiplatform_code/src/index.js"],
      "env": {}
    }
  }
}
```

**Python 版本配置**:
```json
{
  "mcpServers": {
    "multiplatform-code-generator-python": {
      "command": "python",
      "args": ["/绝对路径/到/multiplatform_code/python/start_mcp.py"],
      "env": {
        "PYTHONPATH": "/绝对路径/到/multiplatform_code/python/src"
      }
    }
  }
}
```

3. **重启 Claude Desktop**

#### 配置其他 MCP 客户端

如果您使用其他支持 MCP 的客户端（如 Cursor），请参考对应的 MCP 配置文档。

### 步骤 3: 验证安装

在 Claude Desktop 中输入：

```
请列出支持的平台
```

如果配置成功，您应该看到类似的回复：
```
支持的平台：
- android: Android JNI bindings (Java/Kotlin)
- ios: iOS Objective-C bindings
- harmony: HarmonyOS NAPI bindings
```

## 📖 基本使用方法

### 1. 解析 C++ 接口

```
请解析这个 C++ 接口：
```cpp
namespace Calculator {
    int add(int a, int b);
    double divide(double numerator, double denominator);
}
```

### 2. 生成跨平台代码

```
请根据以下 C++ 接口生成 Android 和 iOS 的代码：

```cpp
namespace MathUtils {
    int factorial(int n);
    std::string formatNumber(double value, int precision);
}
```

输出目录：./generated
Android 配置：
- 包名：com.example.math
- 类名：MathUtils
- 语言：kotlin

iOS 配置：
- 类前缀：MU
- 框架名：MathUtils
```

### 3. 生成单个平台代码

```
请为这个 C++ 函数生成鸿蒙 NAPI 代码：

```cpp
bool validateEmail(const std::string& email);
```

输出目录：./harmony-output
鸿蒙配置：
- 模块名：Validator
- 命名空间：validator
```

## 🔧 高级用法

### 支持的 C++ 类型

| C++ 类型 | Android | iOS | 鸿蒙 |
|----------|---------|-----|------|
| `int` | `int`/`Int` | `int` | `number` |
| `double` | `double`/`Double` | `double` | `number` |
| `bool` | `boolean`/`Boolean` | `BOOL` | `boolean` |
| `std::string` | `String` | `NSString*` | `string` |
| `void` | `void`/`Unit` | `void` | `void` |

### 配置参数详解

#### Android 配置
```json
{
  "package_name": "com.example.package",  // 必需：Java/Kotlin 包名
  "class_name": "ClassName",             // 必需：类名
  "language": "kotlin"                   // 可选：java 或 kotlin (默认 java)
}
```

#### iOS 配置
```json
{
  "class_prefix": "CPP",                 // 可选：Objective-C 类前缀 (默认 CPP)
  "framework_name": "Framework"          // 可选：框架名 (默认 CppBridge)
}
```

#### 鸿蒙配置
```json
{
  "module_name": "Module",               // 可选：模块名 (默认 CppBridge)
  "namespace": "namespace"               // 可选：NAPI 命名空间 (默认 cppbridge)
}
```

## 📁 生成的文件说明

### Android 输出文件

```
android/
├── jni/
│   ├── function_name_jni.cpp     # JNI C++ 实现
│   ├── function_name_jni.h       # JNI C++ 头文件
│   └── CMakeLists.txt            # CMake 构建配置
├── src/main/java/...             # Java 包装类 (如果选择 Java)
├── src/main/kotlin/...           # Kotlin 包装类 (如果选择 Kotlin)
└── build.gradle.jni              # Gradle 配置示例
```

### iOS 输出文件

```
ios/
├── PrefixClassName.h             # Objective-C 头文件
├── PrefixClassName.m             # Objective-C 实现
├── PrefixClassNameBridge.hpp     # C++ 桥接头文件
├── PrefixClassNameBridge.cpp     # C++ 桥接实现
├── PrefixClassNameSwift.swift    # Swift 包装类
├── FrameworkName.podspec         # CocoaPods 配置
└── Config.xcconfig               # Xcode 配置
```

### 鸿蒙输出文件

```
harmony/
├── src/main/cpp/
│   ├── napi/
│   │   ├── function_name_napi.cpp    # NAPI C++ 实现
│   │   ├── function_name_napi.h      # NAPI C++ 头文件
│   │   └── napi_init.cpp            # NAPI 模块注册
│   └── CMakeLists.txt               # CMake 构建配置
├── src/main/ets/
│   ├── ModuleName.ets               # ArkTS 包装类
│   └── types/ModuleName.d.ts        # TypeScript 声明
├── oh-package.json5                 # 鸿蒙包配置
└── build-profile.json5              # 构建配置
```

## 🛠️ 集成到项目

### Android 项目集成

1. **复制生成的文件**到您的 Android 项目
2. **修改 `app/build.gradle`**:
```gradle
android {
    externalNativeBuild {
        cmake {
            path "src/main/cpp/CMakeLists.txt"
        }
    }
}
```
3. **在 Java/Kotlin 中使用**:
```kotlin
val mathUtils = MathUtils()
val result = mathUtils.add(5, 3)
```

### iOS 项目集成

1. **将生成的文件添加到 Xcode 项目**
2. **在 Build Settings 中添加**:
   - Header Search Paths: 包含 C++ 头文件目录
   - Other C++ Flags: `-std=c++17`
3. **在 Swift 中使用**:
```swift
let calculator = CPPCalculatorSwift()
let result = calculator.add(5, b: 3)
```

### 鸿蒙项目集成

1. **复制生成的文件**到 HarmonyOS 项目
2. **在 ArkTS 中使用**:
```typescript
import { Calculator } from './Calculator';

const result = Calculator.add(5, 3);
```

## 🐛 故障排除

### 常见问题

#### 1. "MCP 服务器未连接"
**解决方案**:
- 检查配置文件路径是否正确
- 确保使用绝对路径
- 重启 MCP 客户端

#### 2. "命令未找到"
**解决方案**:
- Node.js: 确保 Node.js 已安装且在 PATH 中
- Python: 确保 Python 已安装且在 PATH 中

#### 3. "权限被拒绝"
**解决方案**:
```bash
# 给启动脚本添加执行权限
chmod +x start-mcp.sh
chmod +x python/start_mcp.sh
```

#### 4. "依赖缺失"
**解决方案**:
```bash
# Node.js 版本
npm install

# Python 版本
pip install -r requirements.txt
```

#### 5. "解析失败"
**解决方案**:
- 检查 C++ 语法是否正确
- 确保函数声明完整
- 避免使用复杂的模板类型

### 调试模式

#### Node.js 版本
```bash
# 启用详细日志
DEBUG=* npm start
```

#### Python 版本
```bash
# 启用详细日志
python start_mcp.py --test
```

## 📚 示例代码

### 完整示例：数学库

```
请为以下数学库生成所有平台的代码：

```cpp
namespace MathLibrary {
    // 基础运算
    int add(int a, int b);
    int subtract(int a, int b);
    double multiply(double x, double y);
    double divide(double numerator, double denominator);
    
    // 实用函数
    bool isPrime(int number);
    std::string formatCurrency(double amount);
}
```

配置：
- 输出目录：./math-library
- 平台：android, ios, harmony
- Android：com.example.mathlib, MathLibrary, kotlin
- iOS：Math, MathLibrary
- 鸿蒙：MathLibrary, mathlib
```

这将生成完整的跨平台数学库代码，包含所有必要的文件和配置。

## 🔄 更新和维护

### 获取更新

```bash
# 拉取最新代码
git pull origin main

# 重新安装依赖
npm install  # Node.js 版本
# 或
pip install -r requirements.txt  # Python 版本
```

### 备份配置

建议备份您的 MCP 客户端配置文件，以便在重新安装时快速恢复。

## 📞 获取帮助

如果遇到问题，可以：

1. **查看文档**: 
   - [README.md](README.md) - 基础文档
   - [EXAMPLES.md](EXAMPLES.md) - 详细示例
   - [DEPLOYMENT.md](DEPLOYMENT.md) - 部署指南

2. **运行测试**: 验证工具是否正常工作
   ```bash
   npm test              # Node.js 版本
   python test_generator.py  # Python 版本
   ```

3. **检查版本**: 确认使用的是哪个版本
   ```bash
   ./start-mcp.sh --version      # Node.js 版本
   python start_mcp.py --version # Python 版本
   ```

4. **联系支持**: 
   - GitHub Issues: 报告 bug 或功能请求
   - 项目文档: 查看最新文档

---

**祝您使用愉快！让跨平台开发变得简单！** 🚀
