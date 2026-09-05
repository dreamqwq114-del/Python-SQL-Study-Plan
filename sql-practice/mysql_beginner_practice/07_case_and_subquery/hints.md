# 第 7 章练习提示

请先独立思考。只在卡住时逐级展开提示，不要一次读完三个提示。

# 练习 1

## 提示 1

使用一个 `WHEN` 和一个 `ELSE`。

## 提示 2

判断 `salary` 是否达到门槛，并给结果列起别名。

## 提示 3

```sql
SELECT
    ...,
    CASE
        WHEN ... >= ... THEN ...
        ELSE ...
    END AS salary_level
FROM employees
ORDER BY ...;
```

# 练习 2

## 提示 1

使用 `CASE` 和空值判断。

## 提示 2

数据来自 `project_metrics`，检查电压等级字段。

## 提示 3

```sql
SELECT
    ...,
    CASE
        WHEN ... IS NULL THEN ...
        ELSE ...
    END AS voltage_status
FROM project_metrics
ORDER BY ...;
```

# 练习 3

## 提示 1

多个 `WHEN` 按优先级从上到下判断。

## 提示 2

先处理管理费为空，再判断数值门槛。

## 提示 3

```sql
CASE
    WHEN ... IS NULL THEN ...
    WHEN ... >= ... THEN ...
    ELSE ...
END AS fee_level
```

# 练习 4

## 提示 1

用标量子查询先得到一个平均值。

## 提示 2

内外层都使用 `projects`，内层聚合预算，外层返回项目明细。

## 提示 3

```sql
SELECT ...
FROM projects
WHERE ... > (
    SELECT AVG(...)
    FROM projects
)
ORDER BY
    ... DESC,
    ... ASC;
```

# 练习 5

## 提示 1

`IN` 可以判断部门编号是否属于子查询结果。

## 提示 2

外层查询部门；子查询从项目中返回符合预算条件的部门编号。

## 提示 3

```sql
SELECT ...
FROM departments
WHERE ... IN (
    SELECT ...
    FROM projects
    WHERE ... >= ...
)
ORDER BY ...;
```

# 练习 6

## 提示 1

先判断业务上优先级更高的“已完成”状态。

## 提示 2

第二个 `WHEN` 再检查结束日期是否为空。

## 提示 3

```sql
CASE
    WHEN ... = ... THEN ...
    WHEN ... IS NULL THEN ...
    ELSE ...
END AS progress_label
```

# 练习 7

## 提示 1

先在子查询中找符合收益率条件的项目所属部门。

## 提示 2

子查询连接 `projects` 与 `project_metrics`，只返回部门编号。

## 提示 3

```sql
SELECT ...
FROM employees
WHERE ... IN (
    SELECT ...
    FROM projects AS p
    INNER JOIN project_metrics AS pm
        ON p.... = pm....
    WHERE pm.... >= ...
)
ORDER BY ...;
```

# 练习 8

## 提示 1

标量子查询必须只有一行一列。

## 提示 2

用聚合函数把全部薪资变成一个平均值。

## 提示 3

```sql
SELECT ...
FROM employees
WHERE ... > (
    SELECT AVG(...)
    FROM employees
);
```
