# MariaDB / MySQL 最终审计总结

## 交付范围

- 已创建并转换独立目录 `mysql_beginner_practice`。
- 原目录 `sql_beginner_practice` 保留不变，方便以后对照 SQL Server 与 MySQL 写法。
- MySQL 目录共有 34 个要求文件：根目录 21 个，`answers` 目录 13 个。
- 课程仍使用独立数据库 `sql_beginner_practice`，没有操作其他现有数据库。

## Subagent 审计

- 已成功调用两个互相独立的 Subagent：
  - SQL 正确性审计员；
  - 教学质量审计员。
- 第一轮 MariaDB / MySQL 审计共发现：
  - 严重：2；
  - 一般：6；
  - 建议：3；
  - 合计：11。
- 11 项全部修复，3 条建议全部采纳，没有未采纳建议。
- 修复后再次进行正确性与教学质量复核。
- 最终未修复：严重 0、一般 0、建议 0。

主要修复包括：

- 第 9 天所有实际数据修改都使用完整的 `sql_beginner_practice.表名`，避免只运行片段时误改其他数据库同名表；
- 初始化末尾加入 `baseline_status` 检查，只有显示 `PASS` 才能继续课程；
- 修正 MariaDB 中无效文字 `CAST` 可能返回 0 并产生警告的说明；
- 让电压转换题同时出现成功、失败和 NULL 分支；
- 分段安排第 8 天内容，并解释最少量正则符号；
- 补齐部分复习题的返回列、预计结果和提示；
- 增加 NULL 与空字符串的重复巩固；
- 统一使用 `START TRANSACTION`、`LIMIT`、`IFNULL` 和 `DATABASE()`。

## 真实数据库执行

- 已在用户当前打开的 XAMPP 数据库服务上实际执行，不是仅静态检查。
- 实际服务端：MariaDB 10.4.32。
- 客户端：`D:\xampp\mysql\bin\mysql.exe`。
- 连接：`127.0.0.1:3306`，本地 `root`。
- 客户端字符集：`utf8mb4`。
- 唯一创建和修改的数据库：`sql_beginner_practice`。
- 最终全量回归：
  - 初始化脚本 1 个：exit 0；
  - 课程与阶段测试脚本 13 个：全部 exit 0；
  - 答案脚本 13 个：全部 exit 0；
  - 总计 27 个 SQL 文件，失败 0。

## 最终数据库状态

- `departments`：5 行；
- `employees`：20 行；
- `projects`：14 行；
- `project_metrics`：12 行；
- `employee_projects`：37 行；
- 临时部门 96、97、98、99：0 行，说明事务均已回滚；
- 员工 19 工资仍为 7200.00，员工 20 工资仍为 5000.00；
- 项目 10 仍为“暂停”、预算 350000.00；
- 电压转换中 10kV、35kV、110kV 成功转换，380V、“低压”和 NULL 返回 NULL。

## 尚存限制

- XAMPP 控制面板虽然把模块标为 MySQL，当前实际服务端是 MariaDB 10.4.32。课程使用的都是本套内容所需的 MariaDB/MySQL 兼容基础语法。
- 初始化脚本不会删除练习库中的额外数据；若 `baseline_status` 显示 `FAIL`，必须停止并检查，不能直接继续做题。
- DBeaver 的“运行选中 SQL”快捷键可能因个人设置不同，应以本机菜单显示为准。

## 第一天推荐顺序

1. 打开并运行 `00_create_database.sql`。
2. 确认末尾 `baseline_status` 为 `PASS`。
3. 运行 `USE sql_beginner_practice;`，再用 `SELECT DATABASE();` 确认当前数据库。
4. 独立完成 `00_diagnostic_test.sql`。
5. 查看 `diagnostic_review.md`，判断哪些知识不稳定。
6. 再开始 `01_select_basics.sql`。
7. 第一天不要打开全部答案文件。
