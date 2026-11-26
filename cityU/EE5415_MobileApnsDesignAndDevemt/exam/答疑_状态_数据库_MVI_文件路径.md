# EE5415 答疑：全局状态 / finish 与 Flag / 数据库写法 / MVI 到底是什么 / 文件路径能不能改

> 配套主手册：`Android前端类比手册.md`（本文是它的补充答疑，章节号沿用主手册）。
> 本文所有代码都取自你**自己已经交过的作业** `BMI-MVI`（可当考试代码参考）或 `D:\ProjectStore\AndroidDemo`，
> 不是我凭空编的 API。
>
> 五个问题：
> 1. 没有全局共享状态的方式？只能 Bundle 硬传或写一堆 State？
> 2. 什么时候用 `finish()`？`FLAG_ACTIVITY_CLEAR_TOP` 什么效果？
> 3. 数据库能不能全用 `execSQL`？`db.query(TABLE, null,null,null,null,null, "date ASC")` 好怪，有条件怎么写？
> 4. MVI 没懂。Handler / Reducer / ExecutorService 有什么区别？全写 onClick 不行吗？
> 5. File 不能改地方吗？能写完整路径？还是保存路径被固定死了？

---

## Q1. 全局共享状态：Android 有，而且不止一种，Bundle 只是其中最弱的一种

### 1.1 先纠正一个印象

你现在的印象是「只能靠 Bundle 硬传，或者写一堆状态量的 State」。实际上是 **6 条路**，按「活多久 + 谁能看到」来选：

| # | 方式 | 生命周期 | 谁能访问 | 前端类比 |
|---|---|---|---|---|
| 1 | Activity 成员变量（`private MainState currentState;`） | 这个页面活着的时候。**旋转屏幕就没了** | 只有这个 Activity | Vue 组件的 `data()` |
| 2 | `Intent.putExtra()` / `Bundle` | 一次跳转，用完就没 | 只有目标 Activity | `router.push({ query: {...} })` |
| 3 | `onSaveInstanceState(Bundle)` | 跨旋转、跨系统杀进程重建 | 只有同一个 Activity 重建后 | 前端没有对应物（页面不会重建） |
| 4 | **static 字段 / 单例** | **整个进程**，App 被杀就没 | **任何页面任何类** | `getApp().globalData` / Pinia store |
| 5 | **ViewModel** | Activity 作用域，**旋转不丢** | 同一 Activity 下的所有 Fragment | 页面级 Pinia store |
| 6 | SharedPreferences / 文件 / SQLite | **永久**，卸载 App 才没 | 任何页面，下次启动还在 | `localStorage` / IndexedDB |

**「写一堆状态量的 State」是第 4/5 条路的一种组织形式（MVI），不是唯一形式，更不是被迫的。**

### 1.2 第 4 条：真正的「全局 store」——Application 子类（≈ Pinia / getApp().globalData）

小程序里你会写 `getApp().globalData.userInfo`。Android 的等价物是**自定义 Application 类**：

```java
// AppData.java —— 全局单例，进程内任何地方都能拿到
public class AppData extends Application {

    private static AppData instance;          // static 引用自己

    private String currentStudent = "";       // 想共享什么就放什么
    private final List<GradeRecord> cart = new ArrayList<>();

    @Override public void onCreate() {
        super.onCreate();
        instance = this;                      // 进程启动时系统会调一次
    }

    public static AppData get() { return instance; }

    public String getCurrentStudent() { return currentStudent; }
    public void setCurrentStudent(String s) { this.currentStudent = s; }
    public List<GradeRecord> getCart() { return cart; }
}
```

**必须在 AndroidManifest.xml 里注册**，否则系统不会创建它（这一步最容易忘）：

```xml
<application
    android:name=".AppData"          <!-- ★ 加这一行 -->
    android:icon="@drawable/ic_launcher"
    android:theme="@style/Theme.GradeCalc">
```

任何 Activity / Fragment / Adapter 里用起来就一行：

```java
AppData.get().setCurrentStudent("Peter");
String who = AppData.get().getCurrentStudent();
```

如果不想动 Manifest，还有个更糙的写法——纯静态持有类：

```java
public class GlobalStore {
    public static final List<String> NAMES = new ArrayList<>();
    public static String currentUser = "";
}
// 用：GlobalStore.currentUser = "Peter";
```

> ⚠️ **static 的两个坑**（面试和期末都可能问）：
> 1. **绝对不要 static 持有 `Context` / `Activity` / `View`** —— Activity 销毁了但 static 还拽着它，
>    整个 Activity 连同它的 View 树都无法回收 = 内存泄漏。要存 Context 就存 `getApplicationContext()`。
> 2. static 数据在 **App 进程被系统杀掉后就没了**，别拿它当持久化用。

### 1.3 第 5 条：ViewModel（多个 Fragment 共享同一份状态，且旋转不丢）

```java
public class MainViewModel extends ViewModel {
    private final MutableLiveData<String> student = new MutableLiveData<>("");
    public LiveData<String> getStudent() { return student; }          // 对外只读
    public void setStudent(String s) { student.setValue(s); }         // 改
}

// Activity 里
MainViewModel vm = new ViewModelProvider(this).get(MainViewModel.class);
// Fragment 里（拿的是同一个实例，因为作用域是宿主 Activity）
MainViewModel vm = new ViewModelProvider(requireActivity()).get(MainViewModel.class);
vm.getStudent().observe(getViewLifecycleOwner(), s -> textView.setText(s));
```

`ViewModel` 比普通 static 强的地方：**旋转屏幕时 Activity 被销毁重建，ViewModel 还活着**（它的存活由
`ViewModelStoreOwner` 管，配置变更不销毁）。这就是 L04 讲的 MVVM 的核心卖点。

### 1.4 考场怎么选（重点）

机考 3 小时，**不要搭全局 store**。理由：多写一个类 + 改 Manifest + 容易 static 泄漏，收益几乎为零。

**推荐用「数据库 / SharedPreferences 当唯一真相源」**，也就是 `AndroidDemo` 里 `HistoryActivity` 的做法：

```java
@Override protected void onResume() {
    super.onResume();
    reload();                       // 每次页面重新可见就重查一遍 DB
}

private void reload() {
    List<GradeRecord> list = dbHelper.getAllRecords();
    adapter.setData(list);          // 列表自己刷新
    chartView.setRecords(list);     // 图表自己刷新
}
```

这样 A 页面写进去的数据，B 页面 `onResume` 时自然就读到了 —— **不需要任何全局变量，也不需要 Bundle 传**。
这就是为什么 `ResultActivity` 存完库，`HistoryActivity` 一进来就能看到：它们共享的是那张表，不是内存。

一句话决策：
- **传一个值给下一页** → `Intent.putExtra`（Bundle）
- **两个页面看同一批数据** → 都去查 SQLite / SP（`onResume` 里刷新）
- **旋转屏幕不想丢输入框内容** → `onSaveInstanceState` 或 ViewModel
- **下次启动 App 还要记得** → SharedPreferences（几个值）/ SQLite（一批记录）
- **确实需要跨页内存共享（比如购物车）** → Application 单例，但机考别用

---

## Q2. `finish()` 什么时候用，`FLAG_ACTIVITY_CLEAR_TOP` 到底干了什么

### 2.1 `finish()` ≠ 退出 App

`finish()` 只做一件事：**把当前 Activity 从返回栈里弹出并销毁**，回到栈里的上一个页面。

前端类比：
- `finish()` ≈ 小程序 `wx.navigateBack()` / Vue `router.back()`
- **不是** `process.exit()`。栈里还有其他页面，App 就还活着。
- 想把整个 App 退掉，得把栈里每个 Activity 都 finish（见 2.4）。

`BMI-MVI/MainActivity` 和 `AndroidDemo/ResultActivity` 里都在 `AlertDialog` 的确认按钮里调了 `finish()`。

### 2.2 四个该用 `finish()` 的场景

```java
// 场景 1：表单提交成功，不想让用户按返回键又回到空表单
saveToDb();
startActivity(new Intent(this, ResultActivity.class));
finish();                                   // ★ 当前页从栈里移除

// 场景 2：登录成功，不能让返回键回到登录页（否则能绕过登录）
startActivity(new Intent(this, HomeActivity.class));
finish();

// 场景 3：校验/前置条件不满足，页面没意义，直接挡住
@Override protected void onCreate(Bundle b) {
    super.onCreate(b);
    if (!isAuthorized()) {
        Toast.makeText(this, "无权访问", Toast.LENGTH_SHORT).show();
        finish(); return;                   // ★ finish 后面要 return，别继续跑 setContentView
    }
    setContentView(R.layout.activity_x);
}

// 场景 4：详情页里「删除本条」，删完这个页面已经没内容可显示了
dbHelper.deleteRecord(id);
finish();                                   // 回列表页，列表页 onResume 会重查（见 Q1.4）
```

**不调 `finish()` 会怎样？** 页面继续留在栈里。A→B→C 之后按返回键是 C→B→A，一个都不会少。
`finish()` 只是「我不需要用户再回到我这一页」的声明。

### 2.3 `FLAG_ACTIVITY_CLEAR_TOP`：把目标页上面的全部清掉

设返回栈是 `A → B → C`（C 在最上面，用户正在看 C）。在 C 里执行：

```java
Intent i = new Intent(this, A.class);
i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
startActivity(i);
```

结果：**B 和 C 被销毁，栈变成只有 A**。这就是「回到首页，中间页别留」。

> ⚠️ **一个必考的细节**：默认情况下，那个已存在的 A 也会被**销毁并重新创建**（重新走 `onCreate`），
> 因为系统默认会新建一个 A 实例压上去。如果你想让 A **保留原样、不重建**，要再加一个 flag：

```java
i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
// 此时 A 不重建，而是收到 onNewIntent(intent) 回调（onCreate 不会再走）
```

例外：如果 A 在 Manifest 里已经写了 `android:launchMode="singleTop"`，那么只用 `CLEAR_TOP` 就会走 `onNewIntent`，不重建。

### 2.4 常见 Flag 速查（考场记住前三个就够）

| 想要的效果 | 写法 |
|---|---|
| 回到已存在的 A，A 上面的全销毁（A 会重建） | `FLAG_ACTIVITY_CLEAR_TOP` |
| 同上，但 A 不重建、走 `onNewIntent` | `FLAG_ACTIVITY_CLEAR_TOP \| FLAG_ACTIVITY_SINGLE_TOP` |
| 彻底清空整个任务栈重来（**登出**的标准写法） | `FLAG_ACTIVITY_NEW_TASK \| FLAG_ACTIVITY_CLEAR_TASK` |
| B 页面不留栈，离开就销毁（比如引导页/支付中间页） | `FLAG_ACTIVITY_NO_HISTORY` |
| 每次点击通知都新建一个实例叠上去 | `FLAG_ACTIVITY_MULTIPLE_TASK`（配 NEW_TASK） |
| 把 B 提到栈顶但不动其他（Android 11+） | `FLAG_ACTIVITY_REORDER_TO_FRONT` |

```java
// 登出：清空整个任务栈，重新开一个登录页
Intent i = new Intent(this, LoginActivity.class);
i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
startActivity(i);
// 注意这里不需要再 finish()，CLEAR_TASK 已经把当前页也清掉了
```

### 2.5 Flag 还能塞数据吗？能

`CLEAR_TOP` 时目标 Activity 如果是 `singleTop`，数据要从 `onNewIntent` 里拿，**不能**在 `onCreate` 里拿：

```java
@Override protected void onNewIntent(Intent intent) {
    super.onNewIntent(intent);
    setIntent(intent);                                  // ★ 不调这句，getIntent() 还是老的
    String id = intent.getStringExtra("id");
}
```

### 2.6 机考口径

- 提交/删除/登出这类「不该再回来」的动作 → 后面补一个 `finish()`，是稳定加分的细节。
- 需要「回首页」按钮 → `CLEAR_TOP | SINGLE_TOP` 一行。
- 其余情况**别碰 launchMode**，容易出诡异 bug 且没时间调。

---

## Q3. 数据库：`execSQL` 能不能包打天下？`query()` 的七个 null 到底是什么？

### 3.1 结论：能，但有分工

| API | 能跑什么 | 返回 |
|---|---|---|
| `db.execSQL(String sql)` | **除 SELECT 外的一切**：CREATE / INSERT / UPDATE / DELETE / DROP | `void` |
| `db.execSQL(String sql, Object[] bindArgs)` | 同上，带 `?` 占位符 | `void` |
| `db.rawQuery(String sql, String[] args)` | **SELECT**（其实也能跑别的但没意义） | `Cursor` |
| `db.insert/update/delete/query(...)` | 封装好的 CRUD，Android 帮你拼 SQL | `long` / `int` / `Cursor` |

所以你完全可以整个 DbHelper 只用 `execSQL` + `rawQuery`，一行 ContentValues 都不写。**这套写法反而更接近你熟悉的 SQL，考场上可能更省心。**

四种写法做同一件事（插入一条记录）：

```java
// 写法 A：execSQL 字符串拼接 —— ❌ 别用，名字里有个单引号就崩，还有 SQL 注入
db.execSQL("INSERT INTO grade_records (student_name, total) VALUES ('" + name + "', " + total + ")");

// 写法 B：execSQL + 占位符 —— ✅ 安全，最像手写 SQL
db.execSQL("INSERT INTO grade_records (student_name, total) VALUES (?, ?)",
           new Object[]{ name, total });

// 写法 C：ContentValues —— ✅ 安全，Android 推荐，但要多写几行
ContentValues v = new ContentValues();
v.put("student_name", name);
v.put("total", total);
db.insert("grade_records", null, v);

// 写法 D：查询用 rawQuery + 占位符 —— ✅ 考场首选，一眼看得懂
Cursor c = db.rawQuery("SELECT * FROM grade_records WHERE total >= ? ORDER BY ts DESC",
                       new String[]{ "60" });
```

> `insert()` 的第二个参数 `nullColumnHack` 是什么？当 ContentValues 为空时，SQL 不允许
> `INSERT INTO t ()`，Android 需要一个列名来写 `INSERT INTO t (那个列) VALUES (NULL)`。
> 你永远会传非空 values，所以**永远填 `null` 就对了**。

### 3.2 `query()` 七个参数逐个拆开

```java
db.query(TABLE, null, null, null, null, null, "date ASC");
//       1      2     3     4     5     6     7
```

| 位置 | 参数名 | 含义 | 传 null 表示 | 对应 SQL |
|---|---|---|---|---|
| 1 | `table` | 表名 | 不能为 null | `FROM bmi_records` |
| 2 | `columns` | 要哪几列 | 全部列（`*`） | `SELECT *` / `SELECT bmi, date` |
| 3 | `selection` | **WHERE 条件**，用 `?` 占位 | 不过滤 | `WHERE ...` |
| 4 | `selectionArgs` | 上面那些 `?` 的**实际值**，按顺序 | 无占位符 | — |
| 5 | `groupBy` | 分组列名 | 不分组 | `GROUP BY ...` |
| 6 | `having` | 分组后的过滤（配 groupBy 用） | 不过滤 | `HAVING ...` |
| 7 | `orderBy` | 排序 | 不排序（数据库随机顺序！） | `ORDER BY date ASC` |

所以 `BMI-MVI/BmiHistoryDbHelper.getAllRecords()` 那一行等价于：

```sql
SELECT * FROM bmi_records ORDER BY date ASC;
```

七个参数里六个 `null`，看着怪，其实就是「我什么条件都不要，只要排个序」。**它怪是因为这是 Java 的方法调用，不是 SQL 字符串**——`query()` 只是 `rawQuery` 的「填空版」。

### 3.3 有条件到底怎么写（6 个真实例子，考场照抄改数字）

```java
// ① 一个等值条件：WHERE gender = 'MALE'
Cursor c = db.query(TABLE,
        null,                        // 所有列
        "gender = ?",                // ← WHERE，? 是占位符
        new String[]{ "MALE" },      // ← 占位符的值，按顺序
        null, null, "date DESC");

// ② 多条件 AND：WHERE age > 18 AND category = 'NORMAL'
//    ★ 坑：selectionArgs 只能是 String[]，数字也要 String.valueOf()
Cursor c = db.query(TABLE, null,
        "age > ? AND category = ?",
        new String[]{ String.valueOf(18), "NORMAL" },
        null, null, null);

// ③ IN：WHERE category IN ('NORMAL','OVERWEIGHT')
Cursor c = db.query(TABLE, null,
        "category IN (?, ?)",
        new String[]{ "NORMAL", "OVERWEIGHT" },
        null, null, null);

// ④ 模糊匹配 LIKE：WHERE name LIKE '%peter%'（% 写在值里，不是写在条件里）
Cursor c = db.query(TABLE, null,
        "student_name LIKE ?",
        new String[]{ "%" + keyword + "%" },
        null, null, null);

// ⑤ 区间 BETWEEN + 只取两列
Cursor c = db.query(TABLE,
        new String[]{ "date", "bmi" },        // ← 只要这两列，省内存
        "bmi BETWEEN ? AND ?",
        new String[]{ "18.5", "24.9" },
        null, null, "date ASC");

// ⑥ 分组统计：SELECT category, COUNT(*) AS n FROM t GROUP BY category HAVING COUNT(*) > 1
Cursor c = db.query(TABLE,
        new String[]{ "category", "COUNT(*) AS n" },
        null, null,
        "category",                   // groupBy
        "COUNT(*) > 1",               // having
        null);
int cnt = c.getInt(c.getColumnIndexOrThrow("n"));   // 聚合列用别名取
```

**`LIMIT` 的坑**：7 参数版 `query()` **没有 limit 参数**。想取前 5 条，三种办法：

```java
// 办法 1：用带 limit 的重载（9 个参数，第一个是 distinct）
db.query(false, TABLE, null, null, null, null, null, "date DESC", "5");

// 办法 2（考场推荐，最直观）：直接 rawQuery
db.rawQuery("SELECT * FROM grade_records ORDER BY ts DESC LIMIT 5", null);

// 办法 3（能用但难看）：把 LIMIT 塞进 orderBy 字符串
db.query(TABLE, null, null, null, null, null, "date DESC LIMIT 5");
```

### 3.4 为什么一定要用 `?` 而不是拼字符串

```java
// 假设用户输入的名字是：Peter'; DROP TABLE grade_records; --
db.execSQL("DELETE FROM t WHERE name = '" + name + "'");   // 表没了
db.delete(TABLE, "name = ?", new String[]{ name });        // 安全，name 只会被当成一个普通字符串
```

即使不考虑恶意注入，**只要用户输入里有一个单引号 `'`，拼接的 SQL 就语法错误直接崩**。这是真实会发生的 bug。

### 3.5 Cursor 的三个必做动作（漏一个就出问题）

```java
Cursor c = db.query(...);
try {
    while (c.moveToNext()) {                      // ① 游标初始在第一行之前，必须先 move
        int idx = c.getColumnIndexOrThrow("bmi"); // ② 用列名换下标（写死下标容易错）
        double bmi = c.getDouble(idx);
        // getString / getInt / getLong / getDouble / isNull
    }
} finally {
    c.close();                                    // ③ 必须关，否则 Logcat 报 Cursor leak 警告
}
```

几个常用：`c.getCount()` 行数、`c.moveToFirst()` 跳到第一行、`c.isNull(i)` 判空、
`c.getColumnIndexOrThrow(name)` 列不存在会抛异常（比 `getColumnIndex` 返回 −1 好，早崩早定位）。

**只要一个值（COUNT / AVG）的标准套路**，直接抄 `BmiHistoryDbHelper.getRecordCount()`：

```java
Cursor c = db.rawQuery("SELECT COUNT(*) FROM " + TABLE, null);
int count = 0;
if (c.moveToFirst()) count = c.getInt(0);   // 只有一行一列，下标就是 0
c.close();
```

### 3.6 考场决策

| 操作 | 用什么 | 理由 |
|---|---|---|
| 建表 / 改表 | `execSQL` | 只能用它 |
| 插入 | `ContentValues` + `insert`，或 `execSQL` + `?` | 都行，选你顺手的 |
| 更新 / 删除 | `update` / `delete` + `?` | 少写字符串 |
| 查询（有条件） | **`rawQuery` 直接写 SQL** | 你最熟 SQL，出错率最低 |
| 查询（无条件全表） | `query(TABLE, null,null,null,null,null, "id DESC")` | 就一行，背下来 |

> `AndroidDemo` 用的是 `query(...)`（跟作业一致），但**考场上你觉得 rawQuery 更顺手就全用 rawQuery，完全没问题，一分不扣**。

---

## Q4. MVI：Handler / Reducer / ExecutorService 是三个不同维度的东西

### 4.1 先给结论，省得你焦虑

**机考不需要写 MVI。全部写 onClick 完全正确，而且更快、更不容易崩。**
MVI 是 L04 的架构内容，期末笔试可能考概念，机考写它是给自己找麻烦（多三个文件、样板代码翻倍）。

但你要**看得懂**，因为你的 Assignment04 就是 MVI 写的，考试允许你把它下载下来当参考。

### 4.2 最关键的一句澄清

你把 Handler、Reducer、ExecutorService 放在一起比，但它们**不在同一个维度上**：

| | 属于什么范畴 | 解决什么问题 | 能不能不用 | 前端类比 |
|---|---|---|---|---|
| **ExecutorService** | 线程 | 「这段耗时活别在 UI 线程跑，开个子线程」 | 没有耗时操作就不用 | Web Worker / 后台跑的 `axios` |
| **Handler** | 线程 | 「子线程的结果切回 UI 线程才能改界面」 | 不跨线程就不用 | Worker 的 `postMessage` 回主线程 |
| **Reducer** | 架构 | 「状态怎么变，集中在一个纯函数里算」 | 小项目完全可以不用 | Vuex 的 mutation / Pinia 的 action |

- **Executor 决定「在哪条线程跑」**
- **Handler 决定「什么时候回到主线程」**
- **Reducer 决定「状态怎么从旧的变成新的」**

三者互相独立：你可以「有 Executor + Handler，但没有 Reducer」（`AndroidDemo` 就是这样）；
也可以「有 Reducer，但没有任何线程操作」（纯本地计算的 MVI）。

**它们唯一的共同点是：在 BMI-MVI 那份作业里同时出现了，所以看起来像一套东西。其实不是。**

### 4.3 MVI 的三个角色（用你作业里的真实文件）

```
Intent.java      ← 「用户想干什么」的清单（动作类型）
MainState.java   ← 「界面现在长什么样」的唯一真相（不可变）
MainReducer.java ← 「新状态 = f(旧状态, 动作)」的纯函数
MainActivity.java← View 层：只干两件事 —— dispatch(动作) 和 render(状态)
```

数据流是**单向的一个圈**：

```
   用户点按钮
       │
       ▼
  dispatch(new Intent.CalculateBmi())     ← Activity 只发一个「动作对象」，不直接改界面
       │
       ▼
  MainReducer.reduce(currentState, intent) ← 唯一能改状态的地方，if/else 分派
       │
       ▼
  返回一个【全新的】MainState              ← 旧 State 一个字都没改（不可变）
       │
       ▼
  render(newState)                         ← Activity 照着新 State 把界面整体刷一遍
       │
       └──────► 用户看到界面变化
```

对应代码（`BMI-MVI/MainActivity.java`，真实存在）：

```java
private MainState currentState;      // 唯一真相
private MainReducer reducer;

private void dispatch(Intent intent) {
    captureInputValues();                                  // 把 EditText 里的值同步进 State
    MainState newState = reducer.reduce(currentState, intent);
    currentState = newState;                               // 换成新对象
    render(currentState);                                  // 整体重绘
    if (intent instanceof Intent.CalculateBmi && newState.getResult() != null) {
        saveAfterCalculation(newState);                    // 副作用（存库）放这里
    }
}

// 所有监听器都只有一行：发动作
findViewById(R.id.btnCalculate).setOnClickListener(v -> dispatch(new Intent.CalculateBmi()));
radioGender.setOnCheckedChangeListener((g, id) -> {
    if (id == R.id.radioMale) dispatch(new Intent.SetGender(Gender.MALE));
    else if (id == R.id.radioFemale) dispatch(new Intent.SetGender(Gender.FEMALE));
});
```

Reducer 就是一个大 if/else（`MainReducer.java` 原文）：

```java
public MainState reduce(MainState currentState, Intent intent) {
    MainState.Builder builder = new MainState.Builder(currentState);  // 拷贝旧状态
    if (intent instanceof Intent.SetHeight) {
        builder.height(((Intent.SetHeight) intent).height());
        builder.errorMessage(null);
    } else if (intent instanceof Intent.CalculateBmi) {
        builder = handleCalculate(builder, currentState);             // 校验 + 算 BMI
    } else if (intent instanceof Intent.Reset) {
        builder = new MainState.Builder();                            // 空 Builder = 回到初始状态
    }
    return builder.build();                                           // 产出一个新对象
}
```

> ⚠️ **一个大坑**：`Intent.java` 里的 `Intent` 和 `android.content.Intent`（页面跳转那个）**同名但毫无关系**。
> 所以作业里跳转页面时被迫写了全限定名：
> ```java
> startActivity(new android.content.Intent(this, BmiHistoryActivity.class));
> ```
> MVI 的 `Intent` = 用户动作（≈ action type），Android 的 `Intent` = 跨组件消息（≈ 路由）。
> 考场上**千万别把这个自定义 `Intent` 类建出来**，会把自己绕晕。

> `MainState` 为什么写成一堆 `final` 字段 + 一个 `Builder`？因为「不可变」= 建好就不能改。
> 想改就 `new MainState.Builder(旧的)` 拷一份、改几个字段、`build()` 出个新的。
> 好处：任何时刻界面都由一个确定的对象描述，不会出现「改了 A 忘了同步 B」的界面错乱。
> 前端类比：就像 Redux 里永远 `{...state, count: state.count + 1}` 而不是 `state.count++`。

### 4.4 Handler / Executor / Reducer 在一段真实代码里怎么配合

这是 `BMI-MVI/MainActivity.fetchAiSuggestion()`（点「获取 AI 建议」按钮），三个角色全出场了：

```java
executorService = Executors.newSingleThreadExecutor();   // onCreate 里建一次
mainHandler     = new Handler(Looper.getMainLooper());

private void fetchAiSuggestion() {
    dispatch(new Intent.SetLlmLoading(true));     // ①【Reducer】状态变「加载中」→ render 立刻显示进度条

    executorService.execute(() -> {               // ②【Executor】开子线程，别卡住 UI
        String suggestion = llmService.fetchSuggestion(...);   // 网络请求，可能几秒

        mainHandler.post(() -> {                  // ③【Handler】结果切回 UI 线程
            if (suggestion != null) dispatch(new Intent.SetLlmSuggestion(suggestion));
            else                    dispatch(new Intent.SetLlmError(getString(R.string.ai_error)));
        });                                       //    又是【Reducer】改状态 → render 显示文字
    });
}
```

把每一步的职责标出来，就再也不会混了：

| 步骤 | 谁在干活 | 换掉它会怎样 |
|---|---|---|
| ① | Reducer + render | 直接在 onClick 里 `progressBar.setVisibility(VISIBLE)` 也行，效果一样 |
| ② | ExecutorService | 去掉它 → 网络请求跑在 UI 线程 → **ANR 卡死**（L09 铁律） |
| ③ | Handler | 去掉它，直接在子线程里 `setText` → **崩溃** `Only the original thread that created a view hierarchy can touch its views` |

**看出区别了吗：② 和 ③ 是「不做就崩/卡」的硬需求；① 是「不做也能跑」的架构选择。**

### 4.5 「全部写 onClick 不就好了？」—— 对，小项目就该这样

同一个功能，两种写法的完整对照：

**版 A：直接 onClick（机考就写这个）**

```java
btnCalc.setOnClickListener(v -> {
    // 1. 读
    double h = Double.parseDouble(editHeight.getText().toString().trim());
    double w = Double.parseDouble(editWeight.getText().toString().trim());
    // 2. 算
    double bmi = w / ((h/100) * (h/100));
    // 3. 写界面
    textBmi.setText(String.format("%.1f", bmi));
    cardResult.setVisibility(View.VISIBLE);
    // 4. 存
    dbHelper.insertRecord(...);
});
```

**版 B：MVI** —— 需要 `Intent.java`（10 行 record）+ `MainState.java`（90 行 Builder）+
`MainReducer.java`（60 行 if/else）+ Activity 里的 `dispatch()` / `render()`，**总共多 150+ 行，界面效果一模一样。**

那 MVI 什么时候**值得**？四个信号：

1. **界面上有一堆互相牵连的东西要一起变**。BMI-MVI 就是典型：成人结果卡 / 儿童结果卡 / AI 建议卡 /
   进度条 / 加载文字 / 建议文字 / 错误文字 / 按钮显隐 —— 8 个 View 的可见性互相关联。
   如果散在各个 onClick 里，很容易出现「显示了进度条忘了隐藏按钮」这类 bug。
   收进一个 State 之后，`render()` 每次照着 State 全刷一遍，**不可能出现状态不一致**。
2. **多个入口改同一份状态**（按钮、菜单、手势、广播都要触发「重置」）。
3. **要写单元测试**。Reducer 是纯函数，不碰 Android API，`new MainReducer().reduce(state, intent)`
   在 JVM 上就能测 —— 你作业里的 `src/test/BmiCalculatorTest.java` 就是这么跑的，不需要模拟器。
4. 多人协作 / 大项目，需要「谁改了状态」可追溯。

MVI 的代价（也是 L04 课件自己列的缺点）：**不可变 State + Intent 的样板代码太多**，
改一个小功能要动三个文件；考试时间根本不够。

### 4.6 「一个页面带一个 Handler、Reducer、ExecutorService、State、Activity 这些东西？」

不完全是。分清「每页一套」和「全 App 一套」：

| 组件 | 该有几个 | 你作业里的情况 | 正规做法 |
|---|---|---|---|
| `Activity` | 每个页面 1 个 | ✔ | — |
| `State` | 每个**界面单元** 1 个 | ✔ `MainState` | 页面复杂就拆多个 State |
| `Reducer` | 每个 State 配 1 个 | ✔ `MainReducer` | — |
| `ExecutorService` | **全 App 1 个就够** | ✘ 每个 Activity 各 new 了一个 | 放 Application 单例里共享 |
| `Handler(主线程)` | **全 App 1 个就够** | ✘ 每个 Activity 各 new 了一个 | 同上；甚至可用 `runOnUiThread()` 完全替代 |

`ExecutorService` 和 `Handler` 是**基础设施**，不是页面逻辑。每页 new 一个线程池其实有点浪费
（作业项目小，无所谓），而且每个都要在 `onDestroy` 里清理：

```java
@Override protected void onDestroy() {
    super.onDestroy();
    if (executorService != null) executorService.shutdownNow();
    if (mainHandler != null) mainHandler.removeCallbacksAndMessages(null);  // ★ 防泄漏
}
```

**替代方案（考场更简单）**：不要 ExecutorService，直接用 Android 自带的两个静态池 + `runOnUiThread`：

```java
// 完全等价，但不需要成员变量，也不需要 onDestroy 清理
Executors.newSingleThreadExecutor().execute(() -> { ... });   // 不推荐，用完不关

// 推荐：Android 提供的共享线程池
AsyncTask 已废弃，用这个 ↓
new Thread(() -> {
    String s = doSlowWork();
    runOnUiThread(() -> textView.setText(s));    // ← 连 Handler 都省了
}).start();
```

`runOnUiThread(Runnable)` / `view.post(Runnable)` / `new Handler(Looper.getMainLooper()).post(...)`
**三者效果完全一样**，都是「把这段代码丢回 UI 线程执行」。挑一个顺手的背下来即可（`AndroidDemo` 用的是 Handler）。

### 4.7 MVI 在 Android 上最别扭的一点（顺便解释 `captureInputValues()`）

Web 里有 `v-model`，输入框和状态天然双向绑定。Android 没有 —— EditText 的文字**存在 View 自己身上**，
不在 State 里。如果不处理，State 就不是「唯一真相」了。

作业里的解决办法是在 dispatch 前先把输入框读一遍：

```java
private void captureInputValues() {
    Double height = parseDouble(editHeight);      // 读不出来就返回 null，不覆盖
    Integer age   = parseInt(editAge);
    MainState.Builder builder = new MainState.Builder(currentState);
    if (height != null) builder.height(height);
    if (age != null) builder.age(age);
    currentState = builder.build();
}
```

正规 MVI 项目会为「每个字符变化」发一个 `Intent.SetHeight`（配 `TextWatcher`），
但那样代码更多。作业选择了「点按钮时统一抓一次」，这是合理的折中。

**这也正是「机考别写 MVI」的最实际理由**：光是让输入框和 State 同步，就要多写几十行没有分数的代码。

---

## Q5. File：路径确实被固定死了，但你能选「哪一类目录」

### 5.1 直接回答

- **不能写 `/sdcard/myapp/data.txt` 这种完整路径。** Android 10（API 29）引入 Scoped Storage 之后，
  App 基本失去了随意读写公共目录的能力，硬编码路径的结果通常是 `FileNotFoundException` 或 `Permission denied`。
- **`openFileOutput()` 的参数里根本没有目录**，只有文件名 —— 这就是「路径被固定死」的最直接证据。
  L10 课件原文签名：`FileOutputStream openFileOutput(String name, int mode)`。
- 你**能控制的是三件事**：① 用哪个目录类别（内部/缓存/外部私有）② 文件名（可以带子目录，如 `"a/b.txt"`）
  ③ 写入模式（覆盖 / 追加）。

### 5.2 课件里的路径对照（L10 原文摘录）

| 你写的代码 | 实际落盘路径 | 卸载 App | 用户能看到吗 | 要权限吗 |
|---|---|---|---|---|
| `openFileOutput("textfile.txt", MODE_PRIVATE)` | `/data/data/<pkg>/files/textfile.txt` | 一起删 | 看不到 | 不要 |
| `new File(getFilesDir(), "a.txt")` | 同上 | 一起删 | 看不到 | 不要 |
| `new File(getCacheDir(), "a.tmp")` | `/data/data/<pkg>/cache/a.tmp` | 一起删（系统空间不足也会自己清） | 看不到 | 不要 |
| `new File(getExternalFilesDir(null), "a.txt")` | `/sdcard/Android/data/<pkg>/files/a.txt` | **一起删** | 连 USB 用文件管理器能看到 | 不要（API 19+） |
| `getSharedPreferences("x", MODE_PRIVATE)` | `/data/data/<pkg>/shared_prefs/x.xml` | 一起删 | 看不到 | 不要 |
| `SQLiteOpenHelper(ctx, "grade_calc.db", ...)` | `/data/data/<pkg>/databases/grade_calc.db` | 一起删 | 看不到 | 不要 |
| `Environment.getExternalStoragePublicDirectory(...)` / MediaStore / SAF | `/sdcard/Download`、`/sdcard/DCIM` 等**公共目录** | **不删** | 能看到 | 要，或走系统选择器 |

课件原文的例子：`/data/data/com.example.FilesInternal/files/textfile.txt`。

**注意 `<pkg>` 就是 `app/build.gradle` 里的 `namespace`**（`AndroidDemo` 是 `com.example.gradecalc`）。
所以「路径固定」的准确说法是：**根目录由包名决定，你不能改；文件名和目录类别你能改。**

### 5.3 三种「换个地方」的合法做法

**做法一：换目录类别（最常用）**

```java
File internal = new File(getFilesDir(), "notes.txt");        // 内部：最安全，别的 App 绝对看不到
File cache    = new File(getCacheDir(), "tmp.json");         // 缓存：随时可能被系统清掉，别放重要数据
File external = new File(getExternalFilesDir(null), "big.csv"); // 外部私有：适合放大文件

// 还可以自己建子目录（目录不会自动创建，必须 mkdirs）
File dir = new File(getFilesDir(), "records/2026");
if (!dir.exists()) dir.mkdirs();                              // ★ mkdirs 带 s，会连父目录一起建
File f = new File(dir, "nov.txt");
```

**做法二：让用户自己选位置（导出文件的标准做法）**

想把 CSV / 图片导出到用户看得见的地方，**不要猜路径，让系统弹文件选择器**：

```java
// 弹出「保存到哪儿」的系统对话框（SAF，Storage Access Framework）
Intent i = new Intent(Intent.ACTION_CREATE_DOCUMENT);
i.setType("text/csv");
i.putExtra(Intent.EXTRA_TITLE, "grades.csv");
startActivityForResult(i, 1001);       // 或 ActivityResultLauncher

@Override protected void onActivityResult(int req, int res, Intent data) {
    super.onActivityResult(req, res, data);
    if (req == 1001 && res == RESULT_OK && data != null) {
        Uri uri = data.getData();                             // 用户选好的位置
        try (OutputStream os = getContentResolver().openOutputStream(uri)) {
            os.write("name,total\nPeter,87.5\n".getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) { e.printStackTrace(); }
    }
}
```

读用户已有的文件同理，把 action 换成 `ACTION_OPEN_DOCUMENT`（或 `ACTION_GET_CONTENT`），
然后用 `getContentResolver().openInputStream(uri)` 读。**拿到的是 `Uri`，不是 `File`，不能 `new File(uri.toString())`。**

**做法三：图片进相册** —— 用 `MediaStore.Images` 插入，不要直接写 `/sdcard/DCIM`。

### 5.4 完整可跑的 File 读写（不用 openFileOutput，用 File 也行）

```java
// ---- 写 ----
try {
    File f = new File(getFilesDir(), "notes.txt");
    FileWriter fw = new FileWriter(f, false);      // false = 覆盖；true = 追加（等于 MODE_APPEND）
    fw.write("第一行\n第二行\n");
    fw.close();
} catch (IOException e) { e.printStackTrace(); }

// ---- 读 ----
try {
    File f = new File(getFilesDir(), "notes.txt");
    if (!f.exists()) { /* 第一次运行必然走这里，一定要处理 */ }
    BufferedReader br = new BufferedReader(new FileReader(f));
    StringBuilder sb = new StringBuilder();
    String line;
    while ((line = br.readLine()) != null) sb.append(line).append('\n');
    br.close();
    textView.setText(sb.toString());
} catch (IOException e) { e.printStackTrace(); }

// ---- 列目录 / 删除 / 大小 ----
File[] files = getFilesDir().listFiles();
if (files != null) for (File x : files) Log.d("FILE", x.getName() + " " + x.length());
boolean ok = new File(getFilesDir(), "notes.txt").delete();
```

两种 API 的对应关系（**同一个目录，可以混用**）：

| Context 方法 | 等价的 File 写法 |
|---|---|
| `openFileOutput("a.txt", MODE_PRIVATE)` | `new FileOutputStream(new File(getFilesDir(), "a.txt"))` |
| `openFileOutput("a.txt", MODE_APPEND)` | `new FileOutputStream(f, true)` |
| `openFileInput("a.txt")` | `new FileInputStream(new File(getFilesDir(), "a.txt"))` |
| `deleteFile("a.txt")` | `new File(getFilesDir(), "a.txt").delete()` |

> `MODE_PRIVATE` = 覆盖写（文件已存在就清空）；`MODE_APPEND` = 追加到末尾。
> 老的 `MODE_WORLD_READABLE` / `MODE_WORLD_WRITABLE` 在 API 17 起抛异常，别用。

### 5.5 怎么亲眼看到这些文件（考前建议做一次）

Android Studio 右侧 **Device Explorer**（T02 课件讲过）→ 进入 `/data/data/com.example.gradecalc/`：

```
├── databases/grade_calc.db          ← SQLiteOpenHelper 建的库
├── files/                           ← openFileOutput / getFilesDir()
├── shared_prefs/grade_prefs.xml     ← SharedPreferences，可以直接打开看 XML 内容
└── cache/
```

> 模拟器上能看到，真机非 root 看不到 `/data/data`（这是系统的安全设计）。
> 顺手可以验证一件事：SharedPreferences 存的东西真的就是一个明文 XML —— 所以 L10 强调
> **不要往里存密码/token**，它不加密。

### 5.6 考场决策

| 需求 | 写法 | 一行搞定吗 |
|---|---|---|
| 存几个配置值 / 上次输入 | `SharedPreferences` | ✔（见主手册 §13.1） |
| 存一批记录（要查询、排序、删单条） | `SQLiteOpenHelper` | 见 Q3 |
| 存一段文本 / 导出内容 | `openFileOutput("x.txt", MODE_PRIVATE)` | ✔ 路径不用管 |
| 大文件、想让用户用文件管理器看到 | `getExternalFilesDir(null)` | ✔ |
| 导出到用户指定位置 | `ACTION_CREATE_DOCUMENT` + `ContentResolver` | ✘ 要十几行 |
| 读用户选的文件 | `ACTION_OPEN_DOCUMENT` + `openInputStream(uri)` | ✘ 要十几行 |

机考里 99% 的情况是前三种，**都不需要你关心路径**。

---

## 附：这五个问题对明天机考的实际影响

| 问题 | 考试要不要写 | 你要记住的一句话 |
|---|---|---|
| Q1 全局状态 | 不要搭 store | **两个页面共享数据 = 都去查同一个 SQLite**，`onResume` 里刷新 |
| Q2 finish / Flag | **要**，一行加分 | 「不该再回来」的动作后补 `finish()`；回首页用 `CLEAR_TOP \| SINGLE_TOP` |
| Q3 数据库 | **要**，几乎必考 | 建表 `execSQL`，查询**直接 `rawQuery` 写 SQL 最省心**，条件一律用 `?` + `String[]`，Cursor 必 `close()` |
| Q4 MVI | **不要写** | 全 onClick 是正确选择。只需能说出「Reducer 改状态、Executor 开线程、Handler 回主线程」三者的区别（期末概念题） |
| Q5 文件路径 | 基本不会考到路径 | `openFileOutput(文件名, MODE_PRIVATE)` 就完了，**路径由包名固定，不能也不需要自己写** |

**如果明天只带三句话进考场（在脑子里）：**
1. 数据要跨页面 → 存 SQLite，目标页 `onResume` 重查。
2. 查询看不懂 `query()` 的七个参数 → 换 `rawQuery("SELECT ... WHERE x = ?", new String[]{值})`。
3. 耗时操作（大量读写/网络）→ `new Thread(...)` + `runOnUiThread(...)`，别在 onClick 里直接干。
