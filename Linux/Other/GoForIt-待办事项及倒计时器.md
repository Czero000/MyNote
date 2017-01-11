title: GoForIt-待办事项及倒计时器
date: 2017/01/04 11:26:27
updated: 2017/01/06 18:08:38
categories:
- Linux系统
- Basic
- Ubuntu
---
如果您是拖延症患者的话，这款集成了待办事项及倒计时器的小软件或许可以帮助您提高工作效率。

Go For It! 界面透着 Elementary/GNOME HIG 的简洁风格，使用 Vala/GTK3 创建，其待办事项部分以 Todo.txt（更多说明参见文末）格式保存。

这个[视频说明了 Go For It! 的工作流程（朝内镜像）](https://www.youtube.com/watch?v=mnw556C9FZQ#t=150)，简单来说：

1. 在待办事项里添加打算完成的工作。
2. 选择一个事项，在倒计时器里设定预期完成时间，点击开始。
3. 开始工作。
4. 倒计时结束或任务完成后，点击确定将事项标记为完成。
5. 可以在事项完成后添加一个休息时间。

Go For It! 提供 Linux 及 [Win](http://manuel-kehl.de/projects/go-for-it/download-windows-version) 平台版本，不久将提供 OS X 版本。
```
Ubuntu PPA：
sudo add-apt-repository ppa:mank319/go-for-it && sudo apt-get update
sudo apt-get install go-for-it
```
[Github编译指南](https://github.com/mank319/Go-For-It)

与 Evernote 或 Google Keep 等具备待办事项功能的便笺本相比，[Todo.txt](http://todotxt.com/) 利用预定义纯文本方式记录事项，某种意义上保证了向前兼容性。同时因为是简单的纯文本，它可以方便和各个平台进行集成，包括命令行终端及 Vim 插件。iOS 及 Android 客户端更是不在话下。同步的工作由 Dropbox 实现。