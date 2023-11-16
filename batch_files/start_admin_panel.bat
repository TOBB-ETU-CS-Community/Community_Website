chcp 65001

@echo

cd ..

poetry run streamlit run "community_website\modules\db op.py" --server.port 8502

pause
