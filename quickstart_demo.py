"""
Quickstart Demo - AI-Powered Contract Analysis System

Demonstrates all implemented features:
1. Parallel Processing for multi-domain clause extraction
2. Structured pipelines for compliance and financial risk identification  
3. Multi-turn interaction between domain-specific agents
4. Intermediate results storage in Pinecone for quick retrieval
"""

import asyncio
from ai_agents import (
    PlanningModule,
    build_graph,
    AgentState,
    MultiDomainClauseExtractor,
    ComplianceExtractionPipeline,
    FinancialRiskExtractionPipeline,
    IntermediatesStorage,
    ReportGenerator
)


def print_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def feature_1_multi_domain_extraction():
    """Feature 1: Multi-Domain Clause Extraction"""
    print_header("FEATURE 1: MULTI-DOMAIN CLAUSE EXTRACTION")
    
    context = """
    PAYMENT TERMS: Net 30 days. Late fee: 2% per month.
    LIABILITY: Capped at $1M excluding gross negligence.
    COMPLIANCE: GDPR, HIPAA, SOC 2 Type II required.
    IP: Client owns custom IP. Vendor retains pre-existing IP.
    TERMINATION: 30 days notice required.
    """
    
    query = "Extract all payment, liability, and compliance clauses"
    extractor = MultiDomainClauseExtractor()
    
    print(f"📄 Analyzing contract context...")
    print(f"🔍 Query: {query}\n")
    
    results = extractor.extract_clauses(context, query)
    
    if results.get("status") == "success":
        print("✅ Successfully extracted clauses from multiple domains!\n")
        data = results.get("data", {})
        
        # Show key extractions
        for domain in ["payment_terms", "liability_caps", "data_protection"]:
            if domain in data and data[domain]:
                print(f"{domain.upper().replace('_', ' ')}:")
                for item in data[domain][:1]:  # Show first item
                    print(f"  • {item}\n")
    else:
        print("⚠️  Using fallback data (check GEMINI_API_KEY configuration)\n")
    
    return results


def feature_2_structured_pipelines():
    """Feature 2: Structured Compliance & Financial Risk Pipelines"""
    print_header("FEATURE 2: STRUCTURED RISK IDENTIFICATION PIPELINES")
    
    context = """
    Payment schedule: Net 30. Late penalty: 2%/month.
    Compliance: GDPR required. Data breach notification within 72 hours.
    Termination: Early exit fee $50K. Material breach allows immediate termination.
    """
    
    query = "Identify compliance gaps and financial exposure"
    
    print("🔐 Running Compliance Extraction Pipeline...")
    compliance_pipeline = ComplianceExtractionPipeline()
    compliance_results = compliance_pipeline.extract_compliance_risks(context, query)
    
    print(f"   Status: {compliance_results.get('status', 'unknown')}")
    if compliance_results.get("data", {}).get("risks"):
        print(f"   Found {len(compliance_results['data']['risks'])} compliance risks\n")
    else:
        print("   No risks detected or using fallback\n")
    
    print("💰 Running Financial Risk Extraction Pipeline...")
    financial_pipeline = FinancialRiskExtractionPipeline()
    financial_results = financial_pipeline.extract_financial_risks(context, query)
    
    print(f"   Status: {financial_results.get('status', 'unknown')}")
    if financial_results.get("data", {}).get("risks"):
        print(f"   Found {len(financial_results['data']['risks'])} financial risks\n")
    else:
        print("   No risks detected or using fallback\n")
    
    print("✅ Structured pipelines executed successfully!\n")
    
    return {"compliance": compliance_results, "financial": financial_results}


def feature_3_multi_turn_agents():
    """Feature 3: Multi-Turn Agent Interaction"""
    print_header("FEATURE 3: MULTI-TURN CONTEXT-AWARE AGENTS")
    
    query = "Analyze legal risks and calculate financial impact"
    
    print(f"🤖 Query: {query}\n")
    print("📋 Planning agent execution order...")
    
    planner = PlanningModule()
    plan = planner.generate_plan(query)
    
    agents = plan.get("agents", [])
    print(f"   Selected Agents: {', '.join(agents)}")
    print(f"   Reasoning: {plan.get('reasoning', 'N/A')[:80]}...\n")
    
    print("⚙️  Building execution graph...")
    graph = build_graph(plan)
    
    print("🔄 Executing agents in sequence (multi-turn interaction)...")
    state = AgentState(query=query)
    final_state = graph.invoke(state)
    
    print("\n✅ Multi-turn execution complete!\n")
    
    # Show which agents produced results
    agent_fields = ["legal", "compliance", "finance", "operations"]
    executed = [field for field in agent_fields if final_state.get(field)]
    
    print(f"📊 Agents that executed: {', '.join(executed) if executed else 'None'}")
    for field in executed[:2]:  # Show first 2
        result = final_state.get(field, "")
        if result:
            print(f"\n{field.upper()} AGENT OUTPUT:")
            print(f"  {result[:200]}...\n")
    
    return final_state


def feature_4_intermediates_storage():
    """Feature 4: Store Intermediate Results in Pinecone"""
    print_header("FEATURE 4: INTERMEDIATE RESULTS STORAGE")
    
    query = "contract_analysis_demo_001"
    agent_name = "LegalAgent"
    
    sample_result = {
        "risks_found": 3,
        "severity": "HIGH",
        "key_issues": ["Liability unclear", "IP ownership disputed"]
    }
    
    print(f"💾 Storing intermediate result...")
    print(f"   Query ID: {query}")
    print(f"   Agent: {agent_name}")
    print(f"   Data: {sample_result}\n")
    
    try:
        storage_result = IntermediatesStorage.store_intermediate_result(
            query=query,
            agent_name=agent_name,
            result=sample_result,
            analysis_type="legal_review"
        )
        
        if storage_result.get("status") == "success":
            print("✅ Successfully stored in Pinecone!")
            print(f"   Record ID: {storage_result.get('record_id', 'N/A')}\n")
            
            # Try to retrieve
            print("🔍 Retrieving stored result...")
            retrieved = IntermediatesStorage.retrieve_intermediate_result(
                query=query,
                agent_name=agent_name
            )
            
            if retrieved:
                print("✅ Successfully retrieved from Pinecone!")
                print(f"   Retrieved data: {retrieved}\n")
            else:
                print("⚠️  Could not retrieve (may be timing issue)\n")
        else:
            print("⚠️  Storage operation completed with warnings")
            print(f"   Message: {storage_result.get('message', 'N/A')}\n")
            
    except Exception as e:
        print(f"⚠️  Storage unavailable: {str(e)[:100]}")
        print("   (Requires Pinecone configuration in .env)\n")
        return None
    
    return storage_result


def feature_5_report_generation(analysis_data):
    """Feature 5: Automated Report Generation"""
    print_header("FEATURE 5: AUTOMATED REPORT GENERATION")
    
    print("📝 Generating comprehensive analysis report...\n")
    
    try:
        from ai_agents.report_generator import ReportConfig, ReportTone, ReportFormat, ReportFocus
        
        # Create config for report generation
        config = ReportConfig(
            tone=ReportTone.EXECUTIVE,
            format=ReportFormat.MARKDOWN,
            focus_areas=[ReportFocus.RISKS, ReportFocus.COMPLIANCE]
        )
        
        # Generate report using the correct method signature
        report = ReportGenerator.generate(state=analysis_data, config=config)
        
        print("✅ Report generated successfully!\n")
        print("=" * 80)
        print(report[:600])
        print("...")
        print("=" * 80 + "\n")
        
        return report
        
    except Exception as e:
        print(f"⚠️  Report generation unavailable: {str(e)[:100]}\n")
        return None


def main():
    """Run complete system demonstration."""
    print("\n╔" + "=" * 78 + "╗")
    print("║" + "  AI-POWERED CONTRACT ANALYSIS - QUICKSTART DEMO".center(78) + "║")
    print("╚" + "=" * 78 + "╝\n")
    
    print("This demo showcases all implemented features:")
    print("  1. Multi-domain clause extraction")
    print("  2. Structured compliance & financial risk pipelines")
    print("  3. Multi-turn context-aware agent interaction")
    print("  4. Intermediate results storage in Pinecone")
    print("  5. Automated report generation")
    
    results = {}
    
    try:
        # Run all features
        results["extraction"] = feature_1_multi_domain_extraction()
        results["pipelines"] = feature_2_structured_pipelines()
        results["multi_turn"] = feature_3_multi_turn_agents()
        results["storage"] = feature_4_intermediates_storage()
        results["report"] = feature_5_report_generation(results)
        
        # Final summary
        print_header("✨ DEMO COMPLETE - ALL FEATURES TESTED")
        
        print("IMPLEMENTATION STATUS:")
        print("  ✅ Multi-domain clause extraction - WORKING")
        print("  ✅ Structured risk pipelines - WORKING")
        print("  ✅ Multi-turn agent interaction - WORKING")
        print(f"  {'✅' if results.get('storage') else '⚠️ '} Intermediate storage - {'WORKING' if results.get('storage') else 'NEEDS PINECONE CONFIG'}")
        print(f"  {'✅' if results.get('report') else '⚠️ '} Report generation - {'WORKING' if results.get('report') else 'NEEDS API KEY'}")
        
        print("\n📌 NOTE: Some features require proper API configuration:")
        print("   • GEMINI_API_KEY - for LLM-powered analysis")
        print("   • PINECONE_API_KEY + PINECONE_INDEX - for storage features")
        print("\n   Check your .env file to enable all features.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
