# 第 1 章练习提示

请先独立思考。只在卡住时逐级展开提示，不要一次读完三个提示。

# 练习 1

## 提示 1

使用 `SELECT` 和 `FROM`。

## 提示 2

数据来自 `departments`，只需要部门名称字段。

## 提示 3

```sql
SELECT ...
FROM departments;
```

# 练习 2

## 提示 1

在 `SELECT` 后可以写多个字段。

## 提示 2

数据来自 `employees`，需要姓名和薪资两个字段。

## 提示 3

```sql
SELECT
    ...,
    ...
FROM employees;
```

# 练习 3

## 提示 1

组合使用别名、排序和限制行数。

## 提示 2

从 `projects` 查询项目名称和预算；先按预算，再按项目名称。

## 提示 3

```sql
SELECT
    ... AS project,
    ... AS project_budget
FROM projects
ORDER BY
    ... DESC,
    ... ASC
LIMIT ...;
```

# 练习 4

## 提示 1

组合使用去重和排序。

## 提示 2

从 `projects` 查询状态字段，去重后按该字段升序。

## 提示 3

```sql
SELECT DISTINCT ...
FROM projects
ORDER BY ... ASC;
```

# 练习 5

## 提示 1

组合使用计算列、别名和排序。

## 提示 2

从 `projects` 读取名称和预算，计算费用后按费用和项目名称排序。

## 提示 3

```sql
SELECT
    ...,
    ...,
    ... * ... AS budget_fee
FROM projects
ORDER BY
    ... DESC,
    ... ASC;
```

# 练习 6

## 提示 1

从业务目标判断数据表、返回列、主排序和并列时的第二排序。

## 提示 2

使用 `projects` 中的编号、名称和预算字段。

## 提示 3

```sql
SELECT
    ...,
    ...,
    ...
FROM projects
ORDER BY
    ... ASC,
    ... ASC
LIMIT ...;
```

# 练习 7

## 提示 1

先确定部门列表需要显示的列和顺序。

## 提示 2

从 `departments` 查询编号、名称和城市；先按名称，再按编号。

## 提示 3

```sql
SELECT
    ...,
    ...,
    ...
FROM departments
ORDER BY
    ... ASC,
    ... ASC
LIMIT ...;
```

# 练习 8

## 提示 1

分别检查语法是否完整，以及查询是否定义了“最高”的排序规则。

## 提示 2

查询员工姓名和薪资；需要用一个排序规则表达“最高”，再处理并列情况。

## 提示 3

```sql
SELECT
    ...,
    ...
FROM employees
ORDER BY
    ... DESC,
    ... ASC
LIMIT ...;
```
