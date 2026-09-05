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

# 第 9 章：数据修改和事务

## 本章计时建议

- 一次 45～60 分钟是一个学习时段，不保证完成整章；
- 时段 A：核心概念、全部示例和最小修改，约 25～35 分钟；
- 时段 B：8 道练习至少 40 分钟，错题整理另需 5～10 分钟；
- 没完成就下次继续，不要为了赶时间提前看答案。

## 1. 本章目标

- 使用 `INSERT` 新增一行数据。
- 按安全顺序练习 `UPDATE` 和 `DELETE`。
- 使用 `START TRANSACTION`、`ROLLBACK` 和 `COMMIT` 控制修改。
- 每次修改前后都用 `SELECT` 验证目标行。
- 暂时不学习批量导入、存储过程和复杂事务控制。

## 2. 前置知识

需要会使用 `SELECT`、`WHERE` 和主键。开始前确认当前数据库是 `mysql_beginner_practice`。

## 3. 核心概念

### INSERT

#### 它解决什么问题

`INSERT` 向表中新增记录。练习时使用 9000 段的专用编号，并放在事务中默认回滚。

#### 最基本语法

```sql
START TRANSACTION;
INSERT INTO table_name (column_a, column_b)
VALUES (value_a, value_b);
SELECT ...;
ROLLBACK;
```

#### 怎么理解

明确写出列名，再按相同顺序提供值。验证后回滚，练习数据不会保留。

#### 常见错误

- 列和值数量不一致。
- 违反主键、非空或外键约束。
- 忘记回滚练习数据。

#### 如何验证结果

按专用主键查询新增行，并在回滚后再次查询确认它已消失。

### UPDATE

#### 它解决什么问题

`UPDATE` 修改已有记录。安全练习必须先确认目标，再修改，再验证，最后默认回滚。

#### 最基本语法

```sql
SELECT ... WHERE id = ...;
START TRANSACTION;
UPDATE table_name
SET column_name = ...
WHERE id = ...;
SELECT ... WHERE id = ...;
ROLLBACK;
```

#### 怎么理解

预览和修改使用同一个精确条件。没有 `WHERE` 会影响整张表，本章不实际执行这种语句。

#### 常见错误

- 漏写 `WHERE`。
- 预览条件与修改条件不一致。
- 看到“执行成功”却没有核对受影响行。

#### 如何验证结果

检查受影响行数、目标值和非目标行；回滚后确认原状态恢复。

### DELETE

#### 它解决什么问题

`DELETE` 删除满足条件的行。必须精确预览目标，并注意外键关联。

#### 最基本语法

```sql
SELECT ... WHERE id = ...;
START TRANSACTION;
DELETE FROM table_name
WHERE id = ...;
SELECT ... WHERE id = ...;
ROLLBACK;
```

#### 怎么理解

`DELETE` 删除整行，不是删除某个字段。练习只删除事务中创建的专用行。

#### 常见错误

- 忘记 `FROM` 或 `WHERE`。
- 删除仍被外键引用的记录。
- 验证时只看是否报错，不检查目标行。

#### 如何验证结果

删除后目标查询应为 0 行；回滚后专用行的状态应恢复。

### ROLLBACK 与 COMMIT

#### 它解决什么问题

`ROLLBACK` 撤销当前未提交事务，`COMMIT` 永久确认当前事务。

#### 最基本语法

```sql
START TRANSACTION;
-- 执行语句
ROLLBACK;
```

#### 怎么理解

本章所有数据修改练习默认 `ROLLBACK`。`COMMIT` 只在只读示例中观察语法，不用于保留练习数据。

#### 常见错误

- 以为 `ROLLBACK` 能撤销已经提交的修改。
- 在不确定结果时使用 `COMMIT`。
- 数据库工具开启自动提交却没有留意。

#### 如何验证结果

回滚后重新查询目标；提交前必须确认数据库、目标行和修改值。

## 4. 可运行示例

## 示例 1：新增一条专用练习部门

### 学习目标

使用明确列名执行 `INSERT`，并用回滚避免污染固定数据。

### 运行前预测

1. 插入后编号 9001 能查到几行？
2. 回滚后还能查到吗？
3. 固定部门数据会不会改变？

### 示例代码

```sql
USE mysql_beginner_practice;

START TRANSACTION;

INSERT INTO departments (department_id, department_name, city)
VALUES (9001, '事务练习部门', '测试城市');

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9001;

ROLLBACK;

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9001;
```

### 运行后观察

1. 回滚前是否有一行？
2. 回滚后是否为 0 行？
3. 是否只操作了编号 9001？

### 结果特征

- 插入后能查到专用行；
- 回滚后专用行消失；
- 固定数据不变。

### 最小修改任务

把专用编号改为 9011，部门名称改为“插入模仿部门”，仍然默认回滚。

### 本例常见错误

- 列和值顺序不一致；
- 使用已存在的主键；
- 忘记 `ROLLBACK`。

## 示例 2：安全修改专用练习部门

### 学习目标

在同一事务内创建专用行，并严格做到修改前预览、修改后验证、最后回滚。

### 运行前预测

1. 预览时城市是什么？
2. 更新后会影响几行？
3. 回滚后专用行还存在吗？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9002;

START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9002, '更新练习部门', '原城市');

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9002;

UPDATE departments
SET city = '新城市'
WHERE department_id = 9002;

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9002;

ROLLBACK;
```

### 运行后观察

1. 更新前后城市是否变化？
2. `WHERE` 是否只指向 9002？
3. 回滚后固定数据是否保持不变？

### 结果特征

- 更新只影响专用行；
- 验证查询显示新城市；
- 整个事务回滚，不保留练习数据。

### 最小修改任务

使用专用编号 9012，把城市从“甲城”改为“乙城”，仍按预览、修改、验证、回滚的顺序。

### 本例常见错误

- 预览与更新条件不同；
- 漏写 `WHERE`；
- 验证后误用 `COMMIT`。

## 示例 3：安全删除专用练习部门

### 学习目标

只删除已预览的专用行，并通过回滚恢复事务前状态。

### 运行前预测

1. 删除前目标查询有几行？
2. 删除后目标查询有几行？
3. 回滚后数据库会保留专用行吗？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9003;

START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9003, '删除练习部门', NULL);

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9003;

DELETE FROM departments
WHERE department_id = 9003;

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9003;

ROLLBACK;
```

### 运行后观察

1. 删除后的查询是否为 0 行？
2. 是否删除了其他部门？
3. 回滚后固定数据是否仍完整？

### 结果特征

- 只删除编号 9003 的专用行；
- 删除后目标为 0 行；
- 回滚后没有留下练习数据。

### 最小修改任务

使用专用编号 9013 和名称“删除模仿部门”重复安全删除流程。

### 本例常见错误

- 实际执行无 `WHERE` 的删除；
- 删除前没有预览；
- 把 `DELETE` 误解为清空一个字段。

## 示例 4：观察 COMMIT 的结束作用

### 学习目标

认识 `COMMIT` 会结束当前事务；本例只查询，不保留任何修改。

### 运行前预测

1. 本例会修改数据吗？
2. `COMMIT` 后能否再用同一事务的 `ROLLBACK` 撤销？
3. 结果会显示哪个数据库名？

### 示例代码

```sql
USE mysql_beginner_practice;

START TRANSACTION;

SELECT
    DATABASE() AS current_database,
    COUNT(*) AS department_count
FROM departments;

COMMIT;
```

### 运行后观察

1. 查询是否正常返回？
2. 部门行数是否改变？
3. 为什么本例可以安全使用 `COMMIT`？

### 结果特征

- 只返回当前数据库和部门数量；
- 没有数据修改；
- `COMMIT` 结束只读事务。

### 最小修改任务

把统计对象改为 `projects`，仍使用只读事务并以 `COMMIT` 结束。

### 本例常见错误

- 误以为 `COMMIT` 等于撤销；
- 修改结果未核对就提交；
- 忘记确认当前数据库。

## 示例 5：用受影响行数检查更新

### 学习目标

在安全更新后查看 `ROW_COUNT()`，再查询实际结果并默认回滚。

### 运行前预测

1. 精确主键条件应影响几行？
2. `ROW_COUNT()` 显示什么？
3. 回滚后专用行会不会保留？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9005;

START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9005, '行数检查部门', '旧城市');

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9005;

UPDATE departments
SET city = '新城市'
WHERE department_id = 9005;

SELECT ROW_COUNT() AS affected_rows;

SELECT department_id, department_name, city
FROM departments
WHERE department_id = 9005;

ROLLBACK;
```

### 运行后观察

1. 受影响行数是否为 1？
2. 验证查询是否显示新城市？
3. 如果受影响行数异常，是否应该提交？

### 结果特征

- 精确更新影响一行；
- 修改值可被查询验证；
- 默认回滚。

### 最小修改任务

使用专用编号 9015，把部门名称改为“已核对部门”，并检查受影响行数。

### 本例常见错误

- 只看 `ROW_COUNT()`，不查询实际值；
- `ROW_COUNT()` 之后又执行其他语句才查看；
- 受影响行数异常仍提交。

## 5. 容易混淆的地方

- `UPDATE` 和 `DELETE` 前必须先预览目标，能运行不等于目标正确。
- 无 `WHERE` 的 `UPDATE` 或 `DELETE` 会影响整张表，本章绝不实际执行。
- `ROLLBACK` 撤销未提交修改，`COMMIT` 永久确认修改。
- 本章 9000 段编号仅为临时练习数据，所有修改练习默认回滚。
- 外键可能阻止删除被其他表引用的记录。

## 6. 本章示例结束自检

1. 我是否每次都先确认当前数据库？
2. 我能否按“预览、修改、验证、回滚”解释安全流程？
3. 我是否知道无 `WHERE` 修改为什么危险？
4. 我能否解释 `ROLLBACK` 与 `COMMIT` 的区别？
5. 我是否检查过目标行、受影响行数和回滚结果？

## 7. 下一步

现在才打开 exercises.sql。不要提前打开 answers.sql。每道题至少独立思考 5～10 分钟，卡住后先看 hints.md。
