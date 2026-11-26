# EE5415 机考模拟题 · ReadTrack 阅读打卡

> **本文件只有需求与验收标准，没有任何实现代码。**
> 卡壳时按文末「卡壳时怎么问」的模板来问我，我只给定位思路，不给答案。
> 参考资料：`Android前端类比手册.md`、`答疑_状态_数据库_MVI_文件路径.md`、你自己的 `BMI-MVI` 作业、`Crouse/` 与 `labs/` 下的课件。

---

## 0. 考试规则复述（做题时按这个来，别自己放宽）

| 项 | 规定 |
|---|---|
| 时长 | 3 小时（真实考试 09:00–12:10，含 10 分钟环境准备） |
| 开卷范围 | 课堂幻灯片 + **你自己在 Canvas 交过的作业**；可上网查 API 文档 |
| 禁止 | 任何 AI 代码生成（包括 Google 搜索结果里的 AI 回答）、U 盘、远程协助、开考后用手机 |
| 环境 | 必须用实验室电脑，**从零新建一个空工程**，不许导入现成项目 |
| 判分现实 | 「能跑起来一个基本 App」就不会挂；先保 A 段，再堆 B/C |

**本模拟题的等价约束**：从 Android Studio「New Project → Empty Views Activity」开始，包名 `com.example.readtrack`，语言 **Java**，Minimum SDK 与实验一致。全程不许复制 `D:\ProjectStore\AndroidDemo` 或 `BMI-MVI` 的代码文件，只许自己敲。

---

## 1. 你要做的 App

**ReadTrack（阅读打卡）**：记录自己在读的书、读到第几页、打几分，能列出书架、看统计图、导出备份。

### 1.1 数据模型（一张表就够）

| 字段 | 含义 | 类型 |
|---|---|---|
| `id` | 自增主键 | INTEGER |
| `title` | 书名 | TEXT，必填 |
| `totalPages` | 总页数 | INTEGER，必填，> 0 |
| `readPages` | 已读页数 | INTEGER，必填，≥ 0 |
| `rating` | 评分 | 1–5（RatingBar 的整数星数即可） |
| `category` | 分类 | 四选一：`TECH` / `LITERATURE` / `HISTORY` / `OTHER` |
| `finished` | 是否已读完 | 布尔（0/1） |
| `note` | 备注 | TEXT，可空 |
| `createdAt` | 记录时间 | INTEGER，用系统当前时间，**不需要日期选择控件** |

**派生量（不入库，用时算）**：`progress = readPages * 100 / totalPages`（整数百分比）。

### 1.2 页面结构（最少三个 Activity，C 段可改成 Fragment）

| 页面 | 职责 |
|---|---|
| `MainActivity` | 录入表单 + 校验 + 入口按钮（去书架、去建议页、同步、导出） |
| `BookListActivity` | RecyclerView 书架列表 + 统计文字 + 自定义条形图（C 段） |
| `AdviceActivity` | 显示针对某一本书的阅读建议，看完 `finish()` 回来 |

---

## 2. 场景总览（16 个场景，A/B/C 三段）

| 场景 | 名称 | 主要考点 | 课件来源 | 段 |
|---|---|---|---|---|
| A1 | 工程与资源规范 | 工程结构、strings.xml、Manifest、两套资源引用 | T01 / T02 / L03 | A |
| A2 | 录入表单 | 6 类输入控件、ScrollView、两种布局容器、dp/sp、weight | L03 / T03 | A |
| A3 | 校验与三种反馈 | 空值/越界校验、Toast、Snackbar、AlertDialog | T02 / T03 | A |
| A4 | 旋转不丢数据 | 生命周期、配置变更、Bundle、onSaveInstanceState | L02 / L08 | A |
| A5 | 建议页与页面跳转 | 显式 Intent、putExtra、getIntent、finish() | L02 / T02 | A |
| B1 | SQLite 落库 | SQLiteOpenHelper、建表、占位符增删改查、Cursor | L10 | B |
| B2 | 书架列表 | RecyclerView、Adapter、ViewHolder、item 布局、onResume 重查 | L12 / L02 | B |
| B3 | 列表交互 | item 点击、长按上下文菜单、删除二次确认、局部刷新 | T04 / L12 | B |
| B4 | 条件查询与统计 | selection/selectionArgs、ORDER BY、COUNT、AVG、LIMIT | L10 | B |
| B5 | 菜单 + 本地化 + 横屏 | OptionsMenu、ContextMenu、values-zh、layout-land | T04 / T03 | B |
| C1 | 偏好记忆 | SharedPreferences、apply、重启后仍在 | L10 | C |
| C2 | 假同步与线程 | 子线程、回主线程三种方式、按钮禁用、onDestroy 清理 | L09 | C |
| C3 | 自定义条形图 | 继承 View、onDraw、Canvas、Paint、外部注入数据 | L12 / L03 | C |
| C4 | Fragment 化 | Fragment 生命周期、FragmentTransaction、onAttach 接口通信、返回栈 | L08 | C |
| C5 | 导出与读回 | openFileOutput/openFileInput、内部存储固定路径、字符流 | L10 | C |
| C6 | 隐式 Intent 与权限 | ACTION_SEND / ACTION_VIEW、INTERNET 权限、主线程不能联网 | T09 / L02 | C |

**建议节奏**：A 段 50 分钟 → B 段 70 分钟 → C 段 50 分钟，留 10 分钟建工程、10 分钟自查。
**允许停在任意一段**：A 段做完就是「能跑的 App」，B 段做完已经是一份合格答卷，C 段是拉开差距的部分。

---

# A 段 · 骨架（必须能跑）

## A1 工程与资源规范

**情景**：教授给的评分细则里有一条是「界面文字不许硬编码」。你新建完工程，第一件事不是拖控件。

**必须做到**
1. 新建工程，包名 `com.example.readtrack`，语言 Java，Empty Views Activity 模板。
2. `res/values/strings.xml` 里定义 **不少于 12 条** 字符串，覆盖：App 名、每个输入项的标签、四个分类名、所有按钮文字、所有提示语。
3. 所有布局文件里的可见文字**一律**用 `@string/xxx`，Java 里一律用 `R.string.xxx`；布局与 Java 中都不许出现中文或英文句子字面量。
4. `res/values/dimens.xml` 里定义至少 3 个尺寸（如统一间距、标题字号），并在布局中引用。
5. 文字大小用 `sp`，间距与宽高用 `dp`，不许出现 `px`。

**验收**：见清单 A1-1 ~ A1-4。

**坑（一句话）**：`layout_width="0dp"` 只有在 ConstraintLayout 里配合约束才有意义，在 LinearLayout 里要用 `layout_weight`。

---

## A2 录入表单

**情景**：用户打开 App，第一屏就是「添加一本书」。屏幕小，控件多，必须能滚动。

**必须做到**
1. 最外层用 `ScrollView` 包住整个表单（竖屏下 6 个输入项 + 3 个按钮必须能滚到）。
2. 表单里必须出现这 6 类输入控件，各至少一个：
   - `EditText`（`inputType="text"`）——书名
   - `EditText`（`inputType="number"`）——总页数、已读页数（两个）
   - `EditText`（`inputType="textMultiLine"`，`minLines` ≥ 2）——备注
   - `RatingBar`——评分（`numStars="5"`，`stepSize` 设为 1）
   - `RadioGroup` + 4 个 `RadioButton`——分类，且默认选中 `TECH`
   - `CheckBox`——是否已读完
3. 布局必须**同时**用到两种容器：外层 `LinearLayout`（垂直），内部至少一块用 `ConstraintLayout` **或** `TableLayout`（把「总页数 / 已读页数」并排放一行，标签在上、输入框在下）。
4. 「总页数 / 已读页数」那一行用 `layout_weight` 平分宽度，或用 ConstraintLayout 的 `0dp` + 约束实现等宽。
5. 三个按钮：`保存这本书`、`我的书架`、`阅读建议`。
6. 每个控件都要有 `android:id`，Java 里用 `findViewById` 拿到全部 6 类控件的引用。
7. 给书名输入框加 `hint`；给两个页数输入框加 `imeOptions` 或 `nextFocusDown` 之类的输入辅助（任选一种即可）。

**验收**：见清单 A2-1 ~ A2-5。

**坑（一句话）**：`RatingBar.getRating()` 返回 float，取整数星数要自己转；`RadioGroup.getCheckedRadioButtonId()` 在没选中时返回 -1。

---

## A3 录入校验与三种反馈

**情景**：用户什么都不填就点「保存」，App 不能崩，也不能静默失败。教授特别强调过「空值会 force close」这个反面教材。

**必须做到**：点「保存这本书」时按顺序校验，任何一条不通过就**停止后续校验**并给出反馈：

| # | 条件 | 反馈方式（必须用这一种） |
|---|---|---|
| 1 | 书名为空或全是空格 | `Toast`，短 |
| 2 | 总页数为空、不是数字、或 ≤ 0 | `AlertDialog`，标题「输入有误」，正文说明原因，一个「知道了」按钮 |
| 3 | 已读页数为空或不是数字 | 同上 `AlertDialog` |
| 4 | 已读页数 > 总页数 | `AlertDialog`，并且**额外**自动把「是否已读完」勾上（让用户看到 App 有反应） |
| 5 | 评分为 0 星 | `Toast`，提示至少给一星 |
| 6 | 全部通过 | `Snackbar`，内容包含书名与算出来的百分比进度，带一个「撤销」按钮，点了就清空整个表单 |

**还必须做到**
- 数字解析必须能容忍非数字输入而不崩溃（用 try/catch 或先判空再解析，任选）。
- 校验逻辑写成一个独立方法，返回一个「错误信息字符串或 null」，不要全塞在 `onClick` 里。
- 表单清空也要写成独立方法（`Snackbar` 的撤销按钮和后面的重置功能都要复用它）。

**验收**：见清单 A3-1 ~ A3-4。

**坑（一句话）**：`AlertDialog` 必须 `.show()` 才会出现，只 `create()` 不 `show()` 是机考最常见的丢分点。

---

## A4 旋转屏幕不丢已填内容

**情景**：用户填了一半书名和页数，把手机横过来（AVD 里按 `Ctrl+F11`），页面重建了，填的东西全没了。这在真机上是投诉级别的 bug。

**必须做到**
1. **不许**用 `android:configChanges` 绕过，也**不许**锁死屏幕方向。必须走正规的保存/恢复流程。
2. 旋转后以下内容必须原样恢复：书名、总页数、已读页数、备注、评分、选中的分类、是否已读完。
3. 另外还要恢复一个「非输入类」状态：页面上有一个 `TextView` 显示「本次会话已保存 N 本」（N 是内存里的计数，不入库），旋转后 N 不能归零。
4. 恢复逻辑要能区分「首次启动」和「旋转回来」两种情况（首次启动不许因为 Bundle 为 null 而崩）。

**验收**：见清单 A4-1 ~ A4-3。

**坑（一句话）**：`onSaveInstanceState` 里只放得下基本类型和 String，别想着把整个 List 塞进去；`onCreate` 的 Bundle 参数在首次启动时是 `null`。

---

## A5 阅读建议页与页面跳转

**情景**：用户点「阅读建议」，跳到第二个页面，那个页面根据当前表单内容给出一句建议；看完点「返回」或「完成」回到主页。

**必须做到**
1. 新建 `AdviceActivity`，并在 `AndroidManifest.xml` 里正确注册。
2. 从 `MainActivity` 用**显式 Intent** 跳过去，至少传 4 个值：书名（String）、进度百分比（int）、分类（String）、是否已读完（boolean）。
3. `AdviceActivity` 用 `getIntent()` 取出这 4 个值，拼出一段建议文字显示在 `TextView` 上。建议文字必须随分类不同而不同（四个分类四种文案），并且「已读完」和「没读完」两种情况的文案也不同 —— 也就是至少 8 种组合里能看出区别。
4. 建议文案写在 `strings.xml` 里，用**带占位符**的字符串资源（`%1$s` / `%1$d` 这种），不许在 Java 里用 `+` 拼中文句子。
5. `AdviceActivity` 上有一个「完成」按钮，点了之后关闭自己回到主页（不是启动新页面）。
6. 从建议页返回主页后，主页顶部要显示「上一次查看建议的书名是 XXX」。（回传方式不限：`Intent` 回传、静态变量、SharedPreferences 都行，但要在代码里用一行注释说明你为什么选这种。）
7. 如果用户**没填书名**就点「阅读建议」，不许跳转，用 Toast 提示，并且当前页面不能被关掉。

**验收**：见清单 A5-1 ~ A5-5。

**坑（一句话）**：`AdviceActivity` 忘记在 Manifest 注册 = 一点就崩（`ActivityNotFoundException`），这是机考第一号事故。

---

# B 段 · 数据与列表

## B1 SQLite 落库

**情景**：现在保存的书一重启就没了。要落盘，而且**不许用 Room**（机考时间不够，注解处理器一报错就全崩）。

**必须做到**
1. 写一个继承 `SQLiteOpenHelper` 的类，库名 `readtrack.db`，表名 `books`，版本 1。
2. `onCreate` 里建表，字段见 §1.1，`id` 自增主键，`title` 加唯一约束或普通索引（任选，但要说明理由）。
3. `onUpgrade` 必须实现（哪怕是「删表重建」也要写出来，并加注释说明真实项目不能这么干）。
4. 提供这些方法：新增一条、按 id 删除、按 id 更新已读页数与是否读完、查全部、查总数。
5. **所有带条件的 SQL 必须用 `?` 占位符 + 参数数组**，不许用字符串拼接把用户输入直接接进 SQL。
6. 非查询语句用 `execSQL` 或 `insert`/`update`/`delete` 都可以；查询用 `rawQuery` 或 `query` 都可以，**你自己选一种并在类顶部用注释写明选择理由**。
7. 所有 `Cursor` 必须在 `finally` 里关闭。

**验收**：见清单 B1-1 ~ B1-5。

**坑（一句话）**：`selectionArgs` 只能是 `String[]`，数字要 `String.valueOf(...)` 转一下；`query()` 的七个参数版本没有 LIMIT。

---

## B2 书架列表（RecyclerView）

**情景**：点「我的书架」进入 `BookListActivity`，用列表显示所有记录。**不许用 ListView，不许用一堆 TextView 拼**。

**必须做到**
1. `BookListActivity` 布局里放一个 `RecyclerView`；列表空的时候显示一个「还没有记录」的 `TextView`，有记录时把它隐藏。
2. 写 `Adapter` + `ViewHolder`，item 布局单独一个 xml 文件（文件名以 `item_` 开头）。
3. 每个 item 至少显示：书名、分类（中文/英文走字符串资源）、一个 `ProgressBar`（`style` 用水平进度条，`max=100`，值 = progress）、评分星数文字（如 `4/5`）。
4. `Adapter` 必须实现「外部塞一个新 List 进来就刷新」的方法（方法名不限），并且**在 `BookListActivity.onResume()` 里重新查库 + 调用它**，这样从主页保存完再回到列表页能看到新数据。
5. `setLayoutManager` 用 `LinearLayoutManager`。
6. item 里 ProgressBar 的颜色或进度值必须随 progress 变化（例如 < 30% 一种颜色、≥ 80% 另一种颜色，用代码设置或 `progressTint` 均可）。

**验收**：见清单 B2-1 ~ B2-6。

**坑（一句话）**：`onBindViewHolder` 里不要再 `findViewById` 整个 item，控件引用应该在 `ViewHolder` 构造里拿一次。

---

## B3 列表交互

**情景**：用户想在列表上直接操作，而不是回主页重填。

**必须做到**
1. **单击 item**：弹一个 `AlertDialog`，列出这本书的完整信息（含备注），并给两个按钮：「标记为已读完」和「关闭」。点前者要真的写库并刷新列表。
2. **长按 item**：弹出**上下文菜单**（`ContextMenu`，不是 AlertDialog），菜单项：`更新进度`、`删除`、`取消`。
3. `更新进度`：弹一个带输入框的 `AlertDialog`（用 `setView` 塞一个 `EditText`），输入新的已读页数，校验（非数字、超过总页数）后写库刷新。
4. `删除`：先弹二次确认 `AlertDialog`，确认后才真删，删完用 `Snackbar` 提示，并提供「撤销」——撤销要能把刚删的那条**原样写回**（所以删除前你得把整条记录留在内存里）。
5. 上下文菜单必须走标准的三件套注册流程（注册、创建、响应选择），并且菜单文字来自 `res/menu/` 下的 xml 文件。
6. 删除到列表为空时，B2 的「还没有记录」提示要重新出现。

**验收**：见清单 B3-1 ~ B3-5。

**坑（一句话）**：AGP 8+ 开了 `android.nonFinalResIds`，`switch (item.getItemId())` **编译不过**，菜单分支要用 if/else。

---

## B4 条件查询与统计

**情景**：列表页顶部要有一块统计区，主页也要能用得上。这些都必须真的从数据库查出来，不许在 Java 里遍历 List 自己算。

**必须做到**：在 `SQLiteOpenHelper` 子类里实现下面 5 个查询，每个都要真的执行 SQL：

| # | 需求 | SQL 要点 |
|---|---|---|
| 1 | 记录总数 | `COUNT(*)` |
| 2 | 平均评分（保留一位小数） | `AVG(rating)` |
| 3 | 每个分类各有多少本 | `GROUP BY category` |
| 4 | 还没读完的书，按进度**从高到低**排，最多取 5 条 | 条件 + `ORDER BY` + `LIMIT`（注意：进度是派生量，你得想清楚是存下来还是用表达式排序） |
| 5 | 书名包含某个关键词的记录（模糊查询，关键词由调用方传入） | `LIKE` + 占位符，通配符位置要说清楚 |

**还必须做到**
- 第 3 条的结果要显示在 `BookListActivity` 顶部（四个分类各一行「分类名：N 本」）。
- 第 4 条的结果做成主页的一个「继续阅读」区域：显示最多 5 条书名 + 进度，点任意一条跳到 `AdviceActivity` 并带上那本书的信息。
- 第 5 条接到列表页的一个搜索入口上：菜单里加一项「搜索书名」，弹输入框，输入后列表只显示匹配项；再点一次「显示全部」可还原。
- 单值查询（总数、平均分）与多行查询要分别用对应的 Cursor 处理方式，别用同一套模板硬套。

**验收**：见清单 B4-1 ~ B4-5。

**坑（一句话）**：`LIMIT` 在 `query()` 的七参数重载里**没有**，要用九参数版本、`rawQuery`，或把 LIMIT 写进 orderBy 字符串。

---

## B5 菜单 + 本地化 + 横屏

**情景**：教授会拿手机横过来看一眼，再把系统语言切成中文看一眼。这两处崩了或乱了，印象分直接扣。

**必须做到**
1. `MainActivity` 的 **OptionsMenu**（`res/menu/` 下 xml）至少 4 项：`我的书架`、`同步到云端`（C2 用，A/B 段先放着并弹 Toast「未实现」）、`导出备份`（C5 用，同上）、`关于`。其中至少 1 项放在溢出菜单里（不写 `showAsAction="always"`）。
2. `关于` 弹 `AlertDialog`，内容包含：App 名、版本号、一句话说明、以及**你这次机考练习花了多少分钟**（写死在 strings.xml 里即可）。
3. `BookListActivity` 也要有自己的 OptionsMenu，至少含 `搜索书名`、`显示全部`、`清空全部数据`（清空要二次确认）。
4. **本地化**：新建 `res/values-zh/strings.xml`，把**全部**字符串翻译成中文。要求切换系统语言后整个 App 无一处残留英文（`TECH`/`LITERATURE` 这类内部分类代号除外，但界面上显示的必须是中文分类名）。
5. **横屏**：新建 `res/layout-land/` 下的主布局，要求横屏时表单**左右分栏**（左边输入项、右边按钮与建议入口），而不是简单地把竖屏布局拉长。`AdviceActivity` 可以共用一份布局，但不能出现文字被截断或按钮点不到的情况。
6. 带占位符的字符串（`%1$s` 那种）在 `values-zh` 里也要保持占位符数量与顺序一致，必要时加 `formatted="false`。

**验收**：见清单 B5-1 ~ B5-5。

**坑（一句话）**：`values-zh` 里少一条字符串不会报错，会静默回落到英文 —— 必须逐条核对数量一致。

---

# C 段 · 加分项

## C1 偏好记忆（SharedPreferences）

**情景**：用户每次打开 App 都要重新填昵称、重新选排序方式，很烦。

**必须做到**
1. 主页顶部有一个「读者昵称」输入框；昵称保存到 SharedPreferences，下次冷启动自动填回。
2. 列表页的排序方式（`按进度` / `按评分` / `按添加时间`，用菜单切换）要记住，下次进列表页沿用上次的选择。
3. 一个「自动标记读完」开关（`CheckBox` 即可）：开启时，只要已读页数 ≥ 总页数就自动把 `finished` 置真。开关状态要持久化。
4. 三项偏好写在**同一个** preferences 文件里，用 `apply()` 而不是 `commit()`，并加一行注释说明两者区别。
5. 菜单里加一项「清除偏好」，点了之后三项回到默认值。

**验收**：见清单 C1-1 ~ C1-3。

**坑（一句话）**：SharedPreferences 是明文 XML，落在 `/data/data/<包名>/shared_prefs/`，不要往里存密码或 token。

---

## C2 假同步与线程

**情景**：「同步到云端」这个按钮其实没有服务器。你要模拟一次 2 秒的网络请求，且**不许卡住界面**。

**必须做到**
1. 点菜单里的 `同步到云端`，开始一个耗时 2 秒的后台任务（`ExecutorService` 或 `new Thread` 均可，二选一并注释说明为什么）。
2. 任务进行期间：该菜单项不可再点（或按钮禁用）、界面出现一个转圈的 `ProgressBar`、状态 `TextView` 显示「同步中…」。
3. 任务内容：统计数据库里的记录总数，生成一句「已同步 N 条记录到云端」。
4. 任务结束后**必须回到主线程**更新 UI：隐藏转圈、恢复可点、状态文字改成结果、并弹一个 `Snackbar`。
5. **反面验证（要真的做一次并在注释里记录现象）**：先故意在子线程里直接改 `TextView`，跑一次，把 Logcat 里的异常类名和那句英文原文抄进代码注释，然后改回正确写法。
6. `onDestroy()` 里清理：关掉线程池、移除 Handler 里所有未执行的任务，并注释说明不清理会怎样。
7. 同步进行中如果用户旋转屏幕，不许崩溃（想清楚这意味着什么，用一句话注释写出你的处理方式）。

**验收**：见清单 C2-1 ~ C2-4。

**坑（一句话）**：`runOnUiThread` / `view.post` / `new Handler(Looper.getMainLooper()).post` 三者等价，选一个即可，但**必须**用；子线程碰 View 会抛 `CalledFromWrongThreadException`。

---

## C3 自定义条形图（画图，你没掌握的那块）

**情景**：列表页顶部要有一张「四个分类各有多少本」的条形图。**不许用图片，不许用第三方图表库，不许用 ProgressBar 冒充**，必须自己画。

**必须做到**
1. 新建一个类继承 `View`，实现三个构造函数（`(Context)`、`(Context, AttributeSet)`、`(Context, AttributeSet, int)`），并在 XML 里用**全限定类名**当标签使用它。
2. 重写 `onDraw(Canvas)`，在里面用 `Paint` 画：
   - 四条竖直或水平的条形，长度正比于该分类的书本数；
   - 每条条形旁边用 `drawText` 标出「分类名 + 数量」；
   - 一条基线（`drawLine`）；
   - 四个分类用四种不同颜色（`Paint.setColor`，颜色值定义在 `res/values/colors.xml`）。
3. `Paint` 对象必须在构造函数里创建，**不许在 `onDraw` 里 new**（注释说明为什么：onDraw 会被频繁调用）。
4. 提供一个公开方法（如 `setData`）让 Activity 把「四个分类的数量」传进来，传完要触发重绘。
5. 数据必须来自 B4 第 3 条那个 `GROUP BY` 查询，不许写死。
6. 尺寸为 0 或数据全为 0 时不许崩溃，要画出一条基线 + 一句「暂无数据」。
7. 横屏时图形不能画出屏幕外：`onDraw` 里必须用 `getWidth()` / `getHeight()` 计算，不许用写死的像素值；并说明 `dp` 转 `px` 在自定义 View 里怎么处理。
8. 数据变化（新增/删除一本书）后回到列表页，图必须跟着变。

**验收**：见清单 C3-1 ~ C3-5。

**坑（一句话）**：`drawText` 的 y 坐标是**文字基线**不是左上角，直接传 0 会画到 View 外面去；改完数据忘了 `invalidate()` 图就不会刷新。

---

## C4 Fragment 化

**情景**：现在 `BookListActivity` 又要放列表又要放统计图，太挤。把它拆成两个 Fragment，用按钮切换。

**必须做到**
1. 两个 Fragment：`BookListFragment`（RecyclerView 列表）与 `StatsFragment`（统计文字 + C3 的条形图）。
2. 用**动态**方式挂载（`FragmentTransaction` 的 `replace`），不用 XML 里的静态 `<fragment>` 标签；容器 id 在 Activity 布局里。
3. `BookListActivity` 底部两个按钮切换两个 Fragment；切换时**至少一个方向要加入返回栈**，使系统返回键能回到上一个 Fragment 而不是直接退出 Activity。
4. Fragment 与 Activity 之间用**接口回调**通信：列表 Fragment 里点某本书时，通过 `onAttach` 拿到的接口把书名回传给 Activity，由 Activity 决定跳到 `AdviceActivity`。
5. Fragment 里取数据库/上下文不许直接持有 Activity 引用，说明你用了什么（`requireContext()` / 接口 / 构造传参）以及为什么不能在 Fragment 构造函数里传参数。
6. 在两个 Fragment 里各自重写至少 4 个生命周期回调，每个回调里打一条 `Log`（TAG 用类名），然后在验收时把旋转屏幕一次得到的日志顺序**抄进一个注释块**，并对比 Activity 与 Fragment 生命周期的嵌套关系。
7. 旋转屏幕后，当前显示的是哪个 Fragment 要保持不变。

**验收**：见清单 C4-1 ~ C4-5。

**坑（一句话）**：Fragment 必须有无参构造函数（系统在重建时靠反射调用它），要传数据只能用 `setArguments(Bundle)`。

---

## C5 导出备份与读回

**情景**：用户想把记录导出成一个文本文件备份，还想在 App 里看到备份文件的信息。

**必须做到**
1. 菜单 `导出备份`：把**全部**记录写入内部存储的一个文本文件，文件名固定为 `backup.txt`，每条记录一行，字段之间用 `|` 分隔，第一行写导出时间与总条数。
2. 用 `openFileOutput` 写入，模式选择 `MODE_PRIVATE` 或 `MODE_APPEND` 之一，并注释说明两者的区别以及你为什么选它。
3. 写完之后弹 `AlertDialog`，内容必须包含这个文件的**完整绝对路径**、文件大小（字节）、行数。路径要用代码取，不许写死字符串。
4. 再提供一个「读取备份」入口：用 `openFileInput` 读回文件，解析出行数与第一行内容，显示在界面上；文件不存在时给友好提示而不是崩溃。
5. 字符编码显式使用 UTF-8（写入与读取都要），注释说明不指定编码在中文书名上会出什么问题。
6. 用一段注释回答：**为什么不能把文件写到 `/sdcard/ReadTrack/backup.txt`**，以及如果非要让用户自己选保存位置，正规做法是什么（写出 Intent 的 action 常量名即可）。
7. 说明你在 Android Studio 的哪个面板里能亲眼看到这个文件，路径是什么。

**验收**：见清单 C5-1 ~ C5-4。

**坑（一句话）**：`openFileOutput(String name, int mode)` 的参数里根本没有目录 —— 这就是路径被固定死的证据。

---

## C6 隐式 Intent 与权限

**情景**：用户想把某本书分享给朋友，或者去网上搜这本书。

**必须做到**
1. 列表 item 的上下文菜单里加一项 `分享这本书`：用**隐式 Intent**（`ACTION_SEND`）把书名 + 进度 + 评分作为纯文本分享出去，要能弹出系统的应用选择器。
2. 详情对话框里加一个按钮 `上网搜这本书`：用 `ACTION_VIEW` 打开一个搜索引擎 URL（URL 里要带上书名，注意空格与中文的编码问题，说明你怎么处理的）。
3. 设备上没有任何 App 能处理这两个 Intent 时不许崩溃 —— 写出你的防护方式并注释说明。
4. 在 `AndroidManifest.xml` 里声明 `INTERNET` 权限，并用注释回答两个问题：**为什么只声明权限还不够、还必须开子线程**；以及**为什么 Android 不允许 App 直连远端数据库、中间要放一层 Web Service**。
5. 写一段注释对比 `HttpURLConnection` / `OkHttp` / `Retrofit` 三者的定位差异（一句话各一条），并说明本 App 为什么一个都没用到。

**验收**：见清单 C6-1 ~ C6-3。

**坑（一句话）**：隐式 Intent 找不到接收方会抛 `ActivityNotFoundException`，要么 try/catch，要么先用 PackageManager 查有没有能响应的 Activity。

---

# 3. 验收清单

> 判据分三级：**必需**（A/B 段，不过就是不及格）、**加分**（C 段）、**警告**（不计入 FAIL，但机考会丢印象分）。
> 全部判据都由 `AndroidExam/check_acceptance.py` 自动扫描你的工程源码得出，脚本只做静态检查，**不代替你在模拟器上跑一遍**。

| 编号 | 级别 | 判据（脚本扫描 `app/src/main`） |
|---|---|---|
| A1-1 | 必需 | `res/values/strings.xml` 存在且 `<string name=` 不少于 12 条 |
| A1-2 | 必需 | `res/values/dimens.xml` 存在且含 `<dimen` |
| A1-3 | 必需 | 布局文件中 `@string/` 出现不少于 8 次；`.java` 中出现 `R.string.` |
| A1-4 | 警告 | 布局文件中出现 `px` 单位（`"12px"` 这类）→ 应改为 dp/sp |
| A2-1 | 必需 | 布局中出现 `ScrollView`、`RatingBar`、`RadioGroup`、`CheckBox`，且 `EditText` 不少于 4 个 |
| A2-2 | 必需 | 布局中出现 `RadioButton` 不少于 4 个 |
| A2-3 | 必需 | 布局中同时出现 `LinearLayout` 与（`ConstraintLayout` 或 `TableLayout`） |
| A2-4 | 必需 | 布局中出现 `layout_weight` 或 `0dp` |
| A2-5 | 必需 | `.java` 中 `findViewById` 不少于 8 次；出现 `textMultiLine` 于布局中 |
| A3-1 | 必需 | `.java` 中同时出现 `Toast.makeText`、`Snackbar.make`、`AlertDialog` |
| A3-2 | 必需 | `.java` 中出现 `try` 与 `catch`，且出现 `isEmpty` 或 `TextUtils.isEmpty` |
| A3-3 | 必需 | `.java` 中出现 `.show()`（AlertDialog 真的显示了） |
| A3-4 | 警告 | `.java` 中出现 `AlertDialog.Builder` 但没有 `.show()` 的类 → 检查是否漏显示 |
| A4-1 | 必需 | `.java` 中出现 `onSaveInstanceState` 且方法体里有 `putString` 或 `putInt` 或 `putBoolean` |
| A4-2 | 必需 | `.java` 中出现 `savedInstanceState != null` 或等价的判空 |
| A4-3 | 必需 | `AndroidManifest.xml` 中**没有** `android:configChanges`（不许绕过重建） |
| A5-1 | 必需 | `AndroidManifest.xml` 中 `<activity` 不少于 3 个 |
| A5-2 | 必需 | `.java` 中出现 `putExtra` 与 `getIntent()`，以及 `getStringExtra`/`getIntExtra`/`getBooleanExtra` 中至少两种 |
| A5-3 | 必需 | `.java` 中出现 `finish()` |
| A5-4 | 必需 | `strings.xml` 中出现带占位符的字符串（`%1$s` 或 `%1$d`） |
| A5-5 | 警告 | `.java` 中出现 `startActivity(new android.content.Intent` → 说明你把自己的类和 `android.content.Intent` 重名了，机考别这么起名 |
| B1-1 | 必需 | `.java` 中出现 `extends SQLiteOpenHelper`、`onCreate(SQLiteDatabase`、`onUpgrade` |
| B1-2 | 必需 | `.java` 中出现 `CREATE TABLE` |
| B1-3 | 必需 | `.java` 中出现 `ContentValues` 或 `execSQL` 或 `db.insert(` |
| B1-4 | 必需 | `.java` 中出现 `= ?` 形式的占位符与 `new String[]` |
| B1-5 | 必需 | `.java` 中出现 `Cursor`、`moveToNext`、`getColumnIndex`（或 `getColumnIndexOrThrow`）、`close()` |
| B1-6 | 警告 | `.java` 中出现 `"SELECT` 与 `+` 同行拼接变量 → SQL 注入风险 |
| B2-1 | 必需 | `.java` 中出现 `extends RecyclerView.Adapter`、`onCreateViewHolder`、`onBindViewHolder`、`getItemCount` |
| B2-2 | 必需 | `.java` 中出现 `RecyclerView.ViewHolder` |
| B2-3 | 必需 | 布局中出现 `androidx.recyclerview.widget.RecyclerView`；存在文件名以 `item_` 开头的布局 |
| B2-4 | 必需 | `.java` 中出现 `setLayoutManager` 与 `LinearLayoutManager` |
| B2-5 | 必需 | `.java` 中出现 `onResume()`，且同一文件里出现 `notifyDataSetChanged` 或 `setData` 或 `submitList` |
| B2-6 | 必需 | 布局中出现 `ProgressBar` |
| B3-1 | 必需 | `.java` 中出现 `registerForContextMenu`、`onCreateContextMenu`、`onContextItemSelected` |
| B3-2 | 必需 | `res/menu/` 下存在至少 2 个 xml 文件 |
| B3-3 | 必需 | `.java` 中出现 `db.delete(` 或 `DELETE FROM` |
| B3-4 | 必需 | `.java` 中出现 `setView(`（带输入框的对话框） |
| B3-5 | 必需 | `.java` 中**没有** `switch (item.getItemId())` 或 `switch(item.getItemId())`（AGP 8+ 编译不过） |
| B4-1 | 必需 | `.java` 中出现 `COUNT(*)` |
| B4-2 | 必需 | `.java` 中出现 `AVG(` |
| B4-3 | 必需 | `.java` 中出现 `GROUP BY` |
| B4-4 | 必需 | `.java` 中出现 `ORDER BY` 与 `LIMIT`（或九参数 `query(` 重载） |
| B4-5 | 必需 | `.java` 中出现 `LIKE` 与 `rawQuery(` 或 `db.query(` |
| B5-1 | 必需 | `.java` 中出现 `onCreateOptionsMenu`、`onOptionsItemSelected`、`MenuInflater` 或 `getMenuInflater()` |
| B5-2 | 必需 | `res/values-zh/strings.xml` 存在，且其 `<string name=` 条数与 `res/values/strings.xml` **完全相等** |
| B5-3 | 必需 | `res/layout-land/` 目录存在且含至少 1 个 xml |
| B5-4 | 必需 | `res/menu/` 中至少一个 xml 含 `showAsAction`，且不是全部都为 `always` |
| B5-5 | 警告 | `values/strings.xml` 中含多个 `%` 占位符的字符串没有 `formatted="false"` |
| C1-1 | 加分 | `.java` 中出现 `getSharedPreferences` 与 `.apply()` |
| C1-2 | 加分 | `.java` 中出现 `getBoolean(` 与 `getString(`（读回偏好） |
| C1-3 | 加分 | `.java` 中出现 `edit()` 不少于 3 次 |
| C2-1 | 加分 | `.java` 中出现 `Executors.new` 或 `new Thread(` |
| C2-2 | 加分 | `.java` 中出现 `runOnUiThread` 或 `Looper.getMainLooper()` 或 `.post(` |
| C2-3 | 加分 | `.java` 中出现 `onDestroy()`，且其中出现 `shutdown` 或 `removeCallbacksAndMessages` |
| C2-4 | 加分 | `.java` 注释中出现 `CalledFromWrongThreadException` 或 `Only the original thread` |
| C3-1 | 加分 | `.java` 中出现 `extends View`、`onDraw(Canvas`、`new Paint` |
| C3-2 | 加分 | `.java` 中出现 `drawText(`、`drawLine(`，以及 `drawRect(` 或 `drawRoundRect(` |
| C3-3 | 加分 | 自定义 View 的类名以**全限定名**形式出现在某个布局 xml 中 |
| C3-4 | 加分 | `.java` 中出现 `invalidate()`、`getWidth()`、`getHeight()` |
| C3-5 | 加分 | 自定义 View 类中出现三个构造函数（`public 类名(Context` 至少 2 处重载） |
| C4-1 | 加分 | `.java` 中出现 `extends Fragment`（至少 2 个类） |
| C4-2 | 加分 | `.java` 中出现 `getSupportFragmentManager()`、`beginTransaction()`、`replace(` |
| C4-3 | 加分 | `.java` 中出现 `addToBackStack(` |
| C4-4 | 加分 | `.java` 中出现 `onAttach(` 与 `setArguments(` 或 `getArguments()` |
| C4-5 | 加分 | `.java` 中出现 `onCreateView(` 与 `onViewCreated(` |
| C5-1 | 加分 | `.java` 中出现 `openFileOutput(` 与 `MODE_PRIVATE` 或 `MODE_APPEND` |
| C5-2 | 加分 | `.java` 中出现 `openFileInput(` 或 `getFilesDir()` |
| C5-3 | 加分 | `.java` 中出现 `UTF-8` 或 `StandardCharsets.UTF_8` |
| C5-4 | 加分 | `.java` 注释中出现 `ACTION_CREATE_DOCUMENT` |
| C6-1 | 加分 | `.java` 中出现 `Intent.ACTION_SEND` 或 `Intent.ACTION_VIEW` |
| C6-2 | 加分 | `AndroidManifest.xml` 中出现 `android.permission.INTERNET` |
| C6-3 | 加分 | `.java` 中出现 `ActivityNotFoundException` 或 `resolveActivity(` |
| G-1 | 必需 | `app/src/main/java` 下 `.java` 文件不少于 7 个 |
| G-2 | 必需 | `res/layout`（含 `layout-land`）下 xml 文件不少于 5 个 |
| G-3 | 警告 | 源码中残留 `TODO`、`FIXME`、`XXX` |
| G-4 | 警告 | `app/build.gradle` 中未开启 `viewBinding`（开了可以少写 findViewById，机考可选） |

**通过标准**：`必需` 与 `加分` 项里，**必需项 FAIL 必须为 0**；加分项允许缺，但你至少要做到 C1、C2、C3 三条（这是你目前最弱的部分）。

---

# 4. 怎么跑验收

在 cmd.exe 里（把 `<你的工程根目录>` 换成你 New Project 时选的路径，就是含 `gradlew.bat` 的那一层）：

```bash
python D:\ProjectStore\one2oneTutorial\AndroidExam\check_acceptance.py "<你的工程根目录>"
python D:\ProjectStore\one2oneTutorial\AndroidExam\check_acceptance.py "<你的工程根目录>" --stage A
python D:\ProjectStore\one2oneTutorial\AndroidExam\check_acceptance.py "<你的工程根目录>" --stage B
python D:\ProjectStore\one2oneTutorial\AndroidExam\check_acceptance.py "<你的工程根目录>" --stage C
```

构建验收（同样在工程根目录）：

```bash
gradlew.bat assembleDebug
```

输出里必须出现 `BUILD SUCCESSFUL`。**先构建、再跑脚本**：编译都过不了的工程，静态检查通过也没意义。

脚本每行输出格式为 `[PASS] B1-4 (必需) …` / `[FAIL] B2-5 …` / `[MISS] C3-2 …` / `[WARN] G-3 …`，四种状态的含义：

| 状态 | 含义 | 是否计入 FAIL |
|---|---|---|
| `PASS` | 判据命中 | 否 |
| `FAIL` | **必需**项没做到 | 是 |
| `MISS` | **加分**项没做（C 段允许缺） | 否，单独列出 |
| `WARN` | 风格/隐患提示 | 否 |

末尾三行依次是：`SUMMARY PASS=xx FAIL=yy MISS=zz WARN=ww`、未通过项编号清单、`RESULT: FAIL=yy`。**`RESULT: FAIL=0` 才算过线。**

脚本会剥掉 Java 注释再做代码级判断（所以「注释里写清楚为什么」这类要求不会误判成你实现了功能），但要求「注释里必须记录某句话」的 C2-4、C5-4 反过来会去读注释原文。

> **难度校准**：把本脚本跑在已有的 `D:\ProjectStore\AndroidDemo`（GradeCalc 演练工程）上，结果是
> `SUMMARY PASS=56 FAIL=8 MISS=9 WARN=3`。也就是说**这道题比演练工程更难**，
> 直接照抄 AndroidDemo 过不了线（缺 setView 输入对话框、COUNT(*)、GROUP BY、ORDER BY + LIMIT、LIKE 模糊查询）。

**脚本查不出来的东西（你必须自己在模拟器上验一遍）**：
1. 旋转屏幕后表单内容是否真的还在（A4）。
2. 系统语言切中文后有没有残留英文（B5）。
3. 横屏布局有没有被截断、按钮能不能点到（B5）。
4. 子线程改 UI 时 Logcat 里那句英文原文到底是什么（C2）。
5. 条形图在横屏与数据为 0 时长什么样（C3）。
6. 返回键在 Fragment 之间是否正确回退（C4）。
7. Device Explorer 里 `backup.txt` 的真实绝对路径（C5）。

---

# 5. 卡壳时怎么问

**不要**问「这个功能怎么写」。**要**按这个模板问，这样我只能给定位思路，你也才真的在练：

```text
场景编号：B3
我想要的效果：长按 item 弹出删除菜单
我已经写了：registerForContextMenu(recyclerView)
现在的现象：长按没有任何反应，Logcat 无报错
我怀疑：是不是 RecyclerView 的 item 触摸事件被拦截了
请只告诉我方向对不对，以及该去查哪个类的哪个方法，不要给代码
```

我回复时会遵守：只指出「你漏了哪一类东西」「去看哪个课件的哪一节」「哪个方法名值得查」，不贴实现。

---

# 6. 交卷前的最后 10 分钟（真实考试照抄这个流程）

1. `gradlew.bat assembleDebug` 或直接 Run 一次，确认没有编译错误。
2. 在模拟器上把主线走一遍：填表 → 保存 → 进列表 → 长按删除 → 回主页 → 旋转 → 看统计。
3. 清一次 App 数据再重开，确认 SharedPreferences 与数据库行为符合预期（冷启动不崩）。
4. 切系统语言到中文，扫一眼有没有英文残留。
5. 横屏看一眼三个页面。
6. 把没做完的场景在代码里留一行注释写清楚「计划怎么做、卡在哪」——**机考改卷看得到思路，空着什么都没有**。
