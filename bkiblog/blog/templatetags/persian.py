"""Persian digit/price template filters.

Django's locale-based grouping produces no digit grouping when
LANGUAGE_CODE='fa', so these filters do the work explicitly:
- fa_digits: Latin 0-9 (and . , -) become Persian ۰-۹ (٫ ٬ ٫ ...)
- fa_price: round to whole rials, group thousands with ٬, then fa_digits.
"""

from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()

_FA_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
_FA_THOUSAND_SEP = '٬'
_FA_DECIMAL_SEP = '٫'


def _to_persian_digits(text):
    out = []
    for ch in str(text):
        if '0' <= ch <= '9':
            out.append(_FA_DIGITS[ord(ch) - ord('0')])
        elif ch == ',':
            out.append(_FA_THOUSAND_SEP)
        elif ch == '.':
            out.append(_FA_DECIMAL_SEP)
        elif ch == '-':
            out.append('−')
        else:
            out.append(ch)
    return ''.join(out)


@register.filter(name='fa_digits')
def fa_digits(value):
    """Render any value with Persian digits (keeps other chars as-is)."""
    if value is None:
        return ''
    return _to_persian_digits(value)


@register.filter(name='fa_price')
def fa_price(value):
    """Render a rial amount: whole number, ٬ grouping, Persian digits."""
    if value is None:
        return '۰'
    try:
        amount = int(Decimal(str(value)).to_integral_value())
    except (InvalidOperation, ValueError, TypeError):
        return '۰'
    negative = amount < 0
    grouped = '{:,}'.format(abs(amount))
    text = ('−' if negative else '') + grouped
    return _to_persian_digits(text)
