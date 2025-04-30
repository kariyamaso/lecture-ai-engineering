import streamlit as st
import time

# ===========================================
# ページ設定
# ===========================================
st.set_page_config(
    page_title="AI コード生成アシスタント",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===========================================
# タイトルと説明
# ===========================================
st.title("🤖 AI コード生成アシスタント (デモ)")
st.markdown("左側のテキストエリアに生成したいコードの概要を自然言語で入力し、「生成」ボタンを押してください。")

# ===========================================
# ダミーのコード生成関数 (実際のAIモデル連携部分)
# ===========================================
def generate_code_dummy(prompt: str) -> str:
    """
    AIモデルによるコード生成をシミュレートするダミー関数。
    実際にはここでOpenAI APIなどを呼び出す。
    """
    st.info(f"受け取った指示: {prompt}")
    time.sleep(1)
    
    if "python" in prompt.lower() and "合計" in prompt and "関数" in prompt:
        return """```python
def sum_two_numbers(a, b):
    \"\"\"二つの数値の合計を返す関数\"\"\"
    return a + b

# 使用例
result = sum_two_numbers(5, 3)
print(f"合計: {result}") 
```"""
    elif "html" in prompt.lower() and "ボタン" in prompt:
        return """```html
<button onclick="alert('クリックされました！')">クリックしてください</button> 
```"""
    elif "css" in prompt.lower() and "中央揃え" in prompt:
         return """```css
.center-element {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* or container height */
}
```"""
    else:
        return f"""```plaintext
# '{prompt}' に基づくコード生成はまだ実装されていません。(ダミー応答)
# ここにAIが生成したコードが表示されます。
print("Hello from AI!")
```"""

# ===========================================
# メインコンテンツ: AIコード生成
# ===========================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("指示を入力")
    prompt_input = st.text_area("生成したいコードの内容を記述してください:", height=300, placeholder="例: 引数を2つ取り、その合計を返すPython関数")
    generate_button = st.button("コード生成 ▶️")

with col2:
    st.subheader("生成されたコード")
    if 'generated_code' not in st.session_state:
        st.session_state.generated_code = "# コードはここに表示されます"

    if generate_button and prompt_input:
        with st.spinner("AIがコードを生成中..."):
            generated_code = generate_code_dummy(prompt_input)
            st.session_state.generated_code = generated_code
        st.code(st.session_state.generated_code, language=None)
    else:
         st.code(st.session_state.generated_code, language=None)


# ===========================================
# カスタマイズ (CSS)
# ===========================================
st.markdown("""
<style>
body {
    color: #E0E0E0; 
    background-color: #1E1E1E; 
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace; 
}

/* Basic Input elements */
input, textarea, select {
    background-color: #2A2A2A !important; 
    color: #E0E0E0 !important;           
    border: 1px solid #555 !important;    
}
textarea {
     font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important; 
}

/* Buttons */
button {
    background-color: #3C3C3C !important; 
    color: #E0E0E0 !important;           
    border: 1px solid #555 !important;
    transition: background-color 0.2s ease; 
}
button:hover {
    background-color: #555555 !important; 
}

/* Code blocks */
pre, code {
    background-color: #282C34 !important; 
    color: #ABB2BF !important;           
    border-radius: 4px;
    padding: 0.5em !important;
    white-space: pre-wrap !important; 
    word-break: break-all !important; 
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: #00AACC; 
}

</style>
""", unsafe_allow_html=True)