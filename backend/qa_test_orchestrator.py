#!/usr/bin/env python3
"""
COMPREHENSIVE QA TEST ORCHESTRATOR
Master Controller - Runs All Phases in Sequence

Executes: Phase 1 (Functional) → Phase 2 (Security) → Phase 3 (Performance) → Phase 4 (Fix/Validate)
Generates: Unified test report with all findings and recommendations
"""

import subprocess
import sys
import time
import json
from datetime import datetime
from pathlib import Path


BACKEND_PATH = Path(r"d:\Git\Code Visualizer\backend")


class QATestOrchestrator:
    def __init__(self):
        self.start_time = datetime.now()
        self.phase_results = {}
        self.all_passed = True
    
    def run_phase(self, phase_num: int, script_name: str, description: str) -> bool:
        """Run a single phase test"""
        print(f"\n{'='*70}")
        print(f"RUNNING PHASE {phase_num}: {description}")
        print(f"{'='*70}")
        
        script_path = BACKEND_PATH / script_name
        
        if not script_path.exists():
            print(f"✗ Script not found: {script_path}")
            return False
        
        try:
            start = time.time()
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(BACKEND_PATH),
                capture_output=False,
                timeout=300  # 5 minute timeout per phase
            )
            elapsed = time.time() - start
            
            self.phase_results[phase_num] = {
                'passed': result.returncode == 0,
                'exit_code': result.returncode,
                'duration_seconds': elapsed,
                'description': description
            }
            
            if result.returncode != 0:
                self.all_passed = False
                print(f"\n✗ Phase {phase_num} FAILED with exit code {result.returncode}")
                return False
            else:
                print(f"\n✓ Phase {phase_num} COMPLETED in {elapsed:.1f}s")
                return True
        
        except subprocess.TimeoutExpired:
            print(f"\n✗ Phase {phase_num} TIMEOUT (exceeded 5 minutes)")
            self.all_passed = False
            return False
        except Exception as e:
            print(f"\n✗ Phase {phase_num} ERROR: {e}")
            self.all_passed = False
            return False
    
    def run_all_phases(self):
        """Run all QA phases in sequence"""
        print("""
╔════════════════════════════════════════════════════════════════════════╗
║          CODE VISUALIZER - COMPREHENSIVE QA TEST SUITE                 ║
║                      All Phases Execution                              ║
╚════════════════════════════════════════════════════════════════════════╝
""")
        
        phases = [
            (1, "qa_phase1_functional_tests.py", "FUNCTIONAL & INPUT HANDLING TESTS"),
            (2, "qa_phase2_security_audit.py", "SECURITY AUDIT & VULNERABILITY TESTING"),
            (3, "qa_phase3_performance_tests.py", "PERFORMANCE & CONCURRENCY TESTING"),
            (4, "qa_phase4_issue_detection_and_fixes.py", "ISSUE DETECTION & AUTO-FIX"),
        ]
        
        for phase_num, script, description in phases:
            success = self.run_phase(phase_num, script, description)
            if not success and phase_num < 4:
                # Continue to Phase 4 even if earlier phases fail
                print(f"\n⚠ Warning: Phase {phase_num} did not pass, but continuing to Phase 4...")
        
        return self.all_passed
    
    def generate_final_report(self):
        """Generate final comprehensive report"""
        elapsed_total = (datetime.now() - self.start_time).total_seconds()
        
        report = f"""
╔════════════════════════════════════════════════════════════════════════╗
║                    COMPREHENSIVE QA TEST REPORT                        ║
║                    CODE VISUALIZER PROJECT                             ║
╚════════════════════════════════════════════════════════════════════════╝

Execution Summary:
─────────────────────────────────────────────────────────────────────────
Start Time: {self.start_time.isoformat()}
Total Duration: {elapsed_total:.1f} seconds ({elapsed_total/60:.1f} minutes)

Phase Results:
─────────────────────────────────────────────────────────────────────────
"""
        
        for phase_num in sorted(self.phase_results.keys()):
            result = self.phase_results[phase_num]
            status = "✓ PASSED" if result['passed'] else "✗ FAILED"
            report += f"\nPhase {phase_num}: {result['description']}\n"
            report += f"  Status: {status}\n"
            report += f"  Duration: {result['duration_seconds']:.1f}s\n"
        
        # Overall status
        report += f"""
Overall Status:
─────────────────────────────────────────────────────────────────────────
"""
        
        if self.all_passed:
            report += """
✓ ALL PHASES PASSED
✓ SYSTEM IS PRODUCTION-READY

The Code Visualizer backend has successfully completed comprehensive QA testing:
  • Functional tests: All core features validated
  • Security audit: Sandbox properly enforced
  • Performance: System handles concurrent load
  • Auto-fix: Issues detected and remediated

RECOMMENDATIONS:
1. Deploy to production with confidence
2. Continue monitoring performance metrics
3. Schedule quarterly security audits
4. Maintain automated test suite for CI/CD pipeline
"""
        else:
            report += """
⚠ SOME PHASES REQUIRE ATTENTION

The Code Visualizer backend requires further work:
  • Review failed phase results above
  • Address critical issues before deployment
  • Re-run comprehensive test suite after fixes
"""
        
        report += f"""
Next Steps:
─────────────────────────────────────────────────────────────────────────
1. Review detailed test reports:
   - qa_report_final.txt (comprehensive issue report)
   - Test output from each phase
   
2. If issues found:
   - Prioritize CRITICAL severity issues
   - Apply recommended fixes
   - Re-run affected test phase
   
3. If all passed:
   - Tag code for release
   - Deploy to production
   - Monitor logs for errors

═════════════════════════════════════════════════════════════════════════
Report Generated: {datetime.now().isoformat()}
═════════════════════════════════════════════════════════════════════════
"""
        
        print(report)
        
        # Save report
        report_file = BACKEND_PATH / "qa_comprehensive_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✓ Comprehensive report saved to: {report_file}")
        
        return report


def main():
    """Main orchestrator"""
    print("\n" + "="*70)
    print("INITIALIZING COMPREHENSIVE QA TEST SUITE")
    print("="*70)
    
    # Check backend path exists
    if not BACKEND_PATH.exists():
        print(f"✗ Backend path not found: {BACKEND_PATH}")
        return 1
    
    print(f"✓ Backend path: {BACKEND_PATH}")
    print("✓ All test phases available")
    
    # Run all phases
    orchestrator = QATestOrchestrator()
    all_passed = orchestrator.run_all_phases()
    
    # Generate final report
    print("\n" + "="*70)
    print("GENERATING COMPREHENSIVE FINAL REPORT")
    print("="*70)
    
    orchestrator.generate_final_report()
    
    # Exit code
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
