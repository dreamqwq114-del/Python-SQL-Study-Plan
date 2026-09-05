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

# 第 5 章：INNER JOIN

## 本章计时建议

- 一次 45～60 分钟是一个学习时段，不保证完成整章；
- 时段 A：核心概念、全部示例和最小修改，约 25～35 分钟；
- 时段 B：8 道练习至少 40 分钟，错题整理另需 5～10 分钟；
- 没完成就下次继续，不要为了赶时间提前看答案。

## 1. 本章目标

- 理解主键、外键以及表之间的对应关系。
- 使用 `INNER JOIN` 连接两张表或三张表。
- 使用表别名明确字段来自哪张表。
- 能发现连接条件缺失或写错造成的行数异常。
- 暂时不学习保留无匹配行的连接方式。

## 2. 前置知识

需要会使用 `SELECT`、`WHERE`、`ORDER BY`，并知道一张表中的一行代表一条记录。

## 3. 核心概念

### 主键与外键

#### 它解决什么问题

主键唯一标识一行；外键保存另一张表的主键值，让两张表可以建立对应关系。

#### 最基本语法

```sql
FROM child_table AS c
INNER JOIN parent_table AS p
    ON c.foreign_key = p.primary_key
```

#### 怎么理解

例如 `employees.department_id` 是外键，指向 `departments.department_id` 主键。一个部门可以对应多名员工。

#### 常见错误

- 把两个不相关的字段连接起来。
- 只凭字段名相似就认定它们有关系。
- 误以为外键列本身必须唯一。

#### 如何验证结果

检查连接字段的含义、返回行数和重复情况。员工连接部门后，每名有匹配部门的员工应出现一次。

### INNER JOIN 与 ON

#### 它解决什么问题

`INNER JOIN` 把两张表中满足 `ON` 条件的行组合起来，只保留两边都匹配的记录。

#### 最基本语法

```sql
SELECT ...
FROM table_a AS a
INNER JOIN table_b AS b
    ON a.key_column = b.key_column;
```

#### 怎么理解

数据库先按照 `ON` 寻找配对，再从配对后的行中选择结果列。没有匹配的行不会出现在结果中。

#### 常见错误

- 漏写或写错 `ON` 条件，产生过多组合。
- 把 `ON` 写成两个主键彼此相等，但它们并不是同一业务含义。
- 以为 `INNER JOIN` 会保留没有匹配的数据。

#### 如何验证结果

检查是否漏掉无匹配记录，比较连接前后的行数，并抽查连接后的名称是否确实对应。

### 表别名与限定列名

#### 它解决什么问题

表别名缩短 SQL；`别名.字段名` 明确字段来自哪张表，避免同名字段产生歧义。

#### 最基本语法

```sql
SELECT
    a.id,
    b.name
FROM table_a AS a
INNER JOIN table_b AS b
    ON a.other_id = b.id;
```

#### 怎么理解

`a`、`b` 只在当前 SQL 中代表对应表。两张表都有 `department_id` 时，必须写清是 `e.department_id` 还是 `d.department_id`。

#### 常见错误

- 定义别名后又继续使用原表名。
- 同名字段前不加表别名。
- 别名太随意，自己也分不清。

#### 如何验证结果

检查每个结果列的来源，确认同名字段没有引用错表。

### 三表连接

#### 它解决什么问题

当目标信息分散在三张表时，可以从第一张表依次连接第二张和第三张表。

#### 最基本语法

```sql
FROM table_a AS a
INNER JOIN table_b AS b ON ...
INNER JOIN table_c AS c ON ...
```

#### 怎么理解

每个 `JOIN` 都需要自己的连接条件。先明确“谁连接谁”，再写对应主键和外键。

#### 常见错误

- 第二个 `JOIN` 复用了错误的连接字段。
- 少写一个连接条件，结果行数突然增多。
- 忘记某个 `INNER JOIN` 会过滤无匹配行。

#### 如何验证结果

先运行两表版本，再加第三张表；每增加一张表都检查行数、重复和缺失记录。

### 连接后的行数

#### 它解决什么问题

理解“一对多”连接为什么会让一方的一行在结果中出现多次。

#### 最基本语法

```sql
FROM one_side AS o
INNER JOIN many_side AS m
    ON o.id = m.one_id
```

#### 怎么理解

一个项目有多名参与人员，项目连接参与记录后会出现多行。这不是数据库自动制造了重复数据，而是每行代表不同的参与关系。

#### 常见错误

- 看到项目名称重复就立即使用 `DISTINCT`。
- 把参与记录行数误当成项目数量。
- 缺少连接条件时没有检查异常大的行数。

#### 如何验证结果

确认结果每行代表什么，检查主键组合是否重复，并比较某个项目的参与人数与返回行数。

## 4. 可运行示例

## 示例 1：为员工显示部门名称

### 学习目标

使用外键和主键完成最基本的两表 `INNER JOIN`。

### 运行前预测

1. 结果有几列？
2. 每名员工会匹配哪个字段相同的部门？
3. 没有匹配部门的员工会不会保留？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    e.employee_id,
    e.employee_name,
    d.department_name
FROM employees AS e
INNER JOIN departments AS d
    ON e.department_id = d.department_id
ORDER BY e.employee_id;
```

### 运行后观察

1. 是否每名员工只出现一次？
2. 员工和部门名称是否对应合理？
3. `department_id` 为什么没有显示在结果中？

### 结果特征

- 结果有三列；
- 当前固定数据中应包含全部员工；
- 结果按 `employee_id` 升序，便于重复核对。

### 最小修改任务

在结果中增加员工的 `job_title`。

### 本例常见错误

- 把 `e.department_id` 与 `d.department_name` 相连；
- 两张表都有 `department_id` 时不写表别名；
- 忘记 `ON`。

## 示例 2：为项目显示所属部门

### 学习目标

用相同连接结构解决另一组主键、外键关系。

### 运行前预测

1. 项目表中的哪个字段指向部门表？
2. 结果会返回项目还是员工？
3. 每个项目应出现几次？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name,
    d.department_name
FROM projects AS p
INNER JOIN departments AS d
    ON p.department_id = d.department_id
ORDER BY p.project_id;
```

### 运行后观察

1. 是否每个项目只有一行？
2. `p` 和 `d` 分别代表哪张表？
3. 返回行数是否与项目总数一致？

### 结果特征

- 结果有三列；
- 当前固定数据中每个项目都有所属部门；
- 表别名只影响当前 SQL。

### 最小修改任务

增加 `project_status`，并把结果按项目编号保持升序。

### 本例常见错误

- 使用员工表的 `department_id` 作为连接字段；
- 定义 `p` 后仍写 `projects.project_name`；
- 误以为表别名会修改表名。

## 示例 3：查询项目及其项目经理

### 学习目标

观察 `INNER JOIN` 会丢掉没有匹配项目经理的项目。

### 运行前预测

1. `project_manager_id` 应与员工表哪个字段连接？
2. 项目经理为 `NULL` 的项目会不会出现？
3. 返回行数会不会等于项目总数？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name,
    e.employee_name AS manager_name
FROM projects AS p
INNER JOIN employees AS e
    ON p.project_manager_id = e.employee_id
ORDER BY p.project_id;
```

### 运行后观察

1. 是否有项目没有出现在结果中？
2. 缺失项目的 `project_manager_id` 有什么特征？
3. `INNER JOIN` 为什么不会为它生成一行？

### 结果特征

- 结果有三列；
- 只包含能匹配到员工的项目；
- 返回行数应少于项目总数。

### 最小修改任务

增加项目的 `project_status` 列。

### 本例常见错误

- 连接 `p.project_id = e.employee_id`；
- 以为无经理项目会显示 `NULL`；
- 只看 SQL 能运行，没有检查遗漏的数据。

## 示例 4：同时显示项目、部门和经理

### 学习目标

为一个项目依次连接部门表和员工表。

### 运行前预测

1. 一共使用几张表？
2. 每个 `INNER JOIN` 是否都需要自己的 `ON`？
3. 无项目经理的项目会不会保留？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_name,
    d.department_name,
    e.employee_name AS manager_name
FROM projects AS p
INNER JOIN departments AS d
    ON p.department_id = d.department_id
INNER JOIN employees AS e
    ON p.project_manager_id = e.employee_id
ORDER BY p.project_id;
```

### 运行后观察

1. 两个连接条件分别描述什么关系？
2. 是否出现无经理项目？
3. 增加第三张表后，行数为何没有成倍增加？

### 结果特征

- 结果有三列；
- 每行表示一个“项目—部门—经理”组合；
- 只保留部门和经理都能匹配的项目。

### 最小修改任务

增加项目预算 `budget`，并按预算降序、项目名称升序排列。

### 本例常见错误

- 第二个 `ON` 仍然连接部门编号；
- 某个同名字段没有表别名前缀；
- 误以为三张表必然产生重复。

## 示例 5：查看项目参与人员

### 学习目标

通过中间表连接员工与项目，并观察一对多关系增加行数。

### 运行前预测

1. `employee_projects` 中哪两个字段负责连接？
2. 同一个项目名称会不会出现多次？
3. 每一行代表员工还是参与关系？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_name,
    e.employee_name,
    ep.role_name,
    ep.working_hours
FROM employee_projects AS ep
INNER JOIN projects AS p
    ON ep.project_id = p.project_id
INNER JOIN employees AS e
    ON ep.employee_id = e.employee_id
ORDER BY
    p.project_id,
    e.employee_id;
```

### 运行后观察

1. 为什么相同项目名称会出现多行？
2. 是否每行都对应一条不同的员工参与记录？
3. 返回行数是否与参与关系总数一致？

### 结果特征

- 结果有四列；
- 项目和员工都可能在不同参与关系中重复出现；
- 当前固定数据中每行对应唯一的“员工—项目”关系。

### 最小修改任务

增加 `p.project_status`，其他连接条件保持不变。

### 本例常见错误

- 把 `ep.project_id` 连接到 `e.employee_id`；
- 看到项目名重复就错误使用 `DISTINCT`；
- 漏写一个 `ON`，使结果行数异常增大。

## 5. 容易混淆的地方

- 主键唯一标识一行；外键可以在多行中重复出现。
- `INNER JOIN` 只保留两边都有匹配的记录。
- `ON` 说明两张表如何配对，不能只看字段类型相同。
- 一对多连接后名称重复可能是正确结果，要先判断每行代表什么。
- 缺少连接条件可能产生大量错误组合；能运行不代表连接正确。

## 6. 本章示例结束自检

1. 我能否指出员工表连接部门表使用的主键和外键？
2. 我能否解释 `INNER JOIN` 为什么会漏掉无经理项目？
3. 我是否会给每个同名字段加上表别名？
4. 我能否为三张表分别写出正确连接关系？
5. 我是否检查过行数、重复和没有匹配的数据？

## 7. 下一步

现在才打开 exercises.sql。不要提前打开 answers.sql。每道题至少独立思考 5～10 分钟，卡住后先看 hints.md。
