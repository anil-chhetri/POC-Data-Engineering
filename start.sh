docker compose -f docker-compose.yml up -d --build --wait
echo "export PS1=\"\\\\W> \" " >> ~/.bashrc
docker exec playground service ssh start
docker exec playground service ssh status
