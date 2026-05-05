# Claude Code 直接使用 DeepSeek API 配置指南

## 原理说明

DeepSeek API 提供了 **Anthropic 兼容端点**，可以直接在 Claude Code 中使用：

```
┌─────────────────┐                    ┌─────────────────┐
│   Claude Code   │ ──────────────────→│   DeepSeek API  │
│                 │   Anthropic 格式   │                 │
│   /v1/messages  │                    │   /anthropic    │
└─────────────────┘                    └─────────────────┘
```

**无需代理，无需额外代码，直接配置即可使用！**

## 配置步骤

### 方法 1：环境变量配置（推荐）

#### Windows (PowerShell)

```powershell
# 设置 DeepSeek API Key
$env:ANTHROPIC_API_KEY = "your-deepseek-api-key"

# 设置 Anthropic 兼容端点
$env:ANTHROPIC_BASE_URL = "https://api.deepseek.com/anthropic"

# 启动 Claude Code
claude
```

#### Windows (CMD)

```cmd
set ANTHROPIC_API_KEY=your-deepseek-api-key
set ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
claude
```

#### Linux/macOS

```bash
export ANTHROPIC_API_KEY="your-deepseek-api-key"
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
claude
```

### 方法 2：配置文件

创建或编辑 `~/.claude/settings.json`：

```json
{
  "apiKeyHelper": "echo your-deepseek-api-key",
  "primaryModel": "deepseek-v4-flash"
}
```

### 方法 3：使用本工具自动配置

```bash
# 运行配置向导
python -m src.main configure-claude-code
```

## 可用模型

| 模型名称 | 说明 | 推荐场景 |
|----------|------|----------|
| `deepseek-v4-flash` | 快速模型 | 日常编程、快速问答 |
| `deepseek-v4-pro` | 专业模型 | 复杂任务、代码生成 |

## 验证配置

启动 Claude Code 后，输入以下命令验证：

```
/model
```

应该显示当前使用的 DeepSeek 模型。

## 注意事项

1. **API Key**: 需要在 [DeepSeek Platform](https://platform.deepseek.com) 申请
2. **端点**: 使用 `https://api.deepseek.com/anthropic`（不是 `/v1`）
3. **模型名称**: 使用 `deepseek-v4-flash` 或 `deepseek-v4-pro`
4. **弃用提醒**: `deepseek-chat` 和 `deepseek-reasoner` 将于 2026/07/24 弃用

## 功能支持

DeepSeek API 通过 Anthropic 兼容端点支持：

- ✅ 代码生成
- ✅ 代码解释
- ✅ 代码重构
- ✅ 多轮对话
- ✅ 流式输出
- ✅ 工具调用（部分支持）

## 故障排除

### 问题：连接失败

```bash
# 测试连接
curl -I https://api.deepseek.com/anthropic
```

### 问题：API Key 无效

1. 确认 API Key 已正确申请
2. 检查 Key 是否有余额
3. 确认 Key 没有过期

### 问题：模型不可用

确认使用正确的模型名称：
- ✅ `deepseek-v4-flash`
- ✅ `deepseek-v4-pro`
- ❌ `deepseek-chat`（即将弃用）
- ❌ `deepseek-reasoner`（即将弃用）

## 参考链接

- [DeepSeek API 文档](https://platform.deepseek.com/api-docs)
- [DeepSeek Platform](https://platform.deepseek.com)
- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code)
