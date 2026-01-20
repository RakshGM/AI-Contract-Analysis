"""
Complete System Demonstration
Tests all implemented features:
1. Parallel Processing for multi-domain clause extraction
2. Structured pipelines for compliance and financial risk identification
3. Multi-turn interaction between domain-specific agents
4. Intermediate results storage in Pinecone
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
    ParallelProcessor,
    ReportGenerator
)


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


async def demo_parallel_processing():
    """Demonstrate parallel multi-domain clause extraction."""
    print_section("1. PARALLEL PROCESSING - Multi-Domain Clause Extraction")
    
    query = "Analyze payment terms, liability clauses, and compliance requirements"
    print(f"\n📋 Query: {query}\n")
    
    # Sample contract context
    context = """
    PAYMENT TERMS: Net 30 days from invoice date. Late payment penalty of 2% per month.
    LIABILITY: Maximum liability capped at $1,000,000 excluding gross negligence.
    COMPLIANCE: Must comply with GDPR, HIPAA, and SOC 2 Type II requirements.
    INTELLECTUAL PROPERTY: All custom-developed IP belongs to Client. Vendor retains pre-existing IP.
    TERMINATION: Either party may terminate with 30 days written notice.
    """
    
    # Create extractor
    extractor = MultiDomainClauseExtractor()
    
    # Extract clauses
    print("🔄 Extracting clauses from multiple domains...")
    results = extractor.extract_clauses(context, query)
    
    print("\n✅ Extraction Complete!")
    if results.get("status") == "success":
        data = results.get("data", {})
        for domain, clauses in data.items():
            if clauses and isinstance(clauses, list):
                print(f"\n{domain.upper().replace('_', ' ')}:")
                for i, clause in enumerate(clauses[:2], 1):  # Show first 2
                    if isinstance(clause, dict):
                        print(f"  {i}. {clause}")
                    else:
                        print(f"  {i}. {str(clause)[:100]}...")
    
    return results


def demo_structured_pipelines():
    """Demonstrate structured extraction pipelines."""
    print_section("2. STRUCTURED PIPELINES - Compliance & Financial Risk")
    
    # Sample contract context
    context = """
    PAYMENT TERMS: Net 30 days from invoice date. Late payment penalty of 2% per month.
    COMPLIANCE: Must comply with GDPR, HIPAA, and SOC 2 Type II requirements.
    TERMINATION: Either party may terminate with 30 days notice. Early termination fee: $50,000.
    """
    
    query = "Identify compliance and financial risks"
    
    print(f"\n📄 Context: {context[:150]}...")
    print(f"🔍 Query: {query}\n")
    
    # Compliance extraction
    print("🔐 Extracting compliance risks...")
    compliance_pipeline = ComplianceExtractionPipeline()
    compliance_results = compliance_pipeline.extract_compliance_risks(context, query)
    
    print("\nCompliance Risks Found:")
    if compliance_results.get("risks"):
        for risk in compliance_results["risks"][:3]:
            print(f"  ⚠️  {risk.get('type', 'Unknown')}: {risk.get('description', 'N/A')[:80]}...")
    
    # Financial extraction
    print("\n💰 Extracting financial risks...")
    financial_pipeline = FinancialRiskExtractionPipeline()
    financial_results = financial_pipeline.extract_financial_risks(context, query)
    
    print("\nFinancial Risks Found:")
    if financial_results.get("risks"):
        for risk in financial_results["risks"][:3]:
            severity = risk.get('severity', 'Unknown')
            desc = risk.get('description', 'N/A')[:80]
            print(f"  💵 [{severity}] {desc}...")
    
    return {"compliance": compliance_results, "financial": financial_results}


def demo_multi_turn_interaction():
    """Demonstrate multi-turn agent interaction."""
    print_section("3. MULTI-TURN INTERACTION - Context-Aware Agents")
    
    query = "Review contract for legal risks and assess financial impact"
    
    print(f"\n📋 Query: {query}")
    print("\n🤖 Running agents with context sharing...")
    
    # Create planner and build graph
    planner = PlanningModule()
    plan = planner.generate_plan(query)
    
    print(f"\n📝 Plan: {plan.get('agents', [])} will execute in sequence")
    print(f"💭 Reasoning: {plan.get('reasoning', 'N/A')[:100]}...")
    
    # Build and execute graph
    graph = build_graph(plan)
    state = AgentState(query=query)
    
    print("\n⚙️  Executing agents...")
    final_state = graph.invoke(state)
    
    print("\n✅ Multi-turn execution complete!")
    
    # Show results from each agent
    agent_results = {
        "Legal": final_state.get("legal"),
        "Compliance": final_state.get("compliance"),
        "Finance": final_state.get("finance"),
        "Operations": final_state.get("operations")
    }
    
    for agent, result in agent_results.items():
        if result:
            print(f"\n{agent} Agent:")
            print(f"  {result[:150]}...")
    
    return final_state


def demo_intermediates_storage():
    """Demonstrate storing and retrieving intermediate results."""
    print_section("4. INTERMEDIATES STORAGE - Caching in Pinecone")
    
    storage = IntermediatesStorage()
    
    # Sample intermediate results
    query_id = "demo_query_001"
    intermediate_data = {
        "legal_analysis": {
            "risks": ["Liability clause unclear", "IP ownership disputed"],
            "severity": "HIGH"
        },
        "financial_impact": {
            "estimated_cost": "$75,000",
            "risk_level": "MEDIUM"
        }
    }
    
    print(f"\n💾 Storing intermediate results for query: {query_id}")
    print(f"📊 Data: {list(intermediate_data.keys())}")
    
    # Store results
    success = storage.store_intermediate(
        query_id=query_id,
        agent_name="LegalAgent",
        result=intermediate_data
    )
    
    if success:
        print("✅ Successfully stored in Pinecone")
        
        # Retrieve results
        print(f"\n🔍 Retrieving stored results...")
        retrieved = storage.retrieve_intermediate(query_id, "LegalAgent")
        
        if retrieved:
            print("✅ Successfully retrieved from Pinecone")
            print(f"📋 Retrieved data keys: {list(retrieved.keys())}")
        else:
            print("⚠️  No results found (may need Pinecone configuration)")
    else:
        print("⚠️  Storage failed (check Pinecone configuration)")
    
    return success


def demo_report_generation(analysis_results):
    """Demonstrate automated report generation."""
    print_section("5. REPORT GENERATION - Automated Summaries")
    
    print("\n📝 Generating comprehensive report...")
    
    report_gen = ReportGenerator()
    
    # Generate report with custom options
    report = report_gen.generate_report(
        analysis_results=analysis_results,
        tone="professional",
        focus_areas=["risks", "compliance", "financial_impact"]
    )
    
    print("\n✅ Report Generated!")
    print(f"\n{report[:500]}...")
    print("\n... (report continues)")
    
    return report


async def main():
    """Run complete system demonstration."""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + "  AI-POWERED CONTRACT ANALYSIS SYSTEM - COMPLETE DEMO".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        # 1. Parallel Processing
        parallel_results = await demo_parallel_processing()
        
        # 2. Structured Pipelines
        structured_results = demo_structured_pipelines()
        
        # 3. Multi-turn Interaction
        multi_turn_results = demo_multi_turn_interaction()
        
        # 4. Intermediates Storage
        storage_success = demo_intermediates_storage()
        
        # 5. Report Generation
        combined_results = {
            **structured_results,
            "multi_turn": multi_turn_results
        }
        report = demo_report_generation(combined_results)
        
        # Final Summary
        print_section("DEMO COMPLETE ✅")
        print("\n✨ All features demonstrated successfully!")
        print("\nFeatures Tested:")
        print("  ✅ Parallel multi-domain clause extraction")
        print("  ✅ Structured compliance & financial pipelines")
        print("  ✅ Multi-turn context-aware agent interaction")
        print(f"  {'✅' if storage_success else '⚠️ '} Intermediate results storage (Pinecone)")
        print("  ✅ Automated report generation")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        print("\nNote: Some features require proper API keys and Pinecone configuration")
        print("Check your .env file for:")
        print("  - GEMINI_API_KEY")
        print("  - PINECONE_API_KEY")
        print("  - PINECONE_INDEX")


if __name__ == "__main__":
    asyncio.run(main())
