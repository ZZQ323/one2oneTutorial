# EE5415 Android 手搓速查手册（前端类比版）

> 面向「写过 Vue / 小程序 / H5，但没真正手搓过 Android」的人。
> 目标：**看懂每一行在干什么，考场上能自己敲出来**。
> 配套可编译工程：`D:\ProjectStore\AndroidDemo`（Java，全新主题 GradeCalc 课程总评计算器），
> 本手册里出现的每个类名都能在那个工程里找到对应实现。
> 配套答疑（读完本手册后的五个疑问）：`答疑_状态_数据库_MVI_文件路径.md`
> —— 全局状态怎么共享、`finish()`/`FLAG_ACTIVITY_CLEAR_TOP` 何时用、`query()` 七个参数与 `rawQuery` 取舍、
> MVI 里 Handler/Reducer/ExecutorService 的区别、文件路径能不能自己指定。
>
> ⚠️ 考试规则（Week 13 邮件 + L10/L12 课件口径，取最严）：
> 可以用课件、可以从 Canvas 下载**自己以前提交的作业**当代码参考、可以 Google 查 API；
> **严禁任何 AI 代码生成**（ChatGPT / Gemini / Copilot，包括 Google 搜索里的 AI 答案）、
> 严禁 U 盘、严禁远程协助、开考后严禁手机。
> 所以这份手册的用法是**考前背写 + 理解**，不是带进考场现抄。

---

## 0. 考场 3 小时作战表（09:00–12:10）

| 时间 | 动作 | 关键提醒 |
|------|------|----------|
| 09:00–09:10 | 准备时间：登录实验室电脑，开 Android Studio，确认 AVD 能启动 | 别急着建工程，先确认模拟器/环境活着 |
| 0–15 min | 读题，写「一句话愿景 + 功能清单 + 几个屏幕」 | 教授课件原话：先定 vision，再定功能，再定 UI |
| 15–25 min | **New Project → Empty Activity**，包名 `com.example.xxx`，Language=Java，Minimum API 21/24 | 千万不要导入旧工程（教授明确要求新建空项目再复制代码） |
| 25–35 min | 等 Gradle sync 完成，直接 Run 一次空的 Hello World | 先确认「能跑」，再往里加功能。**这一步不能省** |
| 35–80 min | 写主界面 XML（布局+输入组件）→ `findViewById` → 按钮事件 → 核心计算 | 每加一块就 Run 一次，别攒到最后 |
| 80–120 min | 第二屏（结果页）：`Intent` + `putExtra` 传值，`AndroidManifest` 注册 | 忘了注册 Activity = 一点就崩 |
| 120–150 min | 加分项：SharedPreferences 记住输入 / SQLite 存历史 / RecyclerView 列表 / Menu | 按分值优先级来，能拿一分是一分 |
| 150–170 min | 收尾：输入校验（空值/非数字）、横屏 layout-land、字符串抽到 strings.xml | 校验是 T02 明确考过的点 |
| 170–180 min | 最后 Run 一遍 + 截图/录屏（如果要求）+ 提交 | 留 10 分钟缓冲，别卡在最后一秒 |

**心法**：Android 的痛点不是算法，是「一堆固定套路的样板代码 + 一堆忘记注册/忘记 findViewById 就崩的坑」。
把套路背下来，3 小时是够的。

---

## 1. 心智模型总对照表（先建立映射，再看细节）

| 你熟悉的前端 | Android 对应物 | 说明 |
|--------------|----------------|------|
| 一个页面（route / 小程序 page） | **Activity** | 一个 Activity = 一屏。必须在 `AndroidManifest.xml` 注册 |
| `pages.json` / `vue-router` 路由表 | **AndroidManifest.xml** | 声明有哪些 Activity、哪个是入口、要什么权限 |
| `router.push('/detail?id=1')` | **Intent + putExtra** | 显式 Intent 点名类；隐式 Intent 让系统挑 App |
| HTML 模板 | **res/layout/*.xml** | 结构和样式都写在这里，和逻辑分家 |
| CSS | **res/values/themes.xml + styles.xml + res/drawable/*.xml** | theme=全局样式，style=class，drawable=背景图/形状 |
| 一个 Vue 组件 / 小程序自定义组件 | **Fragment** | 不能独立存在，必须挂在 Activity 的容器里 |
| `v-for` 长列表 + 虚拟滚动 | **RecyclerView + Adapter + ViewHolder** | 滑出屏幕的 item 会被回收复用 |
| `document.querySelector('#id')` / `this.$refs.x` | **findViewById(R.id.x)** | 返回的是 View 对象，要强转成具体类型（Java 里用泛型自动推断） |
| `@click` / `addEventListener('click')` | **setOnClickListener(...)** | 没有模板语法糖，全部在 Java 里手写绑定 |
| `data()` 里的响应式状态 | **没有！** | Android 不响应式：改了数据必须自己 `setText()` / `notifyDataSetChanged()` |
| `localStorage` | **SharedPreferences** | 键值对，只能存基本类型，明文 XML 文件 |
| IndexedDB / 后端数据库 | **SQLite（SQLiteOpenHelper 或 Room）** | 真·关系型数据库，要写 SQL |
| `fetch()` / `wx.request()` | **HttpURLConnection / OkHttp / Retrofit** | 必须放子线程，且要在 Manifest 申请 INTERNET 权限 |
| `<canvas>` + `ctx.fillRect()` | **自定义 View + onDraw(Canvas) + Paint** | Paint ≈ ctx 的样式状态 |
| `async/await` | **Thread / Executor + Handler** | 更原始：子线程干活，`Handler.post()` 把更新 UI 的任务丢回主线程 |
| `mounted()` | **onCreate() / onViewCreated()** | |
| 构建工具 webpack/vite | **Gradle（build.gradle）** | 依赖、SDK 版本、打包都在这 |
| `npm run build` 产物 dist | **app-debug.apk** | `gradlew assembleDebug` 生成 |

**最大的思维差异**：前端是「改数据 → 视图自动更新」，Android 是「改数据 → 你手动去更新视图」。
Vue 的 `{{ }}`、小程序的 `setData` 那种响应式，只有在用 DataBinding/LiveData/Compose 时才有。

---

## 2. 工程结构：一个文件该放哪里

```
AndroidDemo/                        ← 项目根（≈ 你的 npm 项目根目录）
├── settings.gradle                 ← 声明有哪些模块（≈ pnpm-workspace.yaml）
├── build.gradle                    ← 根构建脚本，声明插件版本
├── gradle.properties               ← Gradle 全局参数（JVM 内存、配置缓存）
├── local.properties                ← 本机 SDK 路径（gitignore，别提交）
├── gradle/libs.versions.toml       ← 依赖版本目录（≈ package.json 的 dependencies）
└── app/                            ← 应用模块
    ├── build.gradle                ← 模块构建脚本：applicationId / minSdk / 依赖
    └── src/main/
        ├── AndroidManifest.xml     ← ★ 路由表 + 全局配置
        ├── java/com/example/gradecalc/
        │   ├── MainActivity.java       ← 页面逻辑
        │   ├── ResultActivity.java
        │   ├── HistoryActivity.java
        │   ├── AboutFragment.java      ← 组件
        │   ├── GradeRecord.java        ← 数据模型（POJO）
        │   ├── GradeDbHelper.java      ← SQLite 封装
        │   ├── GradeAdapter.java       ← RecyclerView 适配器
        │   └── GradeBarChartView.java  ← 自定义 View
        └── res/
            ├── layout/             ← 竖屏布局（activity_main.xml, item_grade.xml…）
            ├── layout-land/        ← 横屏布局（同名文件，系统自动挑）
            ├── menu/               ← 菜单 XML
            ├── drawable/           ← 形状/矢量图/位图（≈ CSS 背景 + SVG）
            ├── mipmap/             ← App 图标（多分辨率）
            └── values/             ← strings.xml / colors.xml / dimens.xml / themes.xml / arrays.xml
                values-zh/          ← 中文本地化，同名 strings.xml
```

**资源引用两套写法，别搞混：**

| 场景 | 写法 | 例子 |
|------|------|------|
| 在 XML 里引用资源 | `@类型/名字` | `android:text="@string/btn_calc"`、`android:background="@drawable/bg_card"` |
| 在 Java 里引用资源 | `R.类型.名字` | `R.string.btn_calc`、`R.id.editName`、`R.layout.activity_main` |

`R.java` 是构建时自动生成的（`app/build/generated/source/r/...`），把每个资源映射成一个 int。
所以：**XML 里写错一个 id 名，Java 里 `R.id.xxx` 直接编译不过**——这是好事，比前端运行时才发现强。

---

## 3. AndroidManifest.xml —— 路由表 + 全局配置

前端类比：小程序的 `app.json`（pages 数组 + window 配置 + 权限声明）合体。

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- 权限声明（≈ 小程序 requiredPrivateInfos / 浏览器权限申请） -->
    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:icon="@drawable/ic_launcher"      <!-- App 图标 -->
        android:label="@string/app_name"          <!-- App 名字 -->
        android:supportsRtl="true"
        android:theme="@style/Theme.GradeCalc">   <!-- 全局主题，≈ 全局 CSS -->

        <!-- 入口 Activity：intent-filter 里的 MAIN + LAUNCHER 就是「桌面图标点我」 -->
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- 其它页面：不注册就 startActivity 直接崩（ActivityNotFoundException） -->
        <activity android:name=".ResultActivity" android:exported="false"
                  android:label="@string/title_result"
                  android:parentActivityName=".MainActivity" />
        <activity android:name=".HistoryActivity" android:exported="false"
                  android:label="@string/title_history" />
    </application>
</manifest>
```

**必背 5 个坑：**
1. `.MainActivity` 前面的点 = 相对包名（等于 `com.example.gradecalc.MainActivity`）。
2. **新建的 Activity 一定要在这里注册**，Android Studio 用「New > Activity」建会自动加，手抄代码时最容易漏。
3. 入口必须有 `intent-filter` 的 `MAIN` + `LAUNCHER`，否则桌面看不到图标。
4. `android:exported` 在 targetSdk 31+ 是**必填**的（有 intent-filter 就写 true，内部页面写 false）。
5. 要联网就得写 `<uses-permission android:name="android.permission.INTERNET" />`，忘了就是 `SecurityException`。

四大组件（L02 考点）都在 Manifest 里声明：`<activity>`、`<service>`、`<receiver>`、`<provider>`。

---

## 4. Activity 与「路由跳转」：Intent

### 4.1 Activity 骨架（每个页面都长这样）

```java
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);          // 必须先调 super
        setContentView(R.layout.activity_main);      // ≈ 把 template 渲染上屏
        // 之后才 findViewById、绑事件、读数据
    }
}
```

`setContentView()` 做的事：把 `res/layout/activity_main.xml` **inflate**（解析 XML → 造出 View 对象树）→ 设为当前窗口内容。
≈ Vue 把 template 编译成真实 DOM 再 `mount('#app')`。

### 4.2 显式 Intent：站内路由（点名要哪个页面）

```java
Intent intent = new Intent(this, ResultActivity.class);   // 从哪 → 到哪
intent.putExtra("extra_name", name);                      // 带参数（≈ query / params）
intent.putExtra("extra_total", 87.5);                     // 支持 int/long/double/boolean/String/Serializable
startActivity(intent);                                    // ≈ router.push()
```

对面接收：

```java
Intent intent = getIntent();
String name   = intent.getStringExtra("extra_name");      // 可能为 null，要判
double total  = intent.getDoubleExtra("extra_total", 0);  // 基本类型必须给默认值
boolean flag  = intent.getBooleanExtra("extra_flag", false);
```

> ⚠️ `getDoubleExtra` 第二个参数是**必填的默认值**，因为 double 不能是 null；
> `getStringExtra` 没有默认值参数，取不到就返回 null，用之前要判空。

### 4.3 隐式 Intent：不点名，让系统挑一个能干的 App

```java
// 打开网页（≈ window.open）
startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("https://developer.android.com/reference")));

// 分享文本（≈ 调起系统分享面板）
Intent share = new Intent(Intent.ACTION_SEND);
share.setType("text/plain");
share.putExtra(Intent.EXTRA_SUBJECT, "我的成绩");
share.putExtra(Intent.EXTRA_TEXT, "我考了 87.5 分");
startActivity(Intent.createChooser(share, "分享到"));

// 打电话 / 发短信 / 发邮件
startActivity(new Intent(Intent.ACTION_DIAL, Uri.parse("tel:10086")));
```

隐式 Intent 还能被别人接住：在 Manifest 里给 Activity 加 `<intent-filter>` 声明
`<action>` / `<category>` / `<data android:mimeType="image/jpeg"/>`，就表示「我能处理这类请求」。

### 4.4 返回与回传

```java
finish();                       // ≈ router.back()，销毁当前 Activity
setResult(RESULT_OK, data);     // 回传结果给上一页（配合 startActivityForResult / ActivityResultLauncher）
```

### 4.5 返回栈（Back Stack，L08 考点）

`startActivity` 会把新页面**压栈**，按返回键**出栈**。
所以 A→B→C 之后连按两次返回会回到 A。想「跳过去并清掉中间页」，用
`intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)`。

---

## 5. 生命周期（Activity / Fragment）

### 5.1 Activity 七个回调

```
        onCreate() → onStart() → onResume()  ← 运行中（Running / Resumed）
                                    ↓
                                onPause()     ← 失去焦点（弹窗/来电/锁屏），还看得见
                                    ↓
                                onStop()      ← 完全看不见
                              ↙        ↘
                    onRestart()        onDestroy()
                        ↓                   ↓
                    onStart()            结束（回到 onCreate 是「重建」）
```

| 回调 | 什么时候 | 该干什么 | 前端类比 |
|------|----------|----------|----------|
| `onCreate()` | 实例第一次创建 | `setContentView`、`findViewById`、初始化数据、注册监听 | `created()` + `mounted()` |
| `onStart()` | 从不可见 → 可见 | 轻量 UI 刷新 | 页面 show |
| `onResume()` | 拿到焦点，可交互 | 开始动画、恢复相机、重新查库刷列表 | 小程序 `onShow` |
| `onPause()` | 失去焦点（还可见） | 暂停动画、释放相机；**别在这里做耗时操作** | 小程序 `onHide` |
| `onStop()` | 完全不可见 | 保存草稿、停掉刷新 | `onHide` |
| `onRestart()` | 从 stop 回来（首次不算） | 银行 App 在这里要求重新登录 | — |
| `onDestroy()` | 被销毁 | **清理线程/Handler/数据库**，防内存泄漏 | `unmounted()` |

**四个必背场景（考试爱考）：**

| 场景 | 回调顺序 |
|------|----------|
| 首次启动 | `onCreate → onStart → onResume` |
| 打开另一个 Activity 后按返回键回来 | `onPause → onStop → onRestart → onStart → onResume` |
| **旋转屏幕** | `onPause → onStop → onDestroy → onCreate → onStart → onResume`（Activity 被销毁重建！） |
| 按 Home 键 | `onPause → onStop` |

### 5.2 旋转屏幕会丢数据 → Bundle 保存状态

因为旋转会销毁重建 Activity，输入框内容默认全丢。想留住：

```java
@Override
protected void onSaveInstanceState(Bundle outState) {
    super.onSaveInstanceState(outState);
    outState.putString("state_name", editName.getText().toString());
    outState.putInt("state_coursework", seekCoursework.getProgress());
}

// onCreate(Bundle savedInstanceState) 里取出来
if (savedInstanceState != null) {
    editName.setText(savedInstanceState.getString("state_name", ""));
    seekCoursework.setProgress(savedInstanceState.getInt("state_coursework", 80));
}
```

> Bundle 只放**少量 UI 状态**（几个字符串/数字）。大数据（历史记录）放 SQLite，用户偏好放 SharedPreferences。
> 另一种偷懒做法：Manifest 里给 Activity 加 `android:configChanges="orientation|screenSize"`，
> 旋转时就不重建了（但要自己重写 `onConfigurationChanged`）。**考试推荐用 Bundle**，因为那是课件教的正解。

### 5.3 Fragment 生命周期（比 Activity 多三个）

```
onAttach() → onCreate() → onCreateView() → onViewCreated() → onStart() → onResume()
                                    ↓
onDetach() ← onDestroy() ← onDestroyView() ← onStop() ← onPause()
```

| 回调 | 干什么 |
|------|--------|
| `onAttach()` | 挂到宿主 Activity 上，拿到 Context；此时**还没有布局**，不能 findViewById |
| `onCreateView()` | **inflate 自己的布局并 return 根 View**（只干这一件事） |
| `onViewCreated()` | View 已就绪，在这里 `view.findViewById(...)` + 绑事件（≈ mounted） |
| `onDestroyView()` | View 被移除，清理 View 相关引用 |
| `onDetach()` | 与宿主解除关联 |

---

## 6. 布局与组件（XML ≈ HTML + CSS）

### 6.1 布局容器（ViewGroup）选型

| 容器 | 作用 | 前端类比 | 什么时候用 |
|------|------|----------|-----------|
| `LinearLayout` | 单方向排列（horizontal/vertical） | `display:flex` + `flex-direction` | 首选，简单行列 |
| `ConstraintLayout` | 用「约束」定位，层级扁平 | 一堆 `position:absolute` + 对齐规则 | 复杂界面、想避免嵌套过深（**官方推荐**） |
| `FrameLayout` | 只放一个子 View，可叠层 | `position:relative` + 子元素 absolute 叠一起 | Fragment 容器、加个浮层 |
| `RelativeLayout` | 相对兄弟/父级定位 | 老式 absolute 布局 | 老代码里常见，新代码用 Constraint |
| `ScrollView` | 让内容可上下滚动 | `overflow-y:auto` | 表单页必套（一屏放不下） |
| `TableLayout` | 行列表格 | `<table>` | 规整的表格式数据 |
| `RecyclerView` | 大量数据列表 | 虚拟滚动长列表 | 列表一律用它，别用 ListView |

> 课件原话：**能用 LinearLayout 解决就别上 ConstraintLayout**，别过度设计；
> 但嵌套太深会卡（View 会被反复 measure），这时才换 ConstraintLayout。

### 6.2 尺寸三件套 + 单位

```xml
android:layout_width="match_parent"   <!-- = width: 100% -->
android:layout_width="wrap_content"   <!-- = width: auto，内容多宽就多宽 -->
android:layout_width="200dp"          <!-- 固定尺寸 -->
android:layout_width="0dp"            <!-- 配合 layout_weight，= flex: 1 -->
android:layout_weight="2"             <!-- 剩余空间按权重分配（flex-grow） -->
```

| 单位 | 含义 | 用在哪 |
|------|------|--------|
| `dp` | 密度无关像素，160dpi 屏上 1dp=1px | **所有控件尺寸、间距** |
| `sp` | 会跟随用户系统字体大小缩放 | **只用于字体大小** |
| `px` | 物理像素 | 基本别用，换设备就崩 |
| `pt` / `mm` / `in` | 物理单位 | 基本别用 |

换算：`px = dp × (dpi / 160)`。

### 6.3 通用属性 ↔ CSS 对照

| Android 属性 | CSS / 前端等价 | 备注 |
|--------------|----------------|------|
| `android:id="@+id/editName"` | `id="editName"` | `@+id` 是「新建一个 id」，`@id` 是「引用已有 id」 |
| `android:text="@string/btn_calc"` | `textContent` | 一律抽到 strings.xml，别硬编码（课件明确列为 Bad Example） |
| `android:hint="请输入"` | `placeholder` | 只有 EditText 有 |
| `android:textSize="16sp"` | `font-size` | 用 sp |
| `android:textColor="@color/text_main"` | `color` | |
| `android:textStyle="bold"` | `font-weight:bold` | bold / italic / normal |
| `android:background="@drawable/bg_card"` | `background` | 可以是颜色、shape、图片 |
| `android:padding="16dp"` | `padding` | **内容到边框**的距离 |
| `android:layout_margin="8dp"` | `margin` | **边框到兄弟**的距离（注意带 layout_ 前缀） |
| `android:gravity="center"` | `text-align` + `vertical-align` | 控制**自己内容**怎么摆 |
| `android:layout_gravity="end"` | `align-self` | 控制**自己在父容器**里怎么摆 |
| `android:visibility="gone"` | `display:none` | `gone`=不占位；`invisible`=占位但看不见（≈visibility:hidden） |
| `android:enabled="false"` | `disabled` | |
| `android:orientation="vertical"` | `flex-direction:column` | 只有 LinearLayout/RadioGroup 有 |
| `android:layout_weight` | `flex-grow` | 必须配 `0dp` 才好使 |

**padding vs margin 记忆法**：`padding` 是自己肚子里的空间，`margin` 是自己和别人之间的距离。
带 `layout_` 前缀的属性都是「我在父容器里的表现」，由**父容器**解释；不带前缀的由**自己**解释。

### 6.4 ConstraintLayout 的约束怎么写（L03 重点）

命名格式：`layout_constraint<自己的边>_to<目标>Of="<目标id 或 parent>"`

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:id="@+id/textTotal"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />   <!-- 左右都约束到 parent = 水平居中 -->

    <Button
        android:id="@+id/btnShare"
        android:layout_width="0dp"                      <!-- 0dp = match_constraint，≈ flex:1 -->
        android:layout_height="wrap_content"
        app:layout_constraintTop_toBottomOf="@id/textTotal"   <!-- 我在它下面 -->
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toStartOf="@id/btnBack" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

三个命名空间（L03 课件）：`android:` = 系统核心属性，`app:` = 第三方库（constraintlayout/material）属性，`tools:` = 只给 Android Studio 预览用、不打包。

---

## 7. 输入组件全家桶（考场最可能考的部分）

| 组件 | XML 标签 | 前端类比 | 取值 / 设值 |
|------|----------|----------|-------------|
| 文本框 | `<EditText>` | `<input>` / `<textarea>` | `edit.getText().toString()` / `edit.setText("x")` |
| 按钮 | `<Button>` | `<button>` | `btn.setText(...)` |
| 图片按钮 | `<ImageButton>` | `<button>` 里塞图 | `img.setImageResource(R.drawable.x)` |
| 文本 | `<TextView>` | `<span>` | `tv.setText(...)`、`tv.getText()` |
| 图片 | `<ImageView>` | `<img>` | `iv.setImageResource(R.drawable.x)` |
| 下拉框 | `<Spinner>` | `<select>` | 见下方完整代码 |
| 单选组 | `<RadioGroup>` + `<RadioButton>` | `<input type="radio">` 组 | `group.getCheckedRadioButtonId()` |
| 复选框 | `<CheckBox>` | `<input type="checkbox">` | `cb.isChecked()` / `cb.setChecked(true)` |
| 开关 | `<Switch>` / `<SwitchCompat>` / `<ToggleButton>` | iOS 风格开关 | `sw.isChecked()` |
| 拖动条 | `<SeekBar>` | `<input type="range">` | `sb.getProgress()`（0..max 的 int） |
| 评分星 | `<RatingBar>` | 五星评价 | `rb.getRating()`（float） |
| 进度条 | `<ProgressBar>` | loading 圈 | `setVisibility(VISIBLE/GONE)` |
| 日期选择 | `DatePickerDialog` | 日期弹层 | 见下方 |

### 7.1 EditText：inputType 决定弹什么键盘

```xml
<EditText android:id="@+id/editName"
    android:layout_width="match_parent" android:layout_height="wrap_content"
    android:hint="@string/hint_name"
    android:inputType="textPersonName" />
```

常用 `inputType`：`text` / `textPersonName` / `textEmailAddress` / `textPassword` /
`number` / `numberDecimal`（允许小数）/ `phone` / `textMultiLine`。
**数字输入一定要写 `numberDecimal`**，否则用户能输入字母，你 `Double.parseDouble` 就崩。

取值 + 校验（T02 明确考过「空值会让 App 崩」）：

```java
String text = editFinal.getText().toString().trim();
if (TextUtils.isEmpty(text)) {                 // 判空
    editFinal.setError("分数不能为空");          // setError 会在输入框下方显示红字，超好用
    return;
}
try {
    double value = Double.parseDouble(text);
    if (value < 0 || value > 100) {
        editFinal.setError("分数必须在 0-100 之间");
        return;
    }
} catch (NumberFormatException e) {
    editFinal.setError("请输入数字");
    return;
}
```

### 7.2 Spinner：下拉选择（三步）

**第一步**，数据放 `res/values/arrays.xml`：

```xml
<resources>
    <string-array name="course_list">
        <item>EE5415 Mobile Apps Design</item>
        <item>CS5285 Intro to Cybersecurity</item>
    </string-array>
</resources>
```

**第二步**，XML 里放 Spinner：

```xml
<Spinner android:id="@+id/spinnerCourse"
    android:layout_width="match_parent" android:layout_height="wrap_content" />
```

**第三步**，Java 里接 Adapter：

```java
Spinner spinner = findViewById(R.id.spinnerCourse);
ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(
        this, R.array.course_list, android.R.layout.simple_spinner_item);
adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
spinner.setAdapter(adapter);

// 取选中项
String selected = spinner.getSelectedItem().toString();
int index = spinner.getSelectedItemPosition();
// 设默认选中
spinner.setSelection(1);
// 监听变化
spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
    @Override public void onItemSelected(AdapterView<?> parent, View view, int position, long id) { }
    @Override public void onNothingSelected(AdapterView<?> parent) { }
});
```

> `android.R.layout.simple_spinner_item` 是**系统自带**的行布局（注意是 `android.R`，不是 `R`）。
> 用 `List<String>` 当数据源时用另一个构造函数：
> `new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, myList)`。

### 7.3 RadioGroup：单选

```xml
<RadioGroup android:id="@+id/radioScale"
    android:layout_width="match_parent" android:layout_height="wrap_content"
    android:orientation="horizontal">
    <RadioButton android:id="@+id/radioScale100" android:text="@string/scale_100" android:checked="true"
        android:layout_width="wrap_content" android:layout_height="wrap_content" />
    <RadioButton android:id="@+id/radioScale4" android:text="@string/scale_4"
        android:layout_width="wrap_content" android:layout_height="wrap_content" />
</RadioGroup>
```

```java
RadioGroup group = findViewById(R.id.radioScale);
group.setOnCheckedChangeListener((g, checkedId) -> {
    if (checkedId == R.id.radioScale4) {          // ★ 不能用 switch(R.id.x)，见下方警告
        scaleMode = GradeScale.SCALE_4;
    } else {
        scaleMode = GradeScale.SCALE_100;
    }
});
// 主动读取 / 设置
int id = group.getCheckedRadioButtonId();
group.check(R.id.radioScale100);
```

> ⚠️ **AGP 8+ 的大坑**：`android.nonFinalResIds` 默认开启，`R.id.xxx` 不再是编译期常量，
> `switch (id) { case R.id.a: ... }` 会**编译报错**（constant expression required）。
> 一律写成 `if (id == R.id.a) {...} else if (...)`。菜单处理同理。

### 7.4 CheckBox / Switch

```java
CheckBox checkBonus = findViewById(R.id.checkBonus);
boolean bonus = checkBonus.isChecked();
checkBonus.setChecked(true);
checkBonus.setOnCheckedChangeListener((buttonView, isChecked) -> { /* 变化时回调 */ });

SwitchCompat switchDetail = findViewById(R.id.switchDetail);   // androidx.appcompat.widget.SwitchCompat
switchDetail.setOnCheckedChangeListener((v, isChecked) ->
        layoutDetail.setVisibility(isChecked ? View.VISIBLE : View.GONE));   // ≈ v-show
```

### 7.5 SeekBar（滑动条）

```xml
<SeekBar android:id="@+id/seekCoursework"
    android:layout_width="match_parent" android:layout_height="wrap_content"
    android:max="100" android:progress="80" />
```

```java
seek.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
    @Override public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
        textValue.setText(progress + " 分");     // 拖动过程中实时回调
    }
    @Override public void onStartTrackingTouch(SeekBar seekBar) { }   // 手指按下
    @Override public void onStopTrackingTouch(SeekBar seekBar) { }    // 手指松开
});
int value = seek.getProgress();
```

### 7.6 DatePickerDialog（选日期）

```java
findViewById(R.id.btnPickDate).setOnClickListener(v -> {
    Calendar c = Calendar.getInstance();
    new DatePickerDialog(this, (view, year, month, dayOfMonth) -> {
        // month 从 0 开始！0=一月，这是经典坑
        String date = String.format(Locale.US, "%d-%02d-%02d", year, month + 1, dayOfMonth);
        textDate.setText(date);
    }, c.get(Calendar.YEAR), c.get(Calendar.MONTH), c.get(Calendar.DAY_OF_MONTH)).show();
});
```

---

## 8. 样式：drawable / style / theme（≈ CSS 的三层）

| 层 | 文件 | 类比 | 作用范围 |
|----|------|------|----------|
| **theme** | `res/values/themes.xml` | 全局 CSS reset + 设计系统 | 整个 App / 单个 Activity |
| **style** | `res/values/themes.xml` 或 `styles.xml` | 一个 CSS class | 任意多个 View |
| **drawable** | `res/drawable/*.xml` 或 png | `background-image` / SVG / 圆角背景 | 单个 View 的背景 |

### 8.1 theme：全局基调

```xml
<resources>
    <!-- 继承 Material3 主题；DayNight = 自动跟随系统深色模式 -->
    <style name="Base.Theme.GradeCalc" parent="Theme.Material3.DayNight">
        <item name="colorPrimary">@color/primary</item>
    </style>
    <style name="Theme.GradeCalc" parent="Base.Theme.GradeCalc" />
</resources>
```

Manifest 里 `android:theme="@style/Theme.GradeCalc"` 引用它。
> 想没有顶部标题栏：parent 改成 `Theme.Material3.DayNight.NoActionBar`。
> **用了 AlertDialog / SwitchCompat / AppCompat 控件，theme 必须是 AppCompat 或 Material 系**，
> 否则会崩 `You need to use a Theme.AppCompat theme`。

### 8.2 style：可复用的 class

```xml
<style name="FieldLabel">
    <item name="android:layout_width">match_parent</item>
    <item name="android:layout_height">wrap_content</item>
    <item name="android:textSize">@dimen/text_label</item>
    <item name="android:textColor">@color/text_sub</item>
    <item name="android:layout_marginTop">@dimen/gap_mid</item>
</style>
```

用起来就一个属性：

```xml
<TextView style="@style/FieldLabel" android:text="@string/label_name" />
```

系统自带的样式用 `?android:attr/xxx` 引用，例如扁平文字按钮：
`style="?android:attr/buttonBarButtonStyle"`。

### 8.3 drawable shape：纯 XML 画背景（不用切图）

`res/drawable/bg_card.xml`：

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="@color/card_bg" />          <!-- 填充色 = background-color -->
    <corners android:radius="12dp" />                 <!-- 圆角 = border-radius -->
    <stroke android:width="1dp" android:color="@color/primary" />  <!-- 边框 = border -->
    <padding android:left="12dp" android:top="12dp" android:right="12dp" android:bottom="12dp" />
</shape>
```

`android:shape` 可选：`rectangle` / `oval` / `line` / `ring`。

渐变：

```xml
<shape android:shape="rectangle">
    <gradient android:startColor="#3F51B5" android:endColor="#FF4081" android:angle="45" />
    <corners android:radius="16dp" />
</shape>
```

矢量图（≈ SVG），`res/drawable/ic_launcher.xml`：

```xml
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="48dp" android:height="48dp"
    android:viewportWidth="48" android:viewportHeight="48">
    <path android:fillColor="#3F51B5" android:pathData="M4,4h40v40H4z" />
</vector>
```

Java 里动态换背景：

```java
view.setBackgroundResource(R.drawable.bg_grade_pass);   // 换 drawable
view.setBackgroundColor(Color.RED);                     // 换纯色
imageView.setImageResource(R.drawable.bot_fit);          // ImageView 换图
```

### 8.4 mipmap vs drawable（T04 考点）

App **图标**放 `mipmap-*`（mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi 五套分辨率全打进 APK，
系统按设备挑最清晰的一套）；普通图片放 `drawable-*`（打包时会剔除不匹配的密度目录，APK 更小）。
Android Studio 里 `File → New → Image Asset` 能一键生成五套图标。

### 8.5 颜色与尺寸也要抽出来

```xml
<!-- res/values/colors.xml -->
<color name="primary">#3F51B5</color>
<!-- res/values/dimens.xml -->
<dimen name="padding_screen">16dp</dimen>
<dimen name="text_title">22sp</dimen>
```

引用：`@color/primary`、`@dimen/padding_screen`。
好处：改一处全局生效，且能按屏幕尺寸提供 `values-sw600dp/dimens.xml` 变体（平板用更大间距）。

---

## 9. Java 操作组件：findViewById 与常用 API

```java
// 声明成员变量（≈ Vue 的 ref）
private EditText editName;
private TextView textTotal;

@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);        // ★ 必须先 setContentView 再 findViewById

    editName = findViewById(R.id.editName);        // 类型要和 XML 里的标签一致
    textTotal = findViewById(R.id.textTotal);
}
```

**常用 setter / getter 速查：**

| 目的 | 代码 |
|------|------|
| 改文字 | `tv.setText("hi")` / `tv.setText(R.string.app_name)` |
| 取文字 | `edit.getText().toString()`（**别忘了 toString**，getText 返回的是 Editable） |
| 格式化文字 | `tv.setText(getString(R.string.format_total, 87.5))` |
| 显示/隐藏 | `v.setVisibility(View.VISIBLE / INVISIBLE / GONE)` |
| 可用/禁用 | `btn.setEnabled(false)` |
| 换颜色 | `tv.setTextColor(Color.RED)` / `tv.setTextColor(ContextCompat.getColor(this, R.color.primary))` |
| 换背景 | `v.setBackgroundResource(R.drawable.bg_card)` |
| 改大小 | `tv.setTextSize(20)`（注意：代码里单位是 sp 数值） |
| 提示红字 | `edit.setError("不能为空")` |
| 请求焦点 | `edit.requestFocus()` |

`getString(R.string.format_total, 87.5)` 对应
`<string name="format_total">总评分数：%1$.1f</string>`。
格式化占位符：`%1$s` 字符串、`%1$d` 整数、`%1$.1f` 一位小数、`%%` 表示字面量百分号。
如果一条字符串里有多个裸 `%` 又不用来格式化，加 `formatted="false"`：

```xml
<string name="main_subtitle" formatted="false">平时 30% + 期中 30% + 期末 40%</string>
```
否则 aapt 会警告 `Multiple substitutions specified in non-positional format`。

**ViewBinding（L12，可选加分项）**：`build.gradle` 里开 `buildFeatures { viewBinding true }`，
之后可以用 `ActivityMainBinding binding = ActivityMainBinding.inflate(getLayoutInflater()); setContentView(binding.getRoot());`
再 `binding.editName.setText(...)`——**类型安全、免 findViewById、免判空**。
考场建议：先用 findViewById（更稳、你更熟），有时间再换。

---

## 10. 事件：Android 没有 @click，全靠监听器

**万能公式：`view.setXxxListener(回调)`**

```java
// 1) 点击（≈ @click）
btnCalc.setOnClickListener(new View.OnClickListener() {
    @Override public void onClick(View v) { doSomething(); }
});
// Lambda 简写（Java 8+，推荐）
btnCalc.setOnClickListener(v -> doSomething());

// 2) 长按（返回 true = 我处理了，别再往下传）
textTip.setOnLongClickListener(v -> { Toast.makeText(this, "长按了", Toast.LENGTH_SHORT).show(); return true; });

// 3) 在 XML 里直接绑（≈ @click="fn"，但要写方法名）
//    <Button android:onClick="onCalcClick" .../>
public void onCalcClick(View view) { /* 必须是 public void 且接收一个 View 参数 */ }

// 4) 焦点变化
edit.setOnFocusChangeListener((v, hasFocus) -> { });

// 5) 按键
edit.setOnKeyListener((v, keyCode, event) -> false);
```

**View 的四大监听接口（T03 原文）：**
`OnClickListener.onClick()` / `OnLongClickListener.onLongClick()` /
`OnFocusChangeListener.onFocusChange()` / `OnKeyListener.onKey()`。

不同控件有各自的监听器：SeekBar→`OnSeekBarChangeListener`，RadioGroup→`OnCheckedChangeListener`，
Spinner→`OnItemSelectedListener`，RecyclerView item→自己在 Adapter 里绑（见第 12 节）。

**事件驱动模型（L02 考点）**：Android 是事件驱动的，不是从头跑到尾的过程式。
套路永远是 `Event → Listener / Callback → Your Code`。生命周期回调（onCreate/onResume…）本质上也是系统调你的回调。

### 10.1 三种提示（T03 考点，考场加分神器）

```java
// Toast：右下角小提示，自动消失，不需要用户操作
Toast.makeText(this, "已保存", Toast.LENGTH_SHORT).show();     // LENGTH_SHORT / LENGTH_LONG

// Snackbar：底部条，可以带一个操作按钮（Material 风格）
Snackbar.make(findViewById(R.id.scrollRoot), R.string.msg_saved, Snackbar.LENGTH_SHORT)
          .setAction("撤销", v -> undo())
          .show();

// AlertDialog：模态弹窗，用户不点掉就不能继续
new AlertDialog.Builder(this)                     // androidx.appcompat.app.AlertDialog
    .setTitle("关于")
    .setMessage("GradeCalc v1.0")
    .setPositiveButton("确定", (dialog, which) -> { /* 点确定 */ })
    .setNegativeButton("取消", null)               // null = 什么都不做，自动关闭
    .show();                                       // ★ 别忘了 .show()，Builder 不会自己弹
```

> `AlertDialog` 一定要 import `androidx.appcompat.app.AlertDialog`，
> 用成 `android.app.AlertDialog` 在 Material 主题下可能崩。

---

## 11. Fragment：可热插拔的 UI 组件

### 11.1 写一个 Fragment（对应 `AboutFragment.java`）

```java
public class AboutFragment extends Fragment {

    public static final String TAG = "about_fragment";

    /** 官方推荐：用静态工厂方法传参（≈ props），不要自己写带参构造函数，
     *  因为系统重建 Fragment 时只会调无参构造。 */
    public static AboutFragment newInstance(String title) {
        AboutFragment f = new AboutFragment();
        Bundle args = new Bundle();
        args.putString("arg_title", title);
        f.setArguments(args);
        return f;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // 只干一件事：inflate 布局并返回根 View（第三个参数必须是 false）
        return inflater.inflate(R.layout.fragment_about, container, false);
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        // ★ Fragment 里必须用 view.findViewById，不能直接 findViewById
        TextView title = view.findViewById(R.id.textAboutTitle);
        Bundle args = getArguments();
        if (args != null) title.setText(args.getString("arg_title"));

        view.findViewById(R.id.btnCloseFragment).setOnClickListener(v ->
                requireActivity().getSupportFragmentManager().popBackStack());
    }
}
```

### 11.2 两种挂载方式

**方式 A：静态，在 XML 里写死**（简单，但不能运行时替换）

```xml
<androidx.fragment.app.FragmentContainerView
    android:id="@+id/fragment_list"
    android:name="com.example.gradecalc.AboutFragment"
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />
```

**方式 B：动态，用 FragmentManager + FragmentTransaction**（推荐，能增删换）

```xml
<!-- 布局里放一个空容器 -->
<FrameLayout android:id="@+id/fragmentContainer"
    android:layout_width="match_parent" android:layout_height="wrap_content" />
```

```java
getSupportFragmentManager().beginTransaction()
        .replace(R.id.fragmentContainer, AboutFragment.newInstance("关于"), AboutFragment.TAG)
        .addToBackStack(null)     // 加入返回栈，按返回键能退回（≈ router.push 而不是 replace）
        .commit();

// 手动退栈（≈ router.back()）
getSupportFragmentManager().popBackStack();

// 找到已挂载的 Fragment
AboutFragment f = (AboutFragment) getSupportFragmentManager().findFragmentByTag(AboutFragment.TAG);
```

事务四步（L08 原文）：`beginTransaction()` → `add/remove/replace` → `addToBackStack()`（可选） → `commit()`。

### 11.3 Fragment 和 Activity 通信：接口回调

Fragment 里定义接口，Activity 实现它，`onAttach()` 时把 Activity 强转成该接口
（L08 的 `ItemListFragment.OnItemSelectedListener` 例子）。这就是「子组件 emit 事件给父页面」的 Android 版。

```java
// Fragment 内
public interface OnItemSelectedListener { void onItemSelected(String item); }
private OnItemSelectedListener listener;

@Override public void onAttach(Context context) {
    super.onAttach(context);
    if (context instanceof OnItemSelectedListener) listener = (OnItemSelectedListener) context;
    else throw new ClassCastException(context + " must implement OnItemSelectedListener");
}
// Activity：implements ItemListFragment.OnItemSelectedListener 并实现方法
```

### 11.4 什么时候用 Fragment 而不是新 Activity？

- 平板/横屏要左右分栏（列表 + 详情）→ Fragment
- 底部 Tab、侧滑抽屉、ViewPager 翻页 → Fragment
- 一个可复用的 UI 块（商品卡片、评论列表）→ Fragment
- 手机上的独立一屏 → 直接新 Activity 更简单（**考试首选**）

---

## 12. RecyclerView：长列表（v-for + 虚拟滚动）

### 12.1 为什么不用 ListView

`ListView` 没被废弃但**不再推荐**。RecyclerView 会「回收」滑出屏幕的 item View 放进池子里复用，
只创建「屏幕能显示的数量 + 几个缓冲」，所以 1 万条数据也不卡。
自动售货机类比（L12 原话）：RecyclerView = 机器，Adapter = 补货员，ViewHolder = 出货槽。

### 12.2 四步套路（必背）

**第一步**：布局里放 RecyclerView

```xml
<androidx.recyclerview.widget.RecyclerView
    android:id="@+id/recyclerHistory"
    android:layout_width="match_parent"
    android:layout_height="0dp"
    android:layout_weight="1"
    android:scrollbars="vertical" />
```

**第二步**：写单条 item 的布局 `res/layout/item_grade.xml`（≈ v-for 里的 template）

```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"        <!-- ★ 宽度必须 match_parent -->
    android:layout_height="wrap_content"       <!-- ★ 高度 wrap_content -->
    android:orientation="horizontal"
    android:background="@drawable/bg_grade_pass"
    android:padding="@dimen/gap_mid">
    <TextView android:id="@+id/textItemName" ... />
    <TextView android:id="@+id/textItemTotal" ... />
</LinearLayout>
```

**第三步**：写 Adapter（含 ViewHolder），重写三个方法

```java
public class GradeAdapter extends RecyclerView.Adapter<GradeAdapter.GradeViewHolder> {

    public interface OnItemClickListener {
        void onItemClick(GradeRecord record, int position);
        void onItemLongClick(GradeRecord record, int position);
    }

    private List<GradeRecord> data;
    private final OnItemClickListener listener;

    public GradeAdapter(List<GradeRecord> data, OnItemClickListener listener) {
        this.data = data;
        this.listener = listener;
    }

    /** 数据换了调它（≈ 改完数组手动触发更新） */
    public void setData(List<GradeRecord> data) {
        this.data = data;
        notifyDataSetChanged();
    }

    @Override
    public GradeViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        // 把 item XML 变成 View 对象（≈ 克隆一份模板）
        View row = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_grade, parent, false);
        return new GradeViewHolder(row);
    }

    @Override
    public void onBindViewHolder(GradeViewHolder holder, int position) {
        GradeRecord r = data.get(position);
        holder.textName.setText(r.getStudentName());
        holder.textTotal.setText(String.format(Locale.US, "%.1f", r.getTotal()));
        holder.itemView.setBackgroundResource(
                r.isPass() ? R.drawable.bg_grade_pass : R.drawable.bg_grade_fail);

        // ★ 事件绑在 bind 里，因为 ViewHolder 会被复用，不能只绑一次
        holder.itemView.setOnClickListener(v -> {
            int pos = holder.getBindingAdapterPosition();     // 别用闭包里的 position（复用时是旧值）
            if (listener != null && pos != RecyclerView.NO_POSITION) {
                listener.onItemClick(data.get(pos), pos);
            }
        });
        holder.itemView.setOnLongClickListener(v -> {
            int pos = holder.getBindingAdapterPosition();
            if (listener != null && pos != RecyclerView.NO_POSITION) {
                listener.onItemLongClick(data.get(pos), pos);
            }
            return true;
        });
    }

    @Override
    public int getItemCount() { return data == null ? 0 : data.size(); }

    /** ViewHolder：findViewById 只做一次，之后反复复用 */
    static class GradeViewHolder extends RecyclerView.ViewHolder {
        final TextView textName;
        final TextView textTotal;
        GradeViewHolder(View itemView) {
            super(itemView);
            textName = itemView.findViewById(R.id.textItemName);
            textTotal = itemView.findViewById(R.id.textItemTotal);
        }
    }
}
```

**第四步**：Activity 里装起来

```java
RecyclerView recyclerView = findViewById(R.id.recyclerHistory);
recyclerView.setLayoutManager(new LinearLayoutManager(this));    // ★ 不设 LayoutManager 列表什么都不显示！
adapter = new GradeAdapter(records, this);                        // this 实现了 OnItemClickListener
recyclerView.setAdapter(adapter);
```

LayoutManager 三选一：

```java
new LinearLayoutManager(this)                     // 竖列表
new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false)  // 横列表
new GridLayoutManager(this, 2)                    // 两列九宫格
```

Activity 实现回调接口：

```java
public class HistoryActivity extends AppCompatActivity implements GradeAdapter.OnItemClickListener {
    @Override public void onItemClick(GradeRecord record, int position) { /* 弹详情对话框 */ }
    @Override public void onItemLongClick(GradeRecord record, int position) { /* Toast */ }
}
```

### 12.3 刷新数据的正确姿势

```java
private void reload() {
    List<GradeRecord> latest = dbHelper.getAllRecords();
    records.clear();
    records.addAll(latest);
    adapter.setData(records);        // 内部调 notifyDataSetChanged()
}

@Override protected void onResume() {
    super.onResume();
    reload();                        // 每次回到这一屏都重新查库，保证看到新数据
}
```

> 进阶（L12 后半，考试基本用不上）：`ListAdapter` + `DiffUtil.ItemCallback` 能只更新变化的行，
> 用 `adapter.submitList(newList)` 提交；多种 item 类型则重写 `getItemViewType()` 并在
> `onCreateViewHolder` 里按 viewType inflate 不同布局。

---

## 13. 数据存储：四种方案怎么选

| 方案 | 存什么 | 类比 | 位置 | 需要权限吗 |
|------|--------|------|------|-----------|
| **SharedPreferences** | 少量键值对（用户名、设置、开关） | `localStorage` | `/data/data/<包名>/shared_prefs/*.xml` | 否（应用私有） |
| **内部文件** | 中小量私有数据（草稿、日志） | Node 的 `fs.writeFile` | `/data/data/<包名>/files/` | 否 |
| **外部文件** | 大文件、用户可见（导出的图片） | 下载到用户目录 | `/storage/emulated/0/Android/data/<包名>/files/` | 应用私有的不需要 |
| **SQLite** | 结构化、多行、要查询（历史记录） | IndexedDB / 后端数据库 | `/data/data/<包名>/databases/*.db` | 否 |

### 13.1 SharedPreferences（T02 考过：记住用户上次输入）

```java
// 写
SharedPreferences prefs = getSharedPreferences("gradecalc_prefs", MODE_PRIVATE);
prefs.edit()
     .putString("student_name", name)
     .putInt("course_index", 2)
     .putBoolean("bonus", true)
     .putFloat("last_total", 87.5f)
     .apply();          // ★ apply() 异步落盘不阻塞 UI；commit() 同步并返回 boolean

// 读（第二个参数是「读不到时的默认值」，必填）
String name  = prefs.getString("student_name", "");
int index    = prefs.getInt("course_index", 0);
boolean b    = prefs.getBoolean("bonus", false);

// 删
prefs.edit().remove("student_name").apply();
prefs.edit().clear().apply();
```

两种获取方式：
- `getPreferences(MODE_PRIVATE)`：当前 Activity 私有的一个文件
- `getSharedPreferences("名字", MODE_PRIVATE)`：全 App 共享的多个文件（跨 Activity/Service/Fragment）

`MODE_PRIVATE`（值 0）= 只有本 App 能读写，是**现在唯一还允许的模式**
（`MODE_WORLD_READABLE` 等从 Android 7 起废弃）。
⚠️ SharedPreferences **不加密**，别存密码/信用卡（要存就用 `EncryptedSharedPreferences`）。
现代替代方案是 Jetpack 的 `DataStore`。

### 13.2 内部文件读写

```java
// 写
try {
    FileOutputStream fOut = openFileOutput("notes.txt", MODE_PRIVATE);
    OutputStreamWriter osw = new OutputStreamWriter(fOut, StandardCharsets.UTF_8);
    osw.write("hello");
    osw.close();                       // close 会自动 flush
} catch (IOException e) { e.printStackTrace(); }

// 读
try {
    FileInputStream fIn = openFileInput("notes.txt");
    BufferedReader reader = new BufferedReader(new InputStreamReader(fIn, StandardCharsets.UTF_8));
    StringBuilder sb = new StringBuilder();
    String line;
    while ((line = reader.readLine()) != null) sb.append(line).append('\n');
    reader.close();
} catch (IOException e) { /* 文件可能不存在，必须处理 FileNotFoundException */ }
```

只读的静态数据可以塞进 `res/raw/`，用 `getResources().openRawResource(R.raw.mydata)` 读。

### 13.3 SQLite：SQLiteOpenHelper（考场首选，零依赖）

对应工程文件 `GradeDbHelper.java`。三步：**建表 → 增删改 → 查（Cursor）**。

```java
public class GradeDbHelper extends SQLiteOpenHelper {

    private static final String DB_NAME = "grade_calc.db";
    private static final int DB_VERSION = 1;      // 改表结构就把这个数 +1，会触发 onUpgrade
    private static final String TABLE = "grade_records";

    public GradeDbHelper(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {     // 只在数据库第一次创建时执行一次
        db.execSQL("CREATE TABLE " + TABLE + " ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                + "ts TEXT NOT NULL,"
                + "student_name TEXT NOT NULL,"
                + "total REAL NOT NULL,"
                + "pass_flag INTEGER NOT NULL)");  // SQLite 没有 boolean，用 0/1
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE);
        onCreate(db);
    }

    /** 增：ContentValues 就是一个 key-value 的行数据 */
    public long insertRecord(GradeRecord r) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put("ts", r.getTimestamp());
        values.put("student_name", r.getStudentName());
        values.put("total", r.getTotal());
        values.put("pass_flag", r.isPass() ? 1 : 0);
        return db.insert(TABLE, null, values);
        // 有唯一约束、想「存在就覆盖」用：
        // db.insertWithOnConflict(TABLE, null, values, SQLiteDatabase.CONFLICT_REPLACE);
    }

    /** 查：Cursor 是游标，一行一行往下走 */
    public List<GradeRecord> getAllRecords() {
        List<GradeRecord> list = new ArrayList<>();
        SQLiteDatabase db = getReadableDatabase();
        Cursor cursor = db.query(TABLE, null, null, null, null, null, "id DESC");
        // query(表, 列, where, whereArgs, groupBy, having, orderBy)
        while (cursor.moveToNext()) {
            long id = cursor.getLong(cursor.getColumnIndexOrThrow("id"));
            String name = cursor.getString(cursor.getColumnIndexOrThrow("student_name"));
            double total = cursor.getDouble(cursor.getColumnIndexOrThrow("total"));
            boolean pass = cursor.getInt(cursor.getColumnIndexOrThrow("pass_flag")) == 1;
            list.add(...);
        }
        cursor.close();                            // ★ 必须关，否则 Logcat 报 Cursor leak
        return list;
    }

    /** 聚合查询用 rawQuery */
    public double getAverageTotal() {
        Cursor c = getReadableDatabase().rawQuery("SELECT AVG(total) FROM " + TABLE, null);
        double avg = 0;
        if (c.moveToFirst() && !c.isNull(0)) avg = c.getDouble(0);
        c.close();
        return avg;
    }

    /** 删：? 是占位符，值从 String[] 传进去（防 SQL 注入，别用字符串拼） */
    public void deleteRecord(long id) {
        getWritableDatabase().delete(TABLE, "id = ?", new String[]{String.valueOf(id)});
    }

    public void deleteAll() { getWritableDatabase().delete(TABLE, null, null); }
}
```

Activity 里用：

```java
GradeDbHelper dbHelper = new GradeDbHelper(this);   // 通常一个 Activity 建一次
dbHelper.insertRecord(record);
List<GradeRecord> all = dbHelper.getAllRecords();

@Override protected void onDestroy() {
    super.onDestroy();
    if (dbHelper != null) dbHelper.close();          // 别忘了关
}
```

SQL 四件套（CRUD）：

```sql
INSERT INTO grade_records (name, total) VALUES ("Peter", 87.5);
SELECT * FROM grade_records;
UPDATE grade_records SET total = 90 WHERE name = "Peter";
DELETE FROM grade_records WHERE name = "Peter";
```

> ⚠️ **别在 UI 线程做大量数据库/文件/网络操作**，会 ANR（Application Not Responding）。
> 小量数据（几十条）在主线程查是考试可接受的；真要严谨就丢进 Executor（见第 14 节）。

### 13.4 Room（L10 教的 ORM，了解即可）

Room = 注解式 ORM，编译期校验 SQL，不用手写 Cursor。代价是要在 `build.gradle` 加依赖：

```groovy
implementation "androidx.room:room-runtime:$room_version"
annotationProcessor "androidx.room:room-compiler:$room_version"   // Java 用 annotationProcessor
```

三个角色：`@Entity`（表/数据类）、`@Dao`（接口，写 `@Query/@Insert/@Update/@Delete`）、
`@Database`（抽象类 extends RoomDatabase，用单例 `getInstance(context)` 拿实例）。

```java
@Entity(tableName = "colors")
public class Color {
    @PrimaryKey(autoGenerate = true) private int id;
    @ColumnInfo(name = "hex_color") private String hex;
    private String name;
}

@Dao
public interface ColorDao {
    @Query("SELECT * FROM colors") List<Color> getAll();
    @Insert void insert(Color... colors);
    @Update void update(Color color);
    @Delete void delete(Color color);
}
```

**考场建议**：机考 3 小时用 `SQLiteOpenHelper`，因为不用改依赖、不会卡在 Gradle 同步上；
Room 留给个人/小组项目。

### 13.5 Repository 模式（L10 后半，架构题爱考）

`UI Controller → ViewModel → Repository → (Room 本地 / 网络远端)`。
Repository 把「数据从哪来」这件事对上层藏起来：读 LiveData 最快，读本地库慢，读网络最慢，
所以常见做法是「先返回本地缓存，同时后台请求网络刷新」。这就是**关注点分离**在数据层的落地。

---

## 14. 线程：UI 线程 + Handler + Executor

### 14.1 两条铁律（L09 原文）

1. **不要阻塞主线程**（Main / UI Thread）——所有点击、绘制、生命周期回调都在这条线程上跑，
   卡住就 ANR。
2. **不要在非 UI 线程碰 UI**——会崩：
   `Only the original thread that created a view hierarchy can touch its views.`

UI 线程内部维护一个**消息队列（Looper）**，FIFO 顺序处理所有事件。你 `handler.post(runnable)`
本质是往这个队列里塞一个任务。

### 14.2 标准写法：Executor 干活 + Handler 回主线程（对应 MainActivity）

```java
private final Handler uiHandler = new Handler(Looper.getMainLooper());
private final ExecutorService executor = Executors.newSingleThreadExecutor();

private void startCalculate() {
    btnCalc.setEnabled(false);
    progressCalc.setVisibility(View.VISIBLE);

    executor.execute(() -> {
        // ── 这里是后台线程：做耗时活儿（计算 / 网络 / 大量数据库）──
        double total = GradeRecord.computeTotal(coursework, midterm, finalExam, bonus);
        try { Thread.sleep(500); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        uiHandler.post(() -> {
            // ── 这里回到 UI 线程：可以安全地更新界面 ──
            progressCalc.setVisibility(View.GONE);
            btnCalc.setEnabled(true);
            openResult(total);
        });
    });
}

@Override protected void onDestroy() {
    super.onDestroy();
    uiHandler.removeCallbacksAndMessages(null);   // ★ 取消防未执行的任务，否则 Activity 已销毁还被回调 → NPE / 内存泄漏
    executor.shutdownNow();
}
```

回主线程的三种等价写法（L09 原文）：

```java
view.post(() -> textView.setText("done"));                       // 1) View.post
runOnUiThread(() -> textView.setText("done"));                   // 2) Activity.runOnUiThread
new Handler(Looper.getMainLooper()).post(() -> textView.setText("done"));  // 3) Handler（最灵活，可延时/可取消）
```

延时执行：`uiHandler.postDelayed(runnable, 2000);`（≈ `setTimeout`）。

### 14.3 裸 Thread 写法（考试写这个也不会错）

```java
new Thread(() -> {
    // 后台干活
    runOnUiThread(() -> textView.setText("done"));   // 回主线程更新 UI
}).start();                                          // ★ 是 start() 不是 run()
```

`thread.run()` 只是普通方法调用，**不会开新线程**；`thread.start()` 才会。
两种定义任务的方式：实现 `Runnable`（推荐，Java 只能单继承）或继承 `Thread` 重写 `run()`。

### 14.4 AsyncTask（已废弃，但考试可能问）

`AsyncTask<Params, Progress, Result>` 四个回调：
`onPreExecute()`（UI 线程，前置）→ `doInBackground()`（后台，可 `publishProgress()`）→
`onProgressUpdate()`（UI 线程，进度）→ `onPostExecute()`（UI 线程，收尾）。
Android 11 起废弃，缺点正是**没有生命周期管理**（Activity 销毁了它还在跑）。
现代替代：`Handler + Executor`（Java）、`Coroutines`（Kotlin）、`WorkManager`（可延迟/可约束的长任务）。

### 14.5 同步/异步、阻塞/非阻塞（L09 概念题）

- 同步 vs 异步：**调用方怎么拿结果**。同步=当场返回；异步=先发起，结果通过回调/Future 后到。
- 阻塞 vs 非阻塞：**调用线程要不要等**。阻塞=干等；非阻塞=立刻返回，先干别的。
- 主线程上的耗时操作，正确答案永远是：**异步 + 非阻塞**。

---

## 15. 网络（了解即可，机考基本不会考联网）

```xml
<!-- 1) Manifest 声明权限 -->
<uses-permission android:name="android.permission.INTERNET" />
```

```java
// 2) 必须在子线程里做
executor.execute(() -> {
    try {
        URL url = new URL("http://www.floatrates.com/daily/hkd.json");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setConnectTimeout(5000);
        conn.setReadTimeout(5000);
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) sb.append(line);
        reader.close();
        String json = sb.toString();
        // 3) 解析 JSON
        JSONObject root = new JSONObject(json);
        double rate = root.getJSONObject("usd").getDouble("rate");
        // 4) 回主线程更新 UI
        uiHandler.post(() -> textRate.setText(String.valueOf(rate)));
    } catch (Exception e) {
        uiHandler.post(() -> Toast.makeText(this, "网络错误", Toast.LENGTH_SHORT).show());
    }
});
```

四个层次（L09/T09）：`java.net`（Socket/URL，最底层）→ `HttpURLConnection`（HTTP 封装）→
`OkHttp`（好用的第三方）→ `Retrofit`（**官方推荐**，基于 OkHttp 的上层框架）。
Android 不能直连远程数据库，必须走 Web Service，通用语言是 XML/JSON，协议是 HTTP。

---

## 16. 自定义 View + Canvas：Android 版 `<canvas>`

对应工程文件 `GradeBarChartView.java`（画总评分数柱状图）。

### 16.1 三个必须写的构造函数

```java
public class GradeBarChartView extends View {

    private final Paint barPaint = new Paint(Paint.ANTI_ALIAS_FLAG);   // 画笔 ≈ ctx 的样式状态
    private List<GradeRecord> records;

    public GradeBarChartView(Context context) { super(context); init(); }                          // 代码 new 出来时
    public GradeBarChartView(Context context, AttributeSet attrs) { super(context, attrs); init(); } // ★ XML 里用时走这个
    public GradeBarChartView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr); init();
    }

    private void init() {
        barPaint.setColor(0xFF3F51B5);
        barPaint.setStyle(Paint.Style.FILL);
    }
}
```

> **只写一个构造函数，XML 里 inflate 时会崩**（系统走的是 `(Context, AttributeSet)` 那个）。
> `Paint.ANTI_ALIAS_FLAG` = 抗锯齿，必开，不然线条毛刺。

### 16.2 XML 里必须写全类名

```xml
<com.example.gradecalc.GradeBarChartView
    android:id="@+id/chartGrades"
    android:layout_width="match_parent"
    android:layout_height="200dp" />
```

### 16.3 onDraw：真正画东西的地方

```java
public void setRecords(List<GradeRecord> records) {
    this.records = records;
    invalidate();               // ★ 数据变了要手动请求重绘（≈ requestAnimationFrame / 手动重画 canvas）
}

@Override
protected void onDraw(Canvas canvas) {
    super.onDraw(canvas);
    float left = 70f, top = 28f;
    float right = getWidth() - 24f, bottom = getHeight() - 56f;

    // 网格线
    canvas.drawLine(left, bottom, right, bottom, axisPaint);
    // 柱子：drawRect(左, 上, 右, 下, 画笔)
    canvas.drawRect(cx - w / 2, barTop, cx + w / 2, bottom, barPaint);
    // 文字：drawText(内容, x, y, 画笔)，y 是文字基线
    canvas.drawText(String.format(Locale.US, "%.1f", value), cx, barTop - 8f, valuePaint);
    // 其它：drawCircle / drawOval / drawBitmap / drawPath / drawColor / drawPoints
}
```

**Paint 常用设置**：`setColor(int)`（`0xAARRGGBB`，前两位是透明度）、`setStrokeWidth(float)`、
`setTextSize(float)`、`setTextAlign(Align.CENTER/LEFT/RIGHT)`、`setStyle(FILL/STROKE/FILL_AND_STROKE)`、
`setAntiAlias(true)`。

**Canvas 进阶**：`canvas.save()` → `canvas.rotate()/translate()/scale()` → 画 → `canvas.restore()`。

**View 渲染三遍（L03/L04 考点）**：`measure`（算尺寸）→ `layout`（摆位置）→ `draw`（画出来）。
需要重新测量时调 `requestLayout()`，只需要重画时调 `invalidate()`。

### 16.4 动画（L12 末尾）

```java
imageView.setImageResource(R.drawable.bot_fit);
imageView.animate().scaleX(1.5f).scaleY(1.5f).setDuration(4000).start();   // 属性动画，链式调用
```

三套动画系统：**View Animation**（TransitionDrawable 淡入淡出 / AnimationDrawable 逐帧 /
Tween 补间）、**Drawable Animation**、**Property Animation**（`android.animation`，官方首选，
可动画任意对象的任意属性）。

---

## 17. Menu：Options Menu 与 Context Menu（T04 实验）

| | Options Menu | Context Menu |
|---|---|---|
| 怎么触发 | 点右上角 ActionBar / 三个点 | **长按**某个 View |
| 长什么样 | 顶部动作栏 + 溢出菜单 | 屏幕中间浮动列表 |
| XML | `res/menu/menu_main.xml` | `res/menu/menu_context.xml` |
| 回调 | `onCreateOptionsMenu` + `onOptionsItemSelected` | `registerForContextMenu` + `onCreateContextMenu` + `onContextItemSelected` |

**菜单 XML：**

```xml
<menu xmlns:android="http://schemas.android.com/apk/res/android"
      xmlns:app="http://schemas.android.com/apk/res-auto">
    <item android:id="@+id/action_history" android:title="@string/menu_history"
          app:showAsAction="ifRoom" />      <!-- ifRoom / always / never -->
    <item android:id="@+id/action_api_doc" android:title="@string/menu_api_doc"
          app:showAsAction="never" />
</menu>
```

**Options Menu（两步）：**

```java
@Override
public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.menu_main, menu);
    return true;
}

@Override
public boolean onOptionsItemSelected(MenuItem item) {
    int id = item.getItemId();
    if (id == R.id.action_history) {                 // ★ if-else，不要 switch（R.id 非常量）
        startActivity(new Intent(this, HistoryActivity.class));
        return true;
    }
    if (id == R.id.action_api_doc) {
        startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("https://developer.android.com/reference")));
        return true;
    }
    return super.onOptionsItemSelected(item);
}
```

**Context Menu（三步）：**

```java
// 1) 注册：告诉系统这个 View 有上下文菜单
registerForContextMenu(findViewById(R.id.textTip));

// 2) 长按时 inflate 菜单
@Override
public void onCreateContextMenu(ContextMenu menu, View v, ContextMenu.ContextMenuInfo menuInfo) {
    super.onCreateContextMenu(menu, v, menuInfo);
    getMenuInflater().inflate(R.menu.menu_context, menu);
}

// 3) 处理点击
@Override
public boolean onContextItemSelected(MenuItem item) {
    int id = item.getItemId();
    if (id == R.id.ctx_fill_demo) { fillDemoValues(); return true; }
    if (id == R.id.ctx_clear_input) { clearInputs(); return true;
    }
    return super.onContextItemSelected(item);
}
```

> 侧滑导航抽屉叫 **Navigation Drawer**（`DrawerLayout`），T04 末尾提到，考试很少考。

---

## 18. 多屏幕适配与本地化（T03 / T04）

### 18.1 配置限定符（Configuration Qualifiers）

同一个文件名，放进带限定符的目录，系统按当前设备状态自动挑最合适的一份：

| 目录 | 什么时候用 | 典型用途 |
|------|-----------|----------|
| `res/layout/` | 默认（竖屏） | 主布局 |
| `res/layout-land/` | 横屏 | 重排成两列 |
| `res/layout-port/` | 竖屏（显式） | |
| `res/layout-sw600dp/` | 最小宽度 ≥600dp（平板） | 平板双栏 |
| `res/values/strings.xml` | 默认语言（惯例放英文） | 兜底 |
| `res/values-zh/strings.xml` | 系统语言是中文 | 中文文案 |
| `res/values-zh-rTW/` | 繁体中文（台湾地区） | |
| `res/drawable-xhdpi/` | 320dpi 屏幕 | 高分辨率位图 |

**横屏适配两种做法（T03）：**
1. ConstraintLayout 方案：在 `res/layout-land/` 放一份同名 XML，重新摆约束位置。
2. LinearLayout 方案：外层 horizontal，里面套两个 vertical，实现「图在左、表单在右」。

⚠️ **横屏那份必须包含竖屏用到的全部 id**，否则横屏时 `findViewById` 返回 null → NPE 崩溃。
（`AndroidDemo` 里 `layout/activity_main.xml` 和 `layout-land/activity_main.xml` 的 id 完全一致，可以对照看。）

字符串查找顺序：`values-zh-rCN` → `values-zh` → `values`（默认兜底）。

### 18.2 本地化三步

1. 所有文案写进 `res/values/strings.xml`，Java 用 `R.string.xxx`，XML 用 `@string/xxx`。
2. 建 `res/values-zh/strings.xml`，**key 一模一样**，value 换成中文。
3. 什么都不用改，系统按设备语言自动选。

```java
String hello = getResources().getString(R.string.hello_world);   // Java 里取
textView.setText(R.string.hello_world);                          // 直接传资源 id 也行
```

> 硬编码用户可见字符串是课件点名的 **Bad Example**；抽出来既方便翻译也方便统一改。

---

## 19. 架构模式：MVP / MVVM / MVI（L04，机考用不上但期末会考）

**为什么需要架构**：避免「God Activity」——所有逻辑堆在一个 Activity 里，改一处动全身，多人协作必冲突。
核心原则是**关注点分离**：UI 层（显示+捕获交互）/ 应用逻辑层（业务规则）/ 数据层（本地库+网络）。

| | MVP | MVVM | MVI |
|---|---|---|---|
| 三个角色 | Model / View / **Presenter** | Model / View / **ViewModel** | Model / View / **Intent** |
| 数据流向 | 双向：View ↔ Presenter | View 主动**观察** ViewModel | **单向**：View → Intent → Model → State → View |
| 谁更新 UI | Presenter 拿到数据后主动调 View 接口的方法 | View 用 `LiveData.observe()` 订阅，数据变了自动回调 | View 订阅唯一的 State，State 变了整体刷新 |
| 关键类 | `MainContract`（View/Presenter 接口）、`MainPresenter` | `ViewModel` + `MutableLiveData` + `observe()` | `State`（不可变）+ `Intent`（用户动作）+ `Reducer` |
| 优点 | 简单直观，小中型项目够用，可测试 | ViewModel 能在旋转屏幕时**活下来**，UI 响应式 | 状态可预测、可追溯，易测试 |
| 缺点 | 复杂后 Presenter 膨胀，要手动管生命周期 | 多个独立 LiveData 会让数据流变乱 | 不可变 State + Intent 样板代码多 |

**MVVM 的核心机制 LiveData**（Observer 设计模式）：

```java
// ViewModel 里
private final MutableLiveData<User> userLive = new MutableLiveData<>();
public LiveData<User> getUser() { return userLive; }      // 对外暴露只读的 LiveData
public void loadUser() { userLive.postValue(fetchFromDb()); }

// Activity/Fragment 里
viewModel.getUser().observe(this, user -> textView.setText(user.getName()));   // this = LifecycleOwner
```

`LiveData` 只能读（getValue），`MutableLiveData` 多了 `setValue()`（主线程）/ `postValue()`（子线程）。
`ViewModel` 的存活时间由 `ViewModelStoreOwner` 决定，**旋转屏幕不会丢**——这是它比普通成员变量强的地方。

**MVI 的单向数据流**：用户点击 → 产生一个 `Intent` 对象 → Model/Reducer 处理后**产生全新的不可变 State** →
View 观察到新 State 整体重绘。`AndroidDemo` 参考的 `BMI-MVI` 作业里就有 `Intent.java` / `MainState.java` / `MainReducer.java`。

**ViewBinding vs DataBinding（L12）：**
- ViewBinding：`buildFeatures { viewBinding true }` → 自动生成 `ActivityMainBinding`，
  取代 findViewById，**类型安全 + 空安全**，但仍需手动 get/set 值。轻量，推荐。
- DataBinding：布局外面包一层 `<layout>`，用 `@{name}` 单向绑定、`@={viewModel.name}` 双向绑定，
  数据变了 UI 自动更新。功能强但有性能开销，且双向绑定会破坏 MVI 的单向数据流。

---

## 20. 背写骨架：从「新建空项目」到「能跑的 App」

### 20.1 环境准备（考前一定要在实验室电脑上走一遍）

1. 实验室电脑 Android Studio 路径：`C:\Program Files\Android\Android Studio\bin\studio64.exe`
2. `File → New → New Project → Empty Views Activity`
   - Name: `MyExamApp`；Package: `com.example.myexamapp`；Language: **Java**；
     Minimum SDK: **API 21 或 24**（课件推荐 21，能覆盖 99.7% 设备）
3. 等 Gradle sync 转完（第一次可能几分钟）
4. `Tools → Device Manager → Create Device`，选 API 33 (Tiramisu) 系统镜像，x86_64 + Use Host GPU
5. 点 ▶ Run，看到 "Hello World!" → **环境 OK**
6. 教授明确要求：**不要导入旧的 BMI 工程**，要新建空项目再把自己作业里的代码**复制**进去练手

### 20.2 十步流程（考场照着走）

| 步 | 做什么 | 产物 |
|----|--------|------|
| 1 | 新建 Empty Activity 项目 | MainActivity.java + activity_main.xml + Manifest 已注册 |
| 2 | 立刻 Run 一次 | 确认环境和模拟器正常 |
| 3 | 改 `res/values/strings.xml`，把所有文案写成 string 资源 | 文案集中管理 |
| 4 | 写 `activity_main.xml`：ScrollView → LinearLayout → 输入控件 + 按钮 | 主界面 |
| 5 | `MainActivity.onCreate` 里 `findViewById` + `setOnClickListener` | 事件通了 |
| 6 | 写业务计算（抽成一个方法或一个 Model 类） | 核心逻辑 |
| 7 | Run 一次，验证主流程 | ★ 中途就要验证 |
| 8 | 需要第二屏：`New → Activity → Empty Activity`（AS 会自动注册到 Manifest），`Intent + putExtra` 跳转 | 多页面 |
| 9 | 加分项：SharedPreferences 记住输入 / SQLite 存历史 / RecyclerView 列表 / Menu | 拿分点 |
| 10 | 收尾：输入校验、Toast 提示、横屏布局、最后 Run + 提交 | 完整可运行 |

### 20.3 最小可跑骨架（背下来，考场默写）

**activity_main.xml**

```xml
<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="match_parent">
    <LinearLayout
        android:layout_width="match_parent" android:layout_height="wrap_content"
        android:orientation="vertical" android:padding="16dp">

        <EditText android:id="@+id/editInput"
            android:layout_width="match_parent" android:layout_height="wrap_content"
            android:hint="@string/hint_input" android:inputType="numberDecimal" />

        <Button android:id="@+id/btnSubmit"
            android:layout_width="match_parent" android:layout_height="wrap_content"
            android:text="@string/btn_submit" />

        <TextView android:id="@+id/textResult"
            android:layout_width="match_parent" android:layout_height="wrap_content"
            android:textSize="24sp" />
    </LinearLayout>
</ScrollView>
```

**MainActivity.java**

```java
package com.example.myexamapp;

import android.os.Bundle;
import android.text.TextUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private EditText editInput;
    private TextView textResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editInput = findViewById(R.id.editInput);
        textResult = findViewById(R.id.textResult);
        Button btnSubmit = findViewById(R.id.btnSubmit);

        btnSubmit.setOnClickListener(v -> calculate());
    }

    private void calculate() {
        String text = editInput.getText().toString().trim();
        if (TextUtils.isEmpty(text)) {
            editInput.setError(getString(R.string.err_empty));
            Toast.makeText(this, R.string.err_empty, Toast.LENGTH_SHORT).show();
            return;
        }
        double value = Double.parseDouble(text);
        textResult.setText(String.format(java.util.Locale.US, "结果：%.2f", value * 2));
    }
}
```

**跳转到第二屏（三行）**

```java
Intent intent = new Intent(this, ResultActivity.class);
intent.putExtra("value", value);
startActivity(intent);
```

---

## 21. 常见崩溃与自救清单（考场上按这个排查）

| 症状 | 大概率原因 | 解法 |
|------|-----------|------|
| `ActivityNotFoundException` | 新 Activity 没在 Manifest 注册 | 加 `<activity android:name=".XxxActivity" android:exported="false"/>` |
| `NullPointerException` on findViewById | ①id 拼错 ②在 setContentView 之前调 ③横屏布局里没这个 id | 对一遍 XML 的 `@+id`；把 findViewById 移到 setContentView 之后 |
| `ClassCastException` | findViewById 的类型和 XML 标签不符（XML 是 TextView，Java 写成 EditText） | 统一类型 |
| `Resources$NotFoundException` | 引用了不存在的 string/drawable | 看报错里的资源名，补上 |
| RecyclerView 一片空白 | **忘了 `setLayoutManager()`** | `recyclerView.setLayoutManager(new LinearLayoutManager(this));` |
| 列表不刷新 | 改了 List 没通知 Adapter | `adapter.notifyDataSetChanged()`（或换 ListAdapter+submitList） |
| 点击 item 位置错乱 | 闭包里用了 `position` 而不是 `getBindingAdapterPosition()` | 用 `holder.getBindingAdapterPosition()` |
| `Only the original thread...can touch its views` | 在子线程里 setText | 用 `runOnUiThread()` / `handler.post()` 包起来 |
| ANR（转圈无响应） | 主线程做了耗时操作（网络/大数据库/sleep） | 丢进 Executor 子线程 |
| `You need to use a Theme.AppCompat theme` | 用了 AppCompat 控件但主题是系统原生主题 | theme parent 改成 `Theme.Material3.DayNight` 或 `Theme.AppCompat.*` |
| `switch case` 编译不过 | AGP 8+ 的 `R.id` 不是常量 | 改成 `if (id == R.id.xxx)` |
| 旋转屏幕数据没了 | Activity 被销毁重建 | `onSaveInstanceState` 存 Bundle，`onCreate` 里恢复 |
| 自定义 View 在 XML 里崩 | 缺 `(Context, AttributeSet)` 构造函数 | 三个构造函数都写上 |
| `Cursor` 警告 / 数据错乱 | 没 `cursor.close()` 或没 `moveToNext()` | while 循环 + 用完关闭 |
| 布局在横屏被截断 | 只写了竖屏布局 | 加 `res/layout-land/同名.xml`，或外层套 ScrollView |
| Gradle sync 失败 | 依赖下载不了 / SDK 版本没装 | 看报错缺哪个 platform，`SDK Manager` 装上；或把 compileSdk 改成已装的版本 |

**Logcat 用法**：底部 Logcat 面板，过滤器里输入自己的 TAG（例如 `GradeCalcLifeCycle`），
只看自己的日志。红字 `FATAL EXCEPTION` 下面的 `Caused by:` 就是真正原因，从下往上读。

---

## 22. `D:\ProjectStore\AndroidDemo` 知识点对照表

演示工程主题：**GradeCalc 课程总评计算器**（平时 30% + 期中 30% + 期末 40%，可选加分，可切评分制）。
和 BMI 完全不同的题材，正好模拟「考试给你一个全新主题」的情形。

| 文件 | 对应知识点 | 对应手册章节 |
|------|-----------|--------------|
| `app/src/main/AndroidManifest.xml` | 三个 Activity 注册、LAUNCHER 入口、exported、parentActivityName | §3 |
| `MainActivity.java` | findViewById、7 类事件监听、输入校验、SharedPreferences、Handler+Executor、Options/Context Menu、Fragment 事务、onSaveInstanceState、生命周期日志 | §5 §7 §9 §10 §13.1 §14 §17 |
| `ResultActivity.java` | 显式 Intent 取参、SQLite 落库、隐式 Intent 分享、AlertDialog、属性动画、Snackbar | §4 §10.1 §13.3 §16.4 |
| `HistoryActivity.java` | RecyclerView + LayoutManager、onResume 刷新、条目点击/长按、删除确认 | §12 |
| `GradeAdapter.java` | RecyclerView.Adapter + ViewHolder + 点击回调接口 + notifyDataSetChanged | §12.2 |
| `GradeDbHelper.java` | SQLiteOpenHelper 建表/增删查、ContentValues、Cursor、rawQuery 聚合 | §13.3 |
| `GradeRecord.java` | POJO 数据模型 + 纯业务计算方法（关注点分离） | §19 |
| `GradeScale.java` | 常量类；说明为什么不能用 switch(R.id.x) | §7.3 |
| `GradeBarChartView.java` | 自定义 View、三个构造函数、Paint、onDraw、invalidate | §16 |
| `AboutFragment.java` | Fragment 生命周期、newInstance 传参、onCreateView/onViewCreated、popBackStack | §11 |
| `res/layout/activity_main.xml` | ScrollView + LinearLayout + weight + 全套输入控件 + FrameLayout 容器 | §6 §7 |
| `res/layout-land/activity_main.xml` | 横屏两列布局，id 与竖屏完全一致 | §18.1 |
| `res/layout/activity_result.xml` | ConstraintLayout 约束定位、0dp = match_constraint | §6.4 |
| `res/layout/activity_history.xml` | 自定义 View 全类名引用、RecyclerView + weight 撑满 | §12 §16.2 |
| `res/layout/item_grade.xml` | 列表单条模板 | §12.2 |
| `res/layout/fragment_about.xml` | Fragment 自己的布局 | §11.1 |
| `res/menu/menu_main.xml`、`menu_context.xml` | 两种菜单、showAsAction | §17 |
| `res/drawable/bg_card.xml` 等 | shape/solid/corners/stroke/padding ≈ CSS 背景 | §8.3 |
| `res/drawable/ic_launcher.xml` | vector 矢量图 ≈ SVG | §8.3 |
| `res/values/themes.xml` | theme（全局）+ style（class）+ FieldLabel/CardBox 复用 | §8.1 §8.2 |
| `res/values/strings.xml`、`values-zh/strings.xml` | 本地化、格式化占位符、`formatted="false"` | §18.2 §9 |
| `res/values/arrays.xml` | Spinner 数据源 | §7.2 |
| `res/values/colors.xml`、`dimens.xml` | 颜色与尺寸资源化 | §8.5 |

**怎么用它复习（建议顺序）：**
1. 先在 Android Studio 打开 `D:\ProjectStore\AndroidDemo`，Run 起来点一遍，知道每个界面能干什么。
2. 打开 `MainActivity.java`，对照本手册 §5/§7/§9/§10 逐行读，每行都能说出「这是干嘛的」。
3. **合上工程**，自己新建一个空项目，凭记忆写一个「输入三个分数 → 算总评 → 显示」的最小版本（§20.3 骨架）。
4. 写不出来就回来看手册，再合上重写一遍。**这一步是关键**——考试考的就是这个。
5. 再加一层：把结果存进 SQLite，用 RecyclerView 显示历史。
6. 最后计时 3 小时，随便找个新题目（例如「汇率换算 + 历史记录」「打卡计时器 + 统计图」）从头撸一遍。

---

## 23. 考前 60 分钟速记清单

**必背 API（写错就崩）**

```java
setContentView(R.layout.activity_main);
EditText e = findViewById(R.id.editX);        String s = e.getText().toString();
TextView t = findViewById(R.id.textX);        t.setText("hi");
Button b = findViewById(R.id.btnX);           b.setOnClickListener(v -> { });
v.setVisibility(View.VISIBLE);                b.setEnabled(false);
Toast.makeText(this, "msg", Toast.LENGTH_SHORT).show();
new AlertDialog.Builder(this).setTitle("t").setMessage("m")
     .setPositiveButton("OK", (d, w) -> { }).show();
startActivity(new Intent(this, SecondActivity.class));
intent.putExtra("key", value);                getIntent().getStringExtra("key");
getSharedPreferences("f", MODE_PRIVATE).edit().putString("k", "v").apply();
new SQLiteOpenHelper(...)                     db.insert / db.query / db.delete
recyclerView.setLayoutManager(new LinearLayoutManager(this));
recyclerView.setAdapter(adapter);             adapter.notifyDataSetChanged();
new Handler(Looper.getMainLooper()).post(() -> { });
runOnUiThread(() -> { });
getSupportFragmentManager().beginTransaction().replace(R.id.container, frag).commit();
canvas.drawRect(l, t, r, b, paint);           invalidate();
getMenuInflater().inflate(R.menu.menu_main, menu);
finish();
```

**十条最容易丢分的细节**

1. `setContentView` 必须在 `findViewById` 之前。
2. 新 Activity 必须在 `AndroidManifest.xml` 注册。
3. `getText()` 要 `.toString()`；`getDoubleExtra` 必须给默认值。
4. RecyclerView 必须 `setLayoutManager`，否则空白。
5. 事件用 `if (id == R.id.x)`，**不要** `switch`。
6. 子线程不能碰 UI，用 `runOnUiThread` / `Handler.post`。
7. `AlertDialog.Builder` 最后要 `.show()`。
8. Cursor 用完要 `close()`。
9. 自定义 View 要写三个构造函数，XML 里写全类名。
10. 横屏布局的 id 必须和竖屏一致。

**Android 系统层次（期末概念题也用得上，L01）**

```
Applications（系统 App：Home / Contacts / Phone / Browser）
    ↑
Java API Framework（Activity Manager / View System / Resource Manager / Content Providers / Notification Manager）
    ↑
Native C/C++ Libraries（libc、SQLite、WebKit、OpenGL、Media Framework） + Android Runtime（Core Libs + ART/Dalvik VM）
    ↑
Linux Kernel（驱动、内存/进程管理、Binder IPC、电源管理）
```

**构建流程**：Java/Kotlin 源码 → javac/kotlinc → Java 字节码 → **dex 编译器** → `.dex`（Dalvik 字节码）→
打包资源 → `.apk`（必须签名）→ 安装到设备 → **ART** 把 dex 转成机器码（Android 5+ 是 AOT+JIT，Android 7+ 安装时只转最少的部分，其余运行时转）。

---

### 附：这份手册没覆盖 / 你需要自己补的部分

- **本地课件缺 L05、L06、L07、L11**（`Crouse` 目录里只有 L01-L04、L08、L09、L10、L12）。
  按课程大纲推断这几讲大概是「界面组件进阶 / 网络服务 / 其它」，考试前请去 Canvas 把缺的 PPT 下下来补看。
- L12 明确写了 **Multimedia（音视频/相机）和 Graphics 动画「不考期末」**，机考也基本不会考，所以本手册只给了最小概览。
- Kotlin 版本没写（你选了 Java）。Kotlin 的差别主要是：`lateinit var` / `by lazy`、`findViewById<TextView>(R.id.x)` 要写泛型、
  空安全 `?.` `!!` `?:`、`when` 代替 `switch`、协程代替 Thread。真要临时切 Kotlin，让 Android Studio 的
  `Code → Convert Java File to Kotlin File` 帮你转，再逐行看懂。

