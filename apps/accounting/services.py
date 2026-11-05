"""Services for Accounting module"""
from django.db import transaction
from decimal import Decimal
from .models import JournalEntry, JournalEntryLine, Ledger, Account


class JournalEntryService:
    @staticmethod
    @transaction.atomic
    def create_journal_entry(data, organization, branch, created_by=None):
        entry = JournalEntry.objects.create(
            organization=organization,
            branch=branch,
            entry_number=JournalEntryService.generate_entry_number(organization, branch),
            reference=data.get('reference'),
            description=data.get('description'),
            entry_date=data.get('entry_date'),
            created_by=created_by,
            approved_by_id=data.get('approved_by_id'),
            is_posted=data.get('is_posted', False),
        )
        
        # Create journal lines
        for line_data in data.get('lines', []):
            JournalEntryLine.objects.create(
                journal_entry=entry,
                account_id=line_data.get('account_id'),
                description=line_data.get('description'),
                debit=Decimal(line_data.get('debit', 0) or 0),
                credit=Decimal(line_data.get('credit', 0) or 0),
            )
        
        # Post to ledger if needed
        if data.get('is_posted', False):
            JournalEntryService.post_to_ledger(entry)
        
        return entry
    
    @staticmethod
    def generate_entry_number(organization, branch):
        from django.utils import timezone
        org_code = organization.code if organization else 'ORG'
        branch_code = branch.code if branch else 'BR'
        date_str = timezone.now().strftime('%Y%m%d')
        last_entry = JournalEntry.objects.filter(entry_number__startswith=f"{org_code}-{branch_code}-{date_str}").order_by('-entry_number').first()
        seq = 1
        if last_entry:
            try:
                seq = int(last_entry.entry_number.split('-')[-1]) + 1
            except:
                seq = 1
        return f"{org_code}-{branch_code}-{date_str}-{seq:04d}"
    
    @staticmethod
    @transaction.atomic
    def post_to_ledger(entry):
        """Post journal entry to ledger"""
        for line in entry.lines.all():
            # Update account balance
            account = line.account
            if line.debit > 0:
                account.current_balance += line.debit
            elif line.credit > 0:
                account.current_balance -= line.credit
            account.save()
            
            # Create ledger entry
            Ledger.objects.create(
                organization=entry.organization,
                branch=entry.branch,
                account=account,
                entry_date=entry.entry_date,
                reference=entry.reference,
                description=line.description or entry.description,
                debit=line.debit,
                credit=line.credit,
                balance=account.current_balance,
                created_by=entry.created_by,
            )
        
        entry.is_posted = True
        entry.posted_at = timezone.now()
        entry.save()


class AccountService:
    @staticmethod
    def get_account_balance(account):
        """Get current balance for an account"""
        from django.db.models import Sum
        
        debit_total = Ledger.objects.filter(account=account).aggregate(total=Sum('debit'))['total'] or 0
        credit_total = Ledger.objects.filter(account=account).aggregate(total=Sum('credit'))['total'] or 0
        
        return account.opening_balance + debit_total - credit_total
