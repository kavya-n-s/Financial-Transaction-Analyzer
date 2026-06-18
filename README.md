# Financial Transaction Analyzer

## Project overview
Python-based finance analytics and validation pipeline for processing transaction datasets, performing data quality checks, generating exception reports, and exporting analytical outputs.

## Features
### Analytics
- Category-wise spending analysis
- Payment method analysis
- Region-wise summaries
- Daily spending trends
### Validation
- Missing value checks
- Negative amount checks
- Invalid status detection
- Invalid region detection
- Threshold-based transaction filtering
### Reporting
- CSV reports
- JSON reports
- Multi-sheet Excel validation workbook
- Exception summaries
- Data quality score

## Technologies used
- Python
- Pandas
- OpenPyXL
- CSV
- JSON
- Git
- GitHub

## Validation Checks
| Validation       | Description                        |
| ---------------- | ---------------------------------- |
| Missing Values   | Detects incomplete records         |
| Negative Amounts | Flags invalid transactions         |
| Invalid Status   | Checks allowed statuses            |
| Invalid Regions  | Verifies region values             |
| Threshold Checks | Identifies high-value transactions |

## Outputs Generated
### Excel Reports
- Validation workbook
### CSV Reports
- Category summary
- Payment summary
- High-value transactions
- Falied transactions
- Pending transactions
- Payment method summary
- Payment Method Analysis
- Region summary
### JSON Reports
Transaction summary

## Sample Workflow
CSV Input
     ->
Data Validation
     ->
Analytics
     ->
Exception Detection
     ->
Excel/CSV/JSON Outputs

## Future Enhancements
- API-based ingestion
- Audit logging
- Data quality dashboard
- Reconciliation engine integration
- PySpark migration


