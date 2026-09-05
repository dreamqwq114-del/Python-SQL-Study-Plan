# 练习 1

## 提示 1

使用事务包住新增、验证和回滚。

## 提示 2

目标表是 `departments`，写明编号、名称、城市三列。

## 提示 3

```sql
SELECT ... WHERE department_id = ...;
START TRANSACTION;
INSERT INTO departments (...) VALUES (...);
SELECT ... WHERE department_id = ...;
ROLLBACK;
SELECT ... WHERE department_id = ...;
```

# 练习 2

## 提示 1

更新前后都按同一个专用主键查询。

## 提示 2

先确认 9102 未被占用，再在事务中创建、预览并修改 `city`。

## 提示 3

```sql
SELECT ... WHERE department_id = ...;
START TRANSACTION;
INSERT INTO departments (...) VALUES (...);
SELECT ... WHERE department_id = ...;
UPDATE departments SET city = ... WHERE department_id = ...;
SELECT ... WHERE department_id = ...;
ROLLBACK;
```

# 练习 3

## 提示 1

删除整行使用 `DELETE FROM`。

## 提示 2

只允许编号 9103 成为删除目标。

## 提示 3

```sql
SELECT ... WHERE department_id = ...;
START TRANSACTION;
INSERT INTO departments (...) VALUES (...);
SELECT ... WHERE ...;
DELETE FROM departments WHERE ...;
SELECT ... WHERE ...;
ROLLBACK;
```

# 练习 4

## 提示 1

先列出 `employees` 的所有必填列。

## 提示 2

部门 5 和经理 5 都是已有外键目标。

## 提示 3

```sql
START TRANSACTION;
INSERT INTO employees
    (employee_id, ..., manager_id)
VALUES
    (..., ..., ...);
SELECT ... WHERE employee_id = ...;
ROLLBACK;
```

# 练习 5

## 提示 1

先确认专用编号未被占用，再新增、预览并更新它。

## 提示 2

`projects` 的名称、状态、预算、开始日期都不能为空。

## 提示 3

```sql
SELECT ... WHERE project_id = ...;
START TRANSACTION;
INSERT INTO projects (...) VALUES (...);
SELECT ... WHERE project_id = ...;
UPDATE projects SET project_status = ... WHERE project_id = ...;
SELECT ... WHERE project_id = ...;
ROLLBACK;
```

# 练习 6

## 提示 1

事务前先确认项目 14 没有指标。

## 提示 2

目标表是 `project_metrics`，需要五个字段。

## 提示 3

```sql
SELECT ... FROM project_metrics WHERE project_id = ...;
START TRANSACTION;
INSERT INTO project_metrics (...) VALUES (...);
SELECT ... WHERE project_id = ...;
ROLLBACK;
SELECT ... WHERE project_id = ...;
```

# 练习 7

## 提示 1

先确认组合键未被占用，再创建员工和引用该员工的参与记录。

## 提示 2

参与表的目标由员工编号和项目编号共同确定。

## 提示 3

```sql
SELECT ... WHERE employee_id = ... AND project_id = ...;
START TRANSACTION;
INSERT INTO employees (...) VALUES (...);
INSERT INTO employee_projects (...) VALUES (...);
SELECT ... WHERE employee_id = ... AND project_id = ...;
DELETE FROM employee_projects WHERE employee_id = ... AND project_id = ...;
SELECT ... WHERE employee_id = ... AND project_id = ...;
ROLLBACK;
```

# 练习 8

## 提示 1

缺少 `WHERE` 的语句会更新所有员工。

## 提示 2

预览、更新和验证都限定 `employee_id = 7`。

## 提示 3

```sql
SELECT ... WHERE employee_id = ...;
START TRANSACTION;
UPDATE employees SET salary = ... WHERE employee_id = ...;
SELECT ROW_COUNT() AS ...;
SELECT ... WHERE employee_id = ...;
ROLLBACK;
```
