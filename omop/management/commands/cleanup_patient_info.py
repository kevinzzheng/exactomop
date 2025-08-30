from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q, Count
from omop.models import (
    Person, PatientInfo, ConditionOccurrence, Measurement, 
    DrugExposure, ProcedureOccurrence, Observation, Episode,
    TreatmentLine, TreatmentRegimen, BiomarkerMeasurement, ClinicalTrialBiomarker,
    GenomicVariant, MolecularTest, ClinicalLabTest, TumorAssessment,
    RadiationOccurrence, StemCellTransplant, ClinicalTrial, BiospecimenCollection,
    OncologyEpisodeDetail
)
from datetime import date, datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Clean up PatientInfo records - remove orphaned, duplicate, or invalid records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--remove-orphaned',
            action='store_true',
            help='Remove PatientInfo records where the Person no longer exists',
        )
        parser.add_argument(
            '--remove-duplicates',
            action='store_true',
            help='Remove duplicate PatientInfo records for the same person',
        )
        parser.add_argument(
            '--remove-empty',
            action='store_true',
            help='Remove PatientInfo records with no meaningful data',
        )
        parser.add_argument(
            '--remove-outdated',
            type=int,
            help='Remove records older than specified days',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletions (required for actual cleanup)',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Number of records to process in each batch',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run')
        confirm = options.get('confirm')
        batch_size = options.get('batch_size')
        
        if not dry_run and not confirm:
            self.stderr.write(
                self.style.ERROR(
                    'This command will delete data. Use --dry-run to see what would be deleted, '
                    'or --confirm to proceed with actual deletion.'
                )
            )
            return
        
        cleanup_stats = {
            'orphaned_removed': 0,
            'duplicates_removed': 0,
            'empty_removed': 0,
            'outdated_removed': 0,
            'total_removed': 0
        }
        
        self.stdout.write(f'Starting PatientInfo cleanup ({"DRY RUN" if dry_run else "LIVE RUN"})')
        
        # Clean up orphaned records
        if options.get('remove_orphaned'):
            orphaned_count = self.cleanup_orphaned_records(dry_run, batch_size)
            cleanup_stats['orphaned_removed'] = orphaned_count
            cleanup_stats['total_removed'] += orphaned_count
        
        # Clean up duplicate records
        if options.get('remove_duplicates'):
            duplicate_count = self.cleanup_duplicate_records(dry_run, batch_size)
            cleanup_stats['duplicates_removed'] = duplicate_count
            cleanup_stats['total_removed'] += duplicate_count
        
        # Clean up empty records
        if options.get('remove_empty'):
            empty_count = self.cleanup_empty_records(dry_run, batch_size)
            cleanup_stats['empty_removed'] = empty_count
            cleanup_stats['total_removed'] += empty_count
        
        # Clean up outdated records
        if options.get('remove_outdated'):
            outdated_count = self.cleanup_outdated_records(
                options['remove_outdated'], dry_run, batch_size
            )
            cleanup_stats['outdated_removed'] = outdated_count
            cleanup_stats['total_removed'] += outdated_count
        
        # Print summary
        self.print_cleanup_summary(cleanup_stats, dry_run)

    def cleanup_orphaned_records(self, dry_run=False, batch_size=1000):
        """Remove PatientInfo records where the associated Person no longer exists"""
        
        self.stdout.write('Checking for orphaned PatientInfo records...')
        
        # Find PatientInfo records with non-existent Person references
        orphaned_query = PatientInfo.objects.filter(
            ~Q(person__isnull=False)
        )
        
        orphaned_count = orphaned_query.count()
        
        if orphaned_count == 0:
            self.stdout.write('No orphaned records found.')
            return 0
        
        self.stdout.write(f'Found {orphaned_count} orphaned PatientInfo records.')
        
        if dry_run:
            self.stdout.write(f'DRY RUN: Would delete {orphaned_count} orphaned records.')
            return orphaned_count
        
        # Delete in batches
        deleted_count = 0
        with transaction.atomic():
            while True:
                batch_ids = list(orphaned_query.values_list('id', flat=True)[:batch_size])
                if not batch_ids:
                    break
                
                batch_deleted = PatientInfo.objects.filter(id__in=batch_ids).delete()[0]
                deleted_count += batch_deleted
                
                self.stdout.write(f'Deleted {deleted_count}/{orphaned_count} orphaned records...')
        
        self.stdout.write(f'Successfully deleted {deleted_count} orphaned records.')
        return deleted_count

    def cleanup_duplicate_records(self, dry_run=False, batch_size=1000):
        """Remove duplicate PatientInfo records for the same person"""
        
        self.stdout.write('Checking for duplicate PatientInfo records...')
        
        # Find persons with multiple PatientInfo records
        duplicates = (
            PatientInfo.objects
            .values('person')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )
        
        duplicate_person_count = duplicates.count()
        
        if duplicate_person_count == 0:
            self.stdout.write('No duplicate records found.')
            return 0
        
        self.stdout.write(f'Found {duplicate_person_count} persons with duplicate PatientInfo records.')
        
        total_to_remove = 0
        duplicate_records = []
        
        for dup in duplicates:
            person_id = dup['person']
            records = PatientInfo.objects.filter(person_id=person_id).order_by('-created_at', '-id')
            
            # Keep the most recent record, mark others for deletion
            records_to_delete = list(records)[1:]  # Skip the first (most recent)
            duplicate_records.extend(records_to_delete)
            total_to_remove += len(records_to_delete)
        
        if dry_run:
            self.stdout.write(f'DRY RUN: Would delete {total_to_remove} duplicate records.')
            return total_to_remove
        
        # Delete duplicates in batches
        deleted_count = 0
        with transaction.atomic():
            for i in range(0, len(duplicate_records), batch_size):
                batch = duplicate_records[i:i + batch_size]
                batch_ids = [record.id for record in batch]
                
                batch_deleted = PatientInfo.objects.filter(id__in=batch_ids).delete()[0]
                deleted_count += batch_deleted
                
                self.stdout.write(f'Deleted {deleted_count}/{total_to_remove} duplicate records...')
        
        self.stdout.write(f'Successfully deleted {deleted_count} duplicate records.')
        return deleted_count

    def cleanup_empty_records(self, dry_run=False, batch_size=1000):
        """Remove PatientInfo records with no meaningful data"""
        
        self.stdout.write('Checking for empty PatientInfo records...')
        
        # Define criteria for "empty" records
        empty_query = PatientInfo.objects.filter(
            Q(disease__isnull=True) | Q(disease=''),
            Q(diagnosis_date__isnull=True),
            Q(patient_age__isnull=True),
            Q(hemoglobin__isnull=True),
            Q(hematocrit__isnull=True),
            Q(platelet_count__isnull=True),
            Q(wbc_count__isnull=True),
            Q(prior_lines_therapy__isnull=True),
            Q(biomarker_results__isnull=True) | Q(biomarker_results=''),
            Q(genetic_test_results__isnull=True) | Q(genetic_test_results=''),
            Q(omop_data_json__isnull=True) | Q(omop_data_json='')
        )
        
        empty_count = empty_query.count()
        
        if empty_count == 0:
            self.stdout.write('No empty records found.')
            return 0
        
        self.stdout.write(f'Found {empty_count} empty PatientInfo records.')
        
        if dry_run:
            self.stdout.write(f'DRY RUN: Would delete {empty_count} empty records.')
            return empty_count
        
        # Delete in batches
        deleted_count = 0
        with transaction.atomic():
            while True:
                batch_ids = list(empty_query.values_list('id', flat=True)[:batch_size])
                if not batch_ids:
                    break
                
                batch_deleted = PatientInfo.objects.filter(id__in=batch_ids).delete()[0]
                deleted_count += batch_deleted
                
                self.stdout.write(f'Deleted {deleted_count}/{empty_count} empty records...')
        
        self.stdout.write(f'Successfully deleted {deleted_count} empty records.')
        return deleted_count

    def cleanup_outdated_records(self, days_old, dry_run=False, batch_size=1000):
        """Remove PatientInfo records older than specified days"""
        
        self.stdout.write(f'Checking for PatientInfo records older than {days_old} days...')
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        outdated_query = PatientInfo.objects.filter(
            created_at__lt=cutoff_date
        )
        
        outdated_count = outdated_query.count()
        
        if outdated_count == 0:
            self.stdout.write(f'No records older than {days_old} days found.')
            return 0
        
        self.stdout.write(f'Found {outdated_count} records older than {days_old} days.')
        
        if dry_run:
            self.stdout.write(f'DRY RUN: Would delete {outdated_count} outdated records.')
            return outdated_count
        
        # Delete in batches
        deleted_count = 0
        with transaction.atomic():
            while True:
                batch_ids = list(outdated_query.values_list('id', flat=True)[:batch_size])
                if not batch_ids:
                    break
                
                batch_deleted = PatientInfo.objects.filter(id__in=batch_ids).delete()[0]
                deleted_count += batch_deleted
                
                self.stdout.write(f'Deleted {deleted_count}/{outdated_count} outdated records...')
        
        self.stdout.write(f'Successfully deleted {deleted_count} outdated records.')
        return deleted_count

    def print_cleanup_summary(self, stats, dry_run):
        """Print cleanup summary"""
        
        self.stdout.write(self.style.SUCCESS('\n=== CLEANUP SUMMARY ==='))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No actual changes made'))
        
        self.stdout.write(f'Orphaned records {"would be " if dry_run else ""}removed: {stats["orphaned_removed"]}')
        self.stdout.write(f'Duplicate records {"would be " if dry_run else ""}removed: {stats["duplicates_removed"]}')
        self.stdout.write(f'Empty records {"would be " if dry_run else ""}removed: {stats["empty_removed"]}')
        self.stdout.write(f'Outdated records {"would be " if dry_run else ""}removed: {stats["outdated_removed"]}')
        self.stdout.write(f'Total records {"would be " if dry_run else ""}removed: {stats["total_removed"]}')
        
        if not dry_run and stats['total_removed'] > 0:
            # Show remaining record count
            remaining_count = PatientInfo.objects.count()
            self.stdout.write(f'PatientInfo records remaining: {remaining_count}')
        
        if dry_run and stats['total_removed'] > 0:
            self.stdout.write(
                self.style.WARNING(
                    '\nTo perform actual cleanup, run this command again with --confirm instead of --dry-run'
                )
            )
