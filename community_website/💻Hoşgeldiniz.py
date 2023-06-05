import streamlit as st
from modules.configurations import add_bg_from_local


def main():
    st.set_page_config(
        page_title="💻Bilgisayar Topluluğu",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/TOBB-ETU-CS-Community",
            "Report a bug": "https://tobbetu-bilgisayar-toplulugu.streamlit.app/Geri Bildirim Formu",
            "About": "Topluluğumuza ait web sayfasında bize dair pek çok bilgiye ulaşabilirsiniz. \
            Her türlü geri bildiriminize her zaman açığız.",
        },
    )
    add_bg_from_local("input/background.png")

    st.markdown(
        "<h1 style='text-align: center; color: black; font-size: 60px;'> TOBB ETU Bilgisayar Topluluğu Web Sayfasına Hoşgeldiniz 👋</h1> \
        <br> <br>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style='text-align: center;  font-size: 20px;'>
        TOBB ETU Bilgisayar Topluluğu, 2022 yılının Nisan ayında kurulmuş bir öğrenci topluluğudur. Bu topluluğun temel amacı,
        öğrencilerin kendilerini sosyal ve teknik becerilerde en iyi şekilde geliştirebilmesi için fırsatlar yaratmaktır. Bu amaçla
        online ya da yüz yüze etkinlikler düzenliyor, ulusal ve uluslararası yarışmalara katılıyor ve açık kaynak kodlu projeler geliştiriyoruz.
        Türkiye'nin her yerinden ve her eğitim seviyesinden insanla birlikte topluluğumuz için birlikte çalışmaya hazırız.
        <br>
        <br>
         <a href='https://linktr.ee/tobbbilgisayartoplulugu'> Linktr.ee </a> adresimizden farklı platformlardaki hesaplarımıza ulaşabilirsiniz.
        </p> """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
