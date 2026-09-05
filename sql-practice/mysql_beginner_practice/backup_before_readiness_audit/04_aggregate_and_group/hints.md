# 第 4 章练习提示

请先独立思考。只在卡住时逐级展开提示，不要一次读完三个提示。

# 练习 1
## 提示 1
使用统计全部行的聚合函数。
## 提示 2
数据来自 `employees`，结果只有一个计数。
## 提示 3
```sql
SELECT COUNT(...) AS employee_count
FROM employees;
```

# 练习 2
## 提示 1
使用总和与平均值两个聚合函数。
## 提示 2
数据来自 `projects`，两个函数都处理预算字段。
## 提示 3
```sql
SELECT
    SUM(...) AS total_budget,
    AVG(...) AS average_budget
FROM projects;
```

# 练习 3
## 提示 1
按状态分组后统计每组行数。
## 提示 2
从 `projects` 显示状态和计数，再使用两个排序规则。
## 提示 3
```sql
SELECT ..., COUNT(*) AS project_count
FROM projects
GROUP BY ...
ORDER BY ... DESC, ... ASC;
```

# 练习 4
## 提示 1
每个部门分别求最小值和最大值。
## 提示 2
从 `employees` 按部门分组，两个函数处理薪资。
## 提示 3
```sql
SELECT ..., MIN(...) AS minimum_salary, MAX(...) AS maximum_salary
FROM employees
GROUP BY ...
ORDER BY ... ASC;
```

# 练习 5
## 提示 1
先筛选原始项目，再分组汇总。
## 提示 2
从 `projects` 用 `WHERE` 限定状态，按部门分组。
## 提示 3
```sql
SELECT ..., COUNT(*) AS project_count, SUM(...) AS total_budget
FROM projects
WHERE ... = ...
GROUP BY ...;
```

# 练习 6
## 提示 1
平均值下限是分组后的条件。
## 提示 2
从 `employees` 按职位分组，用 `HAVING` 检查平均薪资。
## 提示 3
```sql
SELECT ..., COUNT(*) AS employee_count, AVG(...) AS average_salary
FROM employees
GROUP BY ...
HAVING AVG(...) >= ...
ORDER BY ... DESC, ... ASC;
```

# 练习 7
## 提示 1
比较总行数与多个字段的非空数量。
## 提示 2
数据来自 `project_metrics`；星号统计行，字段名统计非空。
## 提示 3
```sql
SELECT
    COUNT(*) AS metric_count,
    COUNT(...) AS fee_count,
    COUNT(...) AS return_count,
    COUNT(...) AS voltage_count
FROM project_metrics;
```

# 练习 8
## 提示 1
`WHERE` 在分组前运行，不能判断分组后的计数。
## 提示 2
先按部门分组，再使用 `HAVING` 保留人数达标的组。
## 提示 3
```sql
SELECT ..., COUNT(*) AS employee_count
FROM employees
GROUP BY ...
HAVING COUNT(*) >= ...;
```
