# VB6 sample

A tiny, fictional VB6 order-entry app used to demo `legacy-lens scan`.

```
legacy-lens scan examples/vb6-sample --out report.html
```

Expected highlights:

- `modReports.OldMonthlyReport` is reported as a dead-code candidate.
- `Form_Load`, `cmdSave_Click` and `Class_Initialize` are recognized as entry points.
- Tables found: `ORDERS`, `CUSTOMERS`, `STOCK`.
