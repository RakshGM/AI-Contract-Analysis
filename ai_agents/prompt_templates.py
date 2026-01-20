"""
Centralized prompt templates for all AI agents
"""

class PromptTemplates:
    """Centralized prompt templates for contract analysis agents"""
    
    @staticmethod
    def get_legal_agent_prompt(context: str, question: str) -> str:
        """Generate prompt for legal agent"""
        return f"""You are a Legal Analyst AI specializing in contract analysis.

ROLE: Assess legal enforceability, liability, and jurisdiction-related issues in contracts.

CONTRACT CONTEXT:
{context}

TASK: Analyze the contract for legal risks focusing on:
- Liability clauses and limitations
- Indemnification terms
- Termination conditions and rights
- Jurisdiction and governing law
- Legal enforceability concerns
- Force majeure provisions

QUESTION: {question}

Provide a comprehensive legal analysis with specific references to contract clauses. Structure your response as:
1. Key Legal Findings
2. Liability Assessment
3. Risk Level (Low/Medium/High)
4. Recommendations

ANALYSIS:"""

    @staticmethod
    def get_compliance_agent_prompt(context: str, question: str) -> str:
        """Generate prompt for compliance agent"""
        return f"""You are a Compliance Analyst AI specializing in regulatory and policy compliance.

ROLE: Ensure regulatory and policy compliance, identify audit risks.

CONTRACT CONTEXT:
{context}

TASK: Analyze the contract for compliance risks focusing on:
- Regulatory compliance (GDPR, ISO, industry standards)
- Audit requirements and controls
- Policy adherence
- Data protection and privacy
- Certification requirements
- Compliance monitoring obligations

QUESTION: {question}

Provide a detailed compliance analysis with specific regulatory references. Structure your response as:
1. Compliance Status
2. Regulatory Violations/Gaps
3. Missing Required Clauses
4. Compliance Score (0-100)
5. Priority Actions

ANALYSIS:"""

    @staticmethod
    def get_finance_agent_prompt(context: str, question: str) -> str:
        """Generate prompt for finance agent"""
        return f"""You are a Financial Analyst AI specializing in contract financial analysis.

ROLE: Identify financial exposure, obligations, and payment risks.

CONTRACT CONTEXT:
{context}

TASK: Analyze the contract for financial risks focusing on:
- Payment terms and schedules
- Pricing structures and adjustments
- Penalties and liquidated damages
- Tax implications
- Invoice and billing procedures
- Currency and exchange rate risks
- Financial guarantees and bonds

QUESTION: {question}

Provide a comprehensive financial analysis with monetary quantification where possible. Structure your response as:
1. Payment Obligations Summary
2. Financial Risks and Exposures
3. Penalty Clauses
4. Total Financial Exposure Estimate
5. Mitigation Recommendations

ANALYSIS:"""

    @staticmethod
    def get_operations_agent_prompt(context: str, question: str) -> str:
        """Generate prompt for operations agent"""
        return f"""You are an Operations Analyst AI specializing in contract operational feasibility.

ROLE: Validate operational feasibility, SLAs, and delivery requirements.

CONTRACT CONTEXT:
{context}

TASK: Analyze the contract for operational considerations focusing on:
- Service Level Agreements (SLAs)
- Uptime and availability requirements
- Delivery schedules and milestones
- Support and maintenance obligations
- Performance metrics and KPIs
- Resource requirements
- Operational constraints

QUESTION: {question}

Provide a detailed operational analysis with feasibility assessment. Structure your response as:
1. SLA Requirements
2. Operational Constraints
3. Feasibility Assessment
4. Resource Implications
5. Execution Recommendations

ANALYSIS:"""

    @staticmethod
    def get_planner_prompt(query: str) -> str:
        """Generate prompt for planning module"""
        return f"""You are an intelligent planning AI that determines which analyst agents should analyze a contract query.

AVAILABLE AGENTS:
- LegalAgent: Analyzes legal enforceability, liability, termination, jurisdiction
- ComplianceAgent: Ensures regulatory compliance, GDPR, ISO, audit requirements
- FinanceAgent: Identifies financial exposure, payment terms, penalties, taxes
- OperationsAgent: Validates operational feasibility, SLAs, delivery, support

QUERY: {query}

TASK: Determine which agents should analyze this query and in what order.

Respond with ONLY a valid JSON object in this exact format:
{{
    "agents": ["LegalAgent", "ComplianceAgent"],
    "execution_order": ["LegalAgent", "ComplianceAgent"],
    "reasoning": "Brief explanation of why these agents were selected"
}}

Rules:
- Include only relevant agents based on the query content
- execution_order should sequence agents logically
- Always return valid JSON

JSON RESPONSE:"""

    @staticmethod
    def get_structured_compliance_prompt(context: str, query: str) -> str:
        """Generate prompt for structured compliance extraction"""
        return f"""You are a Compliance Extraction AI. Extract structured compliance risk data from contracts.

CONTRACT CONTEXT:
{context}

QUERY: {query}

Extract compliance information and return ONLY a valid JSON object with this structure:
{{
    "regulations_violated": [
        {{"regulation": "GDPR Article 32", "description": "Inadequate security measures", "severity": "High"}}
    ],
    "missing_clauses": [
        {{"clause_type": "Data Protection", "requirement": "DPO appointment", "impact": "Medium"}}
    ],
    "overall_compliance_score": 75,
    "priority_actions": [
        {{"action": "Add data breach notification clause", "urgency": "High", "timeline": "Immediate"}}
    ]
}}

Return ONLY the JSON object, no additional text.

JSON:"""

    @staticmethod
    def get_structured_finance_prompt(context: str, query: str) -> str:
        """Generate prompt for structured financial extraction"""
        return f"""You are a Financial Extraction AI. Extract structured financial risk data from contracts.

CONTRACT CONTEXT:
{context}

QUERY: {query}

Extract financial information and return ONLY a valid JSON object with this structure:
{{
    "payment_obligations": [
        {{"type": "Monthly Fee", "amount": "$10,000", "frequency": "Monthly", "due_date": "1st of month"}}
    ],
    "penalties": [
        {{"trigger": "Late delivery", "amount": "$500 per day", "maximum": "$50,000"}}
    ],
    "financial_risks": [
        {{"risk": "Uncapped liability", "exposure": "Unlimited", "probability": "Medium"}}
    ],
    "total_exposure_estimate": "$500,000",
    "mitigation_needed": true
}}

Return ONLY the JSON object, no additional text.

JSON:"""

    @staticmethod
    def get_multi_domain_clause_prompt(context: str, query: str) -> str:
        """Generate prompt for multi-domain clause extraction"""
        return f"""You are a Clause Extraction AI. Extract all important clauses across legal, compliance, financial, and operational domains.

CONTRACT CONTEXT:
{context}

QUERY: {query}

Extract clauses and return ONLY a valid JSON object with this structure:
{{
    "legal_clauses": [
        {{"type": "Indemnification", "summary": "Client indemnifies vendor", "location": "Section 8.1"}}
    ],
    "termination_clauses": [
        {{"condition": "Breach", "notice_period": "30 days", "penalties": "None"}}
    ],
    "liability_caps": [
        {{"type": "General Liability", "limit": "$1,000,000", "exclusions": ["Gross negligence"]}}
    ],
    "ip_clauses": [
        {{"type": "IP Ownership", "owner": "Client", "exceptions": ["Pre-existing vendor IP"]}}
    ],
    "sla_terms": [
        {{"metric": "Uptime", "target": "99.9%", "penalty": "$1000 per 0.1% below"}}
    ],
    "payment_terms": [
        {{"schedule": "Net 30", "method": "Wire transfer", "late_fee": "1.5% per month"}}
    ],
    "data_protection": [
        {{"requirement": "GDPR compliant", "measures": ["Encryption", "Access controls"]}}
    ]
}}

Return ONLY the JSON object, no additional text.

JSON:"""

    @staticmethod
    def get_agent_prompt(role: str, context: str, question: str, instructions: str = "") -> str:
        """Generic agent prompt builder"""
        prompt_map = {
            "legal": PromptTemplates.get_legal_agent_prompt,
            "compliance": PromptTemplates.get_compliance_agent_prompt,
            "finance": PromptTemplates.get_finance_agent_prompt,
            "operations": PromptTemplates.get_operations_agent_prompt,
        }
        
        if role.lower() in prompt_map:
            return prompt_map[role.lower()](context, question)
        
        # Fallback generic prompt
        return f"""You are a {role} AI Analyst.

CONTEXT:
{context}

{instructions}

QUESTION: {question}

ANALYSIS:"""
