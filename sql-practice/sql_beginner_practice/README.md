# SQL 入门 10 天练习

这套材料适合已经见过 `SELECT`、`WHERE`、`JOIN`、`GROUP BY`，但还不能稳定独立写出的初学者。全部代码使用 SQL Server / T-SQL，只操作新建的 `sql_beginner_practice` 练习数据库。

## 开始前的安全提醒

- 不要在 `ecology0110` 或任何业务数据库中运行本目录的修改语句。
- 本机生成材料时没有发现可用的 SQL Server 命令行或服务，所以目前只做了静态检查，不能把“语法看起来正确”当成“已实际运行通过”。
- `00_create_database.sql` 不包含 `DROP DATABASE` 或 `DROP TABLE`。它只在数据库、表或种子数据不存在时创建或插入。
- 第 9 天的 `UPDATE`、`DELETE` 都先 `SELECT` 预览，并放在事务中，默认执行 `ROLLBACK`。

## 在 DBeaver 中打开和运行

1. 连接你的本地 SQL Server，不要连接企业业务服务器。
2. 使用“文件 → 打开文件”打开本目录中的 `.sql` 文件，或把文件拖进 SQL 编辑器。
3. 第一次先完整运行 `00_create_database.sql`。脚本会创建数据库、5 张表和固定测试数据。
4. 平时做题时，只选中当前示例或你填写的一条 SQL，再执行“执行 SQL 语句”。常用快捷键通常是 `Ctrl+Enter`；请以你 DBeaver 当前快捷键设置为准。
5. 不要为了做一道题而执行整个答案文件。

## 确认当前数据库

运行：

```sql
SELECT DB_NAME() AS current_database;
```

必须看到 `sql_beginner_practice`。切换数据库使用：

```sql
USE sql_beginner_practice;
```

每个练习文件也包含 `USE sql_beginner_practice;` 和安全检查。如果数据库不对，脚本会停止。

## TOP 和 LIMIT

SQL Server 使用 `SELECT TOP (5) ...` 限制行数；MySQL 常在语句末尾写 `LIMIT 5`。本课程只使用 SQL Server 的 `TOP`，不要混用 `LIMIT`。

## 建议进度

- 第 0 天：`00_diagnostic_test.sql`，做完后看 `diagnostic_review.md`。
- 第 1～4 天：依次完成 `01_select_basics.sql` 至 `04_aggregate_group.sql`。
- 第 4 天完成后：做 `checkpoint_1.sql`。
- 第 5～8 天：依次完成 `05_inner_join.sql` 至 `08_cte_exists_cast.sql`。
- 第 8 天完成后：做 `checkpoint_2.sql`。
- 第 9 天：`09_data_modification.sql`，逐段执行并确认最后是 `ROLLBACK`。
- 第 10 天：`10_final_practice.sql`。第一轮 45～60 分钟先做题 1～8，
  题 9～12 作为第二轮巩固；不要为了“一次做完”提前看答案。

每天控制在 45～60 分钟。答题顺序是：先独立思考 5～10 分钟，再看 `hints.md`，最后才看 `answers`。答案是核对工具，不是抄写模板。

## 报错时先检查

1. 当前数据库是否为 `sql_beginner_practice`。
2. 表名、字段名是否拼错。
3. 字符串和日期是否使用单引号。
4. NULL 是否使用 `IS NULL` 或 `IS NOT NULL`。
5. JOIN 条件是否遗漏或连错字段。
6. 非聚合列是否完整写入 `GROUP BY`。
7. 同时使用 `AND`、`OR` 时是否需要括号。
8. 比较或 JOIN 的数据类型是否一致。

## 错题记录

只把真正做错的题记录到 `mistake_log.md`，不用提前填写。写清错误原因和正确思路，过 1～2 天后重新独立做一道同类题。不要只复制正确答案。

## 修改数据为什么先 SELECT

`SELECT` 能让你先看到 `WHERE` 会命中哪些行。确认范围后才把同一条件用于 `UPDATE` 或 `DELETE`。`COMMIT` 会永久保存当前事务中的修改；`ROLLBACK` 会撤销当前事务中的修改。本课程默认 `ROLLBACK`。

## 第一天只做这些

1. 运行 `00_create_database.sql`。
2. 用 `SELECT DB_NAME()` 确认当前数据库。
3. 独立完成 `00_diagnostic_test.sql`。
4. 查看 `diagnostic_review.md`，判断不稳定知识点。
5. 再开始 `01_select_basics.sql`。
6. 第一天不要打开全部答案文件。
