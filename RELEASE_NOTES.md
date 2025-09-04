# 🎉 Multiplatform Code Generator v1.0.0

首次发布！一个强大的 MCP 工具，能够从 C++ 接口自动生成 Android、iOS、鸿蒙三平台的调用代码。

## ✨ 主要特性

- 🧠 **智能 C++ 解析**: 自动解析函数签名、参数类型、命名空间
- 🔄 **三平台支持**: Android JNI、iOS Objective-C、鸿蒙 NAPI
- 📦 **完整代码生成**: 包装类 + 构建配置 + 项目文件
- 🛠️ **MCP 集成**: 与 Claude Desktop 等 AI 工具无缝配合
- ⚡ **即用型**: 生成的代码可直接编译运行
- 🐍🟨 **双重实现**: Node.js 和 Python 两个版本

## 📦 包含内容

### 代码生成能力
- **Android**: JNI C++ + Java/Kotlin 包装 + CMake + Gradle 配置
- **iOS**: Objective-C 桥接 + Swift 包装 + Podspec + Xcode 配置  
- **鸿蒙**: NAPI C++ + TypeScript/ArkTS 包装 + 项目配置

### 完整文档
- 📖 [QUICK_START.md](QUICK_START.md) - 5分钟快速上手
- 📚 [USER_GUIDE.md](USER_GUIDE.md) - 详细使用指南
- 💡 [EXAMPLES.md](EXAMPLES.md) - 丰富使用示例
- ⚖️ [COMPARISON.md](COMPARISON.md) - 版本对比说明

## 🚀 快速开始

### 1. 安装
```bash
git clone https://github.com/psply/multiplatform-code-generator.git
cd multiplatform-code-generator

# 选择版本
npm install && npm test              # Node.js 版本
# 或
cd python && pip install -r requirements.txt && python test_generator.py  # Python 版本
```

### 2. 配置 Claude Desktop
按照 [QUICK_START.md](QUICK_START.md) 配置 MCP 服务器

### 3. 开始使用
```
请为这个 C++ 函数生成 Android 和 iOS 代码：

int add(int a, int b);

输出目录：./generated
Android 配置：com.example.math, Calculator, kotlin
```

## 📊 测试结果

✅ **功能测试**: 100% 通过
- C++ 接口解析测试
- 三平台代码生成测试  
- 文件完整性验证测试

✅ **兼容性测试**: 
- macOS, Windows, Linux
- Node.js 18+, Python 3.8+

✅ **性能测试**:
- C++ 解析: < 100ms
- 代码生成: < 500ms (三平台)
- 内存使用: < 100MB

## 🎯 使用场景

- 📱 **跨平台库开发**: 为 C++ 库快速生成多平台绑定
- 🔄 **原型验证**: 快速验证跨平台接口设计
- 🏗️ **代码模板**: 生成标准化的平台特定代码
- 🤖 **AI 辅助开发**: 结合 AI 工具提升开发效率

## 🔧 系统要求

**选择一个版本**:
- **Node.js 版本**: Node.js 18+ + npm
- **Python 版本**: Python 3.8+ + pip

**MCP 客户端**:
- Claude Desktop (推荐)
- 或其他支持 MCP 的客户端

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

- 🐛 [报告 Bug](https://github.com/psply/multiplatform-code-generator/issues)
- 💡 [功能请求](https://github.com/psply/multiplatform-code-generator/issues)
- 📖 [贡献指南](https://github.com/psply/multiplatform-code-generator/blob/main/USER_GUIDE.md)

## 🔄 更新计划

- v1.1: 支持更多 C++ 类型 (vector, map 等)
- v1.2: 添加配置文件支持
- v1.3: Web 界面
- v2.0: 插件系统

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**让跨平台开发变得简单！** 🚀

感谢使用 Multiplatform Code Generator！
