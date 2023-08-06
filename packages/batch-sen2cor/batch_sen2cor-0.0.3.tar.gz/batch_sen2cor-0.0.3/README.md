# Batch Sen2cor

## Description.

The package package_name is used to:
    Processing:
        - batch processing of sentinel 2 image using sen2cor atmospheric correction
    Sen2cor:
        - the sen2cor aplication from [ESA](https://step.esa.int/main/snap-supported-plugins/sen2cor/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install package_name

```bash
pip install batch_sen2cor
```

## Usage

Run the program in the folder where the SENTINEL-2 image is.

```python
>>> from batch_sen2cor.processing import batch_sen2cor
>>> batch_sen2cor.sentinel_sen2cor()
```

## Author
Mateus Miranda

## License
[MIT](https://choosealicense.com/licenses/mit/)
