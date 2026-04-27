# Example invalid signal

Invalid:
- payload contains a raw previous conversation dump
- from/to does not reference known nodes
- payload exceeds allowed depth

Expected result:
- SignalCheck fails
- ValidationFailureHandler routes the issue to SignalDesigner