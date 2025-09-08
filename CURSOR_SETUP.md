# 🖱️ Cursor IDE MCP 配置指南

本指南将帮助您在 Cursor IDE 中配置跨平台代码生成器 MCP 工具。

## 📋 配置步骤

### 1. 打开 Cursor 设置

按 `Cmd+,` (macOS) 或 `Ctrl+,` (Windows/Linux) 打开设置页面。

### 2. 打开 settings.json

1. 在设置页面右上角点击 `{}` 图标
2. 或者按 `Cmd+Shift+P` 搜索 "Preferences: Open Settings (JSON)"

### 3. 添加 MCP 配置

在 `settings.json` 的 `"mcp.servers"` 部分添加以下配置：

#### Node.js 版本配置

```json
{
  "mcp.servers": {
    "multiplatform-code-generator": {
      "command": "node",
      "args": ["/Users/shipan/workspace/multiplatform_code/src/index.js"],
      "env": {}
    }
  }
}
```

#### Python 版本配置 (可选)

```json
{
  "mcp.servers": {
    "multiplatform-code-generator-python": {
      "command": "python",
      "args": ["/Users/shipan/workspace/multiplatform_code/python/start_mcp.py"],
      "env": {
        "PYTHONPATH": "/Users/shipan/workspace/multiplatform_code/python/src"
      }
    }
  }
}
```

#### 同时配置两个版本

```json
{
  "mcp.servers": {
    "multiplatform-code-generator": {
      "command": "node",
      "args": ["/Users/shipan/workspace/multiplatform_code/src/index.js"],
      "env": {}
    },
    "multiplatform-code-generator-python": {
      "command": "python",
      "args": ["/Users/shipan/workspace/multiplatform_code/python/start_mcp.py"],
      "env": {
        "PYTHONPATH": "/Users/shipan/workspace/multiplatform_code/python/src"
      }
    }
  }
}
```

### 4. 保存配置

按 `Cmd+S` (macOS) 或 `Ctrl+S` (Windows/Linux) 保存配置文件。

### 5. 重启 Cursor

完全关闭并重新打开 Cursor IDE 以加载新的 MCP 配置。

## 🧪 测试配置

### 1. 打开 AI Chat

在 Cursor 中按 `Cmd+K` (macOS) 或 `Ctrl+K` (Windows/Linux) 打开 AI 对话。

### 2. 测试工具

发送以下测试消息：

```
请列出支持的平台
```

如果配置成功，您应该看到：
```
支持的平台：
- android: Android JNI bindings (Java/Kotlin)
- ios: iOS Objective-C bindings  
- harmony: HarmonyOS NAPI bindings
```

### 3. 实际使用

发送以下消息开始使用：

```
请为这个 C++ 函数生成 Android 和 iOS 代码：

```cpp
int add(int a, int b);
```

输出目录：./test-generated
Android 配置：
- 包名：com.example.test
- 类名：Calculator
- 语言：kotlin
```

## 📁 完整的 settings.json 示例

以下是包含 MCP 配置的完整示例：

```json
{
  "editor.fontSize": 14,
  "editor.formatOnSave": true,
  "files.autoSave": "onFocusChange",
  
  "mcp.servers": {
    "context7": {
      "command": "npx", 
      "args": ["@upstash/context7-mcp"],
      "env": {}
    },
    "multiplatform-code-generator": {
      "command": "node",
      "args": ["/Users/shipan/workspace/multiplatform_code/src/index.js"],
      "env": {}
    }
  }
}
```

## 🔧 故障排除

### 问题 1: "MCP 服务器无法连接"

**解决方案**:
1. 确认路径是否正确（使用绝对路径）
2. 检查 Node.js 是否已安装: `node --version`
3. 检查项目依赖是否已安装: `npm install`

### 问题 2: "找不到命令"

**解决方案**:
1. 确认 Node.js 在 PATH 中: `which node`
2. 如果使用 Python 版本，确认 Python 路径: `which python`

### 问题 3: "工具不可用"

**解决方案**:
1. 重启 Cursor IDE
2. 检查 settings.json 语法是否正确
3. 查看 Cursor 控制台是否有错误信息

### 问题 4: "权限被拒绝"

**解决方案**:
```bash
chmod +x /Users/shipan/workspace/multiplatform_code/start-mcp.sh
chmod +x /Users/shipan/workspace/multiplatform_code/python/start_mcp.sh
```

## 🎯 使用技巧

### 1. 快速访问

将以下代码片段添加到 Cursor 的 snippets 中：

```json
{
  "Generate cross-platform code": {
    "prefix": "mcp-generate",
    "body": [
      "请为这个 C++ 函数生成 ${1:Android} 代码：",
      "",
      "```cpp",
      "${2:int add(int a, int b);}",
      "```",
      "",
      "输出目录：${3:./generated}",
      "Android 配置：",
      "- 包名：${4:com.example.test}",
      "- 类名：${5:Calculator}",
      "- 语言：${6:kotlin}"
    ],
    "description": "Generate cross-platform code from C++ interface"
  }
}
```

### 2. 常用配置模板

保存常用的配置模板：

```json
{
  "android_configs": {
    "basic": {
      "package_name": "com.example.basic",
      "class_name": "BasicWrapper",
      "language": "kotlin"
    },
    "math": {
      "package_name": "com.example.math",
      "class_name": "MathUtils", 
      "language": "kotlin"
    }
  }
}
```

## ✅ 配置检查清单

- [ ] Cursor IDE 版本支持 MCP
- [ ] settings.json 路径正确
- [ ] Node.js 已安装且可用
- [ ] 项目依赖已安装 (`npm install`)
- [ ] MCP 配置语法正确
- [ ] Cursor 已重启
- [ ] 测试消息获得响应

完成以上步骤后，您就可以在 Cursor IDE 中使用跨平台代码生成器了！

---

🎉 **现在您可以在 Cursor IDE 中享受 AI 辅助的跨平台代码生成了！**
