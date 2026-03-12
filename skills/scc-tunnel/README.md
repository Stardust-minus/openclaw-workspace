# SCC Tunnel Skill - 内网穿透工具

<div align="center">

**SCC Tunnel - Expose Local Services to Public Internet**

[中文](#-中文) | [English](#-english)

</div>

---

## 🌏 中文

### 简介

使用 SCC (scc-cli) 内网穿透工具启动 HTTP/TCP 隧道，将本地服务暴露到公网，无需配置服务器。

### 🔧 功能特性

- ✅ **无需认证** - 无需登录即可使用
- ✅ **HTTP 隧道** - 适用于 Web 服务
- ✅ **TCP 隧道** - 适用于数据库、SSH 等
- ✅ **动态域名** - HTTP 隧道每次生成不同的 UUID 域名
- ✅ **快速启动** - 一条命令即可启动

### 📦 安装

**1. 下载 scc-cli**

访问官网下载对应平台的压缩包：
https://dl.scc.paratera.com/scc-cli/latest/

**Linux x86_64:**
```bash
cd /tmp
curl -LO https://dl.scc.paratera.com/scc-cli/latest/scc-cli-0.1.3_linux_x86_64.tar.gz
tar -xzf scc-cli-0.1.3_linux_x86_64.tar.gz
sudo mv scc /usr/local/bin/
sudo chmod +x /usr/local/bin/scc
```

**2. 验证安装**
```bash
scc --version
# 输出：scc version 0.1.3
```

### 🚀 快速开始

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

### 📋 使用场景

| 场景 | 命令 | 说明 |
|------|------|------|
| v2rayA 管理界面 | `scc tunnel http 2017` | 从公网访问本地管理界面 |
| 本地开发服务器 | `scc tunnel http 3000` | 分享开发中的 Web 应用 |
| OpenClaw Gateway | `scc tunnel http 18789` | 暴露 OpenClaw 网关 |
| 数据库 | `scc tunnel tcp 3306` | 远程数据库访问 |
| SSH | `scc tunnel tcp 22` | 远程 SSH 访问 |

### 🔍 命令别名

```bash
scc tun http 2017    # tunnel 可简写为 tun
scc tun tcp 2017
```

### 📊 输出格式

**HTTP 隧道：**
```
🎉 You're ready to go live at https://<uuid>.tunnel.paracloud.com => http://localhost:<端口>
```

**TCP 隧道：**
```
🎉 You're ready to go live at tcp://tunnel.paracloud.com:<随机端口> => tcp://localhost:<端口>
```

### ⚠️ 注意事项

| 注意事项 | 说明 |
|----------|------|
| **动态域名** | HTTP 隧道每次生成不同的 UUID 域名 |
| **随机端口** | TCP 隧道使用固定域名 + 随机端口 |
| **进程保持** | 隧道需要持续运行，停止命令会关闭隧道 |
| **公网访问** | 生成的 URL 可从任何地方访问 |
| **无需认证** | 无需登录即可使用 |

### 🛠️ 管理隧道进程

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

## 🌍 English

### Introduction

Use SCC (scc-cli) tunnel tool to start HTTP/TCP tunnels and expose local services to public internet without server configuration.

### 🔧 Features

- ✅ **No authentication required** - Use without login
- ✅ **HTTP tunnel** - For web services
- ✅ **TCP tunnel** - For databases, SSH, etc.
- ✅ **Dynamic domain** - HTTP tunnel generates different UUID domain each time
- ✅ **Quick start** - One command to start

### 📦 Installation

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

### 🚀 Quick Start

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

### 📋 Use Cases

| Use Case | Command | Description |
|----------|---------|-------------|
| v2rayA admin UI | `scc tunnel http 2017` | Access local admin interface from public |
| Local dev server | `scc tunnel http 3000` | Share web app under development |
| OpenClaw Gateway | `scc tunnel http 18789` | Expose OpenClaw gateway |
| Database | `scc tunnel tcp 3306` | Remote database access |
| SSH | `scc tunnel tcp 22` | Remote SSH access |

### 🔍 Command Aliases

```bash
scc tun http 2017    # tunnel can be abbreviated as tun
scc tun tcp 2017
```

### 📊 Output Format

**HTTP Tunnel:**
```
🎉 You're ready to go live at https://<uuid>.tunnel.paracloud.com => http://localhost:<port>
```

**TCP Tunnel:**
```
🎉 You're ready to go live at tcp://tunnel.paracloud.com:<random-port> => tcp://localhost:<port>
```

### ⚠️ Notes

| Note | Description |
|------|-------------|
| **Dynamic domain** | HTTP tunnel generates different UUID domain each time |
| **Random port** | TCP tunnel uses fixed domain + random port |
| **Process persistence** | Tunnel needs to run continuously |
| **Public access** | Generated URL can be accessed from anywhere |
| **No auth required** | Can use without login |

### 🛠️ Manage Tunnel Processes

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

## 📝 许可证 / License

MIT License

---

<div align="center">

_最后更新 / Last Updated: 2026-03-12_

**OpenClaw AI Assistant** | [OpenClaw](https://openclaw.ai)

</div>
