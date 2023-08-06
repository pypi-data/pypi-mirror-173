# pyspage <img src="assets/icon.png" align="right" />

Quickly build open source web pages for academic purposes in a pythonic and elegant way.

## Installation

```shell
pip install pyspage
```

## Usage

### Step 1

Create a new file named `index.py` which consists of mainly two parts, **layout** and **script**.

In the layout part, a `layout` variable should be defined, of which the contents are the page elements named in a way you like. The hierarchical relationships are expressed by indenting.

```python
layout = '''
row_a
    box
row_b
    col_a
        btn_a
    col_b
        btn_b
'''
```

In the script part, all the elements above should be created.

```python
from pyspage import *
import matplotlib.pyplot as plt

row_a = Row()
row_b = Row()
col_a = Column()
col_b = Column()
box = Column(class_='col-6')
btn_a = Button('CLICK a')
btn_b = Button('CLICK b')
```

You can define a function and let an element run it on a certain event happens.

```python
btn_a.onclick = lambda e: print('a is clicked!')

def click_b(e):
    fig, ax = plt.subplots()
    fruits = ['apple', 'blueberry', 'cherry', 'orange']
    counts = [40, 100, 30, 55]
    ax.bar(fruits, counts)
    box.write(fig)
btn_b.onclick = click_b

def create_box():
    row_a.classList.add('bg-warning')
    box.write('This is the content.')
box.oncreate = create_box
```

You can create a figure with `matplotlib` or `altair`, and show it in an empty box(`row` or `column`) by `box.write(fig)`.

### Step 2

In your terminal, run as follow
```shell
pyspage index.py
```

a `index.html` in current directionary is generated. 

If you use the arguments `-s`(for server) and `-b`(for browser), pyspage will start a server on 127.0.0.1:8000 and open browser automatically.

```shell
pyspage index.py -sb
```

This page can then be deployed on [GitHub Pages](https://pages.github.com/), you don't have to bother about anything with HTML, JS or backend APIs.🎉🎉🎉

## License
The [MIT License](LICENSE).