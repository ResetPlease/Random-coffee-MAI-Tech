



if [ $IS_UPDATE -eq 1 ]; then
    alembic upgrade head
    alembic revision --autogenerate -m $UPDATE_NAME
fi


alembic upgrade head