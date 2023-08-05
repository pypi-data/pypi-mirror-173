# colorpie
Terminal color style handler.

### Installation:

```commandline
python -m pip install [--upgrade] colorpie
```

### Available tools:

<details>
<summary>Style4Bit</summary>
<p>

```python

from colorpie import Style4Bit

style = Style4Bit(
    color='red',
    highlight='black',
    attributes=['bold', 'slow_blink']
)

if __name__ == '__main__':
    print(style.format('Hello, World!'))
```

</p>
</details>


<details>
<summary>Style8Bit</summary>
<p>

```python

from colorpie import Style8Bit

style = Style8Bit(
    color=0,
    highlight=16,
    attributes=['bold']
)

if __name__ == '__main__':
    print(style.format('Hello, World!'))
```

Some colors can be referred to by their name:

`
black, maroon, green, olive, navy, purple, teal, silver,
grey, red, lime, yellow, blue, magenta, cyan, white and gold
`

Also, by their hex or rgb values.
(see `__256_color__` dict in [mapping.py](src/colorpie/mapping.py)).

</p>
</details>
