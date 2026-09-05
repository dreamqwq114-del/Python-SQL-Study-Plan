# 练习 1

## 提示 1

从部门出发，用左连接保留全部部门。

## 提示 2

连接 `departments` 和 `projects`，计数项目编号。

## 提示 3

```sql
SELECT ..., COUNT(...) AS project_count
FROM departments AS d
LEFT JOIN projects AS p ON ... = ...
GROUP BY ...
ORDER BY ...;
```

# 练习 2

## 提示 1

无经理项目需要左连接和空值替代。

## 提示 2

`projects.project_manager_id` 对应 `employees.employee_id`。

## 提示 3

```sql
SELECT ..., COALESCE(..., ...) AS ..., ...
FROM projects AS p
LEFT JOIN employees AS e ON ... = ...
ORDER BY ... DESC, ... ASC;
```

# 练习 3

## 提示 1

先按状态分组，再用 `HAVING` 筛选组。

## 提示 2

需要 `COUNT` 项目和 `SUM` 预算。

## 提示 3

```sql
SELECT ..., COUNT(...) AS ..., SUM(...) AS ...
FROM projects
GROUP BY ...
HAVING COUNT(...) >= ...
ORDER BY ... DESC, ... ASC;
```

# 练习 4

## 提示 1

连接项目和参与表，再按项目分组。

## 提示 2

人员数使用 `COUNT(DISTINCT ...)`，分组包含所有非聚合列。

## 提示 3

```sql
SELECT ..., COUNT(DISTINCT ...) AS participant_count
FROM projects AS p
LEFT JOIN employee_projects AS ep ON ... = ...
GROUP BY ...
HAVING COUNT(DISTINCT ...) >= ...
ORDER BY ...;
```

# 练习 5

## 提示 1

使用有顺序的 `CASE WHEN`。

## 提示 2

先判断暂停状态，再判断 `end_date IS NULL`。

## 提示 3

```sql
CASE
    WHEN ... = ... THEN ...
    WHEN ... IS NULL THEN ...
    ELSE ...
END AS ...
```

# 练习 6

## 提示 1

结果粒度是部门，不要连接参与人员。

## 提示 2

左连接项目，计数项目编号，对预算总和处理空值。

## 提示 3

```sql
SELECT
    ...,
    COUNT(...) AS ...,
    COALESCE(SUM(...), 0) AS ...
FROM departments AS d
LEFT JOIN projects AS p ON ... = ...
GROUP BY ...
ORDER BY ...;
```

# 练习 7

## 提示 1

可以使用两个 `NOT EXISTS` 分别判断两类缺失。

## 提示 2

外层是项目；参与表和指标表都按项目编号关联。

## 提示 3

```sql
SELECT
    ...,
    CASE WHEN NOT EXISTS (...) THEN ... ELSE ... END AS ...,
    CASE WHEN NOT EXISTS (...) THEN ... ELSE ... END AS ...
FROM projects AS p
WHERE NOT EXISTS (...) OR NOT EXISTS (...)
ORDER BY ...;
```

# 练习 8

## 提示 1

错误不是语法，而是把项目预算按参与人数重复相加。

## 提示 2

题目只需要 `projects` 中已有的项目粒度数据。

## 提示 3

```sql
SELECT ..., ..., ...
FROM projects
ORDER BY ...;
```
