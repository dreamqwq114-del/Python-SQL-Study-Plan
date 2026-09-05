# 第 3 章练习提示

请先独立思考。只在卡住时逐级展开提示，不要一次读完三个提示。

# 练习 1
## 提示 1
使用升序排序。
## 提示 2
从 `employees` 查询姓名和薪资。
## 提示 3
```sql
SELECT ..., ...
FROM employees
ORDER BY ... ASC;
```

# 练习 2
## 提示 1
使用降序排序日期。
## 提示 2
从 `projects` 查询名称和开始日期。
## 提示 3
```sql
SELECT ..., ...
FROM projects
ORDER BY ... DESC;
```

# 练习 3
## 提示 1
三个排序规则按优先级排列。
## 提示 2
先部门，再入职日期，最后员工姓名。
## 提示 3
```sql
SELECT ..., ..., ...
FROM employees
ORDER BY
    ... ASC,
    ... ASC,
    ... ASC;
```

# 练习 4
## 提示 1
先用日期条件筛选，再排序。
## 提示 2
从 `projects` 比较开始日期，并用编号处理同日。
## 提示 3
```sql
SELECT ..., ...
FROM projects
WHERE ... >= '...'
ORDER BY ... ASC, ... ASC;
```

# 练习 5
## 提示 1
组合文本、数值两个条件和排序。
## 提示 2
从 `projects` 检查状态与预算。
## 提示 3
```sql
SELECT ..., ..., ...
FROM projects
WHERE ... = ...
  AND ... < ...
ORDER BY ... DESC;
```

# 练习 6
## 提示 1
日期范围包含起止两端。
## 提示 2
从 `employees` 筛选入职日期，再按日期和编号排序。
## 提示 3
```sql
SELECT ..., ..., ...
FROM employees
WHERE ... BETWEEN '...' AND '...'
ORDER BY ... DESC, ... ASC;
```

# 练习 7
## 提示 1
先排除不符合状态或没有结束日期的行。
## 提示 2
从 `projects` 筛选后，依次使用结束日期、预算、名称排序。
## 提示 3
```sql
SELECT ..., ..., ..., ...
FROM projects
WHERE ... = ...
  AND ... IS NOT NULL
ORDER BY ... DESC, ... DESC, ... ASC;
```

# 练习 8
## 提示 1
语法能运行，但 `DESC` 与“最早优先”相反。
## 提示 2
日期应升序，并增加员工编号作为第二排序列。
## 提示 3
```sql
SELECT ..., ..., ...
FROM employees
WHERE ... >= '...'
ORDER BY ... ASC, ... ASC;
```
