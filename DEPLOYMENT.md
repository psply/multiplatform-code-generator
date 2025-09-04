# 部署指南

本指南将帮助您在本地机器上部署跨平台代码生成器 MCP 工具。

## 环境要求

### 系统要求
- **操作系统**: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+)
- **Node.js**: 18.0.0 或更高版本
- **内存**: 至少 2GB RAM
- **磁盘空间**: 至少 500MB 可用空间

### 必需软件
- Node.js 18+ (https://nodejs.org/)
- npm 8+ 或 yarn 1.22+
- Git (用于克隆仓库)

## 快速部署

### 1. 下载和安装

```bash
# 克隆仓库
git clone https://github.com/yourorg/multiplatform_code.git
cd multiplatform_code

# 安装依赖
npm install

# 验证安装
npm test
```

### 2. 启动 MCP 服务器

```bash
# 开发模式 (带热重载)
npm run dev

# 生产模式
npm start
```

### 3. 验证部署

```bash
# 检查服务器状态
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | node src/index.js
```

## 配置 MCP 客户端

### Claude Desktop

1. 找到配置文件:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. 编辑配置文件:
```json
{
  "mcpServers": {
    "multiplatform-code-generator": {
      "command": "node",
      "args": ["/absolute/path/to/multiplatform_code/src/index.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

3. 重启 Claude Desktop

### Cursor

1. 打开 Cursor 设置
2. 导航到 MCP 配置
3. 添加新的 MCP 服务器:
```json
{
  "name": "multiplatform-code-generator",
  "command": "node",
  "args": ["/absolute/path/to/multiplatform_code/src/index.js"]
}
```

### 自定义 MCP 客户端

如果您使用自定义的 MCP 客户端，请参考 MCP 协议文档进行配置。

## Docker 部署 (可选)

### 创建 Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY src/ ./src/

EXPOSE 3000

USER node

CMD ["npm", "start"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t multiplatform-code-generator .

# 运行容器
docker run -d \
  --name mcp-code-generator \
  -p 3000:3000 \
  multiplatform-code-generator
```

## 系统服务配置

### Linux (systemd)

1. 创建服务文件:
```ini
# /etc/systemd/system/mcp-code-generator.service
[Unit]
Description=Multiplatform Code Generator MCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/multiplatform_code
ExecStart=/usr/bin/node src/index.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

2. 启用和启动服务:
```bash
sudo systemctl enable mcp-code-generator
sudo systemctl start mcp-code-generator
sudo systemctl status mcp-code-generator
```

### macOS (launchd)

1. 创建 plist 文件:
```xml
<!-- ~/Library/LaunchAgents/com.yourorg.mcp-code-generator.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourorg.mcp-code-generator</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/node</string>
        <string>/path/to/multiplatform_code/src/index.js</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/multiplatform_code</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

2. 加载服务:
```bash
launchctl load ~/Library/LaunchAgents/com.yourorg.mcp-code-generator.plist
launchctl start com.yourorg.mcp-code-generator
```

### Windows (NSSM)

1. 下载 NSSM (Non-Sucking Service Manager)
2. 安装服务:
```cmd
nssm install MCPCodeGenerator
nssm set MCPCodeGenerator Application "C:\Program Files\nodejs\node.exe"
nssm set MCPCodeGenerator AppParameters "C:\path\to\multiplatform_code\src\index.js"
nssm set MCPCodeGenerator AppDirectory "C:\path\to\multiplatform_code"
nssm start MCPCodeGenerator
```

## 高级配置

### 环境变量

```bash
# 设置日志级别
export LOG_LEVEL=debug

# 设置输出目录默认路径
export DEFAULT_OUTPUT_DIR=/tmp/generated-code

# 设置最大文件大小 (字节)
export MAX_FILE_SIZE=10485760

# 启用详细日志
export VERBOSE=true
```

### 配置文件

创建 `config.json`:
```json
{
  "server": {
    "name": "multiplatform-code-generator",
    "version": "1.0.0"
  },
  "logging": {
    "level": "info",
    "file": "/var/log/mcp-code-generator.log"
  },
  "limits": {
    "maxFileSize": 10485760,
    "maxFiles": 100
  },
  "platforms": {
    "android": {
      "enabled": true,
      "defaultPackage": "com.example"
    },
    "ios": {
      "enabled": true,
      "defaultPrefix": "CPP"
    },
    "harmony": {
      "enabled": true,
      "defaultModule": "CppBridge"
    }
  }
}
```

## 性能优化

### 1. Node.js 优化

```bash
# 增加内存限制
node --max-old-space-size=4096 src/index.js

# 启用性能分析
node --prof src/index.js
```

### 2. 并发处理

在 `src/index.js` 中配置工作池:
```javascript
import { Worker } from 'worker_threads';

const workerPool = {
  maxWorkers: require('os').cpus().length,
  workers: []
};
```

### 3. 缓存配置

```javascript
// 启用解析结果缓存
const parseCache = new Map();
const CACHE_SIZE = 1000;
```

## 监控和日志

### 1. 日志配置

```javascript
// src/utils/logger.js
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### 2. 健康检查

```javascript
// 添加健康检查端点
server.setRequestHandler('health/check', async () => {
  return {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  };
});
```

### 3. 指标收集

```javascript
// 收集使用统计
const metrics = {
  totalRequests: 0,
  totalGenerations: 0,
  platformStats: {
    android: 0,
    ios: 0,
    harmony: 0
  }
};
```

## 故障排除

### 常见问题

1. **端口冲突**:
   ```bash
   # 检查端口使用
   lsof -i :3000
   
   # 修改端口
   export PORT=3001
   ```

2. **权限问题**:
   ```bash
   # 修复文件权限
   chmod +x src/index.js
   chown -R $USER:$USER .
   ```

3. **依赖问题**:
   ```bash
   # 清除缓存并重新安装
   rm -rf node_modules package-lock.json
   npm install
   ```

### 日志分析

```bash
# 查看错误日志
tail -f error.log

# 搜索特定错误
grep "Error" combined.log

# 分析性能问题
node --prof-process isolate-*.log > processed.txt
```

### 调试模式

```bash
# 启用调试模式
DEBUG=mcp:* npm start

# 使用 Node.js 调试器
node --inspect src/index.js
```

## 安全考虑

### 1. 文件系统安全

```javascript
// 限制文件访问路径
const path = require('path');
const safePath = path.resolve(basePath, userPath);
if (!safePath.startsWith(basePath)) {
  throw new Error('Invalid path');
}
```

### 2. 输入验证

```javascript
// 验证 C++ 代码输入
function validateCppCode(code) {
  if (typeof code !== 'string') return false;
  if (code.length > MAX_CODE_LENGTH) return false;
  if (containsMaliciousPatterns(code)) return false;
  return true;
}
```

### 3. 资源限制

```javascript
// 限制生成文件数量和大小
const limits = {
  maxFiles: 100,
  maxFileSize: 10 * 1024 * 1024, // 10MB
  maxTotalSize: 100 * 1024 * 1024 // 100MB
};
```

## 更新和维护

### 1. 更新步骤

```bash
# 备份配置
cp config.json config.json.backup

# 拉取最新代码
git pull origin main

# 更新依赖
npm update

# 重启服务
sudo systemctl restart mcp-code-generator
```

### 2. 版本管理

```bash
# 检查当前版本
npm run version

# 创建版本标签
git tag v1.1.0
git push origin v1.1.0
```

### 3. 备份策略

```bash
# 创建备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "backup_${DATE}.tar.gz" \
  src/ config.json package.json
```

---

如有部署问题，请参考 [故障排除指南](TROUBLESHOOTING.md) 或联系技术支持。
