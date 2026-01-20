"""
Create a sample contract PDF for testing
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def create_sample_contract_pdf():
    """Create a sample contract PDF with legal, finance, operations, and risk clauses"""
    
    filename = "sample_contract.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    styles = getSampleStyleSheet()
    
    # Title Style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='darkblue',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Heading Style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='navy',
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Body Style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # Title
    title = Paragraph("SOFTWARE SERVICES AGREEMENT", title_style)
    Story.append(title)
    Story.append(Spacer(1, 0.2*inch))
    
    # Contract Number and Date
    contract_info = Paragraph(
        "<b>Contract No:</b> SVC-2026-001<br/>"
        "<b>Effective Date:</b> January 12, 2026<br/>"
        "<b>Parties:</b> TechCorp Inc. (Service Provider) and GlobalCo Ltd. (Client)",
        body_style
    )
    Story.append(contract_info)
    Story.append(Spacer(1, 0.3*inch))
    
    # 1. LEGAL TERMS
    Story.append(Paragraph("1. LEGAL TERMS & LIABILITY", heading_style))
    
    legal_text = """
    <b>1.1 Liability Cap:</b> The total liability of the Service Provider under this agreement 
    shall not exceed $1,000,000 (One Million Dollars) for any single incident or $2,500,000 
    in aggregate for all claims during the contract term. This limitation excludes gross 
    negligence, willful misconduct, and breaches of data protection obligations.
    <br/><br/>
    <b>1.2 Intellectual Property:</b> All intellectual property rights, including but not 
    limited to source code, documentation, and proprietary methodologies developed by the 
    Service Provider remain the exclusive property of TechCorp Inc. Client receives a 
    non-exclusive, non-transferable license for internal business use only.
    <br/><br/>
    <b>1.3 Indemnification:</b> Service Provider shall indemnify and hold harmless the Client 
    against any third-party claims arising from IP infringement, data breaches caused by 
    Provider's negligence, or violations of applicable laws by Provider's personnel.
    <br/><br/>
    <b>1.4 Termination Rights:</b> Either party may terminate this agreement with 90 days 
    written notice. Immediate termination is permitted in cases of material breach, insolvency, 
    or regulatory violations. Upon termination, Client must cease all use of Provider's software 
    and return or destroy all confidential materials.
    """
    Story.append(Paragraph(legal_text, body_style))
    Story.append(Spacer(1, 0.2*inch))
    
    # 2. FINANCIAL TERMS
    Story.append(Paragraph("2. FINANCIAL OBLIGATIONS & PAYMENTS", heading_style))
    
    finance_text = """
    <b>2.1 Service Fees:</b> Client agrees to pay monthly service fees of $50,000 per month, 
    payable in advance on the first business day of each month. Annual prepayment discount 
    of 10% available if paid by January 31, 2026.
    <br/><br/>
    <b>2.2 Payment Terms:</b> All invoices are due within Net 30 days from invoice date. 
    Late payments will incur a penalty of 1.5% per month (18% APR) on the outstanding balance. 
    Payment method: Wire transfer to designated bank account. Client is responsible for all 
    bank transfer fees.
    <br/><br/>
    <b>2.3 Additional Costs:</b> Client shall reimburse Provider for reasonable out-of-pocket 
    expenses including travel costs (maximum $5,000/month), third-party software licenses, 
    and cloud infrastructure costs exceeding $10,000/month. All expenses require prior written 
    approval.
    <br/><br/>
    <b>2.4 Penalty Provisions:</b>
    <br/>• Service Level Agreement (SLA) breaches: Credit of 5% monthly fee per incident
    <br/>• Data breach caused by Provider: Up to $500,000 liquidated damages
    <br/>• Failure to meet project milestones: 2% penalty per week of delay (max 20%)
    <br/>• Early termination by Provider without cause: Refund of 3 months prepaid fees
    <br/><br/>
    <b>2.5 Financial Risk:</b> Total estimated annual cost: $600,000 base + $60,000 expenses 
    + potential $120,000 in penalties = $780,000 maximum exposure. Uncapped liabilities include 
    data breach damages beyond $500,000 and regulatory fines.
    """
    Story.append(Paragraph(finance_text, body_style))
    Story.append(Spacer(1, 0.2*inch))
    
    # 3. OPERATIONAL TERMS
    Story.append(Paragraph("3. OPERATIONAL REQUIREMENTS & SLAs", heading_style))
    
    operations_text = """
    <b>3.1 Service Level Agreements:</b>
    <br/>• System Uptime: 99.9% monthly availability (max 43.2 minutes downtime/month)
    <br/>• Response Times: Critical issues - 1 hour; High priority - 4 hours; Medium - 24 hours
    <br/>• Resolution Times: Critical - 4 hours; High - 24 hours; Medium - 72 hours
    <br/>• Scheduled Maintenance: Maximum 4 hours/month with 7 days advance notice
    <br/><br/>
    <b>3.2 Resource Allocation:</b> Provider commits to:
    <br/>• Dedicated project manager (40 hours/week)
    <br/>• 2 senior developers (80 hours/week combined)
    <br/>• 1 QA engineer (20 hours/week)
    <br/>• 24/7 technical support coverage with maximum 15-minute initial response time
    <br/><br/>
    <b>3.3 Performance Metrics:</b>
    <br/>• System response time: <200ms for 95% of requests
    <br/>• Data processing: Minimum 10,000 transactions/hour
    <br/>• Bug fix deployment: Critical bugs within 24 hours
    <br/>• Monthly service reports due within 5 business days of month end
    <br/><br/>
    <b>3.4 Operational Risks:</b> The 99.9% uptime SLA allows only 43 minutes of monthly 
    downtime which may be challenging during major updates. The 4-hour critical issue 
    resolution time is aggressive and may require additional on-call resources. Resource 
    allocation appears adequate but leaves little buffer for unexpected issues or staff turnover.
    """
    Story.append(Paragraph(operations_text, body_style))
    Story.append(Spacer(1, 0.2*inch))
    
    # 4. COMPLIANCE & DATA PROTECTION
    Story.append(Paragraph("4. COMPLIANCE & DATA PROTECTION", heading_style))
    
    compliance_text = """
    <b>4.1 Data Protection Compliance:</b> Provider must comply with:
    <br/>• GDPR (General Data Protection Regulation) for EU data subjects
    <br/>• CCPA (California Consumer Privacy Act) for California residents
    <br/>• HIPAA (Health Insurance Portability and Accountability Act) for health data
    <br/>• SOC 2 Type II certification required and maintained throughout contract term
    <br/><br/>
    <b>4.2 Security Requirements:</b>
    <br/>• AES-256 encryption for data at rest and TLS 1.3 for data in transit
    <br/>• Multi-factor authentication (MFA) for all system access
    <br/>• Annual third-party security audits (ISO 27001 certified auditor)
    <br/>• Penetration testing quarterly
    <br/>• Data backup daily with 30-day retention
    <br/><br/>
    <b>4.3 Audit Rights:</b> Client may audit Provider's security controls, data handling 
    practices, and compliance documentation with 14 days notice, maximum twice per year. 
    Provider must remediate any findings within 30 days or provide acceptable mitigation plan.
    <br/><br/>
    <b>4.4 Data Breach Notification:</b> Provider must notify Client within 24 hours of 
    discovering any data breach affecting Client data. Notification must include scope, 
    affected records, root cause analysis, and remediation plan.
    <br/><br/>
    <b>4.5 Compliance Gaps:</b> HIPAA compliance requires BAA (Business Associate Agreement) 
    which is not explicitly mentioned. SOC 2 Type II certification typically takes 6-12 months 
    if not already obtained. The 24-hour breach notification timeline is aggressive and may 
    conflict with thorough investigation requirements.
    """
    Story.append(Paragraph(compliance_text, body_style))
    Story.append(Spacer(1, 0.2*inch))
    
    # 5. RISK ASSESSMENT SUMMARY
    Story.append(Paragraph("5. RISK ASSESSMENT & RECOMMENDATIONS", heading_style))
    
    risk_text = """
    <b>5.1 Critical Risks Identified:</b>
    <br/>• <b>HIGH:</b> Uncapped liability for data breaches beyond $500,000
    <br/>• <b>HIGH:</b> Aggressive SLA targets (99.9% uptime, 4-hour critical resolution)
    <br/>• <b>MEDIUM:</b> Missing HIPAA Business Associate Agreement
    <br/>• <b>MEDIUM:</b> No force majeure clause or pandemic/disaster provisions
    <br/>• <b>MEDIUM:</b> Intellectual property ownership entirely with Provider
    <br/><br/>
    <b>5.2 Financial Exposure:</b>
    <br/>• Minimum annual cost: $600,000
    <br/>• Maximum contractual penalties: $120,000
    <br/>• Potential data breach liability: Unlimited (beyond $500,000 cap)
    <br/>• Total quantified risk: $720,000+ annually
    <br/><br/>
    <b>5.3 Recommendations:</b>
    <br/>1. Negotiate cap on data breach liability ($5M recommended)
    <br/>2. Add force majeure and pandemic-related exception clauses
    <br/>3. Request BAA addendum for HIPAA compliance
    <br/>4. Consider lower SLA targets (99.5% uptime) or renegotiate penalties
    <br/>5. Negotiate shared IP rights for custom developments
    <br/>6. Add insurance requirement ($5M cyber liability minimum)
    """
    Story.append(Paragraph(risk_text, body_style))
    Story.append(Spacer(1, 0.3*inch))
    
    # Signature Block
    Story.append(Paragraph("SIGNATURES", heading_style))
    sig_text = """
    <b>TechCorp Inc.</b><br/>
    By: _______________________<br/>
    Name: Sarah Johnson<br/>
    Title: Chief Executive Officer<br/>
    Date: _____________________<br/><br/>
    
    <b>GlobalCo Ltd.</b><br/>
    By: _______________________<br/>
    Name: Michael Chen<br/>
    Title: Chief Procurement Officer<br/>
    Date: _____________________
    """
    Story.append(Paragraph(sig_text, body_style))
    
    # Build PDF
    doc.build(Story)
    print(f"✅ Sample contract PDF created: {filename}")
    print(f"\nThis PDF includes:")
    print("  📋 Legal terms (liability, IP, termination)")
    print("  💰 Financial obligations (fees, penalties, payment terms)")
    print("  ⚙️  Operational requirements (SLAs, resources, metrics)")
    print("  🔒 Compliance requirements (GDPR, HIPAA, SOC 2)")
    print("  ⚠️  Risk assessments and recommendations")
    print(f"\nYou can now upload this PDF to the web interface for analysis!")

if __name__ == "__main__":
    create_sample_contract_pdf()
