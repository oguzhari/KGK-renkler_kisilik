import streamlit as st

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


def cevaplari_kontrol_et(bir, iki, uc, dort):
    bir, iki, uc, dort = int(bir), int(iki), int(uc), int(dort)
    if bir + iki + uc + dort == 3:
        pass
    elif bir + iki + uc + dort == 2:
        pass
    elif bir + iki + uc + dort == 0:
        pass
    else:
        st.error("Soruları cevaplama konusunda bir sorun var."
                 "Cevaplarda en az bir adet 2 olmalıdır. "
                 "Bunun yanında en fazla bir adet 1 olabilir.")


def body():
    options = [0, 1, 2]
    with st.container():
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        a1 = "Güçlü, kararlı, girişken ve doğuştan liderim. Kimseye minnet etmem; düşer kalkar ve yoluma devam ederim."
        with col1.container():
            col1.markdown(f"{a1}", unsafe_allow_html=True)
            value_a1 = col2.selectbox("Seçin", options, key="a1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{a1}", unsafe_allow_html=True)
            value_a2 = col2.selectbox("Seçin", options, key="a2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{a1}", unsafe_allow_html=True)
            value_a3 = col2.selectbox("Seçin", options, key="a3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{a1}", unsafe_allow_html=True)
            value_a4 = col2.selectbox("Seçin", options, key="a4")

        cevaplari_kontrol_et(value_a1, value_a2, value_a3, value_a4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

