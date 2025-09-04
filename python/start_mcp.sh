#!/bin/bash

# 跨平台代码生成器 MCP 服务器启动脚本 (Python 版本)

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：打印彩色消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=================================================${NC}"
    echo -e "${BLUE}  跨平台代码生成器 MCP 服务器 (Python)${NC}"
    echo -e "${BLUE}=================================================${NC}"
}

# 检查 Python 版本
check_python() {
    if ! command -v python &> /dev/null; then
        if ! command -v python3 &> /dev/null; then
            print_error "Python 未安装，请安装 Python 3.8+ 版本"
            exit 1
        else
            PYTHON_CMD="python3"
        fi
    else
        PYTHON_CMD="python"
    fi

    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR_VERSION" -lt 3 ] || ([ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 8 ]); then
        print_error "Python 版本过低，当前版本: $($PYTHON_CMD --version)，需要 3.8+ 版本"
        exit 1
    fi

    print_message "Python 版本检查通过: $($PYTHON_CMD --version)"
}

# 检查依赖
check_dependencies() {
    print_message "检查 Python 依赖..."
    
    if ! $PYTHON_CMD -c "import pydantic" 2>/dev/null; then
        print_warning "缺少依赖，正在安装..."
        $PYTHON_CMD -m pip install pydantic typing-extensions
    fi

    if [ ! -f "src/multiplatform_code_generator/__init__.py" ]; then
        print_error "源代码文件不存在，请检查项目结构"
        exit 1
    fi

    print_message "依赖检查完成"
}

# 设置 Python 路径
setup_python_path() {
    export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
    print_message "设置 PYTHONPATH: $(pwd)/src"
}

# 运行测试（可选）
run_tests() {
    if [ "$1" = "--test" ] || [ "$1" = "-t" ]; then
        print_message "运行测试..."
        $PYTHON_CMD test_generator.py
        echo ""
    fi
}

# 启动服务器
start_server() {
    print_message "启动 MCP 服务器..."
    print_message "服务器地址: stdio (标准输入/输出)"
    print_message "使用 Ctrl+C 停止服务器"
    echo ""
    
    # 启动服务器
    exec $PYTHON_CMD start_mcp.py
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -t, --test     运行测试后启动服务器"
    echo "  -h, --help     显示帮助信息"
    echo "  -v, --version  显示版本信息"
    echo ""
    echo "示例:"
    echo "  $0              # 直接启动服务器"
    echo "  $0 --test       # 运行测试后启动服务器"
    echo ""
}

# 显示版本信息
show_version() {
    if [ -f "pyproject.toml" ]; then
        VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
        echo "跨平台代码生成器 MCP 工具 (Python) v$VERSION"
    else
        echo "无法读取版本信息"
    fi
}

# 清理函数
cleanup() {
    print_message "正在关闭服务器..."
    exit 0
}

# 设置信号处理
trap cleanup SIGINT SIGTERM

# 主函数
main() {
    print_header
    
    # 处理命令行参数
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--version)
            show_version
            exit 0
            ;;
        -t|--test)
            check_python
            check_dependencies
            setup_python_path
            run_tests "$1"
            start_server
            ;;
        "")
            check_python
            check_dependencies
            setup_python_path
            start_server
            ;;
        *)
            print_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
