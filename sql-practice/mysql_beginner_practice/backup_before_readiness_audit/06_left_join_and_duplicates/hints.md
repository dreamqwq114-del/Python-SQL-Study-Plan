# 第 6 章练习提示

请先独立思考。只在卡住时逐级展开提示，不要一次读完三个提示。

# 练习 1

## 提示 1

使用能保留左表全部行的连接。

## 提示 2

以 `projects` 为左表，连接 `project_metrics`。

## 提示 3

```sql
SELECT ...
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON p.... = pm....
ORDER BY ...;
```

# 练习 2

## 提示 1

员工与项目角色之间是一对多关系。

## 提示 2

从 `employees` 左连接 `employee_projects`。

## 提示 3

```sql
SELECT ...
FROM employees AS e
LEFT JOIN employee_projects AS ep
    ON e.... = ep....
ORDER BY
    ...,
    ...;
```

# 练习 3

## 提示 1

先保留全部项目，再找右表没有匹配的行。

## 提示 2

检查 `project_metrics` 中用于连接且非空的项目编号。

## 提示 3

```sql
SELECT ...
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON p.... = pm....
WHERE pm.... IS NULL
ORDER BY ...;
```

# 练习 4

## 提示 1

无参与记录意味着中间表连接失败。

## 提示 2

以员工为左表，检查 `employee_projects` 的连接键。

## 提示 3

```sql
SELECT ...
FROM employees AS e
LEFT JOIN employee_projects AS ep
    ON e.... = ep....
WHERE ep.... IS NULL
ORDER BY ...;
```

# 练习 5

## 提示 1

连接行可能重复项目，计数前先确定去重对象。

## 提示 2

从部门左连接项目，再左连接参与记录，按部门分组。

## 提示 3

```sql
SELECT
    ...,
    COUNT(DISTINCT ...) AS project_count
FROM departments AS d
LEFT JOIN projects AS p ON ...
LEFT JOIN employee_projects AS ep ON ...
GROUP BY
    ...,
    ...
ORDER BY ...;
```

# 练习 6

## 提示 1

保留所有员工，并统计右表匹配列。

## 提示 2

员工左连接参与表，按员工编号和姓名分组。

## 提示 3

```sql
SELECT
    ...,
    COUNT(...) AS project_count
FROM employees AS e
LEFT JOIN employee_projects AS ep ON ...
GROUP BY
    ...,
    ...
ORDER BY ...;
```

# 练习 7

## 提示 1

先保留项目，再对每个项目的员工编号去重计数。

## 提示 2

使用 `projects`、`employee_projects` 和分组。

## 提示 3

```sql
SELECT
    ...,
    COUNT(DISTINCT ...) AS employee_count
FROM projects AS p
LEFT JOIN employee_projects AS ep ON ...
GROUP BY
    ...,
    ...
ORDER BY
    ... DESC,
    ... ASC;
```

# 练习 8

## 提示 1

`WHERE` 会排除右表字段为 `NULL` 的行。

## 提示 2

把电压条件作为“是否匹配”的一部分。

## 提示 3

```sql
SELECT ...
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON p.... = pm....
   AND pm.... = ...;
```
