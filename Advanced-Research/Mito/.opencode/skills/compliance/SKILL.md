-----
name: compliance
description: >
  Expert in regulatory compliance management for data protection, privacy, and security. 
  Use this skill for implementing GDPR, HIPAA, SOC 2, PCI-DSS controls, conducting compliance 
  audits, managing data subject requests, and building compliant systems. Covers regulatory 
  frameworks, technical controls, audit logging, and data governance.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: security
  tags: [compliance, gdpr, hipaa, security, data-protection, privacy]

# Regulatory Compliance Management

Covers: **GDPR · HIPAA · SOC 2 · PCI-DSS · Data Subject Requests · Audit Logging · Encryption · Access Control · Data Governance**

-----

## Compliance Frameworks Overview

### Major Regulatory Frameworks

| Framework | Domain | Key Requirements | Penalties |
|-----------|--------|------------------|-----------|
| **GDPR** | Privacy | Consent, DSAR, Data Minimization | 4% revenue / €20M |
| **HIPAA** | Healthcare | PHI Protection, BAA, Risk Assessment | $1.5M per violation category |
| **SOC 2** | Security | Trust Service Criteria | Loss of trust/certification |
| **PCI-DSS** | Payment | Cardholder Data Protection | Fines + transaction bans |
| **SOX** | Financial | Internal Controls | Criminal penalties |
| **ISO 27001** | Security | ISMS Implementation | Certification costs |

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import json

class ComplianceFramework(Enum):
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    PCIDSS = "pci_dss"
    ISO27001 = "iso27001"

@dataclass
class ComplianceRequirement:
    """Single compliance requirement"""
    id: str
    framework: ComplianceFramework
    title: str
    description: str
    category: str
    severity: str  # critical, high, medium, low
    implemented: bool = False
    evidence: List[str] = field(default_factory=list)

@dataclass
class ComplianceAudit:
    """Compliance audit record"""
    id: str
    framework: ComplianceFramework
    start_date: datetime
    end_date: Optional[datetime]
    auditor: str
    findings: List[Dict]
    status: str  # planned, in_progress, completed, failed
    
    def add_finding(self, severity: str, description: str, remediation: str):
        """Add audit finding"""
        self.findings.append({
            'severity': severity,
            'description': description,
            'remediation': remediation,
            'date': datetime.now().isoformat()
        })
```

-----

## GDPR Compliance

### Data Protection Principles

The GDPR is built on seven key principles:
1. **Lawfulness, fairness, transparency**
2. **Purpose limitation**
3. **Data minimization**
4. **Accuracy**
5. **Storage limitation**
6. **Integrity and confidentiality**
7. **Accountability**

```python
from typing import Callable, Optional, List
from dataclasses import dataclass

@dataclass
class PersonalData:
    """Represents personal data"""
    data_type: str  # email, name, ip, etc.
    category: str   # direct, indirect, special
    legal_basis: str  # consent, contract, legitimate_interest
    retention_period: timedelta
    is_encrypted: bool = False
    is_pseudonymized: bool = False


class GDPRComplianceManager:
    """Manages GDPR compliance"""
    
    def __init__(self):
        self.data_subjects: Dict[str, Dict] = {}
        self.consent_records: Dict[str, List[Dict]] = {}
        self.processing_activities: List[Dict] = []
        self.data_inventory: Dict[str, PersonalData] = {}
    
    # === DATA SUBJECT RIGHTS ===
    
    def handle_data_subject_request(self, request_id: str, 
                                    request_type: str,
                                    subject_id: str) -> Dict:
        """Handle Data Subject Access Request (DSAR)"""
        
        if request_type == 'access':
            return self._handle_access_request(subject_id)
        elif request_type == 'rectification':
            return self._handle_rectification_request(subject_id)
        elif request_type == 'erasure':
            return self._handle_erasure_request(subject_id)
        elif request_type == 'portability':
            return self._handle_portability_request(subject_id)
        elif request_type == 'objection':
            return self._handle_objection_request(subject_id)
        elif request_type == 'restriction':
            return self._handle_restriction_request(subject_id)
        else:
            raise ValueError(f"Unknown request type: {request_type}")
    
    def _handle_access_request(self, subject_id: str) -> Dict:
        """Right of access - provide all personal data"""
        
        if subject_id not in self.data_subjects:
            raise ValueError("Data subject not found")
        
        subject_data = self.data_subjects[subject_id]
        
        # Include processing information
        return {
            'personal_data': subject_data,
            'processing_activities': [
                pa for pa in self.processing_activities 
                if pa.get('subject_id') == subject_id
            ],
            'categories_of_data': list(set(
                d.data_type for d in self.data_inventory.values()
            )),
            'recipients': ['internal', 'third_parties'],
            'retention_period': '2 years',
            'rights_applicable': [
                'right_to_access',
                'right_to_rectification',
                'right_to_erasure',
                'right_to_restrict_processing',
                'right_to_data_portability',
                'right_to_object'
            ]
        }
    
    def _handle_erasure_request(self, subject_id: str) -> Dict:
        """Right to erasure ('right to be forgotten')"""
        
        # Check if exceptions apply
        exceptions = self._check_erasure_exceptions(subject_id)
        
        if exceptions:
            return {
                'status': 'partial',
                'erased': True,
                'exceptions': exceptions,
                'message': 'Some data retained due to legal obligations'
            }
        
        # Delete all personal data
        self._delete_subject_data(subject_id)
        
        return {
            'status': 'completed',
            'erased': True,
            'message': 'All personal data has been erased'
        }
    
    def _check_erasure_exceptions(self, subject_id: str) -> List[str]:
        """Check GDPR Article 17 exceptions"""
        exceptions = []
        
        # Check for legal obligations to retain
        if self._has_tax_obligations(subject_id):
            exceptions.append('legal_obligation_tax')
        
        # Check for ongoing contracts
        if self._has_active_contracts(subject_id):
            exceptions.append('contract_performance')
        
        # Check for legal claims
        if self._has_legal_claims(subject_id):
            exceptions.append('legal_claims')
        
        return exceptions
    
    def _handle_portability_request(self, subject_id: str) -> Dict:
        """Right to data portability"""
        
        import json
        
        subject_data = self.data_subjects.get(subject_id, {})
        
        # Format in machine-readable way
        portable_data = {
            'version': '1.0',
            'export_date': datetime.now().isoformat(),
            'data': subject_data,
            'format': 'json',
            'schema': 'gdpr_portability_v1'
        }
        
        return {
            'status': 'ready',
            'data': json.dumps(portable_data),
            'format': 'json',
            'download_link': f'/api/v1/dsar/{subject_id}/export'
        }
    
    def _delete_subject_data(self, subject_id: str):
        """Delete all data for subject"""
        # Delete from all systems
        if subject_id in self.data_subjects:
            del self.data_subjects[subject_id]
        
        if subject_id in self.consent_records:
            del self.consent_records[subject_id]
        
        # Log the deletion
        self._log_compliance_event('data_erasure', {
            'subject_id': subject_id,
            'timestamp': datetime.now().isoformat()
        })
    
    # === CONSENT MANAGEMENT ===
    
    def record_consent(self, subject_id: str, purpose: str, 
                      granted: bool, granularity: str = 'opt_in') -> Dict:
        """Record user consent with full audit trail"""
        
        consent_record = {
            'purpose': purpose,
            'granted': granted,
            'timestamp': datetime.now().isoformat(),
            'ip_address': self._get_current_ip(),
            'user_agent': self._get_current_user_agent(),
            'granularity': granularity,
            'version': '1.0',
            'withdrawal_method': 'email_privacy@example.com'
        }
        
        if subject_id not in self.consent_records:
            self.consent_records[subject_id] = []
        
        self.consent_records[subject_id].append(consent_record)
        
        # Log consent change
        self._log_compliance_event('consent_change', consent_record)
        
        return consent_record
    
    def verify_consent(self, subject_id: str, purpose: str) -> bool:
        """Verify valid consent exists for purpose"""
        
        records = self.consent_records.get(subject_id, [])
        
        for record in records:
            if (record['purpose'] == purpose and 
                record['granted'] and 
                self._is_consent_valid(record)):
                return True
        
        return False
    
    def _is_consent_valid(self, consent_record: Dict) -> bool:
        """Check if consent is still valid"""
        
        # Check if consent was withdrawn
        # (simplified - in reality would check withdrawal records)
        
        consent_date = datetime.fromisoformat(consent_record['timestamp'])
        age = datetime.now() - consent_date
        
        # Consent typically valid for 2 years unless withdrawn
        return age.days < 730
    
    def _log_compliance_event(self, event_type: str, data: Dict):
        """Log compliance event for audit"""
        # In production, this would write to secure audit log
        print(f"Compliance event: {event_type} - {json.dumps(data)}")
    
    # === DATA INVENTORY ===
    
    def register_personal_data(self, data_type: str, 
                             personal_data: PersonalData):
        """Register personal data in inventory"""
        self.data_inventory[data_type] = personal_data
    
    def generate_data_protection_impact_assessment(self) -> Dict:
        """Generate DPIA (Data Protection Impact Assessment)"""
        
        return {
            'assessment_date': datetime.now().isoformat(),
            'necessity': 'Processing is necessary for service delivery',
            'risks': [
                {
                    'risk': 'Unauthorized access',
                    'likelihood': 'low',
                    'severity': 'high',
                    'mitigation': 'Encryption at rest and in transit'
                },
                {
                    'risk': 'Data breach',
                    'likelihood': 'medium',
                    'severity': 'high',
                    'mitigation': 'Incident response plan, breach notification'
                }
            ],
            'consultation_required': False,
            'dpo_opinion': 'Approved with conditions'
        }
```

-----

## HIPAA Compliance

### Protected Health Information (PHI)

```python
class HIPAAController:
    """HIPAA compliance controller"""
    
    PHI_FIELDS = [
        'patient_name', 'social_security_number', 'medical_record_number',
        'health_plan_beneficiary_number', 'account_number', 'license_number',
        'vehicle_identifier', 'device_identifier', 'url', 'ip_address',
        'biometric_identifiers', 'full_face_photographs', 'date_of_birth',
        'admission_date', 'discharge_date', 'death_date', 'telephone_number',
        'fax_number', 'email_address', 'geographic_data'
    ]
    
    def __init__(self):
        self.phi_access_log = []
        self.encryption_required = True
        self.break_the_glass_log = []
    
    def is_phi(self, data_field: str) -> bool:
        """Check if field contains PHI"""
        return data_field.lower() in [f.lower() for f in self.PHI_FIELDS]
    
    def access_phi(self, user_id: str, patient_id: str, 
                  data_type: str, purpose: str) -> Dict:
        """Log all PHI access per HIPAA requirements"""
        
        # Check minimum necessary standard
        if not self._is_authorized(user_id, patient_id, data_type, purpose):
            raise PermissionError(
                f"User {user_id} not authorized to access {data_type} for {purpose}"
            )
        
        # Log access
        access_record = {
            'user_id': user_id,
            'patient_id': self._pseudonymize(patient_id),
            'data_type': data_type,
            'purpose': purpose,
            'timestamp': datetime.now().isoformat(),
            'action': 'read'
        }
        
        self.phi_access_log.append(access_record)
        
        # Return (would be encrypted in production)
        return {'status': 'accessed', 'phi': self._retrieve_phi(patient_id, data_type)}
    
    def _is_authorized(self, user_id: str, patient_id: str,
                      data_type: str, purpose: str) -> bool:
        """Check minimum necessary standard"""
        
        # Simplified - would check against access control matrix
        authorized_purposes = ['treatment', 'payment', 'operations', 'research']
        
        return purpose in authorized_purposes
    
    def _pseudonymize(self, patient_id: str) -> str:
        """Pseudonymize patient identifier"""
        # Use consistent hash for pseudonymization
        return hashlib.sha256(patient_id.encode()).hexdigest()[:16]
    
    def _retrieve_phi(self, patient_id: str, data_type: str) -> Any:
        """Retrieve PHI (would be decrypted in production)"""
        pass
    
    def encrypt_phi(self, data: bytes) -> bytes:
        """Encrypt PHI at rest and in transit"""
        
        if not self.encryption_required:
            return data
        
        # Use AES-256 encryption
        from cryptography.fernet import Fernet
        key = self._get_encryption_key()  # Would come from KMS
        f = Fernet(key)
        
        return f.encrypt(data)
    
    def decrypt_phi(self, encrypted_data: bytes) -> bytes:
        """Decrypt PHI"""
        
        if not self.encryption_required:
            return encrypted_data
        
        from cryptography.fernet import Fernet
        key = self._get_encryption_key()
        f = Fernet(key)
        
        return f.decrypt(encrypted_data)
    
    def generate_hipaa_business_associate_agreement(self, vendor_name: str) -> Dict:
        """Generate BAA template"""
        
        return {
            'agreement_type': 'Business Associate Agreement',
            'parties': {
                'covered_entity': '[Your Organization]',
                'business_associate': vendor_name
            },
            'obligations': [
                'Implement HIPAA security rules',
                'Report any breaches within 60 days',
                'Ensure PHI confidentiality',
                'Limit PHI use to minimum necessary',
                'Provide breach notification',
                'Return or destroy PHI at termination'
            ],
            'permitted_uses': [
                'Performance of functions per contract',
                'Required by law',
                'Public health activities'
            ],
            'prohibited_uses': [
                'Use for marketing without consent',
                'Sale of PHI',
                'Most research without authorization'
            ]
        }
    
    def conduct_risk_analysis(self) -> Dict:
        """Conduct HIPAA-required risk analysis"""
        
        return {
            'analysis_date': datetime.now().isoformat(),
            'scope': 'All systems containing PHI',
            'threats_identified': [
                {
                    'threat': 'Unauthorized access',
                    'likelihood': 'possible',
                    'impact': 'severe',
                    'mitigations': ['Access controls', 'Encryption', 'Audit logging']
                },
                {
                    'threat': 'Ransomware',
                    'likelihood': 'possible',
                    'impact': 'severe',
                    'mitigations': ['Backups', 'Staff training', 'Endpoint protection']
                }
            ],
            'risk_score': 'medium',
            'recommendations': [
                'Implement MFA for all PHI access',
                'Annual security training',
                'Regular penetration testing'
            ]
        }
```

-----

## SOC 2 Compliance

### Trust Service Criteria

```python
class SOC2Controls:
    """SOC 2 compliance controls"""
    
    # Trust Service Criteria categories
    TSC_CATEGORIES = {
        'security': 'Common Criteria',
        'availability': 'Availability',
        'processing_integrity': 'Processing Integrity',
        'confidentiality': 'Confidentiality',
        'privacy': 'Privacy'
    }
    
    def __init__(self):
        self.controls: Dict[str, Dict] = {}
        self.exceptions: List[Dict] = []
        self.control_tests: List[Dict] = []
    
    def register_control(self, control_id: str, 
                        description: str,
                        category: str,
                        control_type: str,  # preventive, detective, corrective
                        periodicity: str):   # daily, weekly, monthly, quarterly
        
        self.controls[control_id] = {
            'description': description,
            'category': category,
            'type': control_type,
            'periodicity': periodicity,
            'last_tested': None,
            'status': 'active',
            'test_results': []
        }
    
    def document_control_test(self, control_id: str, 
                             test_result: str,
                             evidence: str,
                             tested_by: str):
        """Document control test results"""
        
        if control_id not in self.controls:
            raise ValueError(f"Control {control_id} not found")
        
        test_record = {
            'test_date': datetime.now().isoformat(),
            'result': test_result,  # pass, fail, exception
            'evidence': evidence,
            'tested_by': tested_by,
            'exceptions_noted': None
        }
        
        self.controls[control_id]['test_results'].append(test_record)
        self.controls[control_id]['last_tested'] = datetime.now()
        
        self.control_tests.append({
            'control_id': control_id,
            **test_record
        })
    
    def log_control_exception(self, control_id: str, 
                            description: str,
                            remediation: str,
                            remediation_owner: str):
        """Log control deviation with remediation plan"""
        
        exception = {
            'control_id': control_id,
            'description': description,
            'remediation': remediation,
            'remediation_owner': remediation_owner,
            'exception_date': datetime.now().isoformat(),
            'target_resolution': (datetime.now() + timedelta(days=30)).isoformat(),
            'status': 'open'  # open, resolved, accepted_risk
        }
        
        self.exceptions.append(exception)
    
    def generate_soc2_report(self) -> Dict:
        """Generate SOC 2 Type II report data"""
        
        # Calculate control effectiveness
        total_controls = len(self.controls)
        tested_controls = sum(1 for c in self.controls.values() if c['last_tested'])
        passed_controls = sum(
            1 for c in self.controls.values() 
            if c['test_results'] and 
            all(t['result'] == 'pass' for t in c['test_results'][-5:])
        )
        
        return {
            'report_type': 'SOC 2 Type II',
            'report_period': {
                'start': (datetime.now() - timedelta(days=365)).isoformat(),
                'end': datetime.now().isoformat()
            },
            'controls': {
                'total': total_controls,
                'tested': tested_controls,
                'passed': passed_controls,
                'pass_rate': f"{(passed_controls/tested_controls)*100:.1f}%" if tested_controls else "N/A"
            },
            'exceptions': {
                'total': len(self.exceptions),
                'open': len([e for e in self.exceptions if e['status'] == 'open']),
                'resolved': len([e for e in self.exceptions if e['status'] == 'resolved'])
            },
            'categories': {
                cat: sum(1 for c in self.controls.values() if c['category'] == cat)
                for cat in self.TSC_CATEGORIES.keys()
            }
        }
    
    def get_control(self, control_id: str) -> Dict:
        """Get control details"""
        return self.controls.get(control_id, {})
```

-----

## Data Retention and Disposal

```python
class DataRetentionPolicy:
    """Data retention policy management"""
    
    DEFAULT_RETENTION = {
        'user_data': {'retention': timedelta(days=730), 'deletion': 'automatic'},
        'logs': {'retention': timedelta(days=90), 'deletion': 'automatic'},
        'financial_records': {'retention': timedelta(days=2555), 'deletion': 'manual'},
        'session_data': {'retention': timedelta(hours=24), 'deletion': 'automatic'},
        'backups': {'retention': timedelta(days=30), 'deletion': 'automatic'},
        'email': {'retention': timedelta(days=1095), 'deletion': 'manual'},
        'audit_logs': {'retention': timedelta(days=2555), 'deletion': 'none'},
        'temporary_files': {'retention': timedelta(hours=1), 'deletion': 'automatic'}
    }
    
    def __init__(self, policies: Dict[str, Dict] = None):
        self.policies = policies or self.DEFAULT_RETENTION
    
    def get_retention_period(self, data_category: str) -> timedelta:
        """Get retention period for data category"""
        policy = self.policies.get(data_category)
        return policy['retention'] if policy else timedelta(days=365)
    
    def should_delete(self, data_category: str, created_at: datetime) -> bool:
        """Check if data should be deleted"""
        policy = self.policies.get(data_category)
        
        if not policy:
            return False
        
        if policy['deletion'] == 'none':
            return False
        
        age = datetime.now() - created_at
        return age > policy['retention']
    
    def apply_retention_policy(self, data_store) -> Dict:
        """Apply retention policy and return deletion summary"""
        
        deleted_counts = {}
        
        for category, policy in self.policies.items():
            if policy['deletion'] == 'automatic':
                deleted = self._delete_expired_data(
                    category, 
                    policy['retention']
                )
                deleted_counts[category] = deleted
        
        return {
            'deletion_date': datetime.now().isoformat(),
            'deleted_counts': deleted_counts,
            'total_deleted': sum(deleted_counts.values())
        }
    
    def _delete_expired_data(self, category: str, retention: timedelta) -> int:
        """Delete expired data for category (implementation depends on data store)"""
        # This would connect to actual data store
        pass
    
    def generate_retention_schedule(self) -> List[Dict]:
        """Generate retention schedule for compliance"""
        
        schedule = []
        
        for category, policy in self.policies.items():
            schedule.append({
                'category': category,
                'retention_period_days': policy['retention'].days,
                'deletion_method': policy['deletion'],
                'legal_basis': self._get_legal_basis(category),
                'classification': self._get_classification(category)
            })
        
        return schedule
    
    def _get_legal_basis(self, category: str) -> str:
        """Get legal basis for retention"""
        bases = {
            'user_data': 'Contractual necessity, consent',
            'financial_records': 'Tax law (7 years)',
            'logs': 'Security monitoring',
            'audit_logs': 'Regulatory requirement'
        }
        return bases.get(category, 'Business necessity')
    
    def _get_classification(self, category: str) -> str:
        """Get data classification"""
        classifications = {
            'user_data': 'Confidential',
            'financial_records': 'Restricted',
            'logs': 'Internal',
            'audit_logs': 'Restricted'
        }
        return classifications.get(category, 'Internal')
```

-----

## Audit Logging

```python
import hashlib
import json
import threading

class ComplianceAuditLogger:
    """Immutable audit logger for compliance"""
    
    def __init__(self, log_store=None):
        self.logs = []
        self.log_lock = threading.Lock()
        self.log_store = log_store
    
    def log_event(self, event_type: str, user_id: str, 
                 resource: str, action: str, 
                 result: str, metadata: Dict = None):
        """Create immutable audit log entry"""
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'resource': resource,
            'action': action,
            'result': result,
            'metadata': metadata or {},
            'sequence_number': len(self.logs) + 1
        }
        
        # Add integrity hash
        entry['hash'] = self._calculate_hash(entry)
        
        # Add previous hash for chain
        if self.logs:
            entry['previous_hash'] = self.logs[-1]['hash']
        else:
            entry['previous_hash'] = 'genesis'
        
        with self.log_lock:
            self.logs.append(entry)
        
        # Write to secure storage
        if self.log_store:
            self._write_to_secure_storage(entry)
        
        return entry
    
    def _calculate_hash(self, entry: Dict) -> str:
        """Calculate hash for integrity verification"""
        
        # Create copy without hash field
        entry_copy = {k: v for k, v in entry.items() if k != 'hash'}
        content = json.dumps(entry_copy, sort_keys=True)
        
        return hashlib.sha256(content.encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        """Verify log integrity"""
        
        for i, entry in enumerate(self.logs):
            # Verify hash
            expected_hash = self._calculate_hash(entry)
            if entry['hash'] != expected_hash:
                return False
            
            # Verify chain
            if i > 0:
                if entry['previous_hash'] != self.logs[i-1]['hash']:
                    return False
        
        return True
    
    def query_logs(self, start_time: datetime = None,
                  end_time: datetime = None,
                  user_id: str = None,
                  event_type: str = None,
                  resource: str = None) -> List[Dict]:
        """Query audit logs with filters"""
        
        results = self.logs
        
        if start_time:
            results = [e for e in results 
                      if datetime.fromisoformat(e['timestamp']) >= start_time]
        
        if end_time:
            results = [e for e in results 
                      if datetime.fromisoformat(e['timestamp']) <= end_time]
        
        if user_id:
            results = [e for e in results if e['user_id'] == user_id]
        
        if event_type:
            results = [e for e in results if e['event_type'] == event_type]
        
        if resource:
            results = [e for e in results if e['resource'] == resource]
        
        return results
    
    def generate_audit_report(self, start_date: datetime, 
                            end_date: datetime) -> Dict:
        """Generate compliance audit report"""
        
        logs = self.query_logs(start_time=start_date, end_time=end_date)
        
        # Summarize by event type
        event_counts = {}
        for log in logs:
            event_type = log['event_type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Summarize by user
        user_activity = {}
        for log in logs:
            user = log['user_id']
            user_activity[user] = user_activity.get(user, 0) + 1
        
        return {
            'report_period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'total_events': len(logs),
            'event_type_counts': event_counts,
            'top_users': sorted(user_activity.items(), 
                              key=lambda x: x[1], reverse=True)[:10],
            'integrity_verified': self.verify_integrity()
        }
```
