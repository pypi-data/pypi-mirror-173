# experiences

Provides convenience functions and statistical approaches for Experience Research.

### Features

- Convert lengths between miles, yards, feet and inches.
- Convert weights between hundredweight, stone, pounds and ounces.

### Usage

```
import experiences

# Convert 500 miles to feet
experiences.length.convert_unit(500, from_unit='yd', to_unit='ft')  # returns 1500.0

# Convert 100 ounces to pounds
experiences.weight.convert_unit(100, from_unit='oz', to_unit='lb')  # returns 6.25
```

```
# Create distribution
python setup.py sdist bdist_wheel
```

```
# Upload to PyPi
twine upload dist/*
```
