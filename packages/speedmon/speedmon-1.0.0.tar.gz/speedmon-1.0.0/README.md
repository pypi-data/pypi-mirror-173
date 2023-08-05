# Description

Performance Monitoring Capabilities

# Installation

`pip install speedmon`

# Usage

**Programmatically:**

```python
from speedmon.SpeedMonitor import SpeedMonitor

p = SpeedMonitor(label="Execution Time of Heavy Calcuation")

result = 1000000 * 1000000

p.printExecutionTime()
```

# Example

Produces the following output:

```
----------
         Label: Execution Time of Heavy Calcuation
      Datetime: 23/10/2022 16:41:18
Execution Time: 0.0 sec
----------
```

# License

MIT