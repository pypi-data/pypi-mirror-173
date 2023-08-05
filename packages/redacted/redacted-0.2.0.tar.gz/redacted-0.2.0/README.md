##  redacted

> 1️⃣ version: 0.2.0

> ✍️ author: Mitchell Lisle

📛 An experimental data anonymisation library

## Install

```shell
pip install redacted
```

## Usage

### Anonymiser
```python
from redacted import Anonymiser, AusPostCode, AusDriversLicence

anonymiser = Anonymiser(info_types=[AusPostCode, AusDriversLicence])

# returns an AnonymisedText Object with metadata and information and text replaced with a like-for-like example
anonymised = anonymiser.anonymise('Milhouse Van Houten 2203 18423441')
anonymised.text # Milhouse Van Houten 7862 R90715
```

The `AnonymisedText` object contains all information about what was matched. The
example below shows `matches` that we found with some information about where in the string they occurerd.
`info_types` is a list of all values that we looked for in the given string.

```python
AnonymisedText(
    original='Milhouse Van Houten 2203 18423441',
    text='Milhouse Van Houten 7862 R90715',
    matches=[
        Match(text='2203', start=20, end=24, len=4, type=<class 'redacted.info_types.AusPostCode'>),
        Match(text='18423441', start=25, end=33, len=8, type=<class 'redacted.info_types.AusDriversLicence'>)
    ],
    info_types=[
        <class 'redacted.info_types.AusPostCode'>,
        <class 'redacted.info_types.AusDriversLicence'>
    ]
)

```

### Info Types
The core of what this library does is use regex expressions to look for values in a given string. If 
we find a match there is a replacement strategy for each info type that we can use to replace the value
in the string. The current list of info types is (code for these can be found in `redacted.info_types`:

```text
Email,
AusPassport,
AusDriversLicence,
AusTaxFileNumber,
AusPostCode,
AusLicensePlate,
LongDigit
```

> ⚠️ The order is important when passing them in to the `Anonymiser` class. If we match on an info 
> type at the beginning, subsequent matches will be ignored. More generic types (such as LongDigit)
> should be placed at the end so we don't capture too many non-specific matches.
> For example:
> ```python
> from redacted import Anonymiser, LongDigit, AusDriversLicence
> 
> anonymiser = Anonymiser(info_types=[LongDigit, AusDriversLicence])
>
> # The following is a AusDriversLicence number, but because LongDigit is also a match,
> # we would match this as `LongDigit` which is less specific. In some cases we might want to prefer
> # LongDigit over LicenceNumber, this is left to you to decide when setting up your info_types.
> anonymised = anonymiser.anonymise('18423441')
> anonymised.text # 4563456
> ```