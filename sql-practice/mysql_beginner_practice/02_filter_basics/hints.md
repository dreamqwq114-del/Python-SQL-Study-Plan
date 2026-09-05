# 第 2 章练习提示

请先独立思考。只在卡住时逐级展开提示，不要一次读完三个提示。

# 练习 1

## 提示 1

使用一个等值筛选条件。

## 提示 2

数据来自 `employees`，需要姓名、部门编号和 `WHERE`。

## 提示 3

```sql
SELECT ..., ...
FROM employees
WHERE ... = ...;
```

# 练习 2

## 提示 1

使用空值判断。

## 提示 2

数据来自 `projects`，判断结束日期是否缺失。

## 提示 3

```sql
SELECT ..., ...
FROM projects
WHERE ... IS ...;
```

# 练习 3

## 提示 1

组合列表匹配和数值下限。

## 提示 2

从 `employees` 读取姓名、部门、薪资；两个条件都要成立。

## 提示 3

```sql
SELECT ..., ..., ...
FROM employees
WHERE ... IN (...)
  AND ... >= ...;
```

# 练习 4

## 提示 1

使用包含两端的范围条件。

## 提示 2

从 `projects` 同时检查预算范围和状态。

## 提示 3

```sql
SELECT ..., ..., ...
FROM projects
WHERE ... BETWEEN ... AND ...
  AND ... = ...;
```

# 练习 5

## 提示 1

组合文本包含匹配和排除条件。

## 提示 2

从 `employees` 检查职位文本，并排除一个部门编号。

## 提示 3

```sql
SELECT ..., ..., ...
FROM employees
WHERE ... LIKE ...
  AND NOT (... = ...);
```

# 练习 6

## 提示 1

先组合两个可选状态，再和预算条件连接。

## 提示 2

数据来自 `projects`；括号中的状态条件使用 `OR`。

## 提示 3

```sql
SELECT ..., ..., ..., ...
FROM projects
WHERE (... = ... OR ... = ...)
  AND ... > ...;
```

# 练习 7

## 提示 1

组合非空判断和列表排除。

## 提示 2

从 `projects` 检查 `end_date` 与 `project_status`。

## 提示 3

```sql
SELECT ..., ..., ...
FROM projects
WHERE ... IS NOT NULL
  AND ... NOT IN (...);
```

# 练习 8

## 提示 1

MySQL 会先计算 `AND`，再计算 `OR`。

## 提示 2

原 SQL 没有让两种状态共同受到预算下限约束。

## 提示 3

```sql
SELECT ..., ..., ...
FROM projects
WHERE (... OR ...)
  AND ... >= ...;
```
