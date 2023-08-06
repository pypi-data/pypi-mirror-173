# Python Liquid Babel Change Log

## Version 1.0.0

**Features**

- New `unit` formatting filter. ([docs](https://jg-rp.github.io/liquid/babel/filters#unit), [source](https://github.com/jg-rp/liquid-babel/blob/main/liquid_babel/filters/unit.py))

## Version 0.3.0

**Features**

- New translation tags and message extraction. ([docs](https://jg-rp.github.io/liquid/babel/introduction#translations), [source](https://github.com/jg-rp/liquid-babel/tree/main/liquid_babel/messages))

## Version 0.2.0

**Features**

- New `datetime` formatting filter ([docs](https://jg-rp.github.io/liquid/babel/filters#datetime), [source](https://github.com/jg-rp/liquid-babel/blob/main/liquid_babel/filters/date_and_time.py)).

## Version 0.1.0

Version bump to indicate beta status.

## Version 0.0.1

**Features**

- New currency formatting filter ([docs](https://jg-rp.github.io/liquid/babel/filters#currency), [source](https://github.com/jg-rp/liquid-babel/blob/main/liquid_babel/filters/currency.py)).
- New convenience "money" filters. `money`, `money_with_currency`, `money_without_currency` and `money_without_trailing_zeros` behave similarly to Shopify's equivalents ([docs](https://jg-rp.github.io/liquid/babel/filters#money), [source](https://github.com/jg-rp/liquid-babel/blob/main/liquid_babel/filters/__init__.py)).
- New decimal formatting filter ([docs](https://jg-rp.github.io/liquid/babel/filters#decimal--number), [source](https://github.com/jg-rp/liquid-babel/blob/main/liquid_babel/filters/number.py)).

**Fixes**

- Currency string parsing. Allow an input locale to be set independently from the output locale.
