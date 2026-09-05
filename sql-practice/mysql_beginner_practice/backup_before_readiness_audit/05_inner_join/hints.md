# 第 5 章练习提示

请先独立思考。只在卡住时逐级展开提示，不要一次读完三个提示。

# 练习 1

## 提示 1

使用两表 `INNER JOIN`。

## 提示 2

从员工表取员工信息，从部门表取部门名称。

## 提示 3

```sql
SELECT ...
FROM employees AS e
INNER JOIN departments AS d
    ON e.... = d....
ORDER BY ...;
```

# 练习 2

## 提示 1

找出项目表中指向部门的外键。

## 提示 2

从 `projects` 连接 `departments`，返回项目和部门信息。

## 提示 3

```sql
SELECT ...
FROM projects AS p
INNER JOIN departments AS d
    ON p.... = d....
ORDER BY ...;
```

# 练习 3

## 提示 1

把项目经理编号与员工的唯一编号配对。

## 提示 2

项目数据来自 `projects`，经理姓名来自 `employees`。

## 提示 3

```sql
SELECT
    ...,
    ... AS manager_name,
    ...
FROM projects AS p
INNER JOIN employees AS e
    ON p.... = e....
ORDER BY
    ... DESC,
    ... ASC;
```

# 练习 4

## 提示 1

一个项目需要建立两条不同关系。

## 提示 2

以 `projects` 为起点，分别连接部门和员工。

## 提示 3

```sql
SELECT ...
FROM projects AS p
INNER JOIN departments AS d
    ON p.... = d....
INNER JOIN employees AS e
    ON p.... = e....
ORDER BY ...;
```

# 练习 5

## 提示 1

先找到保存员工—项目关系的中间表。

## 提示 2

`employee_projects` 分别保存员工编号和项目编号。

## 提示 3

```sql
SELECT ...
FROM employee_projects AS ep
INNER JOIN projects AS p
    ON ep.... = p....
INNER JOIN employees AS e
    ON ep.... = e....
ORDER BY
    ...,
    ...;
```

# 练习 6

## 提示 1

每个结果行应代表一条参与关系，而不是一个不重复员工。

## 提示 2

需要员工表、中间表和项目表。

## 提示 3

```sql
SELECT ...
FROM employees AS e
INNER JOIN employee_projects AS ep
    ON e.... = ep....
INNER JOIN projects AS p
    ON ep.... = p....
ORDER BY
    ...,
    ...;
```

# 练习 7

## 提示 1

有匹配指标才保留，适合 `INNER JOIN`。

## 提示 2

连接 `projects` 和 `project_metrics` 的项目编号。

## 提示 3

```sql
SELECT ...
FROM projects AS p
INNER JOIN project_metrics AS pm
    ON p.... = pm....
ORDER BY ...;
```

# 练习 8

## 提示 1

先区分“语法能运行”和“连接关系正确”。

## 提示 2

员工属于部门，不是员工编号等于部门编号。

## 提示 3

```sql
SELECT ...
FROM employees AS e
INNER JOIN departments AS d
    ON e.... = d....;
```
