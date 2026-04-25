---
name: scc-tunnel
description: 使用 ParaCloud Tunnel (paracloud-tunnel + frpc) 启动 HTTP/TCP/UDP/STCP/XTCP 隧道，将本地服务暴露到公网。支持自定义子域名前缀、HTTP Basic Auth、加密压缩等。
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":["scc","frpc"]}}}
---

# ParaCloud Tunnel - 内网穿透工具

快速将本地服务暴露到公网，支持自定义子域名前缀。

## 快速启动

```bash
# HTTP 隧道（自定义子域名前缀）
scc http <名称> -p <前缀> -l <本地端口>
# 例如：scc http myweb -p myapp -l 3000
# 结果：https://myapp.tunnel.paracloud.com => 127.0.0.1:3000

# TCP 隧道
scc tcp <名称> -r <远程端口> -l <本地端口>
# 例如：scc tcp myssh -r 10022 -l 22
# 远程端口范围：10000-20000

# UDP 隧道
scc udp <名称> -r <远程端口> -l <本地端口>

# STCP/XTCP（加密点对点）
scc stcp <名称> -l <本地端口> -k <密钥>
scc xtcp <名称> -l <本地端口> -k <密钥>
```

## 参数说明

### 必需参数
| 类型 | 参数 | 说明 |
|------|------|------|
| http | `-p <prefix>` | 子域名前缀，结果为 `https://<prefix>.tunnel.paracloud.com` |
| tcp/udp | `-r <port>` | 远程端口（10000-20000） |
| 所有 | `-l <port>` | 本地端口（http 默认 8080） |

### 可选参数
| 参数 | 说明 |
|------|------|
| `-u <user>` | 用户名（默认 scc） |
| `-i <ip>` | 本地 IP（默认 127.0.0.1，可代理局域网主机） |
| `-k <key>` | STCP/XTCP 密钥 |
| `--uc` | 启用压缩 |
| `--ue` | 启用加密 |
| `--http-user <u>` | HTTP Basic Auth 用户名 |
| `--http-pwd <p>` | HTTP Basic Auth 密码 |
| `--host-header-rewrite <h>` | 重写 Host 头 |
| `--locations <path>` | URL 路径路由（如 /api） |

## 使用场景

### 1. 暴露本地 Web 服务（自定义域名）
```bash
scc http gpt-image -p gpt-image -l 8502
# => https://gpt-image.tunnel.paracloud.com
```

### 2. 带认证的 Web 服务
```bash
scc http admin -p myadmin -l 8080 --http-user admin --http-pwd secret
```

### 3. 代理局域网其他主机
```bash
scc http nas -p mynas -l 5000 -i 192.168.1.100
```

### 4. TCP 端口转发
```bash
scc tcp db -r 13306 -l 3306
```

### 5. 只路由特定路径
```bash
scc http api -p myapi -l 8000 --locations /api
```

## 管理隧道进程

```bash
# 查看运行中的隧道
ps aux | grep frpc

# 后台运行
nohup scc http myweb -p myapp -l 3000 > /tmp/tunnel.log 2>&1 &

# 停止隧道
pkill -f "frpc.*myweb"
```

## 当前活跃隧道

| 名称 | 前缀 | 本地端口 | URL |
|------|------|----------|-----|
| gpt-image | gpt-image | 8502 | https://gpt-image.tunnel.paracloud.com |
| embed-8b | embed-8b | 8001 | https://embed-8b.tunnel.paracloud.com（3090 机器） |
| qwen36-27b | qwen36-27b | 8000 | https://qwen36-27b.tunnel.paracloud.com（3090 机器） |

## 注意事项

1. **自定义子域名** - 使用 `-p` 指定前缀，域名格式 `<prefix>.tunnel.paracloud.com`
2. **名称唯一** - 相同名称的隧道不能重复启动，会报 `proxy already exists`
3. **进程保持** - 隧道需要持续运行（frpc 进程），停止则关闭
4. **公网访问** - 生成的 URL 可从任何地方访问
5. **frpc 版本** - 0.68.0，基于 ParaCloud 定制

## 安装

从主人服务器下载：
```bash
cd /tmp
curl -L -o paracloud-tunnel-linux-amd64.tar.gz "http://server.hanabi-ai.cn:5244/d/Data/Download/frp/paracloud-tunnel-linux-amd64.tar.gz"
tar xzf paracloud-tunnel-linux-amd64.tar.gz
sudo cp frpc /usr/local/bin/frpc
sudo cp paracloud-tunnel.sh /usr/local/bin/paracloud-tunnel
sudo chmod +x /usr/local/bin/frpc /usr/local/bin/paracloud-tunnel

# 兼容旧命令，创建 scc 符号链接
sudo ln -sf /usr/local/bin/paracloud-tunnel /usr/local/bin/scc

# 修复 frpc 路径（脚本默认用 ./frpc）
sudo sed -i 's|FRPC="./frpc"|FRPC="/usr/local/bin/frpc"|' /usr/local/bin/paracloud-tunnel
```

验证安装：
```bash
frpc --version   # 0.68.0
scc              # 显示用法
```
