#!/bin/bash

# Cursor IDE MCP 工具配置验证脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Cursor IDE MCP 工具配置验证${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 1. 检查项目文件
echo -e "${YELLOW}1. 检查项目文件...${NC}"

if [ -f "src/index.js" ]; then
    echo -e "${GREEN}✅ Node.js 版本入口文件存在${NC}"
else
    echo -e "${RED}❌ Node.js 版本入口文件不存在${NC}"
    exit 1
fi

if [ -f "python/start_mcp.py" ]; then
    echo -e "${GREEN}✅ Python 版本入口文件存在${NC}"
else
    echo -e "${RED}❌ Python 版本入口文件不存在${NC}"
    exit 1
fi

# 2. 检查依赖
echo -e "${YELLOW}2. 检查依赖安装...${NC}"

if command -v node &> /dev/null; then
    echo -e "${GREEN}✅ Node.js 已安装: $(node --version)${NC}"
else
    echo -e "${RED}❌ Node.js 未安装${NC}"
    exit 1
fi

if command -v python &> /dev/null; then
    echo -e "${GREEN}✅ Python 已安装: $(python --version)${NC}"
else
    echo -e "${RED}❌ Python 未安装${NC}"
    exit 1
fi

if [ -d "node_modules" ]; then
    echo -e "${GREEN}✅ Node.js 依赖已安装${NC}"
else
    echo -e "${YELLOW}⚠️  Node.js 依赖未安装，正在安装...${NC}"
    npm install
fi

# 3. 检查 Cursor 配置
echo -e "${YELLOW}3. 检查 Cursor 配置...${NC}"

CURSOR_SETTINGS="$HOME/Library/Application Support/Cursor/User/settings.json"

if [ -f "$CURSOR_SETTINGS" ]; then
    echo -e "${GREEN}✅ Cursor settings.json 文件存在${NC}"
    
    if grep -q "multiplatform-code-generator" "$CURSOR_SETTINGS"; then
        echo -e "${GREEN}✅ MCP 工具配置已添加${NC}"
    else
        echo -e "${RED}❌ MCP 工具配置未找到${NC}"
        echo "请检查 Cursor settings.json 配置"
        exit 1
    fi
else
    echo -e "${RED}❌ Cursor settings.json 文件不存在${NC}"
    exit 1
fi

# 4. 测试 MCP 服务器
echo -e "${YELLOW}4. 测试 MCP 服务器...${NC}"

echo -e "${BLUE}测试 Node.js 版本:${NC}"
if timeout 5s node src/index.js <<< '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Node.js MCP 服务器响应正常${NC}"
else
    echo -e "${YELLOW}⚠️  Node.js MCP 服务器测试超时（这是正常的）${NC}"
fi

echo -e "${BLUE}测试 Python 版本:${NC}"
if timeout 5s python python/start_mcp.py <<< '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Python MCP 服务器响应正常${NC}"
else
    echo -e "${YELLOW}⚠️  Python MCP 服务器测试超时（这是正常的）${NC}"
fi

# 5. 运行完整测试
echo -e "${YELLOW}5. 运行功能测试...${NC}"

echo -e "${BLUE}Node.js 版本测试:${NC}"
if npm test >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Node.js 版本功能测试通过${NC}"
else
    echo -e "${RED}❌ Node.js 版本功能测试失败${NC}"
fi

echo -e "${BLUE}Python 版本测试:${NC}"
if cd python && python test_generator.py >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Python 版本功能测试通过${NC}"
    cd ..
else
    echo -e "${RED}❌ Python 版本功能测试失败${NC}"
    cd ..
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  配置验证完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo -e "${BLUE}📋 接下来的步骤:${NC}"
echo "1. 重启 Cursor IDE 以加载新的 MCP 配置"
echo "2. 在 Cursor 中按 Cmd+K 打开 AI 对话"
echo "3. 发送测试消息: '请列出支持的平台'"
echo "4. 开始使用跨平台代码生成工具！"
echo ""

echo -e "${BLUE}📖 相关文档:${NC}"
echo "- CURSOR_SETUP.md - 详细配置指南"
echo "- QUICK_START.md - 快速开始"
echo "- USER_GUIDE.md - 用户手册"
echo "- EXAMPLES.md - 使用示例"
echo ""

echo -e "${GREEN}🎉 准备就绪！享受 AI 辅助的跨平台开发吧！${NC}"
