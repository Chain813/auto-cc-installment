# 网络说明

## 无需 VPN

本项目设计为**无需使用 VPN 或任何代理工具**。

### 网络连接方式

- **直连模式**: 所有 API 请求均使用直连方式
- **无代理配置**: 代码中不包含任何代理设置
- **国内访问**: DeepSeek API 位于中国，国内用户可直接访问
- **npm 镜像**: 使用国内镜像安装 Claude Code，无需 VPN

### 服务端点

| 服务 | 端点 | 说明 |
|------|------|------|
| DeepSeek API | `https://api.deepseek.com/v1` | 中国服务器，国内直连 |
| npm 淘宝镜像 | `https://registry.npmmirror.com` | 用于安装 Claude Code |
| npm 阿里云镜像 | `https://npm.aliyun.com` | 备用镜像 |
| npm 腾讯云镜像 | `https://mirrors.cloud.tencent.com/npm` | 备用镜像 |

### 网络安全

1. **HTTPS 加密**: 所有 API 请求均使用 HTTPS 加密传输
2. **API Key 安全**: API Key 仅存储在本地配置文件中
3. **无第三方依赖**: 不依赖任何第三方代理服务

### 常见网络问题排查

#### 1. 连接超时

```bash
# 测试网络连通性
ping api.deepseek.com

# 测试 HTTPS 连接
curl -I https://api.deepseek.com
```

#### 2. DNS 解析问题

```bash
# 使用公共 DNS
# Windows:
netsh interface ip set dns "以太网" static 8.8.8.8

# Linux/macOS:
sudo echo "nameserver 8.8.8.8" >> /etc/resolv.conf
```

#### 3. 防火墙设置

确保以下端口未被阻止：
- **443** (HTTPS)
- **80** (HTTP)

#### 4. 公司/学校网络

如果在受限网络环境：
- 联系网络管理员确认 `api.deepseek.com` 可访问
- 请求将以下域名加入白名单：
  - `api.deepseek.com`
  - `nodejs.org`
  - `registry.npmjs.org`

### 离线使用

本项目需要网络连接才能：
- 安装 Node.js 和 Claude Code
- 调用 DeepSeek API 进行聊天
- 测试 API 连接

配置文件管理和查看状态功能可离线使用。

## 技术支持

如遇网络问题，请提供：
1. 操作系统版本
2. 网络环境（家庭/公司/学校）
3. 错误信息截图
4. `ping api.deepseek.com` 结果
