# 🚀 快速开始指南

5 分钟快速上手跨平台代码生成器！

## 📦 第一步：下载和安装

```bash
# 1. 下载项目
git clone <项目地址>
cd multiplatform_code

# 2. 选择版本 (二选一)

# 选项A: Node.js 版本 (推荐新手)
npm install && npm test

# 选项B: Python 版本
cd python && pip install pydantic typing-extensions && python test_generator.py
```

## ⚙️ 第二步：配置 Claude Desktop

打开 Claude Desktop 配置文件：
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

添加以下配置（**请替换为您的实际路径**）：

### Node.js 版本配置
```json
{
  "mcpServers": {
    "multiplatform-code-generator": {
      "command": "node",
      "args": ["/您的路径/multiplatform_code/src/index.js"]
    }
  }
}
```

### Python 版本配置
```json
{
  "mcpServers": {
    "multiplatform-code-generator-python": {
      "command": "python",
      "args": ["/您的路径/multiplatform_code/python/start_mcp.py"],
      "env": {
        "PYTHONPATH": "/您的路径/multiplatform_code/python/src"
      }
    }
  }
}
```

**重启 Claude Desktop**

## 🎯 第三步：开始使用

在 Claude Desktop 中发送消息：

```
请为这个 C++ 函数生成 Android 和 iOS 代码：

```cpp
namespace Calculator {
    int add(int a, int b);
    std::string format(double value);
}
```

输出目录：./my-project
Android 配置：
- 包名：com.example.calculator
- 类名：Calculator
- 语言：kotlin

iOS 配置：
- 类前缀：Calc
- 框架名：Calculator
```

## ✅ 验证成功

如果配置正确，您应该看到：

1. **工具识别**: Claude 能识别并调用代码生成工具
2. **文件生成**: 在指定目录生成多个平台的代码文件
3. **完整输出**: 包含 JNI、Objective-C、构建文件等

## 🔧 路径设置技巧

### 如何获取绝对路径？

```bash
# 在项目目录中运行
pwd
# 复制输出的路径，例如：/Users/yourname/multiplatform_code
```

### Windows 用户注意
Windows 路径使用反斜杠，在 JSON 中需要转义：
```json
"args": ["C:\\Users\\yourname\\multiplatform_code\\src\\index.js"]
```

## 🐛 常见问题

### 问题 1: "工具未找到"
- ✅ 检查路径是否正确（使用绝对路径）
- ✅ 确保重启了 Claude Desktop
- ✅ 运行测试验证安装是否成功

### 问题 2: "命令执行失败"
- ✅ Node.js 版本：确保 Node.js 18+ 已安装
- ✅ Python 版本：确保 Python 3.8+ 已安装
- ✅ 检查依赖是否正确安装

### 问题 3: "权限问题"
```bash
# 给脚本添加执行权限
chmod +x start-mcp.sh
chmod +x python/start_mcp.sh
```

## 🎉 下一步

成功设置后，您可以：

1. **查看完整文档**: [USER_GUIDE.md](USER_GUIDE.md)
2. **学习更多示例**: [EXAMPLES.md](EXAMPLES.md)
3. **了解两个版本对比**: [COMPARISON.md](COMPARISON.md)

---

**开始您的跨平台开发之旅！** 🌟
