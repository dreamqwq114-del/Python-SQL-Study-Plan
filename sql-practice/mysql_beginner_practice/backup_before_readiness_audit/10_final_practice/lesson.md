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

# 第 10 章：综合项目经营分析

## 本章计时建议

- 一次 45～60 分钟是一个学习时段，不保证完成整章；
- 时段 A：分析方法、全部示例和最小修改，约 25～35 分钟；
- 时段 B：8 道练习至少 40 分钟，错题整理另需 5～10 分钟；
- 没完成就下次继续，不要为了赶时间提前看答案。

## 1. 本章目标

- 把筛选、排序、分组、连接和 `CASE` 组合成经营分析查询。
- 围绕部门、员工、项目、经理、参与人员和项目指标检查结果。
- 正确处理管理费、投资收益率、电压等级、项目状态、`NULL` 和重复。
- 能解释查询结果为什么正确，而不只满足于“能够运行”。
- 本章不引入窗口函数、递归 CTE 或高级调优。

## 2. 前置知识

需要完成第 1～8 章。第 9 章事务知识不用于本章查询，但仍要保持只操作练习数据库。

## 3. 核心概念

### 先确定分析粒度

#### 它解决什么问题

先决定“一行代表什么”，才能选择正确的表、连接和聚合。例如一行代表一个项目，还是一个部门。

#### 最基本语法

```sql
SELECT key_column, ...
FROM ...
GROUP BY key_column, ...;
```

#### 怎么理解

先写出结果主键，再检查连接是否让同一个对象出现多行。

#### 常见错误

- 想要每项目一行，却直接显示参与人员明细。
- 分组列不完整。
- 连接后没有检查重复。

#### 如何验证结果

检查结果行数、主键是否重复，以及一行的业务含义是否一致。

### 保留未匹配数据

#### 它解决什么问题

经营分析常要保留没有经理、人员或指标的项目，因此要正确使用 `LEFT JOIN`。

#### 最基本语法

```sql
SELECT ...
FROM main_table AS m
LEFT JOIN detail_table AS d
    ON d.main_id = m.main_id;
```

#### 怎么理解

左表记录全部保留。右表没有匹配时，其字段为 `NULL`，可用 `COALESCE` 显示说明。

#### 常见错误

- 使用 `INNER JOIN` 漏掉无匹配项目。
- 在 `WHERE` 中筛选右表字段，让左连接表现得像内连接。
- 把 `NULL` 当成 0 而没有说明。

#### 如何验证结果

专门检查没有经理、人员或指标的项目是否仍在结果中。

### 一对多下的计数和金额

#### 它解决什么问题

项目连接多人参与表后会变成多行，计数和预算可能被重复计算。

#### 最基本语法

```sql
COUNT(DISTINCT detail_id)
```

#### 怎么理解

先辨认连接关系。计算人员数可去重；项目预算应在项目粒度计算，不能在人员明细上直接重复求和。

#### 常见错误

- `COUNT(*)` 把无匹配左连接行也计为 1。
- 同一项目预算按参与人数重复相加。
- 用 `DISTINCT` 掩盖错误连接。

#### 如何验证结果

挑选一个多人项目手工核对参与数和预算，检查无参与项目是否为 0。

### 指标解释和 NULL

#### 它解决什么问题

管理费、投资收益率、电压等级可能缺失，分析中必须明确“缺失”与“数值为 0”的区别。

#### 最基本语法

```sql
CASE
    WHEN metric_value IS NULL THEN '缺少数据'
    WHEN metric_value >= ... THEN '较高'
    ELSE '较低'
END
```

#### 怎么理解

先判断 `NULL`，再判断数值范围，避免把未知值错误归类。

#### 常见错误

- 用 `= NULL`。
- 没有单独处理缺失值。
- 把比率 `0.08` 误读成 `0.08%`。

#### 如何验证结果

分别抽查缺失、较高和较低指标，手工核对至少一条金额计算。

## 4. 可运行示例

## 示例 1：统计每个部门的员工数

### 学习目标

以部门为粒度，用左连接保留没有员工的部门。

### 运行前预测

1. 一行代表什么？
2. 没有员工的部门会不会出现？
3. 为什么不使用 `COUNT(*)`？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    d.department_id,
    d.department_name,
    COUNT(e.employee_id) AS employee_count
FROM departments AS d
LEFT JOIN employees AS e
    ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name
ORDER BY d.department_id ASC;
```

### 运行后观察

1. 每个部门是否只有一行？
2. 员工数总和是否与员工总数一致？
3. 无匹配时计数是否为 0？

### 结果特征

- 每个部门一行；
- 无员工部门也会保留；
- 不应因连接漏掉部门。

### 最小修改任务

改为统计每个部门的项目数，列名为 `project_count`。

### 本例常见错误

- 使用 `INNER JOIN`；
- 使用 `COUNT(*)` 导致空部门计为 1；
- 漏写分组列。

## 示例 2：制作项目经理清单

### 学习目标

使用左连接保留尚未分配经理的项目，并清楚显示缺失值。

### 运行前预测

1. 没有经理的项目是否会出现？
2. 经理为空时显示什么？
3. 每个项目会出现几行？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name,
    COALESCE(e.employee_name, '未分配') AS project_manager,
    p.project_status
FROM projects AS p
LEFT JOIN employees AS e
    ON e.employee_id = p.project_manager_id
ORDER BY p.project_id ASC;
```

### 运行后观察

1. 项目是否全部保留？
2. `project_manager` 是否还有 `NULL`？
3. 经理连接是否使用了正确字段？

### 结果特征

- 每个项目一行；
- 无经理项目显示“未分配”；
- 项目状态保持原值。

### 最小修改任务

增加项目预算列，并按预算降序、项目编号升序排列。

### 本例常见错误

- 使用部门编号连接经理；
- 使用内连接漏掉无经理项目；
- 在 `WHERE` 中要求经理字段非空。

## 示例 3：统计项目参与人数和工时

### 学习目标

处理项目与参与记录的一对多关系，并保留没有参与人员的项目。

### 运行前预测

1. 无参与项目的人员数是多少？
2. 每个项目会不会重复？
3. 工时没有匹配时会显示什么？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name,
    COUNT(DISTINCT ep.employee_id) AS participant_count,
    COALESCE(SUM(ep.working_hours), 0) AS total_working_hours
FROM projects AS p
LEFT JOIN employee_projects AS ep
    ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name
ORDER BY p.project_id ASC;
```

### 运行后观察

1. 无参与项目是否仍在？
2. 项目 1 的人员数是否与明细一致？
3. 结果是否保持每项目一行？

### 结果特征

- 每个项目一行；
- 无参与项目人数和工时显示 0；
- 人员数不会被其他重复连接放大。

### 最小修改任务

只保留参与人数不少于 3 的项目，并按参与人数降序、项目编号升序。

### 本例常见错误

- 用 `COUNT(*)`；
- 忘记 `GROUP BY`；
- 在 `WHERE` 中筛选参与表导致无参与项目被提前丢弃。

## 示例 4：计算管理费金额并标记收益率

### 学习目标

组合项目预算、管理费率、投资收益率和 `CASE`，并保留缺少指标的项目。

### 运行前预测

1. 没有指标的项目会出现吗？
2. 管理费率缺失时金额是什么？
3. 收益率缺失会被归入高或低吗？

### 示例代码

```sql
USE mysql_beginner_practice;

SELECT
    p.project_id,
    p.project_name,
    p.budget,
    p.budget * pm.management_fee AS management_fee_amount,
    CASE
        WHEN pm.investment_return_rate IS NULL THEN '缺少收益率'
        WHEN pm.investment_return_rate >= 0.08 THEN '收益率较高'
        ELSE '收益率低于 8%'
    END AS return_level
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON pm.project_id = p.project_id
ORDER BY p.project_id ASC;
```

### 运行后观察

1. 无指标项目是否保留？
2. 缺失管理费率时金额是否为 `NULL`？
3. 收益率 `0.08` 是否按 8% 理解？

### 结果特征

- 每个项目一行；
- 指标缺失不会导致项目消失；
- 收益率缺失单独标记。

### 最小修改任务

把较高收益率门槛改为 `0.085`，其余逻辑不变。

### 本例常见错误

- 使用内连接漏掉缺失指标项目；
- 把 `0.08` 当成 `0.08%`；
- 没有先判断 `NULL`。

## 示例 5：按电压等级汇总项目

### 学习目标

用 CTE 先整理项目指标，再按可读电压等级分组汇总。

### 运行前预测

1. 没有电压等级的项目会归到哪一组？
2. 一行代表项目还是电压等级？
3. 项目预算会不会因参与人员重复？

### 示例代码

```sql
USE mysql_beginner_practice;

WITH project_voltage AS
(
    SELECT
        p.project_id,
        p.budget,
        COALESCE(pm.voltage_level, '未填写') AS voltage_level
    FROM projects AS p
    LEFT JOIN project_metrics AS pm
        ON pm.project_id = p.project_id
)
SELECT
    voltage_level,
    COUNT(project_id) AS project_count,
    SUM(budget) AS total_budget
FROM project_voltage
GROUP BY voltage_level
ORDER BY voltage_level ASC;
```

### 运行后观察

1. 结果每行代表什么？
2. 项目数总和是否等于项目总数？
3. “未填写”组是否保留缺失指标或电压等级的项目？

### 结果特征

- 每个电压等级一行；
- 项目只进入一个分组；
- 项目数总和应等于项目总数。

### 最小修改任务

在汇总中增加平均预算列 `average_budget`。

### 本例常见错误

- 连接参与表导致项目预算重复；
- 忘记处理 `NULL`；
- CTE 中漏掉汇总所需字段。

## 5. 容易混淆的地方

- 先明确“一行代表什么”，再决定连接和分组。
- `LEFT JOIN` 后在 `WHERE` 中筛选右表字段，可能让它表现得像 `INNER JOIN`。
- 一对多连接会增加行数，预算等项目级金额可能被重复相加。
- `COUNT(column)` 不统计 `NULL`，这正适合统计左连接中的匹配数。
- 指标缺失不等于指标为 0，必须根据题意明确处理。

## 6. 本章示例结束自检

1. 我能否先说明查询结果的一行代表什么？
2. 我是否会检查无经理、无人员和无指标项目？
3. 我能否判断一对多连接是否放大了计数或金额？
4. 我是否会区分 `NULL` 与数值 0？
5. 我是否检查过列数、行数、重复和排序？

## 7. 下一步

现在才打开 exercises.sql。不要提前打开 answers.sql。每道题至少独立思考 5～10 分钟，卡住后先看 hints.md。
