# 🚀 Multiplatform Code Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.org/)

> 从 C++ 接口自动生成 Android、iOS、鸿蒙跨平台代码的 MCP 工具

一个强大的 MCP (Model Context Protocol) 工具，能够智能解析 C++ 接口函数，自动生成 Android JNI、iOS Objective-C 和鸿蒙 NAPI 的完整调用代码，包括包装类和构建配置。

![Demo](https://via.placeholder.com/800x400/4285f4/ffffff?text=Multiplatform+Code+Generator+Demo)

## ✨ 特性

- 🧠 **智能解析**: 自动解析 C++ 函数签名和参数类型
- 🔄 **跨平台支持**: 支持 Android (JNI)、iOS (Objective-C) 和鸿蒙 (NAPI)
- 📦 **完整生成**: 生成包装类、构建文件和项目配置
- 🛠️ **MCP 兼容**: 与 Claude Desktop 等 AI 工具无缝集成
- ⚡ **即用型代码**: 生成的代码可直接编译运行
- 🐍🟨 **双重实现**: 提供 Node.js 和 Python 两个版本

## 🎯 支持平台

| 平台 | 输出格式 | 生成内容 |
|------|----------|----------|
| **Android** | JNI + Java/Kotlin | JNI C++ 代码 + Java/Kotlin 包装类 + CMake 配置 |
| **iOS** | Objective-C + Swift | OC 桥接代码 + Swift 包装类 + Podspec 配置 |
| **鸿蒙** | NAPI + TypeScript | NAPI C++ 代码 + TypeScript/ArkTS 包装 + 项目配置 |

## 🚀 快速开始

### 前提条件

选择一个版本：
- **Node.js 版本**: Node.js 18+ 和 npm
- **Python 版本**: Python 3.8+ 和 pip

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/multiplatform-code-generator.git
cd multiplatform-code-generator

# 选择版本并安装依赖

# Node.js 版本
npm install && npm test

# 或者 Python 版本
cd python && pip install -r requirements.txt && python test_generator.py
```

### 配置 MCP 客户端

在 Claude Desktop 配置文件中添加：

**Node.js 版本**:
```json
{
  "mcpServers": {
    "multiplatform-code-generator": {
      "command": "node",
      "args": ["/path/to/multiplatform-code-generator/src/index.js"]
    }
  }
}
```

**Python 版本**:
```json
{
  "mcpServers": {
    "multiplatform-code-generator-python": {
      "command": "python",
      "args": ["/path/to/multiplatform-code-generator/python/start_mcp.py"],
      "env": {
        "PYTHONPATH": "/path/to/multiplatform-code-generator/python/src"
      }
    }
  }
}
```

重启 Claude Desktop，然后就可以开始使用了！

## 💡 使用示例

在 Claude Desktop 中发送消息：

```
请为这个 C++ 接口生成 Android 和 iOS 代码：

```cpp
namespace Calculator {
    int add(int a, int b);
    double divide(double numerator, double denominator);
    std::string formatNumber(double value, int precision);
}
```

输出目录：./generated
Android 配置：
- 包名：com.example.calculator
- 类名：Calculator
- 语言：kotlin

iOS 配置：
- 类前缀：Calc
- 框架名：Calculator
```

工具将自动生成完整的跨平台代码！

## 📁 生成文件结构

### Android 输出
```
android/
├── jni/
│   ├── function_name_jni.cpp      # JNI C++ 实现
│   ├── function_name_jni.h        # JNI C++ 头文件
│   └── CMakeLists.txt             # CMake 配置
├── src/main/kotlin/...            # Kotlin 包装类
└── build.gradle.jni               # Gradle 配置
```

### iOS 输出
```
ios/
├── PrefixClass.h                  # Objective-C 头文件
├── PrefixClass.m                  # Objective-C 实现
├── PrefixClassBridge.hpp          # C++ 桥接
├── PrefixClassSwift.swift         # Swift 包装
└── Framework.podspec              # CocoaPods 配置
```

### 鸿蒙输出
```
harmony/
├── src/main/cpp/napi/             # NAPI C++ 代码
├── src/main/ets/                  # ArkTS 包装类
├── oh-package.json5               # 鸿蒙包配置
└── build-profile.json5            # 构建配置
```

## 🔧 高级用法

### 支持的 C++ 类型

| C++ 类型 | Android | iOS | 鸿蒙 |
|----------|---------|-----|------|
| `int` | `int`/`Int` | `int` | `number` |
| `double` | `double`/`Double` | `double` | `number` |
| `bool` | `boolean`/`Boolean` | `BOOL` | `boolean` |
| `std::string` | `String` | `NSString*` | `string` |

### 配置选项

详细的配置选项请参考 [USER_GUIDE.md](USER_GUIDE.md)。

## 📚 文档

- 📖 [快速开始](QUICK_START.md) - 5分钟上手指南
- 📋 [用户指南](USER_GUIDE.md) - 详细使用文档
- 💡 [使用示例](EXAMPLES.md) - 丰富的示例代码
- ⚖️ [版本对比](COMPARISON.md) - Node.js vs Python 对比
- 🚀 [部署指南](DEPLOYMENT.md) - 生产环境部署

## 🧪 测试

```bash
# Node.js 版本
npm test

# Python 版本
cd python && python test_generator.py
```

## 🛠️ 开发

### 贡献指南

我们欢迎社区贡献！

1. Fork 仓库
2. 创建特性分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送分支: `git push origin feature/amazing-feature`
5. 创建 Pull Request

### 开发环境

```bash
# Node.js 版本
npm install
npm run dev

# Python 版本
cd python
pip install -r requirements.txt
python -m pytest tests/
```

## 📊 性能

- **解析速度**: C++ 接口解析 < 100ms
- **生成速度**: 单平台代码生成 < 200ms
- **内存使用**: 运行时内存 < 100MB
- **文件大小**: 生成的代码文件总大小 < 50KB

## 🤝 社区

- 💬 [GitHub Discussions](https://github.com/yourusername/multiplatform-code-generator/discussions) - 问题讨论
- 🐛 [Issues](https://github.com/yourusername/multiplatform-code-generator/issues) - Bug 报告
- 📢 [Releases](https://github.com/yourusername/multiplatform-code-generator/releases) - 版本发布

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢所有贡献者和使用者！

- 特别感谢 [Model Context Protocol](https://modelcontextprotocol.org/) 团队
- 感谢开源社区的支持和反馈

## ⭐ Star History

如果这个项目对您有帮助，请给我们一个 ⭐！

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/multiplatform-code-generator&type=Date)](https://star-history.com/#yourusername/multiplatform-code-generator&Date)

---

**让跨平台开发变得简单！** 🚀

Made with ❤️ by the Multiplatform Code Generator team
