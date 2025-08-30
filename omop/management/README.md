# Django Management Commands

This directory contains custom Django management commands for the Exact-OMOP system. These commands facilitate data loading, validation, and maintenance operations.

## Available Commands

### Data Loading Commands

#### `load_synthetic_breast_cancer_data`
Loads comprehensive synthetic breast cancer patient data with complete treatment regimens.

```bash
# Load synthetic data (keeping existing data)
python manage.py load_synthetic_breast_cancer_data

# Clear existing data and load fresh
python manage.py load_synthetic_breast_cancer_data --clear
```

**Dataset includes:**
- 15 synthetic patients with diverse demographics
- 26 treatment regimens across multiple lines
- Complete biomarker profiles (ER, PR, HER2)
- Realistic treatment outcomes and progressions

#### `load_breast_cancer_data`
Loads the original breast cancer fixture data.

```bash
python manage.py load_breast_cancer_data
```

### Data Validation Commands

#### `validate_patient_info`
Validates the integrity and completeness of patient data.

```bash
python manage.py validate_patient_info
```

**Checks include:**
- Required field completeness
- Referential integrity
- Date consistency
- Clinical logic validation

#### `cleanup_patient_info`
Removes orphaned records and fixes data inconsistencies.

```bash
python manage.py cleanup_patient_info
```

**Operations performed:**
- Removes orphaned treatment regimens
- Fixes broken foreign key references
- Standardizes date formats
- Removes duplicate records

### Data Management Commands

#### `populate_patient_info`
Populates derived fields and calculated values.

```bash
python manage.py populate_patient_info
```

**Updates include:**
- Treatment line sequences
- Response assessment dates
- Progression calculations
- Outcome summaries

#### `update_patient_info`
Updates existing patient records with new data standards.

```bash
python manage.py update_patient_info
```

**Modifications include:**
- Concept ID mappings
- Standard vocabulary alignment
- Field format standardization
- Data quality improvements

## Usage Examples

### Complete Data Refresh
```bash
# Clear and reload with synthetic data
python manage.py load_synthetic_breast_cancer_data --clear

# Validate the loaded data
python manage.py validate_patient_info

# Populate derived fields
python manage.py populate_patient_info
```

### Data Quality Maintenance
```bash
# Regular cleanup routine
python manage.py cleanup_patient_info
python manage.py validate_patient_info
python manage.py update_patient_info
```

### Development Workflow
```bash
# Load test data for development
python manage.py load_synthetic_breast_cancer_data --clear

# Test data validation
python manage.py validate_patient_info

# Make changes to models...

# Re-validate after changes
python manage.py validate_patient_info
```

## Command Development

### Adding New Commands

1. Create a new Python file in the `commands/` directory
2. Inherit from `BaseCommand`
3. Implement the `handle()` method
4. Add appropriate argument parsing
5. Include comprehensive error handling

### Example Command Structure

```python
from django.core.management.base import BaseCommand
from django.core.management import CommandError

class Command(BaseCommand):
    help = 'Brief description of what the command does'

    def add_arguments(self, parser):
        parser.add_argument(
            '--option',
            action='store_true',
            help='Description of the option',
        )

    def handle(self, *args, **options):
        try:
            # Command implementation
            self.stdout.write(
                self.style.SUCCESS('Successfully completed operation')
            )
        except Exception as e:
            raise CommandError(f'Command failed: {str(e)}')
```

### Best Practices

- **Error Handling**: Always include comprehensive error handling
- **Progress Feedback**: Use `self.stdout.write()` for user feedback
- **Transaction Safety**: Use database transactions for data modifications
- **Argument Validation**: Validate command arguments before processing
- **Documentation**: Include detailed help text and examples

## Troubleshooting

### Common Issues

**Command not found:**
```bash
# Ensure you're in the project root directory
cd /path/to/exactomop

# Verify the command exists
python manage.py help

# Check for Python path issues
python manage.py shell -c "import sys; print(sys.path)"
```

**Database connection errors:**
```bash
# Check database settings
python manage.py check --database default

# Test database connectivity
python manage.py dbshell
```

**Migration issues:**
```bash
# Apply pending migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Performance Considerations

- **Large Datasets**: Use batch processing for large data operations
- **Database Locks**: Be mindful of long-running transactions
- **Memory Usage**: Process data in chunks to avoid memory issues
- **Indexing**: Ensure appropriate database indexes are in place

---

For more information about the Exact-OMOP system, see the main [README.md](../../README.md) file.