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

# 第 6 章：LEFT JOIN 和重复

## 本章计时建议

- 一次 45～60 分钟是一个学习时段，不保证完成整章；
- 时段 A：核心概念、全部示例和最小修改，约 25～35 分钟；
- 时段 B：8 道练习至少 40 分钟，错题整理另需 5～10 分钟；
- 没完成就下次继续，不要为了赶时间提前看答案。

## 1. 本章目标

- 使用 `LEFT JOIN` 保留左表中没有匹配的数据。
- 找出没有项目、指标或参与记录的数据。
- 区分一对一、一对多和多对多关系造成的行数变化。
- 使用 `COUNT(DISTINCT ...)` 避免连接后重复计数。
- 暂时不学习更多连接类型或复杂去重技巧。

## 2. 前置知识

需要会使用 `INNER JOIN`、`GROUP BY`、`COUNT`、`WHERE` 和表别名。

## 3. 核心概念

### LEFT JOIN

#### 它解决什么问题

`LEFT JOIN` 保留左表全部行。右表没有匹配时，右表列显示为 `NULL`。

#### 最基本语法

```sql
SELECT ...
FROM left_table AS l
LEFT JOIN right_table AS r
    ON l.id = r.left_id;
```

#### 怎么理解

先决定哪张表必须完整保留，把它写在 `FROM` 后。匹配失败不会删除左表行，只会让右表字段为空。

#### 常见错误

- 把必须保留的表放在右边。
- 以为 `LEFT JOIN` 保留左右两边全部行。
- 没有检查右表字段中的 `NULL`。

#### 如何验证结果

比较左表总行数与结果覆盖范围，检查是否漏掉无匹配数据，并观察右表列的 `NULL`。

### INNER JOIN 与 LEFT JOIN

#### 它解决什么问题

两者使用相同连接条件，但决定是否保留左表无匹配行的规则不同。

#### 最基本语法

```sql
FROM left_table AS l
INNER JOIN right_table AS r ON ...

FROM left_table AS l
LEFT JOIN right_table AS r ON ...
```

#### 怎么理解

只关心匹配成功的记录用 `INNER JOIN`；还要检查“没有匹配”的记录时用 `LEFT JOIN`。

#### 常见错误

- 题目要求全部项目，却使用 `INNER JOIN`。
- 只看返回列，不比较缺失记录。

#### 如何验证结果

分别检查有匹配和无匹配样本，比较两种连接的行数和 `NULL`。

### 查找没有匹配的记录

#### 它解决什么问题

先用 `LEFT JOIN` 保留左表，再筛选右表连接键为 `NULL`，即可找到没有匹配的数据。

#### 最基本语法

```sql
FROM left_table AS l
LEFT JOIN right_table AS r ON ...
WHERE r.primary_key IS NULL;
```

#### 怎么理解

右表主键原本不可能为 `NULL`；连接后它为 `NULL`，说明没有找到对应行。

#### 常见错误

- 写成 `= NULL`。
- 检查右表中本来就允许为 `NULL` 的业务字段。
- 使用 `INNER JOIN` 后再找 `NULL`。

#### 如何验证结果

手工检查这些左表主键在右表中是否真的不存在，并确认没有误选已有匹配的数据。

### 一对一、一对多和多对多

#### 它解决什么问题

关系类型帮助预测连接后行数以及名称为什么会重复。

#### 最基本语法

```sql
FROM projects AS p
LEFT JOIN employee_projects AS ep
    ON p.project_id = ep.project_id
```

#### 怎么理解

项目与指标接近一对一；项目与参与记录是一对多；员工与项目通过 `employee_projects` 形成多对多。连接后每个匹配组合占一行。

#### 常见错误

- 把正确的一对多结果误当成重复数据。
- 直接使用 `DISTINCT` 隐藏没有理解的重复。
- 用参与关系行数代表项目数量。

#### 如何验证结果

先说清每一行代表什么，再检查主键组合、重复来源和没有匹配的记录。

### COUNT(DISTINCT ...)

#### 它解决什么问题

`COUNT(DISTINCT ...)` 在一对多连接后只统计不重复的目标值。

#### 最基本语法

```sql
COUNT(DISTINCT r.id)
```

#### 怎么理解

一对多连接会让同一项目出现多次。计数前要先确定数的是项目、员工还是参与关系行。

#### 常见错误

- 连接后一律使用 `COUNT(*)`；
- 选错需要去重的字段。

#### 如何验证结果

同时查看原始连接行数和不重复计数，解释两者为什么不同。

### LEFT JOIN 后筛选右表字段

#### 它解决什么问题

把右表条件放在 `ON` 中，可以限制匹配内容，同时继续保留左表无匹配行。

#### 最基本语法

```sql
LEFT JOIN right_table AS r
    ON l.id = r.left_id
   AND r.status = ...
```

#### 怎么理解

`WHERE` 在连接完成后筛选。若要求右表字段等于某值，无匹配行中的 `NULL` 会被过滤，使结果表现得像 `INNER JOIN`。

#### 常见错误

- 在 `WHERE` 筛选右表字段，意外丢掉左表无匹配行。
- 只检查匹配行，没有检查应保留的左表行。

#### 如何验证结果

对比条件放在 `WHERE` 和 `ON` 的结果行数，并检查无匹配左表行是否仍存在。

## 4. 可运行示例

## 示例 1：保留所有项目并显示项目指标

### 学习目标

观察 `LEFT JOIN` 如何保留没有指标记录的项目。

### 运行前预测

1. 哪张表必须全部保留？
2. 无指标项目的指标列显示什么？
3. 返回项目数会不会少于项目总数？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name,
    pm.voltage_level
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON p.project_id = pm.project_id
ORDER BY p.project_id;
```

### 运行后观察

1. 是否包含无指标项目？
2. 这些项目的 `voltage_level` 是什么？
3. 为什么必须把 `projects` 放在左边？

### 结果特征

- 结果有三列；
- 应覆盖全部项目；
- 无指标项目的右表列为 `NULL`。

### 最小修改任务

增加 `pm.management_fee` 列。

### 本例常见错误

- 使用 `INNER JOIN` 导致项目缺失；
- 把 `project_metrics` 放在左表；
- 用 `= NULL` 判断空值。

## 示例 2：保留所有员工及其参与项目

### 学习目标

观察一名员工参加多个项目和没有项目时的不同结果。

### 运行前预测

1. 同一员工能否出现多行？
2. 没有项目的员工会不会出现？
3. 无项目员工的项目名称是什么？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    e.employee_id,
    e.employee_name,
    p.project_name
FROM employees AS e
LEFT JOIN employee_projects AS ep
    ON e.employee_id = ep.employee_id
LEFT JOIN projects AS p
    ON ep.project_id = p.project_id
ORDER BY
    e.employee_id,
    p.project_id;
```

### 运行后观察

1. 哪些员工出现了多行，为什么？
2. 是否能找到项目名称为 `NULL` 的员工？
3. 结果行数为什么可能大于员工总数？

### 结果特征

- 应覆盖全部员工；
- 每条匹配的参与关系占一行；
- 无项目员工仍保留，项目名称为 `NULL`。

### 最小修改任务

增加中间表中的 `role_name`。

### 本例常见错误

- 第二个连接错误使用员工编号；
- 看到员工重复就立即加 `DISTINCT`；
- 用 `INNER JOIN` 连接项目表，导致无项目员工再次丢失。

## 示例 3：查找没有参与人员的项目

### 学习目标

用 `LEFT JOIN` 和 `IS NULL` 找无匹配记录。

### 运行前预测

1. 应检查右表哪个连接字段？
2. `WHERE ep.project_id = NULL` 能否找到结果？
3. 返回的项目在中间表中是否存在？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name
FROM projects AS p
LEFT JOIN employee_projects AS ep
    ON p.project_id = ep.project_id
WHERE ep.project_id IS NULL
ORDER BY p.project_id;
```

### 运行后观察

1. 结果中的项目是否都没有参与记录？
2. 为什么检查 `ep.project_id` 而不是项目名称？
3. 如果改成 `INNER JOIN` 会发生什么？

### 结果特征

- 结果只有项目编号和名称；
- 只包含没有参与人员的项目；
- 不应有同一项目重复。

### 最小修改任务

改为查找没有指标记录的项目。

### 本例常见错误

- 写成 `= NULL`；
- 筛选 `p.project_id IS NULL`；
- 先使用 `INNER JOIN`。

## 示例 4：观察一个项目的一对多参与记录

### 学习目标

理解项目名称重复是不同参与关系造成的。

### 运行前预测

1. 项目 1 是否可能返回多行？
2. 每行由哪个员工字段区分？
3. 使用 `DISTINCT project_name` 会丢失什么信息？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name,
    e.employee_id,
    e.employee_name
FROM projects AS p
INNER JOIN employee_projects AS ep
    ON p.project_id = ep.project_id
INNER JOIN employees AS e
    ON ep.employee_id = e.employee_id
WHERE p.project_id = 1
ORDER BY e.employee_id;
```

### 运行后观察

1. 相同项目名称出现了几次？
2. 每行员工编号是否不同？
3. 这些行是错误重复还是不同关系？

### 结果特征

- 每行表示项目 1 的一名参与人员；
- 项目列重复，但员工编号不同；
- 不应把这些关系随意去重。

### 最小修改任务

增加 `ep.working_hours`，并保持员工编号升序。

### 本例常见错误

- 用 `DISTINCT` 隐藏参与人员；
- 把项目重复当成笛卡尔积；
- 忘记检查员工编号。

## 示例 5：按部门统计项目数和参与行数

### 学习目标

比较连接行数与不重复项目数。

### 运行前预测

1. 一个项目有多人参与时，项目编号会出现几次？
2. `COUNT(ep.employee_id)` 统计什么？
3. `COUNT(DISTINCT p.project_id)` 统计什么？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    d.department_name,
    COUNT(DISTINCT p.project_id) AS project_count,
    COUNT(ep.employee_id) AS participation_count
FROM departments AS d
LEFT JOIN projects AS p
    ON d.department_id = p.department_id
LEFT JOIN employee_projects AS ep
    ON p.project_id = ep.project_id
GROUP BY
    d.department_id,
    d.department_name
ORDER BY d.department_id;
```

### 运行后观察

1. 两个计数是否总是相同？
2. 为什么一个项目多人参与不会增加 `project_count`？
3. 没有参与人员的项目是否仍被统计为项目？

### 结果特征

- 每个部门一行；
- `project_count` 统计不重复项目；
- `participation_count` 统计参与关系行。

### 最小修改任务

增加 `COUNT(DISTINCT ep.employee_id) AS employee_count`，统计每个部门项目涉及的不重复员工数。

### 本例常见错误

- 使用 `COUNT(*)` 当项目数；
- 忘记 `DISTINCT` 导致项目重复计数；
- `GROUP BY` 漏掉部门编号或名称。

## 示例 6：对比 WHERE 与 ON 中的右表条件

### 学习目标

观察右表条件放在 `WHERE` 时会丢掉无匹配项目，放在 `ON` 时会保留。

### 运行前预测

1. 查询 A 是否只返回电压等级为 `380V` 的匹配项目？
2. 查询 B 是否仍返回全部项目？
3. 查询 B 中不匹配的 `voltage_level` 会显示什么？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name,
    pm.voltage_level
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON pm.project_id = p.project_id
WHERE pm.voltage_level = '380V'
ORDER BY p.project_id;

SELECT
    p.project_id,
    p.project_name,
    pm.voltage_level
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON pm.project_id = p.project_id
   AND pm.voltage_level = '380V'
ORDER BY p.project_id;
```

### 运行后观察

1. 两个结果集的行数是否相同？
2. 查询 A 为什么没有 `NULL` 行？
3. 查询 B 为什么能保留电压不是 `380V` 或没有指标的项目？

### 结果特征

- 查询 A 只保留右表条件匹配的项目；
- 查询 B 保留全部项目，不匹配的右表列显示 `NULL`；
- 两条 SQL 都能运行，但回答的问题不同。

### 最小修改任务

把两条查询中的目标电压都改为 `110kV`，再次比较行数。

### 本例常见错误

- 认为 `WHERE` 和 `ON` 中的右表条件效果相同；
- 只检查匹配值，不检查无匹配项目；
- 忘记第二条查询的右表字段允许出现 `NULL`。

## 5. 容易混淆的地方

- `LEFT JOIN` 只保证保留左表全部行。
- 查无匹配记录要检查右表连接键 `IS NULL`，不能写 `= NULL`。
- 一对多和多对多连接后重复名称可能是正确业务关系。
- `COUNT(*)`、`COUNT(column)` 和 `COUNT(DISTINCT column)` 统计含义不同。
- `LEFT JOIN` 后在 `WHERE` 中筛选右表字段，可能让它表现得像 `INNER JOIN`。

## 6. 本章示例结束自检

1. 我能否根据题意选择哪张表放在左边？
2. 我能否找到没有参与人员或指标的项目？
3. 我能否解释连接后名称重复的原因？
4. 我是否会使用 `COUNT(DISTINCT ...)` 避免重复计数？
5. 我是否检查了 `NULL`、无匹配记录和右表筛选位置？

## 7. 下一步

现在才打开 exercises.sql。不要提前打开 answers.sql。每道题至少独立思考 5～10 分钟，卡住后先看 hints.md。
