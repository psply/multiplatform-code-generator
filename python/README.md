# 跨平台代码生成器 MCP 工具 (Python 版本)

一个强大的 MCP (Model Context Protocol) 工具的 Python 实现，能够从 C++ 接口函数自动生成 Android、iOS 和鸿蒙等不同平台的调用代码。

## 🌟 特性

- 🔄 **跨平台支持**: 支持 Android (JNI)、iOS (Objective-C) 和鸿蒙 (NAPI)
- 🧠 **智能解析**: 自动解析 C++ 函数签名和参数类型  
- 📦 **完整生成**: 生成包装类、构建文件和配置文件
- 🛠️ **MCP 兼容**: 与大模型无缝集成，支持 Claude、GPT 等
- ⚡ **即用型代码**: 生成的代码可直接编译运行
- 🐍 **Python 原生**: 使用现代 Python (3.8+) 和 asyncio

## 📋 系统要求

- Python 3.8 或更高版本
- pip 包管理器
- 支持的操作系统: Windows, macOS, Linux

## 🚀 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone <repository-url>
cd multiplatform_code/python

# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行测试

```bash
# 运行测试验证安装
python test_generator.py
```

### 3. 启动 MCP 服务器

```bash
# 直接启动
python start_mcp.py

# 或者先运行测试再启动
python start_mcp.py --test
```

## 📁 项目结构

```
python/
├── src/multiplatform_code_generator/
│   ├── __init__.py                    # 包初始化
│   ├── main.py                        # MCP 服务器入口
│   ├── server.py                      # MCP 服务器实现
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── cpp_parser.py              # C++ 接口解析器
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── android_jni.py             # Android JNI 生成器
│   │   ├── ios_oc.py                  # iOS Objective-C 生成器
│   │   └── harmony_napi.py            # 鸿蒙 NAPI 生成器
│   └── utils/
│       ├── __init__.py
│       └── file_manager.py            # 文件管理工具
├── test_generator.py                  # 测试脚本
├── start_mcp.py                       # 启动脚本
├── pyproject.toml                     # 项目配置
├── requirements.txt                   # 依赖列表
└── README.md                          # 本文档
```

## 🔧 配置 MCP 客户端

### Claude Desktop

在 Claude Desktop 的配置文件中添加:

```json
{
  "mcpServers": {
    "multiplatform-code-generator-python": {
      "command": "python",
      "args": ["/path/to/multiplatform_code/python/start_mcp.py"],
      "env": {
        "PYTHONPATH": "/path/to/multiplatform_code/python/src"
      }
    }
  }
}
```

### 配置文件位置

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## 🛠️ 使用方法

### 可用工具

#### 1. generate_multiplatform_code

生成跨平台代码的主要工具。

**参数**:
```python
{
    "cpp_interface": "C++ 接口函数代码",
    "output_directory": "输出目录路径",
    "platforms": ["android", "ios", "harmony"],
    "android_config": {
        "package_name": "com.example.package",
        "class_name": "ClassName",
        "language": "kotlin"  # 或 "java"
    },
    "ios_config": {
        "class_prefix": "CPP",
        "framework_name": "Framework"
    },
    "harmony_config": {
        "module_name": "Module",
        "namespace": "namespace"
    }
}
```

#### 2. parse_cpp_interface

解析 C++ 接口并提取函数信息。

**参数**:
```python
{
    "cpp_interface": "C++ 接口函数代码"
}
```

#### 3. list_supported_platforms

列出所有支持的目标平台。

## 📚 使用示例

### 基本示例

```python
# C++ 接口
cpp_interface = """
namespace Calculator {
    int add(int a, int b);
    double divide(double numerator, double denominator);
    std::string format(double value);
}
"""

# 生成所有平台代码
result = generate_multiplatform_code({
    "cpp_interface": cpp_interface,
    "output_directory": "./generated",
    "platforms": ["android", "ios", "harmony"],
    "android_config": {
        "package_name": "com.example.calculator",
        "class_name": "Calculator",
        "language": "kotlin"
    },
    "ios_config": {
        "class_prefix": "Calc",
        "framework_name": "Calculator"
    },
    "harmony_config": {
        "module_name": "Calculator", 
        "namespace": "calculator"
    }
})
```

### 仅生成单个平台

```python
# 仅生成 Android 代码
result = generate_multiplatform_code({
    "cpp_interface": "int factorial(int n);",
    "output_directory": "./android-only",
    "platforms": ["android"],
    "android_config": {
        "package_name": "com.example.math",
        "class_name": "MathUtils",
        "language": "java"
    }
})
```

## 🧪 开发和测试

### 运行测试

```bash
# 运行主测试
python test_generator.py

# 使用 pytest (如果安装)
pytest tests/ -v
```

### 代码格式化

```bash
# 使用 black 格式化代码
black src/ test_generator.py start_mcp.py

# 使用 isort 排序导入
isort src/ test_generator.py start_mcp.py
```

### 类型检查

```bash
# 使用 mypy 进行类型检查
mypy src/
```

### 代码风格检查

```bash
# 使用 flake8 检查代码风格
flake8 src/
```

## 📦 打包和分发

### 构建包

```bash
# 构建 wheel 包
pip install build
python -m build
```

### 安装本地包

```bash
# 以开发模式安装
pip install -e .

# 或者安装构建的包
pip install dist/multiplatform_code_generator-1.0.0-py3-none-any.whl
```

### 从命令行使用

安装后可以通过命令行启动:

```bash
# 安装后使用
multiplatform-code-generator
```

## 🔍 故障排除

### 常见问题

1. **导入错误**:
   ```bash
   # 确保 PYTHONPATH 正确设置
   export PYTHONPATH="/path/to/multiplatform_code/python/src:$PYTHONPATH"
   ```

2. **依赖缺失**:
   ```bash
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

3. **权限问题**:
   ```bash
   # 确保输出目录有写权限
   chmod 755 /path/to/output/directory
   ```

### 调试模式

```bash
# 启用详细日志
export PYTHONPATH="/path/to/src"
python -u start_mcp.py --test
```

## 🔄 与 Node.js 版本的区别

| 特性 | Python 版本 | Node.js 版本 |
|------|-------------|--------------|
| **运行时** | Python 3.8+ | Node.js 18+ |
| **并发模型** | asyncio | Event Loop |
| **类型系统** | Pydantic + Type Hints | JavaScript |
| **包管理** | pip/pyproject.toml | npm/package.json |
| **性能** | 良好 | 优秀 |
| **内存使用** | 中等 | 较低 |
| **生态系统** | Python 生态 | JavaScript 生态 |

## 🚧 开发路线图

### 当前版本 (1.0.0)
- ✅ 基本 MCP 服务器实现
- ✅ C++ 接口解析
- ✅ 三平台代码生成
- ✅ 完整测试套件

### 下一版本 (1.1.0)
- 📋 支持更多 C++ 类型
- 📋 改进错误处理
- 📋 添加配置文件支持
- 📋 性能优化

### 未来版本
- 📋 Web 界面
- 📋 插件系统
- 📋 更多平台支持

## 🤝 贡献指南

我们欢迎社区贡献！

### 开发环境设置

```bash
# 1. Fork 并克隆仓库
git clone <your-fork-url>
cd multiplatform_code/python

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 3. 安装开发依赖
pip install -r requirements.txt
pip install -e .

# 4. 运行测试
python test_generator.py
```

### 提交流程

1. 创建特性分支: `git checkout -b feature/amazing-feature`
2. 提交更改: `git commit -m 'Add amazing feature'`
3. 推送分支: `git push origin feature/amazing-feature`
4. 创建 Pull Request

### 代码规范

- 使用 Black 进行代码格式化
- 使用 isort 排序导入语句
- 使用 mypy 进行类型检查
- 编写文档字符串
- 添加适当的测试

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE) 文件

## 📞 支持

- **问题报告**: [GitHub Issues](https://github.com/yourorg/multiplatform_code/issues)
- **功能请求**: [GitHub Discussions](https://github.com/yourorg/multiplatform_code/discussions)
- **文档**: [项目 Wiki](https://github.com/yourorg/multiplatform_code/wiki)

---

**让跨平台开发变得简单！** 🚀🐍
