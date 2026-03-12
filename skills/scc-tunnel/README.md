# SCC Tunnel Skill - 内网穿透工具

<div align="center">

**SCC Tunnel - Expose Local Services to Public Internet**

[中文](#-中文) | [English](#-english)

</div>

---

## 中文

### 简介

使用 SCC (scc-cli) 内网穿透工具启动 HTTP/TCP 隧道，将本地服务暴露到公网，无需配置服务器。

**服务信息：**
- **带宽**：10Gbps
- **服务器位置**：宁夏电信
- **服务提供商**：ParaCloud

### 功能特性

- **无需认证** - 无需登录即可使用
- **HTTP 隧道** - 适用于 Web 服务
- **TCP 隧道** - 适用于数据库、SSH 等
- **动态域名** - HTTP 隧道每次生成不同的 UUID 域名
- **快速启动** - 一条命令即可启动

### 安装

**方式 1：一键安装脚本（推荐）**

```bash
# Linux x86_64
curl -fsSL https://dl.scc.paratera.com/scc-cli/latest/scc-cli-0.1.3_linux_x86_64.tar.gz | tar -xz && sudo mv scc /usr/local/bin/ && sudo chmod +x /usr/local/bin/scc

# 验证安装
scc --version
```

**方式 2：手动下载**

访问官方下载页面：
- **下载链接**: https://dl.scc.paratera.com/scc-cli/latest/

**支持平台：**
- `scc-cli-0.1.3_linux_x86_64.tar.gz` - Linux x86_64

> ⚠ **注意**：SCC 目前仅提供 Linux 版本，Windows 和 macOS 用户建议使用 Docker 或虚拟机运行。

**手动安装步骤：**
```bash
# 1. 下载
cd /tmp
curl -LO https://dl.scc.paratera.com/scc-cli/latest/scc-cli-0.1.3_linux_x86_64.tar.gz

# 2. 解压
tar -xzf scc-cli-0.1.3_linux_x86_64.tar.gz

# 3. 移动到系统路径
sudo mv scc /usr/local/bin/
sudo chmod +x /usr/local/bin/scc

# 4. 验证
scc --version
```



### 快速开始

**HTTP 隧道（推荐用于 Web 服务）**
```bash
scc tunnel http <本地端口>

# 示例：暴露本地 2017 端口
scc tunnel http 2017

# 输出：
# 🎉 You're ready to go live at https://59ece46f-4325-471a-9a59-fee389c8b48a.tunnel.paracloud.com => http://localhost:2017
```

**TCP 隧道（用于非 HTTP 服务）**
```bash
scc tunnel tcp <本地端口>

# 示例：暴露 SSH
scc tunnel tcp 22

# 输出：
# 🎉 You're ready to go live at tcp://tunnel.paracloud.com:15627 => tcp://localhost:22
```

### 使用场景

| 场景 | 命令 | 说明 |
|------|------|------|
| v2rayA 管理界面 | `scc tunnel http 2017` | 从公网访问本地管理界面 |
| 本地开发服务器 | `scc tunnel http 3000` | 分享开发中的 Web 应用 |
| OpenClaw Gateway | `scc tunnel http 18789` | 暴露 OpenClaw 网关 |
| 数据库 | `scc tunnel tcp 3306` | 远程数据库访问 |
| SSH | `scc tunnel tcp 22` | 远程 SSH 访问 |

### 命令别名

```bash
scc tun http 2017    # tunnel 可简写为 tun
scc tun tcp 2017
```

### 输出格式

**HTTP 隧道：**
```
🎉 You're ready to go live at https://<uuid>.tunnel.paracloud.com => http://localhost:<端口>
```

**TCP 隧道：**
```
🎉 You're ready to go live at tcp://tunnel.paracloud.com:<随机端口> => tcp://localhost:<端口>
```

### ⚠ 注意事项

| 注意事项 | 说明 |
|----------|------|
| **动态域名** | HTTP 隧道每次生成不同的 UUID 域名 |
| **随机端口** | TCP 隧道使用固定域名 + 随机端口 |
| **进程保持** | 隧道需要持续运行，停止命令会关闭隧道 |
| **公网访问** | 生成的 URL 可从任何地方访问 |
| **无需认证** | 无需登录即可使用 |

### 服务信息

| 项目 | 值 |
|------|-----|
| **带宽** | 10Gbps |
| **服务器位置** | 宁夏电信 |
| **服务提供商** | ParaCloud |
| **服务类型** | 公益免费服务 |

### ⚠ 使用提醒

> **公益服务，请勿滥用！**
> 
> SCC 是 ParaCloud 提供的免费内网穿透服务，适用于：
> - ✅ 临时开发和测试
> - ✅ 短期演示和分享
> - ✅ 学习和个人项目
> 
> 不建议用于：
> - ❌ 生产环境
> - ❌ 大规模商业用途
> - ❌ 长时间高负载运行
> 
> **请合理使用，把资源留给更需要的人～！** 🌸

### 限制与缺点

| 限制 | 说明 |
|------|------|
| **无法指定端口** | TCP 隧道的公网端口是随机的，无法自定义 |
| **无法指定 HTTP 前缀** | HTTP 隧道的域名前缀是随机 UUID，无法自定义 |
| **动态变化** | 每次启动隧道生成的 URL 都不同，不适合长期固定服务 |
| **免费服务限制** | 作为免费服务，可能有稳定性或时长限制 |

**适用场景：**
- ✅ 临时开发和测试
- ✅ 短期演示和分享
- ✅ 快速调试内网服务

**不适用场景：**
- ❌ 需要固定域名的生产环境
- ❌ 需要自定义端口的服务
- ❌ 长期稳定的公网访问

### FAQ

**Q: 为什么二进制文件不推送到 Git 仓库？**

A: 二进制文件不适合版本控制，原因：
- 文件体积大，增加仓库大小
- 无法 diff，每次更新都是全新文件
- GitHub 限制单个文件 100MB
- 更新麻烦，需要重新提交

推荐做法：
- 提供官方下载链接
- 提供一键安装脚本
- 在 README 中说明安装步骤

**Q: SCC 隧道稳定吗？**

A: SCC 是 ParaCloud 提供的免费内网穿透服务，适合临时使用和开发测试。生产环境建议使用：
- 自建 frp/ngrok 隧道
- 云服务器 + 反向代理
- 商业内网穿透服务

**Q: 隧道会超时断开吗？**

A: 免费隧道可能有超时限制，建议：
- 长时间运行使用后台进程
- 重要服务使用付费方案
- 定期检查隧道状态

### 🛠 管理隧道进程

**查看运行中的隧道：**
```bash
ps aux | grep "scc tunnel"
```

**停止隧道：**
```bash
# 通过进程 ID 停止
kill <PID>

# 或在 OpenClaw 中使用 process kill 命令
```

---

## English

### Introduction

Use SCC (scc-cli) tunnel tool to start HTTP/TCP tunnels and expose local services to public internet without server configuration.

### Features

- **No authentication required** - Use without login
- **HTTP tunnel** - For web services
- **TCP tunnel** - For databases, SSH, etc.
- **Dynamic domain** - HTTP tunnel generates different UUID domain each time
- **Quick start** - One command to start

### Installation

**1. Download scc-cli**

Visit official website to download for your platform:
https://dl.scc.paratera.com/scc-cli/latest/

**Linux x86_64:**
```bash
cd /tmp
curl -LO https://dl.scc.paratera.com/scc-cli/latest/scc-cli-0.1.3_linux_x86_64.tar.gz
tar -xzf scc-cli-0.1.3_linux_x86_64.tar.gz
sudo mv scc /usr/local/bin/
sudo chmod +x /usr/local/bin/scc
```

**2. Verify installation**
```bash
scc --version
# Output: scc version 0.1.3
```

### Quick Start

**HTTP Tunnel (for web services)**
```bash
scc tunnel http <local-port>

# Example: expose port 2017
scc tunnel http 2017

# Output:
# 🎉 You're ready to go live at https://59ece46f-4325-471a-9a59-fee389c8b48a.tunnel.paracloud.com => http://localhost:2017
```

**TCP Tunnel (for non-HTTP services)**
```bash
scc tunnel tcp <local-port>

# Example: expose SSH
scc tunnel tcp 22

# Output:
# 🎉 You're ready to go live at tcp://tunnel.paracloud.com:15627 => tcp://localhost:22
```

### Use Cases

| Use Case | Command | Description |
|----------|---------|-------------|
| v2rayA admin UI | `scc tunnel http 2017` | Access local admin interface from public |
| Local dev server | `scc tunnel http 3000` | Share web app under development |
| OpenClaw Gateway | `scc tunnel http 18789` | Expose OpenClaw gateway |
| Database | `scc tunnel tcp 3306` | Remote database access |
| SSH | `scc tunnel tcp 22` | Remote SSH access |

### Command Aliases

```bash
scc tun http 2017    # tunnel can be abbreviated as tun
scc tun tcp 2017
```

### Output Format

**HTTP Tunnel:**
```
🎉 You're ready to go live at https://<uuid>.tunnel.paracloud.com => http://localhost:<port>
```

**TCP Tunnel:**
```
🎉 You're ready to go live at tcp://tunnel.paracloud.com:<random-port> => tcp://localhost:<port>
```

### ⚠ Notes

| Note | Description |
|------|-------------|
| **Dynamic domain** | HTTP tunnel generates different UUID domain each time |
| **Random port** | TCP tunnel uses fixed domain + random port |
| **Process persistence** | Tunnel needs to run continuously |
| **Public access** | Generated URL can be accessed from anywhere |
| **No auth required** | Can use without login |

### 🛠 Manage Tunnel Processes

**View running tunnels:**
```bash
ps aux | grep "scc tunnel"
```

**Stop tunnel:**
```bash
# Stop by process ID
kill <PID>

# Or use process kill command in OpenClaw
```

---

## 许可证 / License

MIT License

---

<div align="center">

_最后更新 / Last Updated: 2026-03-12_

**OpenClaw AI Assistant** | [OpenClaw](https://openclaw.ai)

</div>
