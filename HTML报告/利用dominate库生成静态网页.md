# 利用dominate库生成静态网页

[TOC]

## dominate 简介

dominate是一个使用优雅的DOM API创建和操作HTML文档的Python库。使用它能非常简洁地编写纯Python的HTML页面，这消除了学习另一种模板语言的需要，利用Python更强大的特性。[^1]

[^1]: https://pypi.org/project/dominate/

## 一个生成页面的简单例子

```python
from dominate.tags import *

h = html()
with h.add(body()).add(div(id='content')):
    h1('Hello World!')
    p('This is my first html.')
    with table().add(tbody()):
        l = tr()
        l += td('One')
        l.add(td('Two'))
        with l:
            td('Three')

with open('test.html','w') as f:
    f.write(h.render())
```
生成test.html源码如下:
```html
<html>
  <body>
    <div id="content">
      <h1>Hello World!</h1>
      <p>This is my first html.</p>
      <table>
        <tbody>
          <tr>
            <td>One</td>
            <td>Two</td>
            <td>Three</td>
          </tr>
        </tbody>
      </table>
    </div>
  </body>
</html>
```

##HTML标记
主导的最基本的特性为每个HTML标记构建了一个类。可以使用
```python
from dominate.tags import *
```
导入所有html标记
查看源码可知包含如下标记
>Root element: html
>Document metadata: head, title, base, link, meta, style,
>Scripting: script, noscript
>Sections: body, section, nav, article, aside, h1, h2, h3, h4, h5, h6, hgroup, header, footer, address
>Grouping content: p, hr, pre, blockquote, ol, ul, li, dl, dt, dd, figure, figcaption, div
>Text semantics: a, em, strong, small, s, q, dfn, abbr, time_, code, var, samp, kbd, sub, i, b, u, mark, ruby, rt, rp, bdo, span, br, wbr
>Edits: ins, del_
>Embedded content: img, iframe, embed, object_, param, video, audio, source, track, canvas, map_, area
>Tabular data: table, caption, colgroup, col, tbody, thead, tfoot, tr, td, th
>Forms: form, fieldset, legend, label, input_, button, select, datalist, optgroup, option, textarea, keygen, output, progress, meter
>Interactive elements: details, summary, command, menu, font
>Additional markup: comment

一个例子：
```python
print(html(body(h1('Hello, World!'))))
```
输出：
```html
<html>
    <body>
        <h1>Hello, World!</h1>
    </body>
</html>
```

## 标记的属性
dominate 还可以使用关键字参数将属性附加到标签上。大多数属性都是来自HTML规范的直接拷贝.
class和for可以使用如下别名：

>class: _class, cls, className, class_name
>for: _for, fr, htmlFor, html_for

使用data_*代表定制HTML5数据属性。
属性的声明有如下方式：
```python
test = label('text',cls='classname anothername', fr='someinput')
```
```python
header = div('text')
header['id'] = 'header'
print(header)
```
## 如何生成复杂的文档结构
通过使用+=操作符，如下：
```python
list = ul()
for item in range(4):
    list += li('Item #', item)
print(list)
```
输出：
```html
<ul>
    <li>Item #0</li>
    <li>Item #1</li>
    <li>Item #2</li>
    <li>Item #3</li>
</ul>
```
支持迭代器来帮助简化你的代码：
```python
print(ul(li(a(name, href=link), __pretty=False) for name, link in menu_items))
```
通过add()方法：
```python
_html = html()
_body = _html.add(body())
header  = _body.add(div(id='header'))
content = _body.add(div(id='content'))
footer  = _body.add(div(id='footer'))
print(_html)
```
```python
_html = html()
_head, _body = _html.add(head(title('Simple Document Tree')), body())
names = ['header', 'content', 'footer']
header, content, footer = _body.add(div(id=name) for name in names)
print(_html)
```
## 访问内容和属性
```python
header = div()
header['id'] = 'header'
print(header)
```
```python
header = div('Test')
header[0] = 'Hello World'
print(header)
```
## 渲染
默认情况下，render（）尝试使所有输出都是可读的，每行一个HTML元素和两个缩进空间。render()输出为str格式。
例子
```python
a = div(span('Hello World'))
print(a.render())
```
```python
print(a.render(pretty=False))
```
```python
print(a.render(indent='\t'))
```
```python
a = div(span('Hello World'), __pretty=False)
```
```python
print(d.render(xhtml=True))
```
## 上下文管理器
例子：
```python
h = ul()
with h:
    li('One')
    li('Two')
    li('Three')
print(h)
```
```html
<ul>
    <li>One</li>
    <li>Two</li>
    <li>Three</li>
</ul>
```
更复杂的例子见文章开头的例子。
可以在with内加入attr()，用来使当前的标签加入属性，如：
```python
d = div()
with d:
    attr(id='header')
print(d)
```
输出
```html
<div id="header"></div>
```
可以在with内加入text()，用来使当前的标签加入文字内容，如：
```python
from dominate.util import text
para = p(__pretty=False)
with para:
    text('Have a look at our ')
    a('other products', href='/products')

print(para)
```
```html
<p>Have a look at our <a href="/products">other products</a></p>
```
## 装饰器
```python
@div(h2('Welcome'), cls='greeting')
def greeting(name):
    p('Hello %s' % name)

print(greeting('Bob'))
```
```html
<div class="greeting">
    <h2>Welcome</h2>
    <p>Hello Bob</p>
</div>
```
可以使用标记的实例作为装饰器。每个对装饰函数的调用都会返回用来装饰它的节点的副本。
## 创建文档
创建一个新文档时，创建了基本的HTML标记结构。
```python
from dominate import document
d = document()
d += h1('Hello, World!')
d.body += p('This is a paragraph.')
print(d)
```
输出：
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Dominate</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
    <p>This is a paragraph.</p>
  </body>
</html>
```
还可以直接访问\<title>， \<head>， \<body>
```
>>> d.head
<dominate.tags.head: 0 attributes, 1 children>
>>> d.body
<dominate.tags.body: 0 attributes, 0 children>
>>> d.title
u'Dominate'
```
## 嵌入一个预先形成的HTML节点
```python
from dominate.util import raw
...
td(raw('<a href="example.html">Example</a>'))
```
如果没有原始的调用，这段代码将会呈现出转义的HTML。
