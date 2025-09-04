# 项目总览

## 🎯 项目简介

**跨平台代码生成器 MCP 工具** 是一个强大的模型上下文协议 (Model Context Protocol) 工具，专门设计用于从 C++ 接口函数自动生成多平台的调用代码。该工具可以与大模型（如 Claude、GPT 等）无缝集成，提供智能的跨平台开发解决方案。

## 🏗️ 架构设计

```
multiplatform_code/
├── src/
│   ├── index.js                    # MCP 服务器主入口
│   ├── parsers/
│   │   └── cpp-parser.js          # C++ 接口解析器
│   ├── generators/
│   │   ├── android-jni.js         # Android JNI 代码生成器
│   │   ├── ios-oc.js              # iOS Objective-C 代码生成器
│   │   └── harmony-napi.js        # 鸿蒙 NAPI 代码生成器
│   └── utils/
│       └── file-manager.js        # 文件管理工具
├── test.js                        # 测试脚本
├── start-mcp.sh                   # 启动脚本
├── package.json                   # 项目配置
├── README.md                      # 使用文档
├── DEPLOYMENT.md                  # 部署指南
├── EXAMPLES.md                    # 使用示例
└── LICENSE                        # 许可证
```

## 🚀 核心功能

### 1. 智能解析
- **C++ 函数签名解析**: 自动识别函数名、参数类型、返回值类型
- **命名空间支持**: 正确处理 C++ 命名空间
- **类型映射**: 智能映射 C++ 类型到目标平台类型
- **错误检测**: 提供详细的解析错误信息

### 2. 多平台支持

#### Android (JNI)
- 生成 JNI C++ 桥接代码
- 支持 Java 和 Kotlin 包装类
- 自动处理 JNI 类型转换
- 生成完整的构建配置 (CMakeLists.txt, Gradle)

#### iOS (Objective-C)
- 生成 Objective-C 桥接代码
- 支持 Swift 包装类
- 自动内存管理 (ARC)
- 生成 Podspec 和 Xcode 配置

#### 鸿蒙 (NAPI)
- 生成 NAPI C++ 桥接代码
- 支持 TypeScript/ArkTS 包装类
- 异步调用支持
- 生成完整的 HarmonyOS 项目配置

### 3. MCP 协议集成
- 标准 MCP 协议实现
- 支持多种 MCP 客户端 (Claude Desktop, Cursor 等)
- 实时工具调用
- 错误处理和状态报告

## 🛠️ 技术栈

- **运行时**: Node.js 18+
- **协议**: Model Context Protocol (MCP)
- **语言**: JavaScript (ES6+)
- **依赖**: @modelcontextprotocol/sdk

## 📦 生成的代码结构

### Android 输出
```
android/
├── jni/
│   ├── function_name_jni.cpp      # JNI C++ 实现
│   ├── function_name_jni.h        # JNI C++ 头文件
│   └── CMakeLists.txt             # CMake 构建配置
├── src/main/java/               # Java 包装类
│   └── [package]/[Class].java
├── src/main/kotlin/             # Kotlin 包装类 (可选)
│   └── [package]/[Class].kt
└── build.gradle.jni             # Gradle 配置片段
```

### iOS 输出
```
ios/
├── [Prefix][Class].h            # Objective-C 头文件
├── [Prefix][Class].m            # Objective-C 实现
├── [Prefix][Class]Bridge.hpp    # C++ 桥接头文件
├── [Prefix][Class]Bridge.cpp    # C++ 桥接实现
├── [Prefix][Class]Swift.swift   # Swift 包装类
├── [Framework].podspec          # Podspec 文件
└── Config.xcconfig              # Xcode 配置
```

### 鸿蒙 输出
```
harmony/
├── src/main/cpp/
│   ├── napi/
│   │   ├── function_name_napi.cpp   # NAPI C++ 实现
│   │   ├── function_name_napi.h     # NAPI C++ 头文件
│   │   └── napi_init.cpp            # NAPI 模块注册
│   └── CMakeLists.txt               # CMake 构建配置
├── src/main/ets/
│   ├── [Module].ets                 # ArkTS 包装类
│   └── types/[Module].d.ts          # TypeScript 声明
├── oh-package.json5                 # 鸿蒙包配置
└── build-profile.json5              # 构建配置
```

## 🔧 可用工具

### 1. generate_multiplatform_code
**描述**: 生成跨平台代码的主要工具

**参数**:
- `cpp_interface`: C++ 接口函数代码
- `output_directory`: 输出目录路径
- `platforms`: 目标平台数组
- `android_config`: Android 特定配置
- `ios_config`: iOS 特定配置
- `harmony_config`: 鸿蒙特定配置

### 2. parse_cpp_interface
**描述**: 解析 C++ 接口并提取函数信息

**参数**:
- `cpp_interface`: C++ 接口函数代码

### 3. list_supported_platforms
**描述**: 列出所有支持的目标平台

## 🎯 使用场景

1. **跨平台库开发**: 为 C++ 库快速生成多平台绑定
2. **原型开发**: 快速验证跨平台接口设计
3. **代码模板生成**: 生成标准化的平台特定代码模板
4. **自动化工具**: 集成到 CI/CD 流程中自动生成代码
5. **学习和教育**: 学习不同平台的 FFI (Foreign Function Interface) 实现

## 🌟 核心优势

### 1. 开发效率
- **一次定义，多处生成**: 只需定义 C++ 接口，自动生成所有平台代码
- **即用代码**: 生成的代码可以直接编译和使用
- **智能转换**: 自动处理类型转换和内存管理

### 2. 代码质量
- **最佳实践**: 遵循各平台的编程最佳实践
- **错误处理**: 内置完善的错误处理机制
- **内存安全**: 自动处理内存分配和释放

### 3. 可维护性
- **标准化结构**: 生成统一的项目结构
- **完整文档**: 自动生成注释和文档
- **版本兼容**: 支持各平台的最新版本

### 4. 可扩展性
- **模块化设计**: 易于添加新平台支持
- **插件架构**: 支持自定义代码生成器
- **配置灵活**: 丰富的配置选项

## 📈 性能特点

- **快速解析**: 高效的 C++ 代码解析算法
- **并行生成**: 支持多平台并行代码生成
- **内存优化**: 优化的内存使用模式
- **文件 I/O**: 异步文件操作提高性能

## 🔮 未来规划

### 短期目标 (v1.1)
- 支持更多 C++ 类型 (vector, map 等)
- 添加代码格式化选项
- 改进错误消息和调试信息

### 中期目标 (v1.5)
- 支持 C++ 类和对象
- 添加 Flutter/Dart 平台支持
- 集成代码质量检查

### 长期目标 (v2.0)
- 支持 Rust FFI
- Web Assembly (WASM) 支持
- 图形化配置界面

## 🤝 贡献指南

我们欢迎社区贡献！请参考以下步骤：

1. Fork 项目仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 开发环境设置
```bash
git clone <repository-url>
cd multiplatform_code
npm install
npm test
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 支持与联系

- **文档**: [README.md](README.md)
- **示例**: [EXAMPLES.md](EXAMPLES.md)
- **部署**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **问题报告**: GitHub Issues
- **功能请求**: GitHub Discussions

---

**让跨平台开发变得简单！** 🚀
