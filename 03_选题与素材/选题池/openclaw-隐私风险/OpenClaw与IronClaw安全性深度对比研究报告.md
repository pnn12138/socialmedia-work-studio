# OpenClaw 与 IronClaw 安全性深度对比研究报告

## 1. 引言：AI 代理安全现状与研究背景

### 1.1 OpenClaw 与 IronClaw 发展历程

2026 年初，开源 AI 代理领域迎来了一场前所未有的热潮。OpenClaw（原名 Clawdbot、Moltbot）作为一款革命性的开源 AI 智能体，在短短几个月内就创造了开源界的神话 —— 从 2025 年 11 月推送第一行代码，到 2026 年 3 月，GitHub 星标数突破 26 万，直接超越 React、Linux，登顶全球开源项目榜首，fork 数量更是超过 5 万[(2)](http://m.toutiao.com/group/7614500481976648238/?upstream_biz=doubao)。这款由奥地利工程师 Peter Steinberger 创建的 AI 代理平台，经历了多次更名：最初名为 Clawdbot，后因商标问题更名为 Moltbot，最终在 2026 年 1 月 30 日正式定名为 OpenClaw。

OpenClaw 的核心价值在于实现了 "全自动任务执行"—— 无需人工反复干预，就能自主完成邮件沟通、数据查询、工具调用、任务协调等一系列操作，相当于给每个人配备了一个 "全能 AI 助手"[(4)](http://m.toutiao.com/group/7614148693494727214/?upstream_biz=doubao)。然而，随着其爆发式增长，安全问题也随之浮出水面。

与此同时，面对 OpenClaw 暴露的严重安全隐患，Transformer 架构的共同发明人 Illia Polosukhin（社区称 "菠萝哥"）决定彻底解决这个问题。他用 Rust 语言完全重写了整个系统，命名为 IronClaw—— 钢铁之爪[(123)](http://m.toutiao.com/group/7614667533622444586/?upstream_biz=doubao)。IronClaw 定位为企业级安全与可观测性平台，部署在 Agent 与外部世界之间，充当一个智能代理网关，实时拦截、分析并清洗所有进出 Agent 的数据流[(6)](http://m.163.com/dy/article/KNGM0R8B05566TJ2.html)。

### 1.2 安全问题的重要性与紧迫性

工业和信息化部网络安全威胁和漏洞信息共享平台（NVDB）在 2026 年 3 月发布了关于防范 OpenClaw 开源 AI 智能体安全风险的预警，明确指出 OpenClaw 在默认或不当配置情况下存在较高安全风险，极易引发网络攻击、信息泄露等安全问题[(106)](http://m.toutiao.com/group/7614794707624919579/?upstream_biz=doubao)。这一官方预警将 OpenClaw 的安全问题提升到了国家层面的关注。

卡巴斯基在 2026 年 1 月底进行的安全审计中发现了 512 个漏洞，其中 8 个被归类为关键漏洞[(113)](https://www.kaspersky.com/blog/openclaw-vulnerabilities-exposed/55263/)。更令人担忧的是，全球超过 23 万例 OpenClaw 实例暴露在公网上，其中约 8.78 万例存在数据泄露，约 4.3 万例存在个人身份信息暴露[(87)](https://www.showapi.com/news/article/69a7f3e94ddd79ab67051dca)。SecurityScorecard 的检测显示，有超过 40,000 个配置错误的实例默认绑定在 0.0.0.0 地址上。

主流窃密木马（RedLine、Lumma、Vidar）已经更新了特征库，专门针对 OpenClaw 的数据目录进行窃取。Gartner、Cloud Security Alliance 及卡巴斯基一致警告：OpenClaw 是 2026 年最大的内部威胁之一。

### 1.3 研究范围与目标

本报告旨在深入研究 OpenClaw 在权限管理和隐私保护方面的安全性问题，并与 IronClaw 进行全面对比分析。研究将从用户和技术开发人员的双重视角出发，重点关注以下几个方面：



1. **OpenClaw 权限管理安全分析**：深入剖析 OpenClaw 在身份认证、访问控制、权限粒度等方面的设计缺陷和安全隐患。

2. **OpenClaw 隐私保护机制分析**：重点研究数据加密、通信安全、数据存储等方面的安全措施及其不足。

3. **OpenClaw 与 IronClaw 安全性对比**：从技术架构、安全机制、实现方式等多个维度进行详细对比，分析两者的根本差异。

4. **漏洞利用场景分析**：基于已知漏洞，构建具体的攻击场景，评估潜在风险。

5. **安全修复建议**：针对发现的安全问题，提出切实可行的修复方案和最佳实践。

本报告将为 AI 代理用户、开发人员和安全从业者提供全面的安全评估和决策参考，帮助读者在享受 AI 代理便利的同时，最大限度地降低安全风险。

## 2. OpenClaw 安全性深度分析

### 2.1 用户视角：权限与隐私保护体验

从普通用户的角度来看，OpenClaw 在权限管理和隐私保护方面存在诸多令人担忧的问题。这些问题不仅影响用户体验，更直接威胁到用户的数据安全和系统安全。

#### 2.1.1 权限管理的用户体验问题

OpenClaw 的权限管理机制在设计上存在根本性缺陷，给用户带来了严重的安全隐患。首先，**身份认证机制过于薄弱**。根据卡巴斯基的研究，OpenClaw 在 2026 年 2 月之前的版本默认情况下没有开启认证功能，而其控制面板默认监听 19890 端口[(60)](http://m.toutiao.com/group/7614801961942073871/?upstream_biz=doubao)。这意味着攻击者可以直接访问 OpenClaw 的管理界面，无需任何身份验证。

更严重的是，OpenClaw 对本地连接的 "过度信任"。系统默认将来自 127.0.0.1/[localhost](https://localhost)的连接视为受信任的，无需用户认证即可授予完全访问权限。然而，如果网关位于配置不当的反向代理后面，所有外部请求都会被转发到 127.0.0.1，系统会将它们视为本地流量，自动交出系统控制权。

在权限粒度方面，OpenClaw 的设计**过于粗放**。系统缺乏基于角色的权限控制系统（RBAC），无法为不同操作、不同用户设置差异化权限，这在企业环境中构成严重安全隐患。权限管理仅通过 "角色"（operator/node/adapter）进行基本区分，无法实现细粒度的权限划分，违背了 "最小权限" 原则。

用户在实际使用中还面临着**权限提升风险**。OpenClaw 的架构设计允许 Agent 调用技能时，技能可以直接访问 Agent 持有的所有凭证[(115)](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)。这意味着，一旦恶意技能被安装，它就能够获取用户的所有敏感信息，包括 API 密钥、密码、OAuth 令牌等。

#### 2.1.2 隐私保护的用户体验问题

OpenClaw 在隐私保护方面的表现同样令人担忧。最严重的问题是**敏感信息明文存储**。卡巴斯基的分析报告揭示，OpenClaw 将 API 密钥、密码、整合服务凭证等所有敏感信息全部以明文形式存储在配置文件中[(115)](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)。不仅如此，记忆文件和聊天记录同样包含大量明文敏感信息。

这种设计缺陷的严重性在于，一旦攻击者突破 OpenClaw 的任何防线，所有凭证都唾手可得，无需进一步解密或提权。更糟糕的是，这一设计缺陷已引起恶意软件作者的注意。RedLine、Lumma、Vidar 等主流信息窃取木马，已专门将 OpenClaw 的存储路径加入其 "必偷清单"。

在**通信安全**方面，OpenClaw 也存在严重问题。即使使用 HTTPS，如果未启用加密 SNI，令牌也可能出现在 TLS 元数据中[(16)](https://www.giskard.ai/knowledge/openclaw-security-vulnerabilities-include-data-leakage-and-prompt-injection-risks)。这意味着攻击者可能通过网络嗅探获取用户的认证令牌。

用户还面临着**数据泄露风险**。根据 declawed.io 截至 2026 年 2 月 17 日的数据，全球共探测到超过 23 万例 OpenClaw 公网暴露实例，其中约 8.78 万例存在数据泄露，约 4.3 万例存在个人身份信息暴露[(87)](https://www.showapi.com/news/article/69a7f3e94ddd79ab67051dca)。这些暴露实例遍布全球 52 个国家，美国以 891 例（35.6%）居首，中国以 648 例（25.9%）紧随其后。

### 2.2 技术开发人员视角：安全架构与实现缺陷

从技术开发人员的专业角度来看，OpenClaw 的安全问题不仅体现在表面的配置缺陷，更根植于其底层架构设计的根本性问题。

#### 2.2.1 权限管理架构设计缺陷

OpenClaw 的权限管理架构存在多重设计缺陷，这些缺陷相互叠加，形成了严重的安全风险。首先，**认证机制的设计存在严重漏洞**。CVE-2026-25253 漏洞（CVSS 评分 8.8）就是一个典型的例子，该漏洞存在于 OpenClaw 控制界面的连接流程中。攻击者只需制作一个特制网站或恶意链接，诱导用户点击，OpenClaw 就会自动连接到攻击者控制的端点，泄露浏览器中存储的网关身份验证令牌（Token）[(115)](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)。

这一漏洞的根本原因在于 OpenClaw 会从查询字符串中获取 gatewayUrl 值，并在无任何提示的情况下自动建立 WebSocket 连接并发送 token[(115)](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)。这种设计完全违背了安全的基本原则 ——**用户知情权和选择权**。

在**访问控制模型**方面，OpenClaw 虽然声称支持 RBAC（基于角色的访问控制）和 ABAC（基于属性的访问控制）的混合模型，但在实际实现中存在诸多问题。系统缺乏统一的权限管理框架，不同模块之间的权限控制逻辑不一致，导致权限管理混乱。

更严重的是**权限继承问题**。OpenClaw 的技能系统允许第三方代码直接访问 Agent 的所有权限，这种设计存在严重的安全隐患。Snyk 的安全审计显示，在 ClawHub 技能市场中，36% 的技能存在安全缺陷，1467 个技能含有恶意载荷。一个恶意技能可以轻易窃取用户的所有凭证，执行远程代码，将用户的数字身份洗劫一空。

#### 2.2.2 隐私保护技术实现缺陷

OpenClaw 在隐私保护技术实现方面存在多重缺陷，这些缺陷直接威胁到用户数据的安全性和完整性。

**数据存储安全**是最严重的问题之一。OpenClaw 将所有敏感信息以明文形式存储在以下位置：



* `~/.openclaw/openclaw.json`：配置文件，可能包含令牌、提供商设置和白名单

* `credentials/**`：渠道凭证（如 WhatsApp 凭证）、配对白名单、OAuth 导入

* `agents/<agentId>/agent/auth-profiles.json`：API 密钥和 OAuth 令牌

* `agents/<agentId>/sessions/**`：会话记录，可能包含私人消息和工具输出

这种明文存储方式使得攻击者可以通过多种途径获取敏感信息。例如，通过恶意技能直接读取配置文件，或者通过系统漏洞获取文件系统访问权限。

在**通信安全**方面，OpenClaw 的实现同样存在问题。WebSocket 连接默认情况下不验证来源，这使得跨站 WebSocket 劫持（CSWSH）攻击成为可能。攻击者可以在用户访问恶意网站时，利用浏览器的跨源策略漏洞，在后台悄然与本地运行的 OpenClaw 建立连接。

**加密机制的缺失**也是一个严重问题。虽然 OpenClaw 在 v2026.2.23 版本中引入了三层加密机制，包括文件系统加密和 PBKDF2 密钥派生，但这些改进来得太晚，且覆盖范围有限。许多早期版本和仍在使用的版本仍然缺乏基本的加密保护。

#### 2.2.3 代码层面的安全漏洞

从代码审计的角度来看，OpenClaw 存在大量可被利用的安全漏洞。卡巴斯基的安全审计发现了 512 个漏洞，其中包括两个危险的命令注入漏洞（CVE-2026-24763 和 CVE-2026-25157）。

**命令注入漏洞**的存在使得攻击者可以执行任意系统命令。例如，在处理用户输入时，OpenClaw 没有进行充分的输入验证和转义，导致攻击者可以构造恶意命令。一个典型的例子是，当用户要求 OpenClaw 运行`find ~/`命令时，它会将主目录的内容直接输出到群组聊天中，暴露敏感信息。

**路径穿越漏洞**也是一个严重问题。OpenClaw 在处理文件路径时没有进行严格的验证，攻击者可以利用这一漏洞访问系统的任意文件。在 v2026.3.7 版本的更新中，修复了一个高危路径穿越漏洞，该漏洞允许攻击者绕过目录限制[(92)](https://www.iesdouyin.com/share/note/7614868542777244746/?region=\&mid=7599216671047420722\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&schema_type=37\&share_sign=5dtHnWxItJhdPZok4H2hAybpJ_Zssm0yJzbljMoZqQo-\&share_version=280700\&ts=1772992781\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)。

**内存安全问题**同样不容忽视。由于 OpenClaw 使用 TypeScript 编写，虽然避免了一些底层的内存安全问题，但在处理大量数据时仍可能存在内存泄漏和缓冲区溢出的风险。更重要的是，TypeScript 的动态特性使得一些安全检查在运行时才能发现，增加了安全风险。

## 3. OpenClaw 与 IronClaw 安全性对比分析

### 3.1 权限管理架构对比

OpenClaw 与 IronClaw 在权限管理架构上存在根本性的差异，这种差异源于两者完全不同的设计哲学和安全理念。

**OpenClaw 的权限管理架构**存在明显的设计缺陷。系统缺乏统一的权限管理框架，认证机制薄弱，默认情况下没有开启认证功能[(60)](http://m.toutiao.com/group/7614801961942073871/?upstream_biz=doubao)。OpenClaw 采用了过于宽松的信任模型，将本地连接视为完全可信，这在现代网络环境中是极其危险的设计。

相比之下，**IronClaw 建立了严格的多层权限管理架构**。系统采用了多租户认证机制，用多用户认证替代了单一令牌网关认证。每个 Bearer 令牌映射到一个用户身份，携带用户 ID、工作区读权限和记忆层信息[(71)](https://github.com/nearai/ironclaw/pull/341)。这种设计实现了真正的用户隔离和权限控制。

在**权限粒度控制**方面，两者的差异更加明显。OpenClaw 的权限管理仅通过简单的角色（operator/node/adapter）进行区分，无法实现细粒度的权限控制。而 IronClaw 实现了基于能力的权限模型（capability-based permissions），支持对 HTTP 请求、密钥和工具调用的显式选择加入机制[(67)](https://github.com/veniceai/ironclaw/blob/main/README.md)。

**访问控制策略**的对比同样鲜明。OpenClaw 默认允许所有本地连接，缺乏有效的访问控制机制。而 IronClaw 实施了严格的端点白名单策略，HTTP 请求只能发送到预先批准的主机和路径[(67)](https://github.com/veniceai/ironclaw/blob/main/README.md)。这种设计从根本上限制了攻击面。

在**权限验证流程**上，IronClaw 实现了更加安全和可控的机制。系统在工具批准门（tool approval gate）处进行权限验证，需要用户明确提示，支持每个会话的可选自动批准功能[(95)](https://github.com/nearai/ironclaw/issues/88)。这种设计确保了用户对每一个重要操作都有知情权和控制权。

### 3.2 隐私保护技术对比

隐私保护是 AI 代理安全的核心，OpenClaw 和 IronClaw 在这方面的技术实现存在天壤之别。

**OpenClaw 的隐私保护缺陷**主要体现在以下几个方面：



1. **明文存储问题**：OpenClaw 将所有敏感信息以明文形式存储在配置文件和日志中[(115)](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)，这是最严重的安全隐患。

2. **通信安全不足**：即使使用 HTTPS，如果未启用加密 SNI，令牌可能出现在 TLS 元数据中[(16)](https://www.giskard.ai/knowledge/openclaw-security-vulnerabilities-include-data-leakage-and-prompt-injection-risks)。

3. **缺乏数据加密**：在早期版本中，OpenClaw 完全缺乏对敏感数据的加密保护。

4. **记忆数据泄露**：会话记录和记忆文件包含大量明文敏感信息，容易被窃取。

**IronClaw 的隐私保护架构**则建立在多层加密和隔离的基础上：



1. **加密凭证保险库**：所有 API 密钥和密码都使用 AES-256-GCM 加密存储，每一条凭证都绑定了策略规则，规定它只能用于特定域名[(118)](http://m.toutiao.com/group/7614068855752720934/?upstream_biz=doubao)。

2. **凭证注入边界**：IronClaw 实现了一个创新的凭证注入机制，在主机级别将凭证透明地解析和注入到出站 HTTP 请求中，而沙箱化的工具代码永远无法直接访问原始凭证[(74)](https://github.com/nearai/ironclaw/blob/2f7e4777258e0956d7c88e7ce43c89a5da147699/docs/analysis/secrets-keychain.md)。

3. **内存安全保障**：由于使用 Rust 语言编写，IronClaw 从根本上杜绝了缓冲区溢出等传统内存安全漏洞，这对于处理敏感数据至关重要[(70)](https://www.aipuzi.cn/ai-tools/ironclaw.html)。

4. **硬件级隔离**：IronClaw 支持在可信执行环境（TEE）中运行，利用硬件级别的隔离保护数据，即使是云服务提供商也无法访问用户的敏感信息[(118)](http://m.toutiao.com/group/7614068855752720934/?upstream_biz=doubao)。

**数据处理流程**的对比更能说明两者的差异。在 OpenClaw 中，当用户提供一个 API 密钥时，这个密钥会被直接传递给大语言模型，存在被恶意提示词诱导泄露的风险。而在 IronClaw 中，大语言模型永远接触不到原始凭证。当智能体需要发送请求时，AI 生成请求模板，凭证保险库在验证请求符合策略后，在主机边界将加密的凭证解密并注入到网络请求中[(123)](http://m.toutiao.com/group/7614667533622444586/?upstream_biz=doubao)。

### 3.3 技术架构安全性差异

OpenClaw 和 IronClaw 在技术架构上的差异直接决定了两者的安全性能。这种差异不仅体现在编程语言的选择上，更体现在整体架构设计的理念上。

**编程语言的选择**带来了根本性的安全差异。OpenClaw 使用 TypeScript 编写，这是一种基于 JavaScript 的语言。虽然 TypeScript 提供了类型系统，但仍然存在动态特性带来的安全风险。相比之下，IronClaw 完全使用 Rust 语言重写。Rust 的内存安全特性从根本上消除了缓冲区溢出、悬垂指针等传统漏洞，这对于处理私钥和用户凭证的系统至关重要[(118)](http://m.toutiao.com/group/7614068855752720934/?upstream_biz=doubao)。

**架构设计理念**的差异更加深刻。OpenClaw 采用了 "便利优先" 的设计哲学，为了易用性牺牲了安全性。用户可以一键部署，快速上手，但代价是巨大的安全风险。而 IronClaw 则采用了 "安全优先" 的新范式，承认如果 AI 助手不安全，那么它带来的便利最终会成为灾难[(123)](http://m.toutiao.com/group/7614667533622444586/?upstream_biz=doubao)。

**运行环境隔离**是两者的另一个重要差异。OpenClaw 的工具在共享进程中运行，缺乏有效的隔离机制。一个恶意工具可以轻易访问整个系统的资源。而 IronClaw 实现了严格的 WASM（WebAssembly）沙箱隔离，所有第三方工具和 AI 生成的代码都在独立的 WebAssembly 容器中运行[(82)](http://m.toutiao.com/group/7614077222592201259/?upstream_biz=doubao)。每个容器都有明确的权限边界：能访问哪些网络端点，能使用哪些凭证，能调用哪些其他工具。即使某个工具是恶意的，它的破坏范围也被严格限制在沙箱之内。

**安全层次设计**的对比同样鲜明。IronClaw 建立了四层（或五层）纵深防御体系[(39)](https://36kr.com/p/3711194778054789)：



1. **第一层**：Rust 语言的内存安全保证，从根本上杜绝了底层漏洞。

2. **第二层**：WASM 沙箱隔离，实现工具级别的严格隔离。

3. **第三层**：加密凭证保险库，使用 AES-256-GCM 加密存储所有敏感信息。

4. **第四层**：硬件级可信执行环境（TEE），提供最高级别的硬件保护。

5. **第五层**（某些资料提到）：网络层保护，包括 TLS 1.3 加密、SSRF 防护等。

而 OpenClaw 缺乏这样的纵深防御体系，安全措施零散且薄弱，主要依赖单一的防护手段，一旦被突破就会导致全面沦陷。

**审计和监控能力**也是两者的重要差异。IronClaw 实现了完整的审计日志系统，AI Agent 的每一个操作都会被详细记录，包括操作时间、操作内容、执行结果，一旦出现问题能快速追溯到源头[(121)](http://m.toutiao.com/group/7610299611265139206/?upstream_biz=doubao)。而 OpenClaw 的日志系统虽然能够记录操作，但缺乏有效的审计机制，且日志本身可能包含敏感信息。

## 4. OpenClaw 漏洞利用场景分析

### 4.1 高危漏洞 CVE-2026-25253 利用场景

CVE-2026-25253 是 OpenClaw 迄今为止最严重的安全漏洞，CVSS 评分高达 8.8 分[(13)](https://www.kaspersky.com/blog/moltbot-enterprise-risk-management/55317/)。这个漏洞的可怕之处在于其极低的攻击门槛和极高的破坏力 —— 攻击者只需诱导用户点击一个恶意链接，就能完全接管受害者的 OpenClaw 实例。

**漏洞原理分析**：该漏洞存在于 OpenClaw 控制界面的连接流程中。OpenClaw 的 Web 界面会从 URL 查询字符串中获取 gatewayUrl 参数，并在没有任何用户提示的情况下自动建立 WebSocket 连接，将浏览器中存储的认证令牌发送到该参数指定的地址[(115)](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)。这种设计完全违背了安全原则，为跨站 WebSocket 劫持（CSWSH）攻击提供了完美的条件。

**典型攻击场景**：



1. **钓鱼网站攻击**：攻击者创建一个看似正常的网站，例如 "OpenClaw 官方更新通知" 或 "免费 AI 工具下载"。当用户访问该网站时，页面中嵌入的恶意 JavaScript 会构造一个包含恶意 gatewayUrl 参数的链接。这个参数指向攻击者控制的服务器。

2. **社交媒体传播**：攻击者在社交媒体平台（如 Twitter、Reddit、技术论坛）发布诱人的帖子，声称提供 OpenClaw 的高级功能或独家技巧。帖子中包含恶意链接，诱导用户点击。

3. **邮件钓鱼攻击**：攻击者发送伪造的 OpenClaw 官方邮件，声称用户的账户需要验证或有重要更新。邮件中包含指向恶意网站的链接。

4. **即时通讯软件攻击**：攻击者通过即时通讯软件（如 WhatsApp、Telegram）向用户发送消息，包含恶意链接，利用 OpenClaw 与这些平台的集成特性进行攻击。

**攻击过程演示**：

当用户点击恶意链接后，浏览器会加载一个看似正常的页面。与此同时，页面中的恶意脚本会执行以下操作：



* 构造一个包含攻击者服务器地址的 gatewayUrl 参数

* 创建一个隐藏的 iframe 或 WebSocket 连接

* OpenClaw 检测到这个连接请求，自动建立 WebSocket 连接

* OpenClaw 将存储在浏览器中的认证令牌发送给攻击者的服务器

* 攻击者获得令牌后，可以完全控制用户的 OpenClaw 实例

**攻击后果评估**：

一旦攻击成功，攻击者可以执行以下操作：



* 窃取所有存储的 API 密钥、密码和 OAuth 令牌

* 读取和发送即时通讯消息，冒充用户身份

* 访问和修改用户的文件系统

* 执行任意系统命令，将受害者的电脑变成 "肉鸡"

* 横向渗透到用户的其他设备和网络

* 长期潜伏，持续窃取敏感信息

根据 Hunt.io 的研究，超过 17,500 个暴露的 OpenClaw 实例受到该漏洞影响。这些实例遍布全球，攻击者可以轻易获取大量用户的敏感信息。

### 4.2 其他关键漏洞利用场景

除了 CVE-2026-25253 之外，OpenClaw 还存在多个严重的安全漏洞，这些漏洞相互配合可以形成更加复杂和危险的攻击链。

#### 4.2.1 命令注入漏洞利用

OpenClaw 存在多个命令注入漏洞，其中最严重的是 CVE-2026-24763 和 CVE-2026-25157。这些漏洞允许攻击者在 OpenClaw 的上下文中执行任意系统命令。

**利用场景示例**：



1. **文件泄露攻击**：攻击者发送一个看似无害的请求，例如 "查找系统中的日志文件"。通过精心构造的输入，攻击者可以执行命令读取任意文件的内容。例如，用户要求运行`find ~/`命令时，OpenClaw 会将主目录的内容直接输出到群组聊天中，暴露敏感信息。

2. **权限提升攻击**：攻击者利用命令注入漏洞，通过构造特定的命令序列，提升自己在系统中的权限。例如，通过修改 sudoers 文件或创建具有 SUID 权限的文件。

3. **后门植入攻击**：攻击者通过命令注入在系统中植入后门程序，例如创建一个隐藏的用户账户或安装远程控制软件。

4. **数据破坏攻击**：攻击者可以执行破坏性命令，删除或修改系统文件，导致系统无法正常运行。

#### 4.2.2 路径穿越漏洞利用

路径穿越漏洞允许攻击者访问系统的任意文件，绕过 OpenClaw 的文件访问限制。

**利用场景示例**：



1. **配置文件窃取**：攻击者利用路径穿越漏洞读取 OpenClaw 的配置文件（如`~/.openclaw/openclaw.json`），获取其中存储的所有敏感信息。

2. **系统文件访问**：攻击者可以读取系统的关键文件，如`/etc/passwd`、`/etc/shadow`等，获取用户账户信息。

3. **日志文件篡改**：攻击者可以修改或删除系统日志，掩盖自己的攻击行为。

4. **恶意文件上传**：通过路径穿越漏洞，攻击者可以将恶意文件上传到系统的任意目录，为后续攻击做准备。

#### 4.2.3 恶意技能攻击场景

OpenClaw 的技能市场（ClawHub）已成为恶意软件的温床。Snyk 的安全审计显示，36% 的技能存在安全缺陷，1467 个技能含有恶意载荷。

**典型攻击场景**：



1. **伪装成合法工具**：攻击者将恶意软件伪装成有用的技能，如 "加密货币钱包管理"、"文件加密工具"、"系统优化器" 等。用户下载安装后，恶意技能会在后台窃取敏感信息。

2. **供应链投毒**：攻击者入侵合法技能的开发流程，在其中植入恶意代码。当用户更新技能时，会自动下载包含恶意代码的版本。

3. **权限滥用**：恶意技能利用 OpenClaw 的权限设计缺陷，访问超出其职责范围的数据和功能。例如，一个天气预报技能可以访问用户的所有文件和网络连接。

4. **持续性攻击**：恶意技能在系统中建立后门，即使技能被删除，仍能保持对系统的访问权限。

根据 VirusTotal 的研究，已分析超过 3016 个 OpenClaw 技能，其中数百个存在恶意特征[(117)](https://www.secrss.com/articles/87726?app=1)。这些恶意技能主要分为两类：直接窃取凭证的工具和用于横向移动的后门程序。

#### 4.2.4 记忆污染攻击

OpenClaw 的记忆机制存在严重的安全隐患，攻击者可以通过 "记忆污染" 实现长期的持续性攻击。

**攻击原理**：OpenClaw 使用 JSONL 格式存储会话记录，并使用 Markdown 格式的记忆文件。攻击者通过一次成功的攻击，将恶意规则写入记忆系统。之后，OpenClaw 在处理后续任务时会持续依据这些恶意规则执行。

**攻击场景**：



1. **指令注入攻击**：攻击者发送一个包含恶意指令的消息，这些指令被存储在会话记忆中。当 OpenClaw 处理类似任务时，会自动执行这些恶意指令。

2. **虚假信息植入**：攻击者向 OpenClaw 提供虚假的系统信息或操作指南，污染其知识库。例如，告诉 OpenClaw 某个危险命令是安全的，或者某个恶意网站是可信的。

3. **权限提升记忆**：攻击者通过多次交互，逐步提升自己在 OpenClaw 中的权限级别，并将这些权限信息存储在记忆中。

4. **持续性后门**：通过记忆污染，攻击者可以在 OpenClaw 中建立长期的后门，即使原始攻击被发现和清除，后门仍可能存在。

### 4.3 攻击链与综合威胁评估

OpenClaw 的安全漏洞不是孤立存在的，攻击者可以利用多个漏洞形成复杂的攻击链，实现对系统的全面控制。

**典型攻击链示例**：



1. **第一阶段：初始入侵**

* 攻击者使用 CVE-2026-25253 漏洞获取 OpenClaw 的控制权

* 通过恶意链接窃取认证令牌

* 获得对 OpenClaw 管理界面的完全访问权限

1. **第二阶段：权限提升**

* 使用命令注入漏洞执行系统命令

* 通过路径穿越漏洞访问敏感文件

* 读取配置文件获取更多凭证和权限

1. **第三阶段：横向移动**

* 使用窃取的凭证访问其他系统和服务

* 在局域网内进行扫描和探测

* 寻找其他可攻击的目标

1. **第四阶段：持续控制**

* 植入恶意技能作为后门

* 通过记忆污染保持长期访问

* 定期回传窃取的数据

**综合威胁评估**：

根据卡巴斯基的分析，OpenClaw 具有五大高风险特征[(115)](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)：



1. 拥有高权限：可直接访问文件系统、执行系统命令

2. 接收不可信数据：通过邮件、网页、聊天等渠道接收输入

3. 无法可靠区分指令与数据：极易受提示注入攻击

4. 记忆可被污染：长期影响 Agent 行为

5. 能对外发送数据：可通过邮件、API 调用等方式外泄信息

这些特征使得 OpenClaw 成为一个极其危险的攻击目标。攻击者可以利用这些特性，构建出多种复杂的攻击场景。

**影响范围评估**：



* **个人用户**：面临数据泄露、系统被控制、身份被盗用等风险

* **企业用户**：可能导致商业机密泄露、系统瘫痪、法律责任等严重后果

* **基础设施**：超过 23 万暴露实例可能被攻击者利用，形成大规模的僵尸网络

根据最新统计，全球有超过 23 万例 OpenClaw 实例暴露在公网上，其中约 8.78 万例已发生数据泄露[(87)](https://www.showapi.com/news/article/69a7f3e94ddd79ab67051dca)。这些暴露实例分布在各个行业，包括金融、医疗、政府等敏感领域，构成了严重的安全威胁。

## 5. 安全修复建议与最佳实践

### 5.1 针对 OpenClaw 漏洞的紧急修复措施

面对 OpenClaw 暴露的严重安全问题，用户需要立即采取紧急修复措施来降低安全风险。以下是针对不同漏洞的具体修复建议：

#### 5.1.1 CVE-2026-25253 漏洞修复

针对 CVE-2026-25253 这个最严重的漏洞，用户应立即采取以下修复措施：



1. **紧急升级到最新版本**

* 立即将 OpenClaw 升级到 v2026.2.26 或更高版本，该版本已经修复了此漏洞

* 执行命令：`openclaw upgrade`

* 验证版本号：`openclaw version`

1. **临时防护措施（未升级前）**

* 停止 OpenClaw 服务：`openclaw stop`

* 修改配置文件`~/.openclaw/openclaw.json`，将`gateway.bind`设置为 "loopback"

* 关闭所有对外网络访问，只保留必要的连接

* 使用防火墙限制 OpenClaw 的网络访问

1. **长期防护策略**

* 启用 HTTPS 连接，使用自签名或 CA 签名的证书

* 配置严格的 CSP（内容安全策略），限制 WebSocket 连接来源

* 实现用户确认机制，对所有外部连接请求进行二次确认

* 定期检查系统日志，发现异常连接立即处理

#### 5.1.2 认证机制修复

针对 OpenClaw 认证机制的缺陷，建议采取以下修复措施：



1. **启用强认证机制**

* 设置复杂的管理员密码，至少 12 位，包含字母、数字和特殊字符

* 启用双因素认证（2FA），使用 TOTP 等标准协议

* 定期更换密码，建议每月更新一次

* 禁用默认的空密码或弱密码

1. **限制访问来源**

* 将`gateway.bind`设置为 "loopback"，只允许本地访问

* 使用防火墙限制访问 IP，只允许可信的 IP 地址

* 配置访问白名单，拒绝所有未授权的访问请求

* 启用 IP 地址锁定机制，对多次认证失败的 IP 地址进行临时封锁

1. **会话管理强化**

* 设置会话超时时间，建议不超过 30 分钟

* 使用加密的会话存储，避免明文存储会话 ID

* 实现会话固定攻击防护，在认证成功后生成新的会话 ID

* 定期清理过期会话，减少攻击面

#### 5.1.3 权限管理修复

针对权限管理的缺陷，建议采取以下修复措施：



1. **实施最小权限原则**

* 为不同用户分配不同的角色，每个角色只拥有必要的权限

* 限制技能的访问权限，只授予其完成任务所需的最小权限

* 实现权限分离，将管理权限和操作权限分开

* 定期审核权限分配，删除不必要的权限

1. **加强技能安全管理**

* 只从官方或可信来源下载技能，避免从不可信的第三方获取

* 在安装新技能前进行安全审查，检查代码的安全性

* 限制技能的网络访问权限，使用网络白名单

* 定期检查已安装的技能，删除可疑或不必要的技能

1. **实现细粒度权限控制**

* 为每个文件和目录设置访问控制列表（ACL）

* 限制系统命令的执行权限，只允许执行必要的命令

* 实现基于角色的访问控制（RBAC），为不同角色分配不同权限

* 建立权限审计机制，记录所有权限相关的操作

### 5.2 安全加固最佳实践

除了针对具体漏洞的修复外，用户还需要实施全面的安全加固措施，构建多层次的安全防护体系。

#### 5.2.1 系统层面安全加固



1. **运行环境隔离**

* 使用 Docker 容器运行 OpenClaw，实现与主机系统的隔离

* 配置 Docker 的安全选项，如`--security-opt seccomp=unconfined`

* 使用独立的用户账户运行 OpenClaw，避免使用 root 权限

* 在虚拟机中运行 OpenClaw，提供额外的安全隔离

1. **文件系统保护**

* 将 OpenClaw 的数据目录权限设置为 700（仅所有者可访问）

* 配置文件权限设置为 600（仅所有者可读可写）

* 使用加密文件系统存储敏感数据

* 定期备份重要数据，并加密存储备份文件

1. **网络安全配置**

* 使用防火墙限制 OpenClaw 的网络访问，只开放必要的端口

* 配置 iptables 规则，限制可疑的网络流量

* 启用 IPSec 或 TLS 加密所有网络通信

* 实施网络分段，将 OpenClaw 与其他系统隔离

#### 5.2.2 应用层面安全加固



1. **输入验证和过滤**

* 对所有用户输入进行严格的验证和过滤

* 使用正则表达式验证输入格式，拒绝非法字符

* 实现 XSS 防护，对输出内容进行转义处理

* 限制输入长度，避免缓冲区溢出攻击

1. **命令执行安全**

* 使用安全的命令执行函数，避免使用 eval () 等危险函数

* 对所有命令参数进行转义处理

* 限制可执行命令的范围，使用白名单机制

* 实现命令执行审计，记录所有执行的命令

1. **数据加密保护**

* 对所有敏感数据进行加密存储，使用 AES-256 等强加密算法

* 实现端到端加密，确保数据在传输过程中的安全性

* 使用硬件加密模块（HSM）保护密钥

* 定期轮换加密密钥，提高安全性

#### 5.2.3 监控和审计体系



1. **行为监控**

* 实现对 OpenClaw 行为的实时监控

* 建立异常行为检测机制，识别可疑操作

* 设置告警规则，对高风险操作进行实时告警

* 使用机器学习算法识别攻击模式

1. **日志审计**

* 配置详细的日志记录，包括用户操作、系统事件、错误信息等

* 对日志进行加密存储，防止日志被篡改

* 定期进行日志分析，发现潜在的安全问题

* 实现日志的集中管理和备份

1. **安全审计**

* 定期进行安全审计，检查系统配置和安全策略的执行情况

* 使用安全扫描工具检测漏洞，如 OWASP ZAP、Burp Suite 等

* 进行渗透测试，模拟攻击者的行为

* 建立安全审计报告机制，及时发现和修复安全问题

### 5.3 迁移至 IronClaw 的建议

鉴于 OpenClaw 存在的根本性安全问题，我们强烈建议用户考虑迁移至更加安全的 IronClaw 平台。以下是迁移建议和实施步骤：

#### 5.3.1 迁移准备



1. **环境评估**

* 检查当前硬件环境是否满足 IronClaw 的要求（至少 512MB 内存）[(120)](https://blog.csdn.net/qq_44866828/article/details/158661946)

* 准备 PostgreSQL 数据库，版本 15 或更高，需要 pgvector 扩展[(67)](https://github.com/veniceai/ironclaw/blob/main/README.md)

* 评估现有 OpenClaw 的配置和数据，制定迁移计划

1. **数据备份**

* 备份 OpenClaw 的所有配置文件：`~/.openclaw/`目录

* 备份所有技能和扩展

* 备份会话记录和记忆文件

* 确保备份文件的安全性，使用加密存储

1. **账户准备**

* 注册 NEAR AI Cloud 账户（如果选择云端部署）

* 创建 IronClaw 的管理员账户

* 准备必要的 API 密钥和凭证

#### 5.3.2 迁移实施



1. **安装 IronClaw**

* 下载最新版本的 IronClaw：`curl -fsSL ``https://raw.githubusercontent.com/nearai/ironclaw/main/install.sh`` | sh`

* 或者使用 Homebrew 安装：`brew install nearai/tap/ironclaw`

* 验证安装：`ironclaw version`

1. **配置迁移**

* 逐步迁移配置，从简单的功能开始

* 先配置基本的认证和权限设置

* 然后迁移技能和工具配置

* 最后迁移数据和记忆

1. **功能验证**

* 验证基本功能是否正常工作

* 测试与外部服务的集成

* 检查数据同步和备份功能

* 进行安全测试，确保没有遗留漏洞

#### 5.3.3 安全配置建议



1. **启用所有安全功能**

* 启用 WASM 沙箱隔离，确保工具的安全运行

* 配置加密凭证保险库，保护所有敏感信息

* 启用网络白名单，严格控制网络访问

* 配置泄露检测功能，实时监控数据泄露风险

1. **实施最佳实践**

* 遵循 IronClaw 的安全最佳实践文档

* 使用最小权限原则配置所有用户和角色

* 定期更新 IronClaw 到最新版本

* 启用自动安全更新功能

1. **持续监控和改进**

* 建立完善的监控体系，实时监控系统状态

* 定期进行安全审计，发现潜在问题

* 参与 IronClaw 社区，获取最新的安全信息

* 考虑购买专业的安全服务和支持

## 6. 结论与展望

### 6.1 主要发现总结

通过对 OpenClaw 和 IronClaw 的深入对比研究，我们得出以下关键发现：

**OpenClaw 的安全现状堪忧**。作为 2026 年初最火爆的开源 AI 代理项目，OpenClaw 在安全性方面存在系统性的设计缺陷。卡巴斯基的安全审计发现了 512 个漏洞，其中 8 个为关键漏洞[(113)](https://www.kaspersky.com/blog/openclaw-vulnerabilities-exposed/55263/)。最严重的 CVE-2026-25253 漏洞（CVSS 评分 8.8）允许攻击者通过一个恶意链接完全接管用户的系统[(13)](https://www.kaspersky.com/blog/moltbot-enterprise-risk-management/55317/)。更令人担忧的是，全球超过 23 万例 OpenClaw 实例暴露在公网上，其中近 9 万例已发生数据泄露[(87)](https://www.showapi.com/news/article/69a7f3e94ddd79ab67051dca)。

OpenClaw 的安全问题主要体现在四个方面：**一是权限管理混乱**，缺乏统一的权限框架，默认情况下没有认证机制，对本地连接过度信任[(60)](http://m.toutiao.com/group/7614801961942073871/?upstream_biz=doubao)；**二是隐私保护薄弱**，所有敏感信息以明文存储，缺乏基本的加密保护[(115)](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)；**三是架构设计缺陷**，使用 TypeScript 编写，存在内存安全风险，技能系统缺乏隔离机制[(70)](https://www.aipuzi.cn/ai-tools/ironclaw.html)；**四是漏洞利用门槛低**，攻击者可以通过命令注入、路径穿越、恶意技能等多种方式入侵系统。

**IronClaw 提供了根本性的安全解决方案**。作为由 Transformer 作者 Illia Polosukhin 主导开发的项目，IronClaw 从设计之初就将安全性作为核心考量。它采用 Rust 语言编写，从根本上杜绝了内存安全漏洞[(118)](http://m.toutiao.com/group/7614068855752720934/?upstream_biz=doubao)。更重要的是，IronClaw 建立了四层（或五层）纵深防御体系，包括 WASM 沙箱隔离、加密凭证保险库、硬件级可信执行环境等，实现了 "大模型永远接触不到原始凭证" 的安全目标[(123)](http://m.toutiao.com/group/7614667533622444586/?upstream_biz=doubao)。

在具体的安全机制对比中，两者的差异是根本性的。OpenClaw 采用 "便利优先" 的设计哲学，为了易用性牺牲了安全性；而 IronClaw 则坚持 "安全优先" 的原则，宁可增加一些使用复杂度也要确保用户数据的安全[(123)](http://m.toutiao.com/group/7614667533622444586/?upstream_biz=doubao)。这种理念差异直接体现在技术实现上：OpenClaw 的技能可以直接访问所有系统资源，而 IronClaw 的每个工具都运行在独立的 WASM 沙箱中，权限被严格限制[(82)](http://m.toutiao.com/group/7614077222592201259/?upstream_biz=doubao)。

### 6.2 安全风险评估

基于我们的研究，我们对使用 OpenClaw 和 IronClaw 的安全风险进行如下评估：

**使用 OpenClaw 的风险等级：极高**



1. **数据泄露风险**：由于明文存储和公网暴露，用户的所有敏感信息（包括 API 密钥、密码、聊天记录等）都面临被窃取的风险。主流窃密木马已经专门针对 OpenClaw 进行了优化。

2. **系统控制风险**：攻击者可以通过多种漏洞获得系统的完全控制权，将用户的设备变成 "肉鸡"，用于发起进一步的攻击或挖矿等恶意活动。

3. **身份冒用风险**：攻击者可以利用窃取的凭证冒充用户身份，发送消息、访问账户、进行交易等，造成严重的身份安全问题。

4. **法律合规风险**：在某些行业（如金融、医疗），使用 OpenClaw 可能违反数据保护法规，导致巨额罚款和法律责任。

**使用 IronClaw 的风险等级：低**



1. **架构安全保障**：Rust 语言的内存安全特性和 WASM 沙箱隔离机制从根本上降低了被攻击的可能性。

2. **数据保护机制**：所有敏感信息都经过加密存储和传输，大模型无法直接访问原始凭证，有效防止了数据泄露风险[(118)](http://m.toutiao.com/group/7614068855752720934/?upstream_biz=doubao)。

3. **权限控制严格**：基于能力的权限模型和严格的网络白名单机制，确保了最小权限原则的实施[(67)](https://github.com/veniceai/ironclaw/blob/main/README.md)。

4. **持续安全改进**：IronClaw 团队承诺进行定期的安全审计和红队测试，不断提升系统的安全性[(118)](http://m.toutiao.com/group/7614068855752720934/?upstream_biz=doubao)。

### 6.3 未来发展建议

基于研究发现，我们对不同类型的用户提出以下建议：

**对于个人用户**：



1. 立即停止使用未更新的 OpenClaw 版本，升级到最新版本或考虑迁移到 IronClaw

2. 如果必须使用 OpenClaw，请严格按照安全最佳实践进行配置，包括启用认证、限制网络访问、定期审计等

3. 不要在 OpenClaw 中存储过于敏感的信息，特别是金融相关的凭证

4. 定期备份数据，并加密存储备份

**对于企业用户**：



1. 强烈建议使用 IronClaw 或其他经过安全审计的企业级 AI 代理解决方案

2. 实施严格的安全策略，包括访问控制、数据分类、安全审计等

3. 考虑购买专业的安全服务，定期进行安全评估和渗透测试

4. 建立完善的事件响应机制，一旦发生安全事件能够快速响应和处理

**对于开发者**：



1. 在开发 AI 代理时，始终将安全性放在首位，采用 "安全左移" 的理念

2. 使用安全的编程语言和框架，避免已知的安全风险

3. 实现全面的测试覆盖，包括单元测试、集成测试和安全测试

4. 积极参与安全社区，及时了解最新的安全威胁和防护措施

**对于政策制定者**：



1. 建议将 AI 代理纳入网络安全监管范围，制定相应的安全标准和规范

2. 加强对开源 AI 项目的安全审查，特别是那些可能处理敏感数据的项目

3. 推动建立 AI 安全事件报告机制，及时发现和应对安全威胁

4. 支持安全技术研究，特别是在 AI 安全和隐私保护领域

展望未来，AI 代理技术的发展将不可避免地面临安全与便利之间的权衡。OpenClaw 的安全危机给整个行业敲响了警钟：**没有安全保障的 AI 代理不仅无法带来便利，反而可能成为最大的安全隐患**。IronClaw 的出现代表了一种新的发展方向 —— 通过技术创新实现安全与功能的平衡。我们相信，随着更多安全技术的应用和安全标准的完善，AI 代理将能够在保障用户安全的前提下，真正成为人们生活和工作的得力助手。

在这个 AI 快速发展的时代，每一个用户都应该成为自己数字安全的守护者。选择安全的工具，采用正确的使用方法，建立良好的安全习惯，这些都是我们在享受 AI 技术红利的同时必须承担的责任。只有这样，我们才能真正迎来一个安全、可信、高效的 AI 时代。

**参考资料&#x20;**

\[1] OpenClaw\[一款开源的AI智能体]\_百科[ https://m.baike.com/wiki/OpenClaw/7603566610000314404?baike\_source=doubao](https://m.baike.com/wiki/OpenClaw/7603566610000314404?baike_source=doubao)

\[2] OpenClaw爆火:4个月登顶GitHub，AI代理的狂欢还是安全陷阱?\_知识大胖[ http://m.toutiao.com/group/7614500481976648238/?upstream\_biz=doubao](http://m.toutiao.com/group/7614500481976648238/?upstream_biz=doubao)

\[3] 2026 年 最 火 开源 AI “ 龙虾 ” Open Claw ： 它 能 真正 帮 你 干活 ， 但 小心 它 吃掉 你 的 文件 ！ # 人工 智能 # open claw # 科技[ https://www.iesdouyin.com/share/video/7614777109718786651/?region=\&mid=7614777113987517226\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=hNKsE7ZSVJisbwr4pEqVgFPF5SV\_sJotGLSWz0EWpVk-\&share\_version=280700\&ts=1772992738\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614777109718786651/?region=\&mid=7614777113987517226\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=hNKsE7ZSVJisbwr4pEqVgFPF5SV_sJotGLSWz0EWpVk-\&share_version=280700\&ts=1772992738\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[4] OpenClaw爆火背后:千亿AI代理风口，机遇窗口只剩最后一年?\_知识大胖[ http://m.toutiao.com/group/7614148693494727214/?upstream\_biz=doubao](http://m.toutiao.com/group/7614148693494727214/?upstream_biz=doubao)

\[5] openclaw：从爆火github到重塑ai体验，能干活的数字员工究竟有多强[ https://36kr.com/p/3706443833487493](https://36kr.com/p/3706443833487493)

\[6] OpenClaw 生态正在疯长，我们拆解了 PH 上 40 多款相关产品|agent|市场口碑\_手机网易网[ http://m.163.com/dy/article/KNGM0R8B05566TJ2.html](http://m.163.com/dy/article/KNGM0R8B05566TJ2.html)

\[7] KimiClaw/MaxClaw/NullClaw/OpenFang/ZeroClaw/PicoClaw/TinyClaw/Miclaw/ArkClaw等18大小龙虾AI Agent框架技术选型全解析-CSDN博客[ https://blog.csdn.net/qq\_44866828/article/details/158776305](https://blog.csdn.net/qq_44866828/article/details/158776305)

\[8] IronClaw : 比 Open Claw 更 安全 的 AI Agent IronClaw 是 一款 基于 Rust 语言 开发 的 开源 个人 AI 助手 ， 旨在 通过 先进 的 架构 解决 传统 AI 系统 中 的 隐私 与 安全 隐患 。 该 项目 作为 Open Claw 的 高性能 替代 方案 ， 核心 优势 在于 其 安全 防护 机制 ， 通过 Was m 沙箱 隔离 运行 工具 ， 并 利用 加密 保险库 确保 LLM 无法 直接 接触 用户 的 原始 密钥 。 它 支持 在 NEAR AI 云端 的 受 信任 执行 环境 （ TEE ） 中 一键 部署 ， 也 支持 在 本地 环境 运行 。 系统 具备 持续 记忆 、 多 通道 交互 及 自动化 任务 处理 功能 ， 且 强制 执行 网络 白 名单 以 防止 数据 外泄 。 总之 ， IronClaw 致力 于 构建 一个 完全 由 用户 掌控 、 具备 透明性 且 防御 能力 极 强 的 私人 智能 体 生态 。[ https://www.iesdouyin.com/share/video/7614522763906223423/?region=\&mid=7614523084657183534\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=eqqGSeM0bxSdAbVhNtcMDfFLFVP5k85O2enyIG9zRjw-\&share\_version=280700\&ts=1772992738\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614522763906223423/?region=\&mid=7614523084657183534\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=eqqGSeM0bxSdAbVhNtcMDfFLFVP5k85O2enyIG9zRjw-\&share_version=280700\&ts=1772992738\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[9] GitHub 30日趋势榜|无噪[ https://www.wuzao.com/projects/trends/monthly/](https://www.wuzao.com/projects/trends/monthly/)

\[10] OpenClaw六大开源替代方案深度解析，从极简原型到生产级巨兽\_AI码韵匠道[ http://m.toutiao.com/group/7611863462766969344/?upstream\_biz=doubao](http://m.toutiao.com/group/7611863462766969344/?upstream_biz=doubao)

\[11] 重要提醒!工信部提示OpenClaw安全隐患\_人民日报[ http://m.toutiao.com/group/7614794707624919579/?upstream\_biz=doubao](http://m.toutiao.com/group/7614794707624919579/?upstream_biz=doubao)

\[12] \[RFC] Security Hardening Architecture & Vulnerability Report #8093[ https://github.com/openclaw/openclaw/issues/8093](https://github.com/openclaw/openclaw/issues/8093)

\[13] OpenClaw threats: assessing the risks, and how to handle shadow AI[ https://www.kaspersky.com/blog/moltbot-enterprise-risk-management/55317/](https://www.kaspersky.com/blog/moltbot-enterprise-risk-management/55317/)

\[14] explain-openclaw/08-security-analysis/ecosystem-security-threats.md at master · centminmod/explain-openclaw · GitHub[ https://github.com/centminmod/explain-openclaw/blob/master/08-security-analysis/ecosystem-security-threats.md](https://github.com/centminmod/explain-openclaw/blob/master/08-security-analysis/ecosystem-security-threats.md)

\[15] 正安研究院丨OpenClaw安全防护技术研究:筑牢AI工具安全防线\_新闻动态\_北方实验室[ http://www.northlab.cn/index/news/show/id/732/cid/10.html](http://www.northlab.cn/index/news/show/id/732/cid/10.html)

\[16] OpenClaw security vulnerabilities include data leakage and prompt injection risks[ https://www.giskard.ai/knowledge/openclaw-security-vulnerabilities-include-data-leakage-and-prompt-injection-risks](https://www.giskard.ai/knowledge/openclaw-security-vulnerabilities-include-data-leakage-and-prompt-injection-risks)

\[17] openclaw/openclaw

&#x20;v2026.3.1[ https://newreleases.io/project/github/openclaw/openclaw/release/v2026.3.1](https://newreleases.io/project/github/openclaw/openclaw/release/v2026.3.1)

\[18] openclaw/README.md at main · tao-lian/openclaw · GitHub[ https://github.com/tao-lian/openclaw/blob/main/README.md](https://github.com/tao-lian/openclaw/blob/main/README.md)

\[19] 别再用旧版了!OpenClaw 2026.2.9 更新迁移避坑指南\_openclaw更新-CSDN博客[ https://blog.csdn.net/github\_39378307/article/details/157931759](https://blog.csdn.net/github_39378307/article/details/157931759)

\[20] openclaw/openclaw

&#x20;v2026.2.24[ https://newreleases.io/project/github/openclaw/openclaw/release/v2026.2.24](https://newreleases.io/project/github/openclaw/openclaw/release/v2026.2.24)

\[21] openclaw v2026.2.21版本正式发布:新增Gemini 3.1支持、火山引擎对接、全新Discord语音系统与超200项安全和性能升级-腾讯云开发者社区-腾讯云[ https://cloud.tencent.cn/developer/article/2634000](https://cloud.tencent.cn/developer/article/2634000)

\[22] OpenClaw:重新定义个人AI助手，实现专属“贾维斯”\_opencraw-CSDN博客[ https://blog.csdn.net/weixin\_43107715/article/details/157877560](https://blog.csdn.net/weixin_43107715/article/details/157877560)

\[23] GitHub 167k 星标!OpenClaw 深度解析:本地 AI 代理的技术革命与实战部署\_openclaw github-CSDN博客[ https://blog.csdn.net/m0\_52307083/article/details/157904784](https://blog.csdn.net/m0_52307083/article/details/157904784)

\[24] OpenClaw 技术架构深度拆解:14 个子系统的源码级分析[ https://www.axtonliu.ai/newsletters/ai-2/posts/openclaw-architecture-deep-dive](https://www.axtonliu.ai/newsletters/ai-2/posts/openclaw-architecture-deep-dive)

\[25] 爆火OpenClaw到底是什么?一文吃透架构原理，AI智能体从此可控\_遥望星辰6699[ http://m.toutiao.com/group/7612927966380687908/?upstream\_biz=doubao](http://m.toutiao.com/group/7612927966380687908/?upstream_biz=doubao)

\[26] OpenClaw 技术架构深度解析 - AI全书[ https://aibook.ren/archives/openclaw-architecture-deep-dive](https://aibook.ren/archives/openclaw-architecture-deep-dive)

\[27] OpenClaw 还在硬撑?NanoClaw 一登场，差距直接拉满!\_知识有点料[ http://m.toutiao.com/group/7614820633179947574/?upstream\_biz=doubao](http://m.toutiao.com/group/7614820633179947574/?upstream_biz=doubao)

\[28] openclaw是哪个公司开发 openclaw背后团队背景介绍-人工智能-PHP中文网[ https://m.php.cn/faq/2148629.html](https://m.php.cn/faq/2148629.html)

\[29] openclaw生态爆发的核心标志是什么?[ http://m.toutiao.com/group/7614778392503829026/?upstream\_biz=doubao](http://m.toutiao.com/group/7614778392503829026/?upstream_biz=doubao)

\[30] （ 2 ） Open Claw 项目 介绍 - 完整 讲解 文案 # open claw # ai # 智能 体[ https://www.iesdouyin.com/share/video/7614152957454591055/?region=\&mid=7614152918211955510\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=hnrHl0jN\_anhTJe5hIn2y1ZPpbX\_q3Ykfg.1xgFq9.Q-\&share\_version=280700\&ts=1772992751\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614152957454591055/?region=\&mid=7614152918211955510\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=hnrHl0jN_anhTJe5hIn2y1ZPpbX_q3Ykfg.1xgFq9.Q-\&share_version=280700\&ts=1772992751\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[31] OpenClaw:从退休工程师到11万Star，一只太空龙虾的AI革命\_openclaw太空龙虾-CSDN博客[ https://blog.csdn.net/SCHOLAR\_II/article/details/157687664](https://blog.csdn.net/SCHOLAR_II/article/details/157687664)

\[32] 小shyzz的微博[ https://m.weibo.cn/detail/5273846896921639](https://m.weibo.cn/detail/5273846896921639)

\[33] IronClaw — Master Architecture Document[ https://github.com/nearai/ironclaw/blob/2f7e4777258e0956d7c88e7ce43c89a5da147699/docs/ARCHITECTURE.md](https://github.com/nearai/ironclaw/blob/2f7e4777258e0956d7c88e7ce43c89a5da147699/docs/ARCHITECTURE.md)

\[34] IronClaw Agent Runtime System — Deep Dive[ https://github.com/nearai/ironclaw/blob/2f7e4777258e0956d7c88e7ce43c89a5da147699/docs/analysis/agent.md](https://github.com/nearai/ironclaw/blob/2f7e4777258e0956d7c88e7ce43c89a5da147699/docs/analysis/agent.md)

\[35] IronClaw : 比 Open Claw 更 安全 的 AI Agent IronClaw 是 一款 基于 Rust 语言 开发 的 开源 个人 AI 助手 ， 旨在 通过 先进 的 架构 解决 传统 AI 系统 中 的 隐私 与 安全 隐患 。 该 项目 作为 Open Claw 的 高性能 替代 方案 ， 核心 优势 在于 其 安全 防护 机制 ， 通过 Was m 沙箱 隔离 运行 工具 ， 并 利用 加密 保险库 确保 LLM 无法 直接 接触 用户 的 原始 密钥 。 它 支持 在 NEAR AI 云端 的 受 信任 执行 环境 （ TEE ） 中 一键 部署 ， 也 支持 在 本地 环境 运行 。 系统 具备 持续 记忆 、 多 通道 交互 及 自动化 任务 处理 功能 ， 且 强制 执行 网络 白 名单 以 防止 数据 外泄 。 总之 ， IronClaw 致力 于 构建 一个 完全 由 用户 掌控 、 具备 透明性 且 防御 能力 极 强 的 私人 智能 体 生态 。[ https://www.iesdouyin.com/share/video/7614522763906223423/?region=\&mid=7614523084657183534\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=eqqGSeM0bxSdAbVhNtcMDfFLFVP5k85O2enyIG9zRjw-\&share\_version=280700\&ts=1772992756\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614522763906223423/?region=\&mid=7614523084657183534\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=eqqGSeM0bxSdAbVhNtcMDfFLFVP5k85O2enyIG9zRjw-\&share_version=280700\&ts=1772992756\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[36] IronClaw Documentation[ https://github.com/nearai/ironclaw/blob/7590a874e4303f62b6bc9a3146cb2c154efa8f4a/docs/README.md](https://github.com/nearai/ironclaw/blob/7590a874e4303f62b6bc9a3146cb2c154efa8f4a/docs/README.md)

\[37] 用Rust重写OpenClaw，Transformer作者下场造了安全版「龙虾」\_新浪财经[ http://m.toutiao.com/group/7614320468044071467/?upstream\_biz=doubao](http://m.toutiao.com/group/7614320468044071467/?upstream_biz=doubao)

\[38] IronClaw:OpenClaw的Rust实现，专注于隐私和安全 - 极道[ https://www.jdon.com/90413-IronClaw-OpenClaw-Rust-privacy-and-security.html](https://www.jdon.com/90413-IronClaw-OpenClaw-Rust-privacy-and-security.html)

\[39] transformer论文作者重造龙虾，rust搓出钢铁版，告别openclaw裸奔漏洞[ https://36kr.com/p/3711194778054789](https://36kr.com/p/3711194778054789)

\[40] OpenClaw六大开源替代方案深度解析，从极简原型到生产级巨兽\_AI码韵匠道[ http://m.toutiao.com/group/7611863462766969344/?upstream\_biz=doubao](http://m.toutiao.com/group/7611863462766969344/?upstream_biz=doubao)

\[41] Transformer作者出手:用Rust打造“钢铁”AI助手\_围炉笔谈123[ http://m.toutiao.com/group/7614667533622444586/?upstream\_biz=doubao](http://m.toutiao.com/group/7614667533622444586/?upstream_biz=doubao)

\[42] 打造你的 Claw 帝国:深度解析 OpenClaw 及新兴 Claw 的底层架构\_Crypto第一深情[ http://m.toutiao.com/group/7610095219270222362/?upstream\_biz=doubao](http://m.toutiao.com/group/7610095219270222362/?upstream_biz=doubao)

\[43] OpenClaw六大开源替代架构的深度对比与选型指南 - 极道[ https://www.jdon.com/90621-openclaw-alternatives-architecture-comparison.html](https://www.jdon.com/90621-openclaw-alternatives-architecture-comparison.html)

\[44] IronClaw Codebase Analysis — Safety & Sandbox Security Model[ https://github.com/nearai/ironclaw/blob/2f7e4777258e0956d7c88e7ce43c89a5da147699/docs/analysis/safety-sandbox.md](https://github.com/nearai/ironclaw/blob/2f7e4777258e0956d7c88e7ce43c89a5da147699/docs/analysis/safety-sandbox.md)

\[45] feat: Security hardening (device pairing, elevated mode, safe bins, media URL validation) #88[ https://github.com/nearai/ironclaw/issues/88](https://github.com/nearai/ironclaw/issues/88)

\[46] IronClaw[ https://github.com/veniceai/ironclaw/blob/main/README.md](https://github.com/veniceai/ironclaw/blob/main/README.md)

\[47] fix: security hardening across all layers #35[ https://github.com/nearai/ironclaw/pull/35](https://github.com/nearai/ironclaw/pull/35)

\[48] ironclaw/src/tools/wasm/mod.rs at 8b35489ce7a96b2106b1e74acb6c5475d72d2ea8 · nearai/ironclaw · GitHub[ https://github.com/nearai/ironclaw/blob/8b35489ce7a96b2106b1e74acb6c5475d72d2ea8/src/tools/wasm/mod.rs](https://github.com/nearai/ironclaw/blob/8b35489ce7a96b2106b1e74acb6c5475d72d2ea8/src/tools/wasm/mod.rs)

\[49] IronClaw[ https://www.toolify.ai/tool/ironclaw](https://www.toolify.ai/tool/ironclaw)

\[50] openclaw架构原理-单进程应用 + 插件式扩展-CSDN博客[ https://blog.csdn.net/inthat/article/details/158097236](https://blog.csdn.net/inthat/article/details/158097236)

\[51] # Moltbot/OpenClaw 架构解读与二次开发完全指南\_openclaw 二次开发-CSDN博客[ https://blog.csdn.net/u013134676/article/details/157611299](https://blog.csdn.net/u013134676/article/details/157611299)

\[52] Open Claw 里 “ 放开 ” 权限 技巧 Allow list 通 配 （ 最 常用 ） 对 指定 agent 放开 ： open claw approvals allow list add - - agent main " \* " open claw approvals allow list add - - agent ops " \* " 对 所有 agent 放开 ： open claw approvals allow list add - - agent " \* " " \* " 对 gateway 或 某个 node 放开 （ 如果 你 是 在 控制 gateway / node 的 approvals ） ： open claw approvals allow list add - - gateway - - agent " \* " " \* " open claw approvals allow list add - - node < id |name | ip > - - agent " \* " " \* " 注 ： \` open claw approvals \` 默认 操作 的 是 “ 本机 local approvals 文件 ” 。 \` - - gateway / - - node \` 会 把 修改 作用 到 对应 执行 主机 。 # open claw # opc law 教程 # linux 常用 命令 # 外贸 开发 技巧[ https://www.iesdouyin.com/share/note/7614349568444532337/?region=\&mid=7599573295705688065\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&schema\_type=37\&share\_sign=6AiNb9wrDkxT7OhbTsl.xPVM4eM\_Na0BvMWyYzAnBm4-\&share\_version=280700\&ts=1772992764\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/note/7614349568444532337/?region=\&mid=7599573295705688065\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&schema_type=37\&share_sign=6AiNb9wrDkxT7OhbTsl.xPVM4eM_Na0BvMWyYzAnBm4-\&share_version=280700\&ts=1772992764\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[53] 容器化部署OpenClaw授权View权限对Kubernetes集群进行巡检故障排查 | i4T[ https://i4t.com/25788.html](https://i4t.com/25788.html)

\[54] OpenClaw的执行层如何实现本地系统深度访问?\_热点解读[ http://m.toutiao.com/group/7612581103123137050/?upstream\_biz=doubao](http://m.toutiao.com/group/7612581103123137050/?upstream_biz=doubao)

\[55] 重要提醒!工信部提示OpenClaw安全隐患\_人民日报[ http://m.toutiao.com/group/7614794707624919579/?upstream\_biz=doubao](http://m.toutiao.com/group/7614794707624919579/?upstream_biz=doubao)

\[56] 近期 ， 工业 和 信息化 部 网络 安全 威胁 和 漏洞 信息 共享 平台 监测 发现 ， “ 龙虾 ” Open Claw 开源 AI 智能 体 部分 实例 ， 在 默认 或 不当 配置 情况 下 ， 存在 较 高 安全 风险 ， 极 易 引发 网络 攻击 、 信息 泄露 等 安全 问题 。 （ 央视 新闻 ）[ https://www.iesdouyin.com/share/video/7614848695762292018/?region=\&mid=7419372064316164097\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=z2pNvDz139.3IeHQQZFCfmRc5t4QH5wW37VQMFqL59k-\&share\_version=280700\&ts=1772992765\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614848695762292018/?region=\&mid=7419372064316164097\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=z2pNvDz139.3IeHQQZFCfmRc5t4QH5wW37VQMFqL59k-\&share_version=280700\&ts=1772992765\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[57] 能 帮 你 干活 的 AI “ 龙虾 ” 爆 火 ， 工 信 部 发 高 风险 提醒 ， 建议 相关 单位 和 用户 在 部署 和 应用 时 ， 防范 潜在 网络 安全 风险[ https://www.iesdouyin.com/share/video/7614808984637213986/?region=\&mid=7614809017982683950\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=3L85ipR6QQO2rJ71m\_LS.Y1yYmpmhzPUv1Ff9X8rqEU-\&share\_version=280700\&ts=1772992765\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614808984637213986/?region=\&mid=7614809017982683950\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=3L85ipR6QQO2rJ71m_LS.Y1yYmpmhzPUv1Ff9X8rqEU-\&share_version=280700\&ts=1772992765\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[58] 安全性 - OpenClaw[ https://docs.openclaw.ai/zh-CN/gateway/security](https://docs.openclaw.ai/zh-CN/gateway/security)

\[59] 转发 提醒 ！ AI 养 “ 龙虾 ” 警惕 安全 风险[ https://www.iesdouyin.com/share/video/7614797970709531919/?region=\&mid=7614798005720976154\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=m8eXETFcZGa12rBff12KyxlgpgCzhX6YO3c3B0oCHDk-\&share\_version=280700\&ts=1772992765\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614797970709531919/?region=\&mid=7614798005720976154\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=m8eXETFcZGa12rBff12KyxlgpgCzhX6YO3c3B0oCHDk-\&share_version=280700\&ts=1772992765\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[60] 警惕!你的“AI龙虾”可能成黑客后门OpenClaw默认配置藏高危风险\_AI我AI你[ http://m.toutiao.com/group/7614801961942073871/?upstream\_biz=doubao](http://m.toutiao.com/group/7614801961942073871/?upstream_biz=doubao)

\[61] OpenClaw安全深度剖析:爆红AI代理平台背后的安全隐患\_xiaofeng[ http://m.toutiao.com/group/7614815574866002486/?upstream\_biz=doubao](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)

\[62] OpenClaw 安全崩盘:史上最快 AI Agent 灾难潮\_openclaw exposure watchboard-CSDN博客[ https://blog.csdn.net/weixin\_53707930/article/details/158619820](https://blog.csdn.net/weixin_53707930/article/details/158619820)

\[63] 龙虾 事件 引爆 AI 安全 ！ 网络 安全 板块 迎 双重 驱动[ https://www.iesdouyin.com/share/video/7614772693766345061/?region=\&mid=7614772691158551306\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=LBLylbE9WPPMRupSpO4riYWBHx5xuTErMk.M5s8s3MU-\&share\_version=280700\&ts=1772992764\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614772693766345061/?region=\&mid=7614772691158551306\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=LBLylbE9WPPMRupSpO4riYWBHx5xuTErMk.M5s8s3MU-\&share_version=280700\&ts=1772992764\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[64] "小龙虾”背后暗藏极大危险:目前所有部署OpenClaw的电脑都可能成为"肉鸡"!|openclaw|密钥|小龙虾|电脑|肉鸡|黑客\_手机网易网[ http://m.163.com/news/article/KNEM26CV0556I98Q.html](http://m.163.com/news/article/KNEM26CV0556I98Q.html)

\[65] 养虾(OpenClaw)很火，但是也很不安全\_机情烩[ http://m.toutiao.com/group/7614785019151647273/?upstream\_biz=doubao](http://m.toutiao.com/group/7614785019151647273/?upstream_biz=doubao)

\[66] 正安研究院丨OpenClaw安全防护技术研究:筑牢AI工具安全防线\_新闻动态\_北方实验室[ http://www.northlab.cn/index/news/show/id/732/cid/10.html](http://www.northlab.cn/index/news/show/id/732/cid/10.html)

\[67] IronClaw[ https://github.com/veniceai/ironclaw/blob/main/README.md](https://github.com/veniceai/ironclaw/blob/main/README.md)

\[68] IronClaw — Master Architecture Document[ https://github.com/nearai/ironclaw/blob/7590a874e4303f62b6bc9a3146cb2c154efa8f4a/docs/ARCHITECTURE.md](https://github.com/nearai/ironclaw/blob/7590a874e4303f62b6bc9a3146cb2c154efa8f4a/docs/ARCHITECTURE.md)

\[69] feat: Security hardening (device pairing, elevated mode, safe bins, media URL validation) #88[ https://github.com/nearai/ironclaw/issues/88](https://github.com/nearai/ironclaw/issues/88)

\[70] IronClaw:开源AI代理平台，安全、可靠的OpenClaw替代品 | AI铺子[ https://www.aipuzi.cn/ai-tools/ironclaw.html](https://www.aipuzi.cn/ai-tools/ironclaw.html)

\[71] feat: multi-tenant auth with per-user identity and workspace isolation[ https://github.com/nearai/ironclaw/pull/341](https://github.com/nearai/ironclaw/pull/341)

\[72] Authenticate a Request[ https://developer.ironcladapp.com/reference/authenticate-a-request](https://developer.ironcladapp.com/reference/authenticate-a-request)

\[73] 2026年阿里云零门槛1分钟部署OpenClaw+7个OpenClaw生态顶级开源项目实战指南-阿里云开发者社区[ https://developer.aliyun.com/article/1713191](https://developer.aliyun.com/article/1713191)

\[74] IronClaw Codebase Analysis — Secrets Management & Keychain[ https://github.com/nearai/ironclaw/blob/2f7e4777258e0956d7c88e7ce43c89a5da147699/docs/analysis/secrets-keychain.md](https://github.com/nearai/ironclaw/blob/2f7e4777258e0956d7c88e7ce43c89a5da147699/docs/analysis/secrets-keychain.md)

\[75] Transformer论文作者重造龙虾，Rust搓出钢铁版，告别OpenClaw裸奔漏洞\_36氪[ http://m.toutiao.com/group/7614068855752720934/?upstream\_biz=doubao](http://m.toutiao.com/group/7614068855752720934/?upstream_biz=doubao)

\[76] IronClaw - OpenI[ https://openi.cn/316313.html](https://openi.cn/316313.html)

\[77] Secure Your Family Information in Digital Vaults with IronClad Family[ https://www.ironcladfamily.com/digital-family-vaults-and-estate-planning](https://www.ironcladfamily.com/digital-family-vaults-and-estate-planning)

\[78] IronClaw vs OpenClaw:AI Agent终极对决，选对能避90%的坑\_知识大胖[ http://m.toutiao.com/group/7610299611265139206/?upstream\_biz=doubao](http://m.toutiao.com/group/7610299611265139206/?upstream_biz=doubao)

\[79] Give Your Family Instant Access to What Matters Most[ https://www.ironcladfamily.com/digital-vault](https://www.ironcladfamily.com/digital-vault)

\[80] Transformer作者出手:用Rust打造“钢铁”AI助手\_围炉笔谈123[ http://m.toutiao.com/group/7614667533622444586/?upstream\_biz=doubao](http://m.toutiao.com/group/7614667533622444586/?upstream_biz=doubao)

\[81] IronClaw : 比 Open Claw 更 安全 的 AI Agent IronClaw 是 一款 基于 Rust 语言 开发 的 开源 个人 AI 助手 ， 旨在 通过 先进 的 架构 解决 传统 AI 系统 中 的 隐私 与 安全 隐患 。 该 项目 作为 Open Claw 的 高性能 替代 方案 ， 核心 优势 在于 其 安全 防护 机制 ， 通过 Was m 沙箱 隔离 运行 工具 ， 并 利用 加密 保险库 确保 LLM 无法 直接 接触 用户 的 原始 密钥 。 它 支持 在 NEAR AI 云端 的 受 信任 执行 环境 （ TEE ） 中 一键 部署 ， 也 支持 在 本地 环境 运行 。 系统 具备 持续 记忆 、 多 通道 交互 及 自动化 任务 处理 功能 ， 且 强制 执行 网络 白 名单 以 防止 数据 外泄 。 总之 ， IronClaw 致力 于 构建 一个 完全 由 用户 掌控 、 具备 透明性 且 防御 能力 极 强 的 私人 智能 体 生态 。[ https://www.iesdouyin.com/share/video/7614522763906223423/?region=\&mid=7614523084657183534\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=eqqGSeM0bxSdAbVhNtcMDfFLFVP5k85O2enyIG9zRjw-\&share\_version=280700\&ts=1772992772\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614522763906223423/?region=\&mid=7614523084657183534\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=eqqGSeM0bxSdAbVhNtcMDfFLFVP5k85O2enyIG9zRjw-\&share_version=280700\&ts=1772992772\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[82] Transformer作者重造龙虾，Rust搓出钢铁版，告别OpenClaw裸奔\_量子位[ http://m.toutiao.com/group/7614077222592201259/?upstream\_biz=doubao](http://m.toutiao.com/group/7614077222592201259/?upstream_biz=doubao)

\[83] 南方日报的微博[ https://m.weibo.cn/detail/5274192033351567](https://m.weibo.cn/detail/5274192033351567)

\[84] 【 AI “ 养 龙虾 ” 走红 ， 官方 提示 ： 极 易 引发 网络 攻击 、 信息 泄露 等 安全 问题 】 # AI 养 龙虾 （ 新华社 ）[ https://www.iesdouyin.com/share/video/7614809369074535695/?region=\&mid=7535368170631579667\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=ERLbBn1WsKQ9NVPxHt5ee\_dpJg0v2sqwKAPPgb5f3\_k-\&share\_version=280700\&ts=1772992772\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614809369074535695/?region=\&mid=7535368170631579667\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=ERLbBn1WsKQ9NVPxHt5ee_dpJg0v2sqwKAPPgb5f3_k-\&share_version=280700\&ts=1772992772\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[85] 龙虾 事件 引爆 AI 安全 ！ 网络 安全 板块 迎 双重 驱动[ https://www.iesdouyin.com/share/video/7614772693766345061/?region=\&mid=7614772691158551306\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=LBLylbE9WPPMRupSpO4riYWBHx5xuTErMk.M5s8s3MU-\&share\_version=280700\&ts=1772992781\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614772693766345061/?region=\&mid=7614772691158551306\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=LBLylbE9WPPMRupSpO4riYWBHx5xuTErMk.M5s8s3MU-\&share_version=280700\&ts=1772992781\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[86] 爆火背后:OpenClaw 开源AI智能体应用攻击面与安全风险系统剖析 – 绿盟科技技术博客[ https://blog.nsfocus.net/%E7%88%86%E7%81%AB%E8%83%8C%E5%90%8E%EF%BC%9Aopenclaw-%E5%BC%80%E6%BA%90ai%E6%99%BA%E8%83%BD%E4%BD%93%E5%BA%94%E7%94%A8%E6%94%BB%E5%87%BB%E9%9D%A2%E4%B8%8E%E5%AE%89%E5%85%A8%E9%A3%8E%E9%99%A9%E7%B3%BB/](https://blog.nsfocus.net/%E7%88%86%E7%81%AB%E8%83%8C%E5%90%8E%EF%BC%9Aopenclaw-%E5%BC%80%E6%BA%90ai%E6%99%BA%E8%83%BD%E4%BD%93%E5%BA%94%E7%94%A8%E6%94%BB%E5%87%BB%E9%9D%A2%E4%B8%8E%E5%AE%89%E5%85%A8%E9%A3%8E%E9%99%A9%E7%B3%BB/)

\[87] 22万OpenClaw实例公网暴露:安全危机与防范之道-易源AI资讯 | 万维易源[ https://www.showapi.com/news/article/69a7f3e94ddd79ab67051dca](https://www.showapi.com/news/article/69a7f3e94ddd79ab67051dca)

\[88] AI 红队 OpenClaw:安全审计员指南 | 登链社区 | 区块链技术社区[ https://main.learnblockchain.cn/article/23699](https://main.learnblockchain.cn/article/23699)

\[89] 安全性 - OpenClaw[ https://docs.openclaw.ai/zh-CN/gateway/security](https://docs.openclaw.ai/zh-CN/gateway/security)

\[90] OpenClaw 安全配置最佳实践[ https://openclawai.net/zh/docs/security-best-practices](https://openclawai.net/zh/docs/security-best-practices)

\[91] 安全视角下的 OpenClaw:Shell 级权限的风险防控与沙箱模式最佳实践\_openclaw shell-CSDN博客[ https://blog.csdn.net/weixin\_43107715/article/details/158505764](https://blog.csdn.net/weixin_43107715/article/details/158505764)

\[92] Open claw 3 . 7 更新 解读 。 # open claw 升级 前 做好 备份 2026 年 3 月 8 日 凌晨 ， Open Claw 发布 了 v 2026 . 3 . 7 。 这 是 一个 从 架构 设计 到 安全 基线 全面 升级 的 版本 ， 改动 量 远超 此前 任何 一 次 迭代 。 整个 change log 涵盖 新 功能 、 破坏性 变更 、 安全 修复 、 模型 更新 和 容器 重构 本文 内容 ， 按 重要 程度 排列 ， 每个 模块 给出 足够 的 背景 和 判断 依据 ， 帮 你 在 升级 前 建立 基本 了解[ https://www.iesdouyin.com/share/note/7614868542777244746/?region=\&mid=7599216671047420722\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&schema\_type=37\&share\_sign=5dtHnWxItJhdPZok4H2hAybpJ\_Zssm0yJzbljMoZqQo-\&share\_version=280700\&ts=1772992781\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/note/7614868542777244746/?region=\&mid=7599216671047420722\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&schema_type=37\&share_sign=5dtHnWxItJhdPZok4H2hAybpJ_Zssm0yJzbljMoZqQo-\&share_version=280700\&ts=1772992781\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[93] OpenClaw 安全加固完全指南:从裸奔到生产级防护 - 网硕互联帮助中心[ https://www.wsisp.com/helps/78790.html](https://www.wsisp.com/helps/78790.html)

\[94] OpenClaw 安全生存指南:5分钟防黑客安全加固傻瓜教程\_芃爸玩儿编程[ http://m.toutiao.com/group/7614879357114286619/?upstream\_biz=doubao](http://m.toutiao.com/group/7614879357114286619/?upstream_biz=doubao)

\[95] feat: Security hardening (device pairing, elevated mode, safe bins, media URL validation) #88[ https://github.com/nearai/ironclaw/issues/88](https://github.com/nearai/ironclaw/issues/88)

\[96] OpenClaw六大开源替代方案深度解析，从极简原型到生产级巨兽\_AI码韵匠道[ http://m.toutiao.com/group/7611863462766969344/?upstream\_biz=doubao](http://m.toutiao.com/group/7611863462766969344/?upstream_biz=doubao)

\[97] 用Rust重写OpenClaw，Transformer作者下场造了安全版「龙虾」|调用|代码|rust|显式标识|openclaw\_网易订阅[ https://www.163.com/dy/article/KNDIQMUA05568W0A.html](https://www.163.com/dy/article/KNDIQMUA05568W0A.html)

\[98] Transformer论文作者重造龙虾，Rust搓出钢铁版，告别OpenClaw裸奔漏洞\_36氪[ http://m.toutiao.com/group/7614068855752720934/?upstream\_biz=doubao](http://m.toutiao.com/group/7614068855752720934/?upstream_biz=doubao)

\[99] IronClaw:OpenClaw的Rust实现，专注于隐私和安全 - 极道[ https://www.jdon.com/90413-IronClaw-OpenClaw-Rust-privacy-and-security.html](https://www.jdon.com/90413-IronClaw-OpenClaw-Rust-privacy-and-security.html)

\[100] 养虾(OpenClaw)很火，但是也很不安全\_机情烩[ http://m.toutiao.com/group/7614785019151647273/?upstream\_biz=doubao](http://m.toutiao.com/group/7614785019151647273/?upstream_biz=doubao)

\[101] OpenClaw 安全崩盘:史上最快 AI Agent 灾难潮\_openclaw exposure watchboard-CSDN博客[ https://blog.csdn.net/weixin\_53707930/article/details/158619820](https://blog.csdn.net/weixin_53707930/article/details/158619820)

\[102] Open Claw 、 Molt book 全球 爆 火 ！ 专家 ： 需要 尽快 加强 监管 👀 # 拒绝 废话 # 科普[ https://www.iesdouyin.com/share/video/7614520047331986762/?region=\&mid=7614519946063907626\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=TrPBr7jQEN2JpOEPIlMrooXFBjYsUS\_iNp9XG\_sSrVk-\&share\_version=280700\&ts=1772992789\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614520047331986762/?region=\&mid=7614519946063907626\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=TrPBr7jQEN2JpOEPIlMrooXFBjYsUS_iNp9XG_sSrVk-\&share_version=280700\&ts=1772992789\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[103] OpenClaw安全指南:理性发展AI-CSDN博客[ https://blog.csdn.net/qq\_37865996/article/details/158542942](https://blog.csdn.net/qq_37865996/article/details/158542942)

\[104] 一键破防!OpenClaw 远程代码执行漏洞的深度剖析与防御体系\_cve-2026-25253-CSDN博客[ https://blog.csdn.net/weixin\_42376192/article/details/157684596](https://blog.csdn.net/weixin_42376192/article/details/157684596)

\[105] 正安研究院丨OpenClaw安全防护技术研究:筑牢AI工具安全防线\_技术研究\_北方实验室[ http://www.northlab.cn/index/news/show/id/733/cid/13.html](http://www.northlab.cn/index/news/show/id/733/cid/13.html)

\[106] 重要提醒!工信部提示OpenClaw安全隐患\_人民日报[ http://m.toutiao.com/group/7614794707624919579/?upstream\_biz=doubao](http://m.toutiao.com/group/7614794707624919579/?upstream_biz=doubao)

\[107] OpenClaw是馅饼还是陷阱\_景帝轩[ http://m.toutiao.com/group/7614678217911304704/?upstream\_biz=doubao](http://m.toutiao.com/group/7614678217911304704/?upstream_biz=doubao)

\[108] 当″龙虾″爬进你的电脑:工信部高危预警背后的AI安全困局|OpenClaw|风险|监管|权限|邮件\_新浪新闻[ https://k.sina.com.cn/article\_972897\_000ed86100101bb7g.html](https://k.sina.com.cn/article_972897_000ed86100101bb7g.html)

\[109] Open Claw 龙虾 Ai 数据 安全 Open Claw 龙虾 Ai # 数据 安全 # 信息 安全 # Open Claw[ https://www.iesdouyin.com/share/video/7614825882726004148/?region=\&mid=7276798078488905729\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=jZkwP.AkrcoIbxwASRyNAPzMabf\_2uR53ZxsmhwSzLY-\&share\_version=280700\&ts=1772992789\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614825882726004148/?region=\&mid=7276798078488905729\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=jZkwP.AkrcoIbxwASRyNAPzMabf_2uR53ZxsmhwSzLY-\&share_version=280700\&ts=1772992789\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[110] “AI龙虾”火到全国两会!它到底什么来头?\_搜狐网[ https://m.sohu.com/a/993968265\_121955537/](https://m.sohu.com/a/993968265_121955537/)

\[111] 重要提醒!工信部提示OpenClaw安全隐患[ http://m.cnhubei.com/content/2026-03/08/content\_19858110.html](http://m.cnhubei.com/content/2026-03/08/content_19858110.html)

\[112] “养龙虾” 突然爆火，官方提示来了\_中国日报双语新闻[ http://m.toutiao.com/group/7614829665298956850/?upstream\_biz=doubao](http://m.toutiao.com/group/7614829665298956850/?upstream_biz=doubao)

\[113] Don’t get pinched: the OpenClaw vulnerabilities[ https://www.kaspersky.com/blog/openclaw-vulnerabilities-exposed/55263/](https://www.kaspersky.com/blog/openclaw-vulnerabilities-exposed/55263/)

\[114] 警惕 这 只 危险 的 龙虾 。 # 龙虾 open claw # 科技 # AI # 人工 智能 # open claw[ https://www.iesdouyin.com/share/video/7614510767999817140/?region=\&mid=7614510743429794570\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=rTa.9x3mHeS1LaSd19Egug7tO9qWUHaNLbFmBHWpbVo-\&share\_version=280700\&ts=1772992789\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614510767999817140/?region=\&mid=7614510743429794570\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=rTa.9x3mHeS1LaSd19Egug7tO9qWUHaNLbFmBHWpbVo-\&share_version=280700\&ts=1772992789\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[115] OpenClaw安全深度剖析:爆红AI代理平台背后的安全隐患\_xiaofeng[ http://m.toutiao.com/group/7614815574866002486/?upstream\_biz=doubao](http://m.toutiao.com/group/7614815574866002486/?upstream_biz=doubao)

\[116] 我们用 AI Observe Stack 观测 OpenClaw，发现 AI Agent 背后的这些隐患\_SelectDB[ http://m.toutiao.com/group/7614064894589010472/?upstream\_biz=doubao](http://m.toutiao.com/group/7614064894589010472/?upstream_biz=doubao)

\[117] AI Agent生态新威胁:Skills武器化与完整攻击链解析 - 安全内参 | 决策者的网络安全知识库[ https://www.secrss.com/articles/87726?app=1](https://www.secrss.com/articles/87726?app=1)

\[118] Transformer论文作者重造龙虾，Rust搓出钢铁版，告别OpenClaw裸奔漏洞\_36氪[ http://m.toutiao.com/group/7614068855752720934/?upstream\_biz=doubao](http://m.toutiao.com/group/7614068855752720934/?upstream_biz=doubao)

\[119] IronClaw : 比 Open Claw 更 安全 的 AI Agent IronClaw 是 一款 基于 Rust 语言 开发 的 开源 个人 AI 助手 ， 旨在 通过 先进 的 架构 解决 传统 AI 系统 中 的 隐私 与 安全 隐患 。 该 项目 作为 Open Claw 的 高性能 替代 方案 ， 核心 优势 在于 其 安全 防护 机制 ， 通过 Was m 沙箱 隔离 运行 工具 ， 并 利用 加密 保险库 确保 LLM 无法 直接 接触 用户 的 原始 密钥 。 它 支持 在 NEAR AI 云端 的 受 信任 执行 环境 （ TEE ） 中 一键 部署 ， 也 支持 在 本地 环境 运行 。 系统 具备 持续 记忆 、 多 通道 交互 及 自动化 任务 处理 功能 ， 且 强制 执行 网络 白 名单 以 防止 数据 外泄 。 总之 ， IronClaw 致力 于 构建 一个 完全 由 用户 掌控 、 具备 透明性 且 防御 能力 极 强 的 私人 智能 体 生态 。[ https://www.iesdouyin.com/share/video/7614522763906223423/?region=\&mid=7614523084657183534\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=eqqGSeM0bxSdAbVhNtcMDfFLFVP5k85O2enyIG9zRjw-\&share\_version=280700\&ts=1772992797\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614522763906223423/?region=\&mid=7614523084657183534\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=eqqGSeM0bxSdAbVhNtcMDfFLFVP5k85O2enyIG9zRjw-\&share_version=280700\&ts=1772992797\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[120] 除了OpenClaw大龙虾，还有6只“小龙虾“:什么是Nanobot:Py开发者，什么是NanoClaw:多智能体， 什么是IronClaw:安全，什么是ZeroClaw:树莓派，什么是PicoCla-CSDN博客[ https://blog.csdn.net/qq\_44866828/article/details/158661946](https://blog.csdn.net/qq_44866828/article/details/158661946)

\[121] IronClaw vs OpenClaw:AI Agent终极对决，选对能避90%的坑\_知识大胖[ http://m.toutiao.com/group/7610299611265139206/?upstream\_biz=doubao](http://m.toutiao.com/group/7610299611265139206/?upstream_biz=doubao)

\[122] 2026 AI Agent 新趋势:OpenClaw 衍生项目 Nanobot/IronClaw 等深度测评-CSDN博客[ https://blog.csdn.net/kingsley99/article/details/158569800](https://blog.csdn.net/kingsley99/article/details/158569800)

\[123] Transformer作者出手:用Rust打造“钢铁”AI助手\_围炉笔谈123[ http://m.toutiao.com/group/7614667533622444586/?upstream\_biz=doubao](http://m.toutiao.com/group/7614667533622444586/?upstream_biz=doubao)

\[124] NEAR AI Launches IronClaw, A Secure Runtime for Always-On AI Agents[ https://aithority.com/machine-learning/near-ai-launches-ironclaw-a-secure-runtime-for-always-on-ai-agents/](https://aithority.com/machine-learning/near-ai-launches-ironclaw-a-secure-runtime-for-always-on-ai-agents/)

\[125] IronClaw - OpenI[ https://openi.cn/316313.html](https://openi.cn/316313.html)

\[126] OpenClaw的5个替代方案 - 汇智网[ http://www.hubwiz.com/blog/top5-openclaw-alternatives/](http://www.hubwiz.com/blog/top5-openclaw-alternatives/)

\[127] NEAR Protocol launches IronClaw AI assistant and decentralized GPU marketplace for data security[ https://www.raptorgroup.com/news/near-protocol-launches-ironclaw-ai-assistant-and-decentralized-gpu-marketplace-for-data-security/](https://www.raptorgroup.com/news/near-protocol-launches-ironclaw-ai-assistant-and-decentralized-gpu-marketplace-for-data-security/)

\[128] 爆冷!OpenClaw凉了?5款平替封神，轻量又安全，程序员必藏\_知识大胖[ http://m.toutiao.com/group/7612975295456477732/?upstream\_biz=doubao](http://m.toutiao.com/group/7612975295456477732/?upstream_biz=doubao)

\[129] Audit V3 — Post-Fix Codebase Quality Review[ https://github.com/nearai/ironclaw/blob/21df2fd6f0ae3303086da6473b3058ac8bb23af1/.claude/docs/audit-v3.md](https://github.com/nearai/ironclaw/blob/21df2fd6f0ae3303086da6473b3058ac8bb23af1/.claude/docs/audit-v3.md)

\[130] IronClaw— NearAI团队开源的本地安全AI助手-人工智能-PHP中文网[ https://m.php.cn/faq/2147029.html](https://m.php.cn/faq/2147029.html)

\[131] IronClaw Codebase Quality Audit: Agentic Development Smells[ https://github.com/nearai/ironclaw/blob/21df2fd6f0ae3303086da6473b3058ac8bb23af1/.claude/docs/codebase-quality-audit.md](https://github.com/nearai/ironclaw/blob/21df2fd6f0ae3303086da6473b3058ac8bb23af1/.claude/docs/codebase-quality-audit.md)

> （注：文档部分内容可能由 AI 生成）