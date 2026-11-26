# Project Summary

## Overall Goal
Prepare the user (CityU graduate student Zhanquan Zhuang, 60209978) for the EE5415 Mobile App Design & Development programming exam on 2026-11-28 (Saturday, 09:00–12:10, lab B7701), including a comprehensive Android knowledge handbook mapped to their Vue/MiniProgram/H5 frontend experience, a Q&A document addressing five specific conceptual doubts, and a demo project (`D:\ProjectStore\AndroidDemo`) — all under strict exam rules (open-book with own slides/submissions only, no AI code generation, lab PCs, must create new empty project).

## Key Knowledge

### Exam Rules & Constraints
- **Date/time:** 2026-11-28 Saturday, 09:00–12:10 (10 min setup + 3h coding), lab B7701
- **Allowed:** course slides, own Canvas submissions as code reference, Google for docs
- **Banned:** all AI code-generation (incl. AI answers in search results), USB, remote desktop/help, phones after start
- **Must:** use lab computers, create a NEW empty project (must NOT import existing BMI project), copy code in manually
- **Grading:** assignments 5%, individual project 8%, group project 12%, programming test 25%, final 50%; pass = ≥30% coursework AND ≥30% exam
- **Language chosen:** Java; verification = build success only
- **Drill project location:** `D:\ProjectStore\AndroidDemo\` (outside git repo)

### User's Background & Preferences
- Frontend experience: Vue, WeChat MiniProgram, H5
- Self-described difficulty: "not very familiar with Android, roughly knows XML+Java structure but struggles to write from scratch"
- Core request: comprehensive knowledge mapping (components, attributes, input widgets, CSS analogues, Java component manipulation, event handling, routing/registration, lifecycle) explained via direct analogy to Vue/MiniProgram/H5
- All session artifacts must go into project directory, never system Temp/C drive
- Content language: Chinese body text, English technical terms preserved verbatim

### Technical Decisions & Patterns (from Q&A doc and handbook)

**Q1 – Global/shared state (6 mechanisms):**
- Activity member fields (lost on rotation), Bundle/Intent.putExtra, onSaveInstanceState, static field / Application subclass singleton (≈ getApp().globalData / Pinia), ViewModel+MutableLiveData (survives rotation, shared across Fragments via `requireActivity()` scope), SharedPreferences/file/SQLite (persistent)
- Exam recommendation: **no global store** — use SQLite as single source of truth, re-query in `onResume()`
- Static pitfalls: never hold Context/Activity/View statically (leak); use `getApplicationContext()`; statics die with process
- Verified pattern in AndroidDemo HistoryActivity.java: `onResume() → reload() → adapter.setData(records); chartView.setRecords(records);`

**Q2 – finish() and Intent flags:**
- `finish()` = pop+destroy current Activity (≈ wx.navigateBack() / router.back()), NOT app exit
- 4 scenarios to use: post-submit, post-login, guard-fail with `finish(); return;`, after deleting displayed record
- `FLAG_ACTIVITY_CLEAR_TOP`: destroys activities above target; target is **destroyed and recreated** by default
- Add `| FLAG_ACTIVITY_SINGLE_TOP` to keep target alive → receives `onNewIntent` → must call `setIntent(intent)`
- Logout: `NEW_TASK | CLEAR_TASK`; other flags: `NO_HISTORY`, `MULTIPLE_TASK`, `REORDER_TO_FRONT`
- `launchMode="singleTop"` makes CLEAR_TOP alone use `onNewIntent`
- Exam guidance: don't touch launchMode

**Q3 – SQLite APIs:**
- `execSQL(sql)` / `execSQL(sql, Object[] bindArgs)`: everything except SELECT
- `rawQuery(sql, String[])` → Cursor (exam-friendly, lower error rate)
- `insert/update/delete/query` convenience wrappers; `insertWithOnConflict(..., CONFLICT_REPLACE)`
- `nullColumnHack` always `null`
- `db.query(table, columns, selection, selectionArgs, groupBy, having, orderBy)` — 7 params map to SQL fragments
- The user's specific line `db.query(TABLE, null, null, null, null, null, "date ASC")` = `SELECT * FROM bmi_records ORDER BY date ASC`
- **No LIMIT in 7-arg overload** → use 9-arg `query(false, TABLE, null,null,null,null,null,"date DESC","5")`, or `rawQuery(... LIMIT 5)`, or append LIMIT into orderBy string
- `selectionArgs` is `String[]` only (numbers need `String.valueOf`)
- `%` wildcards go in the **value** for LIKE; `?` placeholders prevent injection and single-quote breakage
- Cursor rules: `moveToNext()` loop, `getColumnIndexOrThrow`, `close()` in `finally`; single-value: `if (c.moveToFirst()) c.getInt(0)`
- Exam decision: recommend `rawQuery` for conditional queries ("一分不扣")

**Q4 – MVI architecture:**
- Machine exam does NOT require MVI; plain onClick is correct approach
- Three dimensions (not alternatives): ExecutorService (thread: *where* work runs), Handler (thread: *when* to return to UI thread), Reducer (architecture: *how* state changes)
- Removing Executor → ANR; removing Handler → crash ("Only the original thread..."); removing Reducer → still works
- `Intent.java` name collision with `android.content.Intent` → must write `new android.content.Intent(this, ...)`
- `runOnUiThread(Runnable)` ≡ `view.post(...)` ≡ `new Handler(Looper.getMainLooper()).post(...)`
- Cleanup: `executorService.shutdownNow()` + `mainHandler.removeCallbacksAndMessages(null)` in `onDestroy`
- ExecutorService/Handler are app-wide infra; State/Reducer are per-screen
- Reducer is JVM-testable without emulator
- Android lacks `v-model` → `captureInputValues()` pattern exists
- Version A (15-line onClick) vs Version B (150+ lines MVI) — exam should use Version A

**Q5 – File paths (Scoped Storage):**
- Paths are fixed by package name; `openFileOutput(String name, int mode)` has **no directory parameter**
- `<pkg>` = `namespace` in `app/build.gradle`
- Directory map: `getFilesDir()`→`/data/data/<pkg>/files`, `getCacheDir()`→`/data/data/<pkg>/cache`, `getExternalFilesDir(null)`→`/sdcard/Android/data/<pkg>/files`, SharedPreferences→`/data/data/<pkg>/shared_prefs/<name>.xml`, SQLite→`/data/data/<pkg>/databases/<name>.db`
- Public storage → MediaStore / `Environment.getExternalStoragePublicDirectory()`
- Relocation methods: directory category + `new File(getFilesDir(), "records/2026")` with `mkdirs()`; SAF `ACTION_CREATE_DOCUMENT` + `getContentResolver().openOutputStream(uri)`; `ACTION_OPEN_DOCUMENT` + `openInputStream(uri)` — Uri is NOT a File
- `MODE_PRIVATE` = overwrite, `MODE_APPEND` = append; `MODE_WORLD_READABLE/WRITABLE` throw since API 17
- SharedPreferences is plaintext XML (don't store passwords/tokens)

**Other critical technical facts from earlier session:**
- AGP 8+ `android.nonFinalResIds` → `switch(R.id.x)` won't compile, use if/else
- AGP 9.3.2 / Gradle 9.5.0 / `compileSdk { version = release(37) }` / JDK 25 toolchain
- Lifecycle 7 callbacks, Bundle/rotation, layouts+units, input widgets, drawable/style/theme, listeners, Fragment, RecyclerView+Adapter+ViewHolder, SharedPreferences, Room, Repository, threading, custom View/onDraw, Menus, localization, MVP/MVVM/MVI, ViewBinding/DataBinding
- pypdf 7.1.1 used for PDF extraction (no pdftotext on this machine)
- cmd.exe `%VAR%` parse-time expansion pitfall

### User's Own Submitted Code Reference (BMI-MVI Assignment)
Located at `D:\ProjectStore\Android-Work\60209978_ZhanQuanZhuang_Assignment04\BMI-MVI\app\src\main\java\com\example\bmi_mvi\`:
- `MainState.java` — immutable, 11 private final fields, nested Builder with copy constructor
- `MainReducer.java` — pure `reduce(state, intent) → newState` with instanceof chain
- `Intent.java` — sealed interface with records (SetHeight/SetWeight/SetAge/etc.)
- `MainActivity.java` — dispatch/captureInputValues/reduce/render pattern, executorService + mainHandler
- `BmiHistoryDbHelper.java` — contains the exact `db.query(TABLE, null, null, null, null, null, "date ASC")` line user asked about
- `UserPreferences.java` — SharedPreferences wrapper

### Known Gap
- User explicitly stated they understood everything **except the drawing/Canvas part (§16)** — not yet addressed

## Recent Actions

### Completed
1. Created `cityU/EE5415_MobileApnsDesignAndDevemt/exam/答疑_状态_数据库_MVI_文件路径.md` (815 lines, 35 headings) answering all 5 questions with code grounded in user's own BMI-MVI submission and AndroidDemo project
2. Added 3-line cross-reference pointer in `exam/Android前端类比手册.md` header pointing to the new Q&A doc
3. Fixed §5.2 heading from "（L10 原文 + 实测）" to "（L10 原文摘录）" (nothing was device-tested)
4. Verified HistoryActivity.java `onResume → reload()` pattern via grep (lines 75-77, 88, 92-93 confirmed real)
5. Read all 6 BMI-MVI source files to ground answers in primary sources rather than generic knowledge
6. Delivered concise inline summary of all 5 answers in chat

### Pre-existing deliverables (unchanged this turn)
- `exam/Android前端类比手册.md` (~1,859 lines, §0–§23 + appendix, 15 required keywords, 68 grep hits)
- `exam/课件覆盖对照.md` (14 PDF mapping table)
- `exam/extract_pdfs.py`, `exam/verify_exam_pack.py`
- `exam/extracted/*.txt` ×14
- `D:\ProjectStore\AndroidDemo` GradeCalc app (outside git repo)

## Current Plan

1. [DONE] Create comprehensive Android knowledge handbook with Vue/MiniProgram/H5 analogies
2. [DONE] Extract all 14 lecture PDFs to text
3. [DONE] Create coverage mapping document
4. [DONE] Build verification script for exam pack completeness
5. [DONE] Answer 5 specific conceptual questions in dedicated Q&A document
6. [IN PROGRESS] `/commit` request pending — gather git context, stage only EE5415 exam-prep deliverables under `cityU/EE5415_MobileApnsDesignAndDevemt/exam/` (7 groups: handbook, coverage map, Q&A doc, extract script, verify script, 14 extracted txt files), draft short Chinese commit message matching repo style, verify with `git diff --cached --name-status`, execute commit. Must confirm with user whether to include untracked EE5415 course PDFs (Crouse/, labs/) or restrict to exam/ only. Exclude unrelated EE5609 presentation files and root QWEN.md.
7. [TODO] Address the drawing/Canvas (§16) gap if user requests it before the exam tomorrow (2026-11-28 09:00)

---

## Summary Metadata
**Update time**: 2026-11-26T19:53:13.178Z
