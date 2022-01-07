clean:
	echo "\n\nCLEANING OUT DOCKER RESOURCES!\n\n"
	- docker ps -aq | xargs docker rm -f
	- docker images -aq | xargs docker rmi -f
	- docker volumes ls -q | xargs docker volume rm
	echo "\n\nDESTROYED DOCKER RESOURCES!\n\n"

docker-mathengine:
	docker build -t zmgsabstract/mathengine .

render: docker-mathengine
	echo "\n\nSTARTING MATH ENGINE\n\n"

	docker run --name mathengine \
	--mount type=volume,src=mathengine-data,dst="/data" \
	zmgsabstract/mathengine python3 -m demo.render_5_cube

	echo "\n\nEXECUTION SUCCESSFUL!\n\n"
