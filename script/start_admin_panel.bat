chcp 65001

@echo

cd ..

poetry run streamlit run "community_website\admin\db op.py" --server.port 8502

pause
