---
typora-root-url: https://github.com/zhangfeibao/pygame-for-chinese-children/tree/main/images
---

# pygame simple wraper

A lite,simple package for game makeing based on pygame.

more:https://github.com/zhangfeibao/pygame-for-chinese-children

# 安装

```python
pip install nngame
```

# Hello World

## 1.导入模块

```python
import nngame.easygame as game
```

## 2.创建窗口

```python
game.创建窗口("Hello World",800,600)
```

## 3.创建字体和文本框

```python
字体1 = game.创建字体()
文本框1 = game.创建文本框(字体1,"Hello World")
```

## 4.循环(检测各种按键，鼠标，定时器等事件,刷新界面)

```python
while True:
    game.检测事件()

    game.窗口填充颜色(255,255,255)
    game.添加文本框到窗口(文本框1,200,200)

    game.刷新画面()
```

现在如果运行程序，应该能看到一个简单的窗口，显示Hello World文本

![窗口](https://github.com/zhangfeibao/pygame-for-chinese-children/tree/main/images/hello.png)

但是，你会发现，我们无法关闭这个窗口，那是因为我们还没有编写代码对这个用户点击关闭按钮的动作做出响应。

在主循环之前添加如下代码：

```python
def 用户点击了关闭按钮():
    game.退出()

game.添加退出事件处理函数(用户点击了关闭按钮)
```

现在应该可以正常关闭窗口了

# 完整代码

```python
import nngame.easygame as game

game.创建窗口("Hello World",800,600)

字体1 = game.创建字体()
文本框1 = game.创建文本框(字体1,"Hello World")

def 用户点击了关闭按钮():
    game.退出()

game.添加退出事件处理函数(用户点击了关闭按钮)

while True:
    game.检测事件()

    game.窗口填充颜色(255,255,255)
    game.添加文本框到窗口(文本框1,200,200)

    game.刷新画面()

```



