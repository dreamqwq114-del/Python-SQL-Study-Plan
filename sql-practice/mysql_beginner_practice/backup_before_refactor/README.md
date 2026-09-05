# MariaDB / MySQL 入门 10 天练习

这套材料适合见过 `SELECT`、`WHERE`、`JOIN`、`GROUP BY`，但还不能稳定独立写出的初学者。SQL 已转换为 MariaDB/MySQL 兼容语法，只操作独立的 `sql_beginner_practice` 练习数据库。

## 已实际验证的环境

- XAMPP 自带 MariaDB `10.4.32`；
- 地址：`127.0.0.1`；
- 端口：`3306`；
- 实际执行了初始化脚本、全部课程示例、全部答案和两份阶段测试答案；
- 最终固定数据和事务回滚均已重新查询确认。

MariaDB 与 MySQL 非完全相同。本目录以当前 XAMPP 的 MariaDB 10.4.32 实测结果为准，同时只使用二者常见的基础语法。

## 安全提醒

- 不要在 `company`、`myschema` 或其他现有数据库中运行本目录的数据修改语句。
- 本目录不包含 `DROP DATABASE` 或 `DROP TABLE`。
- 第 9 天所有 `UPDATE`、`DELETE` 都先 `SELECT`，放在事务中并默认 `ROLLBACK`。
- `00_create_database.sql` 只创建或更新固定主键对应的练习数据，不删除其他数据库。

## 在 DBeaver 中连接 XAMPP

1. 在 XAMPP Control Panel 启动 MySQL。
2. 在 DBeaver 新建 `MariaDB` 连接；没有该选项时可选 `MySQL`。
3. 主机填写 `127.0.0.1`，端口填写 `3306`。
4. 用户名填写你的 XAMPP MariaDB 用户；本次本机验证使用 `root`。
5. 密码使用你自己在 XAMPP 中设置的密码，不要照抄他人的配置。
6. 测试连接成功后打开本目录的 `.sql` 文件。

平时只选中当前示例或你填写的一条 SQL，再执行“执行 SQL 语句”。DBeaver 常用快捷键通常是 `Ctrl+Enter`，以你当前快捷键设置为准。

## 第一次运行

第一次完整运行：

```text
00_create_database.sql
```

然后执行：

```sql
SELECT DATABASE() AS current_database;
```

结果必须是：

```text
sql_beginner_practice
```

初始化输出中的 `baseline_status` 也必须是 `PASS`。如果显示 `FAIL`，说明练习库已有额外或不一致数据，请停止，不要继续运行课程。脚本不会自动删除这些数据。

切换数据库使用：

```sql
USE sql_beginner_practice;
```

## LIMIT 和 TOP

MariaDB/MySQL 把行数限制写在查询末尾：

```sql
SELECT employee_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5;
```

SQL Server 使用 `TOP (5)`；本目录只在改错题中展示 `TOP`，可执行答案使用 `LIMIT`。

## 建议进度

- 第 0 天：`00_diagnostic_test.sql`，完成后看 `diagnostic_review.md`。
- 第 1～4 天：依次完成 `01_select_basics.sql` 至 `04_aggregate_group.sql`。
- 第 4 天后：完成 `checkpoint_1.sql`。
- 第 5～8 天：依次完成 `05_inner_join.sql` 至 `08_cte_exists_cast.sql`。
- 第 8 天后：完成 `checkpoint_2.sql`。
- 第 9 天：完成 `09_data_modification.sql`，逐段执行并确认最后是 `ROLLBACK`。
- 第 10 天：完成 `10_final_practice.sql`。第一轮先做题 1～8，题 9～12 留作第二轮巩固。

每天控制在 45～60 分钟。答题顺序：

1. 独立思考 5～10 分钟；
2. 再看 `hints.md`；
3. 最后才查看 `answers`。

## 报错时先检查

1. XAMPP 中的 MySQL 是否已启动。
2. 当前数据库是否为 `sql_beginner_practice`。
3. 表名、字段名是否拼错。
4. 字符串和日期是否使用单引号。
5. NULL 是否使用 `IS NULL` 或 `IS NOT NULL`。
6. JOIN 条件是否遗漏或连错字段。
7. 非聚合列是否完整写入 `GROUP BY`。
8. `AND`、`OR` 是否需要括号。
9. 是否误用了 SQL Server 的 `TOP`、`dbo.`、`GO`、`ISNULL` 或 `TRY_CAST`。

## 错题记录

只把真正做错的题写进 `mistake_log.md`，不需要提前填写。写清错误原因和正确思路，过 1～2 天后重新独立做同类题，不要只复制答案。

## 修改数据为什么先 SELECT

`SELECT` 用来预览 `WHERE` 会命中哪些行。确认范围后，才把完全相同的条件用于 `UPDATE` 或 `DELETE`。

- `COMMIT`：永久保存当前事务修改；
- `ROLLBACK`：撤销当前事务修改。

本课程默认使用 `ROLLBACK`。

## 第一天只做这些

1. 运行 `00_create_database.sql`。
2. 用 `SELECT DATABASE()` 确认当前数据库。
3. 独立完成 `00_diagnostic_test.sql`。
4. 查看 `diagnostic_review.md`。
5. 再开始 `01_select_basics.sql`。
6. 第一天不要打开全部答案文件。
