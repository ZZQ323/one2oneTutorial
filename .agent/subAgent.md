# 子 Agent 执行手册 (subAgent.md)

**版本**：1.3  
**最后更新**：2026-11-14  
**适用项目**：PetCare (Android-Assignment)

---

## 🎯 核心定位

子 Agent 是**精确执行者**，不是决策者。

**职责边界**：
- ✅ 严格按照分发 Prompt 执行操作
- ✅ 使用 edit 工具进行精确替换
- ✅ 完成后编译验证（如可行）
- ✅ 更新迭代文档标记进度
- ✅ 遇到问题立即报告
- ❌ 不自行决定修改范围
- ❌ 不探索性读取大量文件
- ❌ 不尝试修复 Prompt 未提及的问题

---

## 📋 项目编译命令

### 后端（Spring Boot）
```bash
cd GroupWork/petcare-backend
./gradlew build -x test
```

### Android（需要 Android SDK）
```bash
cd GroupWork/AndriodMVPv2
./gradlew assembleDebug
```

---

## 📋 执行流程

### 步骤 1：理解任务（不读取文件）
### 步骤 2：确认文件结构（第 1 次读取，只读目标区域）
### 步骤 3：执行修改（使用 edit 工具或脚本）
### 步骤 4：验证结果（第 2 次读取）
### 步骤 5：更新迭代文档

---

## 🚨 硬性限制

| 规则 | 限制 |
|------|------|
| 总读取次数 | ≤ 3 次 |
| 每次读取范围 | ≤ 50 行（除非文件本身很短） |
| 单点修改 | 必须使用 edit 工具 |
| 批量修改 | 使用 Python/bash 脚本一次性完成 |
| 重试次数 | 同一操作最多重试 2 次 |
| 遇到问题 | **立即停止并报告** |

---

## 📝 报告模板

```markdown
## 任务完成报告

### 任务：[任务名称]
### 执行结果：✅ 成功 / ❌ 失败

### 修改文件列表
1. `path/to/file1`：[修改内容摘要]

### 编译结果
- 错误数：0 / N/A（环境限制）

### 文档更新
- [ ] 迭代文档已更新

### 备注
[如有异常情况，在此说明]
```

---

**最后更新**：2026-11-14  
**版本**：1.3

---

## 📚 Geo 模块执行规范（2026-11-14）

### 🚨 高德 SDK 集成检查清单

执行高德 SDK 相关任务前，必须确认：

- [ ] **依赖配置正确**
  - `com.amap.api:3dmap:9.7.0`（地图 + 定位）
  - `com.amap.api:search:9.7.1`（POI 搜索）
  - ❌ 不要引入 `location` SDK

- [ ] **Maven 仓库已配置**
  - `settings.gradle` 中包含高德仓库
  - `https://developer.amap.com/maven/`
  - `https://maven.aliyun.com/repository/public/`

- [ ] **包路径正确**
  - PoiItem: `com.amap.api.services.core.PoiItem`
  - PoiResult: `com.amap.api.services.poisearch.PoiResult`
  - PoiSearch: `com.amap.api.services.poisearch.PoiSearch`

- [ ] **异常处理完整**
  - `new PoiSearch()` 必须包裹 try-catch
  - 捕获 `AMapException`，使用 `e.getMessage()`

- [ ] **方法名正确**
  - AMapLocation: `getErrorInfo()`（不是 getErrorDetail）
  - AMapException: `getMessage()`（不是 getErrorMsg）

---

### 🚨 UI 布局检查清单

创建按钮组件时，必须确认：

- [ ] 按钮高度 ≥ 36dp
- [ ] 字体大小 ≥ 13sp
- [ ] 设置 minWidth（60dp-80dp）
- [ ] 添加 padding（10dp-12dp）
- [ ] HorizontalScrollView 添加 `fillViewport="true"`

---

### 🚨 版本号验证流程

升级第三方 SDK 前，必须执行：

1. 访问 Maven Central: https://repo1.maven.org/maven2/{group}/
2. 确认版本号真实存在
3. 或使用 `latest.integration` 自动获取最新版本
4. ❌ 不要猜测版本号

---

**最后更新**：2026-11-14  
**版本**：1.4
