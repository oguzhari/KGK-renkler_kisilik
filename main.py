from utils import *

st.config.set_option("theme.primaryColor", "white")

css_code = """
<style>
    .content-container {
        border-top: 3px solid black;
        border-bottom: 3px solid black;
    }
    .row-divider {
        border-bottom: 1px solid gray;
        margin: 10px 0;
    }
</style>
"""

# CSS kodlarını uygulamaya ekleyin
st.markdown(css_code, unsafe_allow_html=True)

head()
kisisel_bilgiler()
sorular()
kontrol_butonu()
version()
