# 环境准备

本节只负责创建独立练习库和确认固定数据。不要在公司、课程项目或其他业务数据库中运行这些脚本。

## 本节目标

- 创建 `mysql_beginner_practice`；
- 创建 5 张练习表并写入固定数据；
- 确认当前数据库和基线行数；
- 发现 `FAIL` 时停止，不带着错误数据继续学习。

## 文件运行顺序

1. 在 DBeaver 或 JetBrains 中连接自己的 MySQL 服务。
2. 打开并完整运行 `create_database.sql`。
3. 打开并完整运行 `verify_database.sql`。
4. 确认 `current_database` 是 `mysql_beginner_practice`。
5. 确认 `baseline_status` 是 `PASS`。
6. 如果出现 `FAIL`，先查看明细，不要运行后续章节。

## 为什么使用独立数据库

`USE mysql_beginner_practice;` 把后续查询限制在练习库中。脚本不包含 `DROP DATABASE`，也不应改成其他数据库名称。

## 安全说明

- `create_database.sql` 使用 `CREATE ... IF NOT EXISTS`，不会删除已有数据库或表。
- 固定主键的数据会被更新为课程基线，但不会清理你额外增加的练习行。
- 第 9 章修改数据时必须先预览，并默认 `ROLLBACK`。
- 如果基线行数不是预期值，重新运行脚本也不一定会删除额外行，应先查明原因。

## 你应该看到什么

- 数据库：`mysql_beginner_practice`；
- 表：`departments`、`employees`、`projects`、`project_metrics`、`employee_projects`；
- 基线行数依次为 5、20、14、12、37；
- 特意保留了 `NULL`、无项目员工、无参与者项目和无指标项目，供后续练习。

## 下一步

只有 `verify_database.sql` 显示 `PASS` 后，才进入 `00_diagnostic/lesson.md`。
