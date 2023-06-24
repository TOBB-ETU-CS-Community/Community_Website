import streamlit as st
from modules.utils import add_bg_from_local, load_excel, set_page_config
from streamlit_timeline import st_timeline


def main():
    set_page_config()

    add_bg_from_local(
        background_file="input/Community Logo.png",
        sidebar_background_file="input/Lila Gradient.png",
    )

    st.markdown(
        "<h1 style='text-align: center; color: black; font-size: 40px;'> Etkinlik takvimimizi aşağıdaki \
            zaman çizelgesi üzerinden inceleyebilirsiniz </h1> \
        ",
        unsafe_allow_html=True,
    )

    desired_date_format = "%Y-%m-%d"
    date_columns = ["Tarih"]
    calendar = load_excel(
        file="input/Etkinlik Takvimi.xlsx", date_columns=date_columns
    )

    items = []

    for i in range(len(calendar)):
        clubs = {
            "Bilgisayar Topluluğu": 1,
            "Blockchain Kulübü": 2,
            "Yapay Zeka Kulübü": 3,
            "Oyun Geliştirme Kulübü": 4,
            "Uygulama Geliştirme Kulübü": 5,
        }
        reversed_clubs = {v: k for k, v in clubs.items()}
        item = {
            "id": i,
            "content": calendar["İsim"][i],
            # "start": new_date_string
            "start": calendar["Tarih"][i].strftime(desired_date_format)
            + " "
            + str(calendar["Başlangıç Saati"][i])
            + ":00",
            "title": calendar["Düzenleyen"][i],
        }
        items.append(item)

    timeline = st_timeline(items, groups=[], options={}, height="500px")


if __name__ == "__main__":
    main()
