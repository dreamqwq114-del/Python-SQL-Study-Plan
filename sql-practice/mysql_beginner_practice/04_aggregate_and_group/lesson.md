# 本章学习顺序

1. 先完整阅读本章 lesson.md。
2. 按顺序阅读并运行 lesson.md 中的每个示例。
3. 每个示例运行前，先回答“运行前预测”。
4. 每次只复制并运行一个示例，不要整章一次执行。
5. 运行后回答“运行后观察”。
6. 完成示例后的“最小修改任务”。
7. 所有示例完成后，才打开 exercises.sql。
8. 每道练习至少独立思考 5～10 分钟。
9. 卡住后先看 hints.md。
10. 全部完成后才打开 answers.sql。
11. 真正做错的题记录到根目录 mistake_log.md。
12. 1～2 天后重新独立完成错题。

# 第 4 章：聚合和分组

## 本章计时建议

- 一次 45～60 分钟是一个学习时段，不保证完成整章；
- 时段 A：核心概念、全部示例和最小修改，约 25～35 分钟；
- 时段 B：8 道练习至少 40 分钟，错题整理另需 5～10 分钟；
- 没完成就下次继续，不要为了赶时间提前看答案。

## 1. 本章目标

- 使用 `COUNT`、`SUM`、`AVG`、`MIN`、`MAX` 汇总多行数据。
- 使用 `GROUP BY` 按类别得到一组一行的结果。
- 区分 `WHERE` 的分组前筛选和 `HAVING` 的分组后筛选。
- 解释 `COUNT(*)`、`COUNT(column)` 以及其他聚合函数如何处理 `NULL`。
- 暂时不学习连接分组、窗口函数和高级统计。

## 2. 前置知识

需要会使用 `SELECT`、`FROM`、`WHERE` 和 `ORDER BY`。

## 3. 核心概念

### COUNT 与 NULL

#### 它解决什么问题

`COUNT` 统计数量。`COUNT(*)` 统计行，`COUNT(column)` 只统计该列非 `NULL` 的行。

#### 最基本语法

```sql
SELECT
    COUNT(*) AS row_count,
    COUNT(nullable_column) AS non_null_count
FROM table_name;
```

#### 怎么理解

如果一行存在但目标列为空，`COUNT(*)` 会统计它，`COUNT(column)` 不会统计它。

#### 常见错误

- 以为两种 `COUNT` 永远相同。
- 使用 `COUNT('column_name')`，把字段名写成了固定文本。

#### 如何验证结果

找一列确实含 `NULL` 的字段，比较两个计数，并单独筛选 `IS NULL` 核对差值。

### SUM、AVG、MIN 与 MAX

#### 它解决什么问题

这些函数分别求合计、平均值、最小值和最大值。

#### 最基本语法

```sql
SELECT
    SUM(number_column),
    AVG(number_column),
    MIN(number_column),
    MAX(number_column)
FROM table_name;
```

#### 怎么理解

聚合函数把多行压缩成汇总结果。除 `COUNT(*)` 外，这些函数通常忽略输入中的 `NULL`。

#### 常见错误

- 对文本列使用 `SUM`。
- 把平均值误当成总和除以全部行数，即使该列含 `NULL`。

#### 如何验证结果

确认最小值不大于平均值，平均值不大于最大值，并核对汇总列是否有合理含义。

### GROUP BY

#### 它解决什么问题

`GROUP BY` 按一个或多个字段分组，每组返回一行汇总。

#### 最基本语法

```sql
SELECT
    group_column,
    COUNT(*) AS row_count
FROM table_name
GROUP BY group_column;
```

#### 怎么理解

相同分组值的行先放在一起，再对每组单独执行聚合函数。

#### 常见错误

- 在 `SELECT` 中放入既未分组也未聚合的字段。
- 忘记 `GROUP BY`，只得到整张表的一行汇总。

#### 如何验证结果

检查每个分组值是否只出现一行，并将各组计数相加与原总行数比较。

### WHERE 与 HAVING

#### 它解决什么问题

`WHERE` 在分组前筛选原始行；`HAVING` 在分组后筛选汇总后的组。

#### 最基本语法

```sql
SELECT group_column, COUNT(*) AS row_count
FROM table_name
WHERE row_condition
GROUP BY group_column
HAVING COUNT(*) >= 2;
```

#### 怎么理解

先用 `WHERE` 决定哪些原始行参与分组，再用 `HAVING` 决定保留哪些组。

#### 常见错误

- 在 `WHERE` 中写 `COUNT(*) >= 2`。
- 用 `HAVING` 代替所有普通行筛选。

#### 如何验证结果

先核对参与分组的原始行，再检查每个保留组是否满足聚合条件。

## 4. 可运行示例

## 示例 1：比较项目总数和非空结束日期数

### 学习目标

直观看到 `COUNT(*)` 与 `COUNT(column)` 对 `NULL` 的不同处理。

### 运行前预测

1. 结果有几列、几行？
2. 两个计数是否相同？
3. 哪个计数不会忽略 `NULL`？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    COUNT(*) AS project_count,
    COUNT(end_date) AS projects_with_end_date
FROM projects;
```

### 运行后观察

1. `project_count` 是否大于或等于第二个计数？
2. 两个计数的差值代表什么？
3. 返回结果中是否逐行列出项目？

### 结果特征

- 结果只有一行两列；
- 第一列统计所有项目；
- 第二列忽略 `end_date` 为 `NULL` 的行。

### 最小修改任务

改为比较员工总数和 `manager_id` 非空的员工数。

### 本例常见错误

- 把 `COUNT(*)` 理解成统计非空值；
- 给字段名加单引号；
- 看到一行结果就以为只检查了一行数据。

## 示例 2：汇总员工薪资

### 学习目标

用四种聚合函数从同一数值列得到不同汇总。

### 运行前预测

1. 结果会返回多少行？
2. 平均薪资是否应在最小值和最大值之间？
3. 原始薪资是否会被修改？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    SUM(salary) AS total_salary,
    AVG(salary) AS average_salary,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary
FROM employees;
```

### 运行后观察

1. 是否只有一行？
2. 最小值、平均值、最大值关系是否合理？
3. 再查询员工表时薪资是否未变？

### 结果特征

- 一行四列；
- 每列表示不同汇总含义；
- 聚合查询不会修改原数据。

### 最小修改任务

改为汇总项目预算的总和、平均值、最小值和最大值。

### 本例常见错误

- 聚合了错误字段；
- 忘记给汇总列起别名；
- 把结果当成新写入的数据。

## 示例 3：统计各部门员工数

### 学习目标

理解 `GROUP BY` 让每个部门得到一行计数。

### 运行前预测

1. 结果是一行还是多行？
2. 每个 `department_id` 会出现几次？
3. 各组人数相加是否应等于员工总数？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    department_id,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department_id
ORDER BY department_id ASC;
```

### 运行后观察

1. 每个部门是否只有一行？
2. `employee_count` 是否都是正数？
3. 各组计数之和是否等于员工总数？

### 结果特征

- 每个已有员工的部门一行；
- 结果有部门编号和人数两列；
- 排序让部门顺序稳定。

### 最小修改任务

改为按 `job_title` 分组统计各职位人数，并按人数降序、职位升序排列。

### 本例常见错误

- 忘记 `GROUP BY department_id`；
- 查询员工姓名却不聚合；
- 把分组行数误当成员工总数。

## 示例 4：先筛选再按状态汇总预算

### 学习目标

理解 `WHERE` 先决定哪些项目参与分组。

### 运行前预测

1. 2024-01-01 之前开始的项目是否参与汇总？
2. 结果每个状态有几行？
3. `SUM(budget)` 是整表总预算还是组内总预算？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    project_status,
    COUNT(*) AS project_count,
    SUM(budget) AS total_budget
FROM projects
WHERE start_date >= '2024-01-01'
GROUP BY project_status
ORDER BY project_status ASC;
```

### 运行后观察

1. 是否每个状态只有一行？
2. 计数之和是否等于符合日期条件的项目数？
3. 总预算是否只来自筛选后的项目？

### 结果特征

- 每个出现过的状态一行；
- 先按日期筛选，再按状态汇总；
- 总预算按组计算。

### 最小修改任务

把日期下限改为 2023-01-01，并按 `total_budget` 从高到低排列。

### 本例常见错误

- 把 `WHERE` 写到 `GROUP BY` 后；
- 认为日期筛选只影响显示、不影响汇总；
- 排序使用了错误方向。

## 示例 5：保留员工较多的部门

### 学习目标

使用 `HAVING` 筛选分组后的计数。

### 运行前预测

1. 人数少于 4 的部门会不会保留？
2. `HAVING` 在 `GROUP BY` 前还是后？
3. 能否把聚合条件直接写进 `WHERE`？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    department_id,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department_id
HAVING COUNT(*) >= 4
ORDER BY
    employee_count DESC,
    department_id ASC;
```

### 运行后观察

1. 每组人数是否都至少为 4？
2. 结果是否按人数降序？
3. 各组代表原始员工还是部门汇总？

### 结果特征

- 每行代表一个部门；
- 只保留满足人数条件的组；
- 相同人数时部门编号升序。

### 最小修改任务

改为保留平均薪资至少 12000 的部门，并显示部门编号和平均薪资。

### 本例常见错误

- 在 `WHERE` 中使用 `COUNT(*)`；
- 忘记分组；
- 用员工薪资行条件代替平均薪资组条件。

## 5. 容易混淆的地方

- `COUNT(*)` 统计行，`COUNT(column)` 不统计该列为 `NULL` 的行。
- `SUM`、`AVG`、`MIN`、`MAX` 通常忽略 `NULL` 输入。
- `GROUP BY` 后每行代表一个组，不再代表一条原始记录。
- `WHERE` 在分组前筛选行，`HAVING` 在分组后筛选组。
- 能运行的分组 SQL 也要检查计数是否因字段选择而错误。

## 6. 本章示例结束自检

1. 我能否解释两种 `COUNT` 的差别？
2. 我能否判断一条聚合查询返回一行还是多行？
3. 我是否会检查各组计数之和？
4. 我能否区分 `WHERE` 和 `HAVING`？
5. 我是否检查过 `NULL`、分组重复和汇总范围？

## 7. 下一步

现在才打开 exercises.sql。不要提前打开 answers.sql。每道题至少独立思考 5～10 分钟，卡住后先看 hints.md。
