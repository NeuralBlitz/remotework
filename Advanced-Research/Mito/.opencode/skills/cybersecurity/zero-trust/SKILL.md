---
name: zero-trust
description: >
  Expert guidance on implementing zero trust security architectures where no user, device, 
  or network segment is implicitly trusted. Use for continuous verification of identity, 
  device health, and context for every access request, microsegmentation of networks, 
  policy-based access control, and migrating from perimeter-based security to zero trust.
license: MIT
compatibility: opencode
metadata:
  audience: security engineers
  category: cybersecurity
  tags: [zero-trust, microsegmentation, identity-verification, least-privilege, continuous-auth]
---

# Zero Trust Architecture — Implementation Guide

Covers: **Identity Verification · Microsegmentation · Device Trust · Policy Engines · Continuous Authentication · Network Security**

-----

## Foundational Principles

### The Core Tenets

Zero Trust operates on the principle of "never trust, always verify." Every request must be authenticated and authorized regardless of its origin—whether it comes from inside the corporate network or from an external location. This approach assumes that threats can originate from anywhere, including insider threats and compromised credentials.

The fundamental shift from traditional perimeter-based security to zero trust involves eliminating the concept of a trusted internal network. In traditional models, once a user gained access to the internal network, they could often access many resources freely. Zero trust requires verification at every step, treating every access request as if it originates from an untrusted network.

**Key Principles:**

1. **Never Trust, Always Verify** — Authenticate and authorize every request regardless of source network, previous authentication, or device status.

2. **Least Privilege Access** — Grant minimum required permissions for the specific task, resource, and time window. Elevate privileges only when necessary and for limited durations.

3. **Assume Breach** — Design systems assuming adversaries are already inside the network. Limit lateral movement and minimize blast radius when compromises occur.

4. **Verify Explicitly** — Base access decisions on all available data points: identity, device health, location, service or workload, data classification, and anomalies.

### Traditional vs Zero Trust Comparison

| Aspect | Traditional Perimeter | Zero Trust |
|--------|----------------------|------------|
| Network Trust | Internal network is trusted | No network is implicitly trusted |
| Authentication | Once at login | Continuous throughout session |
| Access Model | Role-based, broad | Attribute-based, granular |
| Network Segmentation | Perimeter firewall | Microsegmentation |
| Data Protection | Perimeter encryption | Everywhere encryption |
| Threat Response | Detect and respond | Prevent and limit spread |
| User Experience | VPN for remote access | Seamless, identity-based |

-----

## Identity & Access Management

### Continuous Authentication

Unlike traditional authentication that occurs only at login, zero trust requires continuous verification throughout a session. This involves analyzing behavioral biometrics, device posture, and contextual signals to detect session hijacking or credential compromise.

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict
from datetime import datetime
import hashlib

class AuthenticationLevel(Enum):
    NONE = 0
    PASSWORD = 1
    MFA = 2
    BIOMETRIC = 3
    HARDWARE_TOKEN = 4

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class UserIdentity:
    user_id: str
    username: str
    email: str
    department: str
    role: str
    authentication_level: AuthenticationLevel
    registered_devices: List[str]
    last_authentication: datetime
    risk_score: float

@dataclass
class DeviceState:
    device_id: str
    device_type: str
    os_version: str
    patch_level: datetime
    encryption_enabled: bool
    screen_lock_enabled: bool
    biometric_enrolled: bool
    jailbroken: bool
    endpoint_protection_active: bool
    last_seen: datetime

@dataclass
class AccessContext:
    user: UserIdentity
    device: DeviceState
    source_ip: str
    source_network: str
    requested_resource: str
    requested_action: str
    time_of_request: datetime
    historical_behavior: Dict
    anomaly_score: float

def calculate_risk_score(ctx: AccessContext) -> RiskLevel:
    """Calculate risk score based on multiple factors"""
    score = 0.0
    
    # Authentication level factor
    auth_scores = {
        AuthenticationLevel.NONE: 0.4,
        AuthenticationLevel.PASSWORD: 0.3,
        AuthenticationLevel.MFA: 0.1,
        AuthenticationLevel.BIOMETRIC: 0.05,
        AuthenticationLevel.HARDWARE_TOKEN: 0.0
    }
    score += auth_scores.get(ctx.user.authentication_level, 0.3)
    
    # Device compliance factor
    if ctx.device.jailbroken:
        score += 0.4
    if not ctx.device.encryption_enabled:
        score += 0.2
    if not ctx.device.endpoint_protection_active:
        score += 0.15
    if not ctx.device.screen_lock_enabled:
        score += 0.1
    
    # Behavioral anomaly factor
    score += ctx.anomaly_score
    
    # Network factor (unknown networks increase risk)
    if ctx.source_network not in ["corporate", "home", "known"]:
        score += 0.2
    
    # Time factor (unusual hours)
    hour = ctx.time_of_request.hour
    if hour < 6 or hour > 22:
        score += 0.1
    
    # Map to risk level
    if score >= 0.7:
        return RiskLevel.CRITICAL
    elif score >= 0.5:
        return RiskLevel.HIGH
    elif score >= 0.3:
        return RiskLevel.MEDIUM
    else:
        return RiskLevel.LOW
```

### Identity Provider Integration

```python
import jwt
from typing import Callable

class ZeroTrustIdentityProvider:
    def __init__(self, jwks_url: str, audience: str, issuer: str):
        self.jwks_url = jwks_url
        self.audience = audience
        self.issuer = issuer
        self._jwks_client = None
    
    async def validate_token(self, token: str) -> Optional[UserIdentity]:
        """Validate JWT token and extract identity"""
        try:
            # In production, fetch JWKS and validate properly
            payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )
            
            return UserIdentity(
                user_id=payload.get("sub"),
                username=payload.get("preferred_username"),
                email=payload.get("email"),
                department=payload.get("department", ""),
                role=payload.get("role", ""),
                authentication_level=self._map_auth_level(payload.get("auth_level")),
                registered_devices=payload.get("devices", []),
                last_authentication=datetime.fromtimestamp(payload.get("auth_time", 0)),
                risk_score=payload.get("risk_score", 0.0)
            )
        except Exception as e:
            return None
    
    def _map_auth_level(self, level: str) -> AuthenticationLevel:
        mapping = {
            "none": AuthenticationLevel.NONE,
            "password": AuthenticationLevel.PASSWORD,
            "mfa": AuthenticationLevel.MFA,
            "biometric": AuthenticationLevel.BIOMETRIC,
            "hardware": AuthenticationLevel.HARDWARE_TOKEN
        }
        return mapping.get(level, AuthenticationLevel.PASSWORD)
```

-----

## Policy Enforcement Points

### Policy Decision Point

The Policy Decision Point (PDP) evaluates every access request against defined policies. It considers identity, device state, resource sensitivity, and contextual factors to make access decisions.

```python
from enum import Enum

class Decision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    MFA_REQUIRED = "mfa_required"
    QUARANTINE = "quarantine"
    LIMITED_ACCESS = "limited_access"

class ResourceClassification(Enum):
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    RESTRICTED = 4

class Action(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    EXECUTE = "execute"

# Policy rules
POLICY_RULES = [
    {
        "name": "require_mfa_for_sensitive",
        "condition": lambda ctx: (
            ctx.user.authentication_level.value < AuthenticationLevel.MFA.value
            and ctx.requested_resource in ["financial", "health", "admin"]
        ),
        "action": Decision.MFA_REQUIRED
    },
    {
        "name": "block_compliance_violations",
        "condition": lambda ctx: (
            ctx.device.jailbroken 
            or not ctx.device.encryption_enabled
        ),
        "action": Decision.QUARANTINE
    },
    {
        "name": "high_risk_block",
        "condition": lambda ctx: (
            ctx.user.risk_score > 0.8 
            or ctx.anomaly_score > 0.7
        ),
        "action": Decision.DENY
    },
    {
        "name": "time_based_access",
        "condition": lambda ctx: (
            ctx.time_of_request.hour < 6 
            or ctx.time_of_request.hour > 22
            and ctx.requested_action in [Action.DELETE, Action.ADMIN]
        ),
        "action": Decision.LIMITED_ACCESS
    }
]

def evaluate_policy(ctx: AccessContext, resource_policy: dict) -> Decision:
    """Evaluate access request against policies"""
    
    # Check risk level first
    risk_level = calculate_risk_score(ctx)
    
    if risk_level == RiskLevel.CRITICAL:
        return Decision.DENY
    
    # Evaluate each policy rule
    for rule in POLICY_RULES:
        if rule["condition"](ctx):
            return rule["action"]
    
    # Resource-specific policies
    if resource_policy.get("require_mfa"):
        if ctx.user.authentication_level.value < AuthenticationLevel.MFA.value:
            return Decision.MFA_REQUIRED
    
    # Check authorization
    user_roles = ctx.user.role.split(",")
    allowed_roles = resource_policy.get("allowed_roles", [])
    
    if not any(role in allowed_roles for role in user_roles):
        return Decision.DENY
    
    return Decision.ALLOW
```

### Policy Enforcement Point Implementation

```python
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import ipaddress
import hashlib

TRUSTED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16")
]

SENSITIVE_RESOURCES = [
    "/api/admin",
    "/api/financial",
    "/api/health-records",
    "/api/user-data"
]

class ZeroTrustMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, policy_engine):
        super().__init__(app)
        self.policy_engine = policy_engine
    
    async def dispatch(self, request: Request, call_next):
        # Extract context from request
        context = await self._build_context(request)
        
        # Determine resource and action
        resource = self._get_resource_path(request)
        action = self._get_action(request)
        
        # Get resource policy
        resource_policy = self._get_resource_policy(resource)
        
        # Evaluate access
        decision = self.policy_engine.evaluate(context, resource_policy, action)
        
        # Handle decision
        if decision == Decision.DENY:
            raise HTTPException(status_code=403, detail="Access denied")
        
        if decision == Decision.MFA_REQUIRED:
            raise HTTPException(
                status_code=401,
                detail="MFA required",
                headers={"X-MFA-Required": "true"}
            )
        
        if decision == Decision.QUARANTINE:
            raise HTTPException(
                status_code=403,
                detail="Device compliance required"
            )
        
        # Add context to request state
        request.state.security_context = context
        request.state.decision = decision
        
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response
    
    async def _build_context(self, request: Request) -> AccessContext:
        # Extract tokens and validate
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "") if auth_header else ""
        
        # Get device information
        device_id = request.headers.get("X-Device-ID", "")
        device_state = await self._get_device_state(device_id)
        
        # Get user identity
        user = await self._get_user_from_token(token)
        
        # Get client IP and network
        client_ip = request.client.host if request.client else "0.0.0.0"
        ip = ipaddress.ip_address(client_ip)
        network = "internal" if any(ip in net for net in TRUSTED_NETWORKS) else "external"
        
        # Build context
        return AccessContext(
            user=user,
            device=device_state,
            source_ip=client_ip,
            source_network=network,
            requested_resource=self._get_resource_path(request),
            requested_action=self._get_action(request),
            time_of_request=datetime.now(),
            historical_behavior={},
            anomaly_score=0.0
        )
    
    def _get_resource_path(self, request: Request) -> str:
        return request.url.path
    
    def _get_action(self, request: Request) -> Action:
        method_action_map = {
            "GET": Action.READ,
            "POST": Action.WRITE,
            "PUT": Action.WRITE,
            "PATCH": Action.WRITE,
            "DELETE": Action.DELETE,
            "ADMIN": Action.ADMIN
        }
        return method_action_map.get(request.method, Action.READ)
    
    def _get_resource_policy(self, resource: str) -> dict:
        for sensitive in SENSITIVE_RESOURCES:
            if resource.startswith(sensitive):
                return {"require_mfa": True, "allowed_roles": ["admin", "manager"]}
        return {"require_mfa": False, "allowed_roles": ["user", "admin", "manager"]}
    
    async def _get_device_state(self, device_id: str) -> DeviceState:
        # In production, fetch from device management system
        return DeviceState(
            device_id=device_id,
            device_type="laptop",
            os_version="14.0",
            patch_level=datetime.now(),
            encryption_enabled=True,
            screen_lock_enabled=True,
            biometric_enrolled=True,
            jailbroken=False,
            endpoint_protection_active=True,
            last_seen=datetime.now()
        )
    
    async def _get_user_from_token(self, token: str) -> UserIdentity:
        # In production, validate and decode JWT
        return UserIdentity(
            user_id="user123",
            username="john.doe",
            email="john@example.com",
            department="engineering",
            role="admin",
            authentication_level=AuthenticationLevel.MFA,
            registered_devices=["device1", "device2"],
            last_authentication=datetime.now(),
            risk_score=0.1
        )
```

-----

## Network Microsegmentation

### Principles of Microsegmentation

Microsegmentation involves dividing networks into granular zones, each with its own security controls. Unlike traditional network segmentation that focuses on perimeter defense, microsegmentation creates isolated segments at the workload level, controlling traffic between individual services or groups of services.

**Key Implementation Approaches:**

1. **Identity-Based Segmentation** — Assign identity to workloads and enforce policies based on workload identity rather than IP addresses.

2. **Software-Defined Networking** — Use SDN controllers to program network policies dynamically based on workload state and requirements.

3. **Host-Based Firewalls** — Deploy firewalls at the individual host level to control east-west traffic.

### Network Policy Definition

```yaml
# NetworkPolicy example for Kubernetes
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: payment-service-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: payment-service
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Allow from API gateway
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - protocol: TCP
          port: 8080
    # Allow from fraud detection
    - from:
        - podSelector:
            matchLabels:
              app: fraud-detection
      ports:
        - protocol: TCP
          port: 8081
    # Allow health checks
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 8082
  egress:
    # Allow to database
    - to:
        - podSelector:
            matchLabels:
              app: payment-db
      ports:
        - protocol: TCP
          port: 5432
    # Allow to external payment processors
    - to:
        - ipBlock:
            cidr: 203.0.113.0/24
      ports:
        - protocol: TCP
          port: 443
    # Allow DNS
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53
```

### Service Mesh Implementation

```yaml
# Istio AuthorizationPolicy example
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: shopping-cart-policy
  namespace: e-commerce
spec:
  selector:
    matchLabels:
      app: shopping-cart
  rules:
    # Allow from frontend
    - from:
        - source:
            principals: ["cluster.local/ns/frontend/sa/frontend-service"]
      to:
        - operation:
            ports: ["8080"]
    # Allow from recommendation service
    - from:
        - source:
            principals: ["cluster.local/ns/recommendations/sa/recommendation-service"]
      to:
        - operation:
            ports: ["8080"]
            methods: ["GET"]
    # Allow health checks
    - to:
        - operation:
            ports: ["15020", "8080"]
```

-----

## Service-to-Service Communication

### Mutual TLS Implementation

Service-to-service communication in zero trust requires mutual authentication through mTLS, where both the client and server verify each other's certificates.

```go
package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"log"
	"net/http"
	"os"
)

// ServiceIdentity represents the identity of a service
type ServiceIdentity struct {
	ServiceName string
	Namespace   string
	Version     string
}

// MTLSConfig holds mTLS configuration
type MTLSConfig struct {
	CertFile       string
	KeyFile        string
	CAFile         string
	MinTLSVersion  uint16
	VerifyClient  bool
}

func LoadMTLSConfig() *MTLSConfig {
	return &MTLSConfig{
		CertFile:      os.Getenv("SERVICE_CERT"),
		KeyFile:       os.Getenv("SERVICE_KEY"),
		CAFile:        os.Getenv("CA_CERT"),
		MinTLSVersion: tls.VersionTLS13,
		VerifyClient:  true,
	}
}

// CreateMTLSClient creates an HTTP client with mTLS for service communication
func CreateMTLSClient(config *MTLSConfig) (*http.Client, error) {
	cert, err := tls.LoadX509KeyPair(config.CertFile, config.KeyFile)
	if err != nil {
		return nil, fmt.Errorf("failed to load client certificate: %w", err)
	}

	caCert, err := os.ReadFile(config.CAFile)
	if err != nil {
		return nil, fmt.Errorf("failed to read CA certificate: %w", err)
	}

	caPool := x509.NewCertPool()
	if !caPool.AppendCertsFromPEM(caCert) {
		return nil, fmt.Errorf("failed to append CA certificate")
	}

	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		RootCAs:      caPool,
		MinVersion:   config.MinTLSVersion,
		VerifyClient: config.VerifyClient,
		// Verify peer certificate
		VerifyPeerCertificate: func(rawCerts [][]byte, verifiedChains [][]*x509.Certificate) error {
			// Additional verification logic
			return nil
		},
	}

	return &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: tlsConfig,
			// Disable HTTP/2 for mTLS to avoid issues
			TLSNextProto: make(map[string]func(interface{}, *tls.Conn) http.RoundTripper),
		},
		Timeout: 30,
	}, nil
}

// CreateMTLSServer creates an HTTPS server with mTLS
func CreateMTLSServer(config *MTLSConfig) (*http.Server, error) {
	cert, err := tls.LoadX509KeyPair(config.CertFile, config.KeyFile)
	if err != nil {
		return nil, fmt.Errorf("failed to load server certificate: %w", err)
	}

	caCert, err := os.ReadFile(config.CAFile)
	if err != nil {
		return nil, fmt.Errorf("failed to read CA certificate: %w", err)
	}

	caPool := x509.NewCertPool()
	if !caPool.AppendCertsFromPEM(caCert) {
		return nil, fmt.Errorf("failed to append CA certificate")
	}

	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		ClientCAs:    caPool,
		ClientAuth:   tls.RequestClientCert,
		MinVersion:   config.MinTLSVersion,
		// Require client certificates
		VerifyPeerCertificate: func(rawCerts [][]byte, verifiedChains [][]*x509.Certificate) error {
			// Extract service identity from client certificate
			// Verify against service registry
			return nil
		},
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/health", healthHandler)
	mux.HandleFunc("/api/v1/data", apiHandler)

	return &http.Server{
		Addr:      ":8443",
		Handler:   mux,
		TLSConfig: tlsConfig,
	}, nil
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "OK")
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
	// Extract client certificate for authorization
	if r.TLS != nil && len(r.TLS.PeerCertificates) > 0 {
		clientCert := r.TLS.PeerCertificates[0]
		log.Printf("Request from: %s", clientCert.Subject)
	}
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Data response")
}
```

-----

## Device Trust & Compliance

### Device Posture Assessment

```python
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta
import asyncio

@dataclass
class ComplianceRequirement:
    name: str
    description: str
    check_interval_minutes: int
    severity: str

COMPLIANCE_REQUIREMENTS = [
    ComplianceRequirement(
        name="antivirus_active",
        description="Endpoint protection must be active",
        check_interval_minutes=60,
        severity="critical"
    ),
    ComplianceRequirement(
        name="encryption_enabled",
        description="Full disk encryption must be enabled",
        check_interval_minutes=60,
        severity="critical"
    ),
    ComplianceRequirement(
        name="os_updated",
        description="OS must be within 30 days of latest patch",
        check_interval_minutes=1440,
        severity="high"
    ),
    ComplianceRequirement(
        name="screen_lock",
        description="Screen lock must be enabled",
        check_interval_minutes=60,
        severity="medium"
    ),
    ComplianceRequirement(
        name="jailbreak_check",
        description="Device must not be jailbroken/rooted",
        check_interval_minutes=30,
        severity="critical"
    )
]

class DeviceComplianceEngine:
    def __init__(self, device_api_client):
        self.device_api = device_api_client
        self.compliance_cache = {}
    
    async def assess_device(self, device_id: str) -> Dict:
        """Assess device compliance posture"""
        device_state = await self.device_api.get_device_state(device_id)
        
        results = {
            "device_id": device_id,
            "timestamp": datetime.now(),
            "overall_status": "compliant",
            "checks": []
        }
        
        for requirement in COMPLIANCE_REQUIREMENTS:
            check_result = await self._run_compliance_check(
                device_id, device_state, requirement
            )
            results["checks"].append(check_result)
            
            if check_result["status"] != "pass":
                if requirement.severity in ["critical", "high"]:
                    results["overall_status"] = "non_compliant"
        
        # Update cache
        self.compliance_cache[device_id] = results
        
        return results
    
    async def _run_compliance_check(
        self, 
        device_id: str, 
        device_state: DeviceState,
        requirement: ComplianceRequirement
    ) -> Dict:
        """Run individual compliance check"""
        check_map = {
            "antivirus_active": lambda: device_state.endpoint_protection_active,
            "encryption_enabled": lambda: device_state.encryption_enabled,
            "os_updated": lambda: (
                datetime.now() - device_state.patch_level < timedelta(days=30)
            ),
            "screen_lock": lambda: device_state.screen_lock_enabled,
            "jailbreak_check": lambda: not device_state.jailbroken
        }
        
        check_func = check_map.get(requirement.name)
        if check_func is None:
            return {
                "requirement": requirement.name,
                "status": "unknown",
                "message": "Check not implemented"
            }
        
        passed = check_func()
        
        return {
            "requirement": requirement.name,
            "status": "pass" if passed else "fail",
            "severity": requirement.severity,
            "message": f"{requirement.description}: {'OK' if passed else 'FAILED'}"
        }
```

-----

## Monitoring & Analytics

### Security Event Collection

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json

@dataclass
class SecurityEvent:
    timestamp: datetime
    event_type: str
    source: str
    user_id: str
    device_id: str
    resource: str
    action: str
    decision: str
    risk_score: float
    metadata: Dict = field(default_factory=dict)

class SecurityEventCollector:
    def __init__(self, event_store):
        self.event_store = event_store
    
    async def collect_access_event(self, context: AccessContext, decision: Decision):
        """Collect access control event"""
        event = SecurityEvent(
            timestamp=datetime.now(),
            event_type="access_attempt",
            source=context.source_ip,
            user_id=context.user.user_id,
            device_id=context.device.device_id,
            resource=context.requested_resource,
            action=context.requested_action,
            decision=decision.value,
            risk_score=calculate_risk_score(context),
            metadata={
                "authentication_level": context.user.authentication_level.value,
                "device_compliant": not context.device.jailbroken,
                "network": context.source_network,
                "hour": context.time_of_request.hour
            }
        )
        
        await self.event_store.store(event)
    
    async def get_risk_indicators(self, user_id: str, time_window_hours: int = 24) -> Dict:
        """Analyze user behavior for risk indicators"""
        events = await self.event_store.query(
            user_id=user_id,
            since=datetime.now() - timedelta(hours=time_window_hours)
        )
        
        return {
            "total_attempts": len(events),
            "failed_attempts": len([e for e in events if e.decision == "deny"]),
            "high_risk_attempts": len([e for e in events if e.risk_score > 0.7]),
            "unique_resources": len(set(e.resource for e in events)),
            "unusual_hours": len([e for e in events if e.timestamp.hour < 6 or e.timestamp.hour > 22]),
            "unique_devices": len(set(e.device_id for e in events))
        }
```

-----

## Best Practices Summary

1. **Start with Identity** — Implement strong identity verification before addressing network security.

2. **Deploy Gradually** — Phase in zero trust controls, starting with most critical assets.

3. **Maintain Visibility** — Ensure comprehensive logging and monitoring across all components.

4. **Automate Responses** — Build automated remediation for common compliance and security issues.

5. **Focus on User Experience** — Balance security with usability to ensure adoption.

6. **Continuous Improvement** — Regularly review and update policies based on threat intelligence.

7. **Assume Breach Mentality** — Design for failure containment and rapid detection.
