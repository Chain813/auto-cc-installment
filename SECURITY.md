# 安全说明

## 安全措施

### 1. API Key 保护

- **不硬编码**: 启动脚本不再包含 API Key
- **环境变量**: API Key 通过环境变量传递
- **配置文件**: `config.yaml` 已添加到 `.gitignore`
- **显示遮蔽**: 日志中 API Key 自动遮蔽显示

### 2. 命令执行安全

- **避免 shell=True**: 所有 subprocess 调用使用列表形式
- **参数分离**: 命令和参数分开传递，防止注入攻击
- **超时控制**: 所有外部命令设置超时限制

### 3. 网络安全

- **仅官方 API**: 只连接 DeepSeek 官方 API
- **HTTPS**: 所有 API 请求使用 HTTPS
- **无数据收集**: 不收集或上传用户数据

### 4. 依赖安全

- **版本锁定**: 提供 `requirements-lock.txt` 锁定版本
- **知名依赖**: 仅使用 PyPI 官方知名库
- **定期更新**: 建议定期更新依赖版本

## 安全配置建议

### 1. 保护 API Key

```bash
# 使用环境变量（推荐）
export DEEPSEEK_API_KEY="your-key"

# 或使用 .env 文件（不要提交到 Git）
echo "DEEPSEEK_API_KEY=your-key" > .env
```

### 2. 检查依赖漏洞

```bash
# 安装安全扫描工具
pip install safety

# 扫描依赖
safety check -r requirements.txt
```

### 3. 定期更新

```bash
# 更新依赖
pip install --upgrade -r requirements.txt

# 更新 Claude Code
npm update -g @anthropic-ai/claude-code
```

## 已修复的安全问题

| 问题 | 状态 | 说明 |
|------|------|------|
| API Key 硬编码 | ✅ 已修复 | 改为环境变量 |
| shell=True 使用 | ✅ 已修复 | 改为列表形式 |
| 版本未锁定 | ✅ 已修复 | 添加 lock 文件 |

## 报告安全问题

如发现安全漏洞，请通过以下方式报告：

1. 创建 GitHub Issue（标记为 security）
2. 发送邮件至项目维护者

## 免责声明

本工具仅供学习和合法使用。用户需自行承担使用风险，遵守相关服务条款。
