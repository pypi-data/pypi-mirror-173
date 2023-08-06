# packagebmi

Description. 

The package packagebmi is used to:
- Calculate individual body mass index.
- Find out what basic category the person is.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packagebmi

```bash
pip install packagebmi
```

## Usage

```python
from packagebmi import filebmi
filebmi.bmi(weight, height)
filebmi.bmi_category(weight, height)
```

## Important

The function 'filebmi.bmi(weight, height)' returns bmi result
The function 'filebmi.bmi_category(weight, height)' returns bmi category

## Author
Glauco Mori

## License
[MIT](LICENSE.txt)