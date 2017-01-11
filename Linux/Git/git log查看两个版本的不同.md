title: git log查看两个版本的不同
date: 2017/01/06 17:29:32
updated: 2017/01/06 17:31:22
categories:
- Linux系统
- Basic
- Git
---
- 当前版本和上一个版本

```
git diff HEAD HEAD^
```

- 特定版本
```
git diff commitID1 commitID2
```

- 通过日志查看
```
git log state
```