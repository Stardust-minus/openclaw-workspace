---
name: scc-tunnel
description: 使用 SCC (scc-cli) 内网穿透工具启动 HTTP/TCP 隧道，将本地服务暴露到公网。
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":["scc"]},"install":[{"id":"manual","kind":"manual","label":"下载 scc-cli","url":"https://dl.scc.paratera.com/scc-cli/latest/"}]}}
---

# SCC Tunnel - 内网穿透工具

快速将本地服务暴露到公网，无需配置服务器。

## 快速启动

```bash
# HTTP 隧道（推荐用于 Web 服务）
scc tunnel http <本地端口>
# 例如：scc tunnel http 2017
# 返回：https://<uuid>.tunnel.paracloud.com => http://localhost:2017

# TCP 隧道（用于非 HTTP 服务）
scc tunnel tcp <本地端口>
# 例如：scc tunnel tcp 2017
# 返回：tcp://tunnel.paracloud.com:<随机端口> => tcp://localhost:2017
```

## 命令别名

```bash
scc tun http 2017    # tunnel 可简写为 tun
scc tun tcp 2017
```

## 使用场景

### 1. 暴露本地 Web 服务
- v2rayA 管理界面：`scc tunnel http 2017`
- 本地开发服务器：`scc tunnel http 3000`
- OpenClaw Gateway：`scc tunnel http 18789`

### 2. 暴露 TCP 服务
- 数据库：`scc tunnel tcp 3306`
- SSH：`scc tunnel tcp 22`
- 自定义 TCP 服务

## 输出格式

**HTTP 隧道：**
```
🎉 You're ready to go live at https://59ece46f-4325-471a-9a59-fee389c8b48a.tunnel.paracloud.com => http://localhost:2017
```

**TCP 隧道：**
```
🎉 You're ready to go live at tcp://tunnel.paracloud.com:15627 => tcp://localhost:2017
```

## 管理隧道进程

隧道以后台进程方式运行，需要时停止：

```bash
# 查看运行中的隧道进程
ps aux | grep "scc tunnel"

# 停止隧道（通过进程管理工具）
# 在 OpenClaw 中使用 process kill 命令
```

## 注意事项

1. **无需认证** - scc tunnel 无需登录即可使用
2. **动态域名** - HTTP 隧道每次生成不同的 UUID 域名
3. **随机端口** - TCP 隧道使用固定域名 + 随机端口
4. **进程保持** - 隧道需要持续运行，停止命令会关闭隧道
5. **公网访问** - 生成的 URL 可从任何地方访问

## 安装

从官网下载对应平台的压缩包：
https://dl.scc.paratera.com/scc-cli/latest/

Linux x86_64:
```bash
cd /tmp
curl -LO https://dl.scc.paratera.com/scc-cli/latest/scc-cli-0.1.3_linux_x86_64.tar.gz
tar -xzf scc-cli-0.1.3_linux_x86_64.tar.gz
sudo mv scc /usr/local/bin/
sudo chmod +x /usr/local/bin/scc
```

验证安装：
```bash
scc --version
```
