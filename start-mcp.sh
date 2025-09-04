#!/bin/bash

# 跨平台代码生成器 MCP 服务器启动脚本

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
    echo -e "${BLUE}===========================================${NC}"
    echo -e "${BLUE}  跨平台代码生成器 MCP 服务器${NC}"
    echo -e "${BLUE}===========================================${NC}"
}

# 检查 Node.js 版本
check_nodejs() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js 未安装，请安装 Node.js 18+ 版本"
        exit 1
    fi

    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js 版本过低，当前版本: $(node --version)，需要 18+ 版本"
        exit 1
    fi

    print_message "Node.js 版本检查通过: $(node --version)"
}

# 检查依赖
check_dependencies() {
    if [ ! -d "node_modules" ]; then
        print_warning "依赖未安装，正在安装..."
        npm install
    fi

    if [ ! -f "package.json" ]; then
        print_error "package.json 文件不存在"
        exit 1
    fi

    print_message "依赖检查完成"
}

# 运行测试（可选）
run_tests() {
    if [ "$1" = "--test" ] || [ "$1" = "-t" ]; then
        print_message "运行测试..."
        node test.js
        echo ""
    fi
}

# 启动服务器
start_server() {
    print_message "启动 MCP 服务器..."
    print_message "服务器地址: stdio (标准输入/输出)"
    print_message "使用 Ctrl+C 停止服务器"
    echo ""
    
    # 设置环境变量
    export NODE_ENV=production
    export LOG_LEVEL=info
    
    # 启动服务器
    exec node src/index.js
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
    if [ -f "package.json" ]; then
        VERSION=$(node -p "require('./package.json').version")
        echo "跨平台代码生成器 MCP 工具 v$VERSION"
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
            check_nodejs
            check_dependencies
            run_tests "$1"
            start_server
            ;;
        "")
            check_nodejs
            check_dependencies
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
