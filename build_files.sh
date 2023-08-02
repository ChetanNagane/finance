echo "Build Start"
pip install -r requirements.txt
pip install pysqlite3
python3.9 manage.py collectstatic --noinput --clear
echo "Build End"