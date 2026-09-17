import streamlit as st

def show_code_latex():
    st.header("💻 코드 블록 및 LaTeX 수식 (st.code & st.latex)")

    # 1. 코드 블록 (st.code)
    st.subheader("1. 구문 강조 코드 블록 (st.code)")
    st.caption("언어 지정(language) 및 줄 번호 표시(line_numbers=True) 옵션을 지원합니다.")

    python_code = """def calculate_total(prices, tax_rate=0.1):
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)

print(calculate_total([1000, 2000, 3000]))"""

    st.code(python_code, language="python", line_numbers=True)

    # 2. LaTeX 수식 (st.latex)
    st.subheader("2. 수학 수식 렌더링 (st.latex)")
    st.caption("LaTeX 문법으로 복잡한 수식을 깨끗하게 표시합니다.")

    st.latex(r"""
    f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}
    """)

    st.latex(r"E = mc^2")

