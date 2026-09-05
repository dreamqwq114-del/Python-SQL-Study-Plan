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

# 第 8 章：CTE、EXISTS 和类型转换

## 本章计时建议

- 一次 45～60 分钟是一个学习时段，不保证完成整章；
- 时段 A：核心概念、全部示例和最小修改，约 25～35 分钟；
- 时段 B：8 道练习至少 40 分钟，错题整理另需 5～10 分钟；
- 没完成就下次继续，不要为了赶时间提前看答案。

## 1. 本章目标

- 使用 MySQL 8.0 非递归 CTE 为查询中的临时结果命名。
- 使用 `EXISTS` 和 `NOT EXISTS` 判断关联记录是否存在。
- 使用 `CAST` 转换结果的数据类型。
- 使用 `COALESCE` 为 `NULL` 提供显示值。
- 暂时不学习递归 CTE 和复杂嵌套子查询。

## 2. 前置知识

需要完成第 1～7 章，理解 `SELECT`、筛选、连接、分组和简单子查询。

## 3. 核心概念

### 非递归 CTE

#### 它解决什么问题

CTE 用 `WITH` 给一个临时查询结果起名字，让后面的主查询更容易分段阅读。

#### 最基本语法

```sql
WITH result_name AS
(
    SELECT ...
)
SELECT ...
FROM result_name;
```

#### 怎么理解

先阅读括号内的查询，再把它当作临时结果表使用。CTE 只在紧随其后的那一条语句中有效。

#### 常见错误

- 写完 CTE 后没有主查询。
- 误以为 CTE 会永久保存数据。
- 本章写递归 CTE，超出学习范围。

#### 如何验证结果

先单独理解 CTE 应产生哪些列和行，再检查主查询是否遗漏或重复记录。

### EXISTS 与 NOT EXISTS

#### 它解决什么问题

`EXISTS` 判断子查询是否至少找到一行；`NOT EXISTS` 判断一行也没有找到。

#### 最基本语法

```sql
SELECT ...
FROM parent_table AS p
WHERE EXISTS
(
    SELECT 1
    FROM child_table AS c
    WHERE c.parent_id = p.parent_id
);
```

#### 怎么理解

对子查询中的每个外层记录，只关心“有没有”，不关心 `SELECT 1` 的数值。内外层字段必须正确关联。

#### 常见错误

- 忘记关联内外层字段，导致所有外层行得到相同判断。
- 把“没有匹配”写成 `EXISTS`。
- 以为子查询中的 `SELECT 1` 会显示在结果里。

#### 如何验证结果

抽查一条有匹配和一条无匹配的数据，并确认结果没有因一对多关系而重复。

### CAST

#### 它解决什么问题

`CAST` 把查询结果转换为另一种数据类型，便于显示或比较。

#### 最基本语法

```sql
CAST(expression AS CHAR)
```

#### 怎么理解

转换只影响本次查询结果，不会修改原字段类型。本章只做简单、明确的转换。

#### 常见错误

- 使用其他数据库的专有转换函数。
- 忘记 `AS`。
- 误以为转换会永久改变表结构。

#### 如何验证结果

检查结果列的显示形式，并确认原字段值和表结构没有变化。

### COALESCE

#### 它解决什么问题

`COALESCE` 从左到右返回第一个非 `NULL` 值，适合为缺失值提供可读文本。

#### 最基本语法

```sql
COALESCE(nullable_column, '暂无')
```

#### 怎么理解

如果第一项不是 `NULL` 就返回它；否则继续看下一项。它不会回填原表。

#### 常见错误

- 把空字符串和 `NULL` 当成同一件事。
- 替代值的数据含义与原列不一致。
- 误以为结果中的替代值已写回数据库。

#### 如何验证结果

检查原本为 `NULL` 的行是否显示替代值，同时确认原字段仍包含 `NULL`。

## 4. 可运行示例

## 示例 1：用 CTE 整理高预算项目

### 学习目标

理解非递归 CTE 是一条查询中的临时命名结果。

### 运行前预测

1. CTE 中会产生哪三列？
2. 主查询会不会显示预算低于 700000 的项目？
3. CTE 会不会创建永久表？

### 示例代码

```sql
USE mysql_beginner_practice;

WITH high_budget_projects AS
(
    SELECT
        project_id,
        project_name,
        budget
    FROM projects
    WHERE budget >= 700000
)
SELECT
    project_name,
    budget
FROM high_budget_projects
ORDER BY budget DESC, project_id ASC;
```

### 运行后观察

1. 最终结果有几列？
2. 预算是否都达到 700000？
3. 下一条语句还能直接使用 `high_budget_projects` 吗？

### 结果特征

- 最终结果只有项目名称和预算两列；
- 预算按从高到低排列；
- CTE 不会永久保存。

### 最小修改任务

把预算条件改为不少于 800000，并按预算降序、项目编号升序排列。

### 本例常见错误

- CTE 后漏写主查询；
- 在主查询中引用 CTE 未提供的字段；
- 误把 CTE 当成永久表。

## 示例 2：查找有参与人员的项目

### 学习目标

使用 `EXISTS` 判断项目是否至少有一条人员参与记录。

### 运行前预测

1. 没有参与人员的项目会出现吗？
2. 一个项目有多人参与时会重复几行？
3. `SELECT 1` 会成为结果列吗？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name
FROM projects AS p
WHERE EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.project_id = p.project_id
)
ORDER BY p.project_id ASC;
```

### 运行后观察

1. 结果中的每个项目是否至少有一条参与记录？
2. 项目是否因多人参与而重复？
3. 结果是否只有两列？

### 结果特征

- 只返回有参与人员的项目；
- 每个项目最多一行；
- 子查询中的 `1` 不会显示。

### 最小修改任务

改为查找至少有项目参与记录的员工，显示员工编号和姓名。

### 本例常见错误

- 漏写 `ep.project_id = p.project_id`；
- 把项目编号和员工编号错误关联；
- 使用连接后忘记处理重复。

## 示例 3：查找没有指标记录的项目

### 学习目标

使用 `NOT EXISTS` 找出完全没有匹配记录的数据。

### 运行前预测

1. 有指标记录的项目会出现吗？
2. 结果是否可能包含 `project_metrics` 的列？
3. 项目会不会重复？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name
FROM projects AS p
WHERE NOT EXISTS
(
    SELECT 1
    FROM project_metrics AS pm
    WHERE pm.project_id = p.project_id
)
ORDER BY p.project_id ASC;
```

### 运行后观察

1. 每个结果项目是否都找不到指标记录？
2. 返回了多少列？
3. 与 `LEFT JOIN ... IS NULL` 的目标是否相同？

### 结果特征

- 只返回没有指标记录的项目；
- 每个项目一行；
- 不显示右表字段。

### 最小修改任务

改为查找没有任何项目参与记录的员工。

### 本例常见错误

- 把 `NOT EXISTS` 写成 `EXISTS`；
- 漏写内外层关联条件；
- 在外层 `SELECT` 中直接引用子查询别名。

## 示例 4：把项目编号转换为文本

### 学习目标

理解 `CAST` 只改变本次结果的类型。

### 运行前预测

1. 结果有几列？
2. `project_id_text` 是否仍显示编号内容？
3. 原字段类型会不会变化？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    project_id,
    CAST(project_id AS CHAR) AS project_id_text,
    project_name
FROM projects
ORDER BY project_id ASC;
```

### 运行后观察

1. 原编号和文本编号内容是否对应？
2. 两个编号列的显示类型是否相同？
3. 再查表结构时，`project_id` 是否仍为整数？

### 结果特征

- 结果有三列；
- 编号内容保持对应；
- 表结构没有变化。

### 最小修改任务

把 `employee_id` 转换为文本，显示原编号、文本编号和员工姓名。

### 本例常见错误

- 写成其他数据库的专有转换函数；
- 漏写目标类型；
- 误以为转换会修改表结构。

## 示例 5：显示缺失的电压等级

### 学习目标

使用 `COALESCE` 为 `NULL` 提供清楚的显示文本。

### 运行前预测

1. `voltage_level` 为 `NULL` 时会显示什么？
2. 非 `NULL` 值会不会改变？
3. 原表中的 `NULL` 会不会被更新？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    project_id,
    COALESCE(voltage_level, '未填写') AS voltage_level_display
FROM project_metrics
ORDER BY project_id ASC;
```

### 运行后观察

1. 是否还能在显示列中看到 `NULL`？
2. 已填写的电压等级是否保持原值？
3. 再查询原字段时，原来的 `NULL` 是否仍存在？

### 结果特征

- 每条指标记录一行；
- 缺失电压等级显示为“未填写”；
- 原数据没有被修改。

### 最小修改任务

为缺失的投资收益率显示 `0`，保留项目编号，并按项目编号升序。

### 本例常见错误

- 把 `NULL` 与空字符串混淆；
- 在结果显示数值列时填入难以计算的文本；
- 误以为 `COALESCE` 会更新原表。

## 5. 容易混淆的地方

- CTE 只服务于紧随其后的一条语句，不是永久表。
- `EXISTS` 只判断是否存在，不会把子查询的 `SELECT 1` 加入结果。
- `EXISTS` 或 `NOT EXISTS` 忘记关联条件，通常会得到整体错误的结果。
- `CAST` 只转换查询结果，不会修改原字段类型。
- `COALESCE` 只改变显示结果，不会把替代值写回原表。

## 6. 本章示例结束自检

1. 我能否解释 CTE 为什么只是临时命名结果？
2. 我能否分清 `EXISTS` 与 `NOT EXISTS`？
3. 我是否会检查存在性查询有没有漏写关联条件？
4. 我能否解释 `CAST` 和 `COALESCE` 不会修改原数据？
5. 我是否检查过列数、行数、`NULL` 和重复？

## 7. 下一步

现在才打开 exercises.sql。不要提前打开 answers.sql。每道题至少独立思考 5～10 分钟，卡住后先看 hints.md。
