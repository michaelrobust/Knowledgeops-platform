from fpdf import FPDF

# 如果沒有 fpdf，改用文字轉 PDF
try:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Python Programming Guide", ln=1, align='C')
    pdf.ln(10)
    
    content = """
    Python Best Practices for Professional Development
    
    1. Code Quality
    - Always follow PEP 8 style guidelines
    - Write self-documenting code
    - Use meaningful variable names
    
    2. Testing
    - Write unit tests for all functions
    - Aim for 80% code coverage minimum
    - Use pytest framework
    
    3. Documentation
    - Write clear docstrings
    - Maintain updated README files
    - Document API endpoints
    
    4. Performance
    - Profile before optimizing
    - Use appropriate data structures
    - Consider memory usage
    """
    
    for line in content.split('\n'):
        pdf.cell(0, 10, txt=line, ln=1)
    
    pdf.output("test_python_guide.pdf")
    print("✅ Created test_python_guide.pdf")
    
except ImportError:
    print("fpdf not installed, creating simple test file instead")
    # 備用方案：直接下載或使用現有 PDF
