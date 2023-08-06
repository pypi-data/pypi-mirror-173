# Version 1.1.0

- Added 'fast_evaluate'
    - Returns True if the message contains an OwO-like expression.
        Fast evaluate checks only if the message contains the exact
        characters 'owo' and 'uwu', and therefore is much less accurate
        than the normal evaluate function.

- Added a string length and whitespace check.
  This removes redundant REGEX searches on empty or short strings.