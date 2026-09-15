# 第三方 AI API / 中转站分流规则集 (Loon / Surge / Clash / Shadowrocket)

本规则集汇总了全网各大第三方 AI API 中转平台、转售网关与代理站的域名，专门用于在 **Loon**、**Surge**、**Shadowrocket**、**Clash / Clash Meta (Mihomo)**、**Stash** 等代理工具中进行独立分流配置（例如：将第三方中转站请求分流至「直连 DIRECT」或「特定低延迟中转节点」，避免与官方 OpenAI / Anthropic 分流规则产生冲突）。

---

## 规则集文件列表

| 文件名 | 格式类型 | 适用客户端 | 规则数量 | 远程订阅链接 (Raw) |
| :--- | :--- | :--- | :--- | :--- |
| **[`AIProxy.list`](./AIProxy.list)** | TEXT (`.list`) | **Loon / Surge / Shadowrocket** | **883 条** | `https://raw.githubusercontent.com/zhousulong/ai-proxy-rules/main/AIProxy.list` |
| **[`AIProxy_Lite.list`](./AIProxy_Lite.list)** | TEXT (`.list`) | **Loon / Surge / Shadowrocket** | **458 条** | `https://raw.githubusercontent.com/zhousulong/ai-proxy-rules/main/AIProxy_Lite.list` |
| **[`AIProxy.yaml`](./AIProxy.yaml)** | YAML (Classical) | **Clash / Clash Meta / Verge / Stash** | **883 条** | `https://raw.githubusercontent.com/zhousulong/ai-proxy-rules/main/AIProxy.yaml` |
| **[`AIProxy_Lite.yaml`](./AIProxy_Lite.yaml)** | YAML (Classical) | **Clash / Clash Meta / Verge / Stash** | **458 条** | `https://raw.githubusercontent.com/zhousulong/ai-proxy-rules/main/AIProxy_Lite.yaml` |

---

## 过滤与清洗标准

1. **已剔除全部国内平台与国内域名**：
   - **国家顶级域名**：全部以 `.cn`（包括 `.com.cn`、`.net.cn`、`.org.cn` 等）结尾的域名均已剔除；
   - **国内大模型及云厂商**：百度千帆/文心、阿里通义/DashScope/魔搭、腾讯混元、字节火山引擎/豆包/扣子、华为盘古、DeepSeek、智谱 GLM、月之暗面 Kimi、MiniMax、百川智能、零一万物、阶跃星辰、商汤日日新、讯飞星火、天工 AI、360智脑、网易伏羲、硅基流动 (SiliconFlow)、秘塔科技 (Metaso)、面壁智能 (ModelBest)、澜舟科技、无问芯穹、中国移动/电信/联通等。
2. **已剔除官方大模型直连接口**：
   - OpenAI、Anthropic Claude、Google Gemini、xAI Grok、Perplexity、Mistral、Cohere、Together AI、Groq 等（请使用官方专属规则分流）。
3. **已剔除公共基础设施与社交平台**：
   - GitHub、GitLab、Vercel、Cloudflare、Linux.do、V2EX、知乎、Bilibili、微信、支付宝、各大统计分析平台与支付网关。

---

## Clash / Clash Meta (Mihomo) 配置与使用指南

在 Clash / Clash Meta / Clash Verge / Stash 配置中引入 Rule Provider：

### 1. 配置规则集订阅 `rule-providers`
```yaml
rule-providers:
  AIProxy:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/zhousulong/ai-proxy-rules/main/AIProxy.yaml"
    path: ./ruleset/AIProxy.yaml
    interval: 86400

  # 如需使用精选版，可引入：
  # AIProxy_Lite:
  #   type: http
  #   behavior: classical
  #   url: "https://raw.githubusercontent.com/zhousulong/ai-proxy-rules/main/AIProxy_Lite.yaml"
  #   path: ./ruleset/AIProxy_Lite.yaml
  #   interval: 86400
```

### 2. 配置策略组 `proxy-groups`
```yaml
proxy-groups:
  - name: AI-Proxy
    type: select
    proxies:
      - DIRECT
      - PROXY
      # - 香港节点
      # - 日本节点
```

### 3. 配置分流规则 `rules`
```yaml
rules:
  # 建议排在官方 OpenAI/Claude 分流之后
  - RULE-SET,AIProxy,AI-Proxy
  - MATCH,DIRECT
```

---

## Loon 配置与使用指南

### 方式一：远程规则集引入（推荐）

在 Loon 配置文件的 `[Remote Rule]` 节点下添加：

```ini
[Remote Rule]
# 第三方 AI 中转站分流（全量版，策略组指向 AI-Proxy 或 DIRECT）
https://raw.githubusercontent.com/zhousulong/ai-proxy-rules/main/AIProxy.list, policy=AI-Proxy, tag=AI-Proxy, enabled=true
```

### 方式二：直接在 Loon 配置文件中添加策略组与规则

#### 1. 新增策略组 `[Proxy Group]`
```ini
[Proxy Group]
# 第三方中转站策略组：根据自身网络情况选择直连 (DIRECT) 或指定节点
AI-Proxy = select, DIRECT, PROXY, 香港节点, 日本节点, 新加坡节点, node-select=false
```

#### 2. 配置规则分流顺序 `[Rule]`
> **注意**：建议将 `AIProxy.list` 放置在官方 `OpenAI` / `Anthropic` 规则之后，以保证官方 API 请求走官方专属代理，而第三方中转域名走 `AI-Proxy` 策略。

```ini
[Rule]
# 1. 官方 AI 服务规则（走官方专属代理）
# RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Loon/OpenAI/OpenAI.list,OpenAI
# RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Loon/Claude/Claude.list,Claude

# 2. 第三方 AI 中转站规则（走直连或特定中转节点）
RULE-SET,https://raw.githubusercontent.com/zhousulong/ai-proxy-rules/main/AIProxy.list,AI-Proxy

# 3. 最终兜底规则
FINAL,DIRECT
```

---


## 规则更新与维护

### 1. GitHub Actions 自动云端更新（全自动）
本项目已配置 GitHub Actions 定时任务：
- **执行频率**：每天北京时间 04:00 (UTC 20:00) 自动运行最新数据抓取、深度重定向解析与规则清洗流程；
- **智能推送**：仅在规则列表（`AIProxy.list`、`AIProxy_Lite.list`）发生变动时自动提交并推送到 `main` 分支；
- **客户端自动生效**：Loon 等客户端只要订阅了上述远程链接，将全自动获取最新分流规则，无需任何人工维护。

### 2. 本地一键更新
如果需要本地即时调试或全量更新，只需执行：
```bash
python3 update_rules.py
```
该脚本将依次执行 IANA 顶级域名拉取、外部数据源抓取、深度跳转解析与规则清洗过滤，最终重新生成最新的分流列表。

