# 练习 1

## 提示 1

先用非递归 CTE 筛选，再从 CTE 查询。

## 提示 2

CTE 来自 `employees`，需要保留员工编号、姓名和薪资。

## 提示 3

```sql
WITH ... AS
(
    SELECT ...
    FROM employees
    WHERE salary >= ...
)
SELECT ...
FROM ...
ORDER BY ... DESC, ... ASC;
```

# 练习 2

## 提示 1

使用 `EXISTS` 判断“至少有一条”。

## 提示 2

外层查询 `projects`，子查询检查 `project_metrics`。

## 提示 3

```sql
SELECT ...
FROM projects AS p
WHERE EXISTS
(
    SELECT 1
    FROM project_metrics AS pm
    WHERE pm.project_id = ...
)
ORDER BY ...;
```

# 练习 3

## 提示 1

“完全没有”对应 `NOT EXISTS`。

## 提示 2

外层是员工，子查询在参与表中按员工编号查找。

## 提示 3

```sql
SELECT ...
FROM employees AS e
WHERE NOT EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.employee_id = ...
)
ORDER BY ...;
```

# 练习 4

## 提示 1

CTE 负责筛选，主查询负责显示和排序。

## 提示 2

从 `projects` 保留编号、名称、预算，并在 CTE 中按状态筛选。

## 提示 3

```sql
WITH ... AS
(
    SELECT ...
    FROM projects
    WHERE project_status = ...
)
SELECT ...
FROM ...
ORDER BY ... DESC, ... ASC;
```

# 练习 5

## 提示 1

组合 `CAST` 和 `COALESCE`。

## 提示 2

要先把数字编号转成字符，才能与“未分配”作为同一显示列。

## 提示 3

```sql
SELECT
    ...,
    COALESCE(CAST(... AS CHAR), ...) AS ...
FROM projects
ORDER BY ...;
```

# 练习 6

## 提示 1

使用否定的存在性判断。

## 提示 2

从项目出发，到 `employee_projects` 检查项目编号。

## 提示 3

```sql
SELECT ...
FROM projects AS p
WHERE NOT EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ... = ...
)
ORDER BY ...;
```

# 练习 7

## 提示 1

对两个可空字段分别使用空值替代函数。

## 提示 2

数据来自 `project_metrics`；文本字段用文本替代，数值字段用数值替代。

## 提示 3

```sql
SELECT
    ...,
    COALESCE(..., ...) AS ...,
    COALESCE(..., ...) AS ...
FROM project_metrics
ORDER BY ...;
```

# 练习 8

## 提示 1

语法能运行不代表存在性判断正确。

## 提示 2

原子查询没有引用外层项目，所以无法逐个项目判断。

## 提示 3

```sql
WHERE EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.project_id = ...
)
```
