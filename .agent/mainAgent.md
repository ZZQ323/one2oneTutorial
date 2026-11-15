# 主 Agent 工作手册 (mainAgent.md)

**版本**：1.3  
**最后更新**：2026-11-14  
**适用项目**：PetCare (Android-Assignment)

---

## 🎯 核心定位

主 Agent 是**架构师 + 协调者**，不是执行者。

**职责边界**：
- ✅ 需求分析与任务拆分
- ✅ 迭代文档编写与更新
- ✅ 子 Agent 任务分发与调度
- ✅ 子 Agent 结果验证
- ✅ 进度追踪与报告
- ❌ 不直接执行大量代码修改（除非是简单的单行修复）
- ❌ 不反复读取大文件
- ❌ 不替代子 Agent 做重活

---

## 📋 项目结构

```
Android-Assignment/
├── .agent/                    # Agent 工作手册
├── GroupWork/
│   ├── AndriodMVPv2/          # Android 前端项目
│   │   ├── app/               # 主应用模块
│   │   ├── core/              # 核心模块（network, common, database）
│   │   ├── feature/           # 功能模块（login, profile, care, collab, ask）
│   │   └── docs/iteration/    # 迭代文档
│   └── petcare-backend/       # Spring Boot 后端项目
│       ├── main/              # 启动入口
│       ├── module-common/     # 公共模块
│       ├── module-base/       # 用户/家庭基础域
│       ├── module-care/       # 照护记录域
│       ├── module-profile/    # 宠物档案域
│       ├── module-rag/        # AI/RAG 域
│       └── docs/iteration/    # 迭代文档
```

---

## 📋 工作流程

### 阶段 1：需求分析
```
用户输入 → 理解意图 → 评估影响范围 → 确定阶段划分
```

### 阶段 2：任务拆分

**拆分原则**：
1. **单一职责**：每个子任务只修改 1-2 个文件
2. **可验证**：每个子任务有明确的验收标准
3. **可接力**：子任务之间通过迭代文档传递上下文
4. **原子性**：每个子任务可以独立完成和验证

### 阶段 3：子 Agent 分发

**分发策略**：
- 独立任务 → 并行分发（最多 3 个/轮）
- 依赖任务 → 串行分发
- 前后端并行 → 同时分发前端和后端任务

### 阶段 4：结果验证

**验证方法**：
```bash
# 后端编译验证
cd GroupWork/petcare-backend && ./gradlew build

# Android 编译验证（需要 Android SDK）
cd GroupWork/AndriodMVPv2 && ./gradlew assembleDebug
```

---

## 🚨 禁止行为

1. **禁止直接执行大量代码修改** → 分发给子 Agent
2. **禁止反复读取大文件** → 只读取目标区域
3. **禁止忽略迭代文档** → 所有上下文写入迭代文档
4. **禁止跳过验证** → 必须编译验证 + 文档检查

---

## 📚 迭代教训记录

### 迭代 1.2 教训（2026-11-14）

#### 🔴 高频卡点 1：API 路径单复数不匹配
- **现象**：前端用 `reminder`（单数），后端用 `reminders`（复数），导致 404
- **解决**：统一使用复数形式（RESTful 规范）
- **规则**：建立 API 路径对照表，前后端同步维护

#### 🔴 高频卡点 2：XML 布局文件残留孤立属性
- **现象**：edit 工具修改 XML 后留下孤立属性，编译失败
- **解决**：XML 编辑后立即验证格式
- **规则**：使用结构化编辑，保持 XML 格式化

#### 🟡 中频卡点 3：Edit 工具 old_string 匹配多次
- **现象**：追加内容时 old_string 在文件中出现多次
- **解决**：使用更具体的 old_string，包含独特上下文
- **规则**：追加内容使用文件末尾特征

---

## 🔄 持续改进

**每次迭代后更新**：
- 本文件的经验教训
- 任务拆分模板
- 子 Agent 分发 Prompt 模板

---

**最后更新**：2026-11-14  
**版本**：1.3

---

## 📚 Geo 模块开发教训（2026-11-14）

### 🔴 高频卡点 1：高德 SDK 依赖管理

**问题**：
1. 重复类冲突（3dmap + location SDK）
2. 版本号不存在（猜测版本号）
3. Maven 仓库未配置（高德 SDK 不在标准仓库）

**规则**：
> 高德 SDK 正确依赖组合：
> - `com.amap.api:3dmap` — 地图 + 定位（已内置）
> - `com.amap.api:search` — POI 搜索
> - ❌ 不要单独引入 `location` SDK
>
> 必须在 `settings.gradle` 中添加高德 Maven 仓库：
> - `https://developer.amap.com/maven/`
> - `https://maven.aliyun.com/repository/public/`
>
> 升级 SDK 前必须查阅 Maven Central 确认版本存在，不要猜测版本号。

---

### 🔴 高频卡点 2：高德 SDK API 使用

**问题**：
1. POI 类包路径错误（3 轮修正）
2. 方法名错误（getErrorDetail → getErrorInfo）
3. 异常处理缺失（PoiSearch 构造函数抛异常）

**规则**：
> 高德 SDK 包路径规范：
> - 地图：`com.amap.api.maps.*`
> - 定位：`com.amap.api.location.*`（内置在 3dmap 中）
> - POI搜索：`com.amap.api.services.poisearch.*`
> - 模型：`com.amap.api.services.model.*`（部分类在 core 中）
> - 核心：`com.amap.api.services.core.*`（LatLonPoint、PoiItem 等）
>
> POI 搜索必须包裹 try-catch：
> ```java
> try {
>     poiSearch = new PoiSearch(context, query);
>     poiSearch.setBound(...);
>     poiSearch.setOnPoiSearchListener(listener);
>     poiSearch.searchPOIAsyn();
> } catch (AMapException e) {
>     Toast.makeText(context, "搜索失败: " + e.getMessage(), Toast.LENGTH_SHORT).show();
> }
> ```

---

### 🟡 中频卡点 3：UI 布局问题

**问题**：分类按钮显示不全

**规则**：
> 按钮设计规范：
> - 高度至少 36dp
> - 字体至少 13sp
> - 设置 minWidth 确保宽度一致
> - 添加 padding（10dp-12dp）让文字不贴边
> - HorizontalScrollView 添加 `fillViewport="true"`

---

### ✅ 成功经验

1. **分批迭代策略**：Backend Agent、Android Agent、Config Agent 并行开发
2. **错误日志持续更新**：每个错误立即记录到 error.md
3. **多 Agent 并行**：独立任务并行，依赖任务串行

---

**最后更新**：2026-11-14  
**版本**：1.4
