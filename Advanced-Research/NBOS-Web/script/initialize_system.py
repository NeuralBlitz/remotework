#!/usr/bin/env python3
"""
System initialization script.
Sets up NBOS with default configuration and verification.
"""

import sys
import logging
import asyncio
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def initialize_nbos():
    """Initialize NBOS system"""
    logger.info("=" * 60)
    logger.info("Initializing NBOS: NeuralBlitz Operating System")
    logger.info("=" * 60)
    
    try:
        # Import core modules
        from core import ModuleConfig, ModuleRegistry
        from synergy_engine.core import SynergyEngine
        from charter.charter import CharterLayer
        from governance.bias_detection import BiasDetectionModule
        from governance.privacy_preservation import PrivacyPreservationModule
        
        logger.info("✓ Core modules imported successfully")
        
        # Initialize Synergy Engine
        engine_config = ModuleConfig(
            name="synergy_engine_primary",
            version="1.0.0",
            governance_level="strict",
            audit_enabled=True
        )
        
        synergy = SynergyEngine(engine_config)
        registry = ModuleRegistry()
        registry.create_and_register(engine_config, SynergyEngine)
        
        logger.info("✓ Synergy Engine initialized")
        logger.info("✓ Module Registry active")
        
        # Verify charter compliance
        charter = CharterLayer()
        test_output = "This is a test output with confidence level 0.85"
        verification = await charter.verify_output(test_output, {})
        
        logger.info("✓ Charter Layer operational")
        logger.info(f"  - NO_DECEPTION: {verification.principle_results.get('no_deception')}")
        logger.info(f"  - HUMAN_DIGNITY: {verification.principle_results.get('human_dignity')}")
        logger.info(f"  - FAIRNESS: {verification.principle_results.get('fairness')}")
        logger.info(f"  - TRANSPARENCY: {verification.principle_results.get('transparency')}")
        logger.info(f"  - SAFETY: {verification.principle_results.get('safety')}")
        
        # Verify governance modules
        bias_module = BiasDetectionModule()
        logger.info("✓ Bias Detection Module initialized")
        
        privacy_module = PrivacyPreservationModule()
        logger.info("✓ Privacy Preservation Module initialized")
        
        # Run test processing
        test_input = {
            'feature1': 0.5,
            'feature2': 0.75,
            'feature3': 0.3
        }
        
        test_context = {
            'task_id': 'test_001',
            'demographics': {'race': 'majority', 'gender': 'male'},
            'apply_dp': False
        }
        
        result = await synergy.process(test_input, test_context)
        logger.info(f"✓ Test processing successful")
        logger.info(f"  - Prediction: {result['prediction']:.2f}")
        logger.info(f"  - Charter Verified: {result['charter_verified']}")
        logger.info(f"  - Confidence: {result['explanation_detail']['confidence']:.2f}")
        
        # System status
        status = synergy.get_system_status()
        logger.info("✓ System Status Report:")
        logger.info(f"  - Alignment Score: {status['state']['alignment_score']:.2f}")
        logger.info(f"  - Active Tasks: {status['active_tasks']}")
        logger.info(f"  - Audit Entries: {len(synergy.audit_log)}")
        
        logger.info("=" * 60)
        logger.info("NBOS initialization SUCCESSFUL")
        logger.info("System ready for generative tasks")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Initialization failed: {e}", exc_info=True)
        return False


if __name__ == '__main__':
    success = asyncio.run(initialize_nbos())
    sys.exit(0 if success else 1)
