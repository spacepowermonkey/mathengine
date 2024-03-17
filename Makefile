clean:
	echo "\n\nCLEANING OUT DOCKER RESOURCES!\n\n"
	- docker ps -aq | xargs docker rm -f
	- docker images -aq | xargs docker rmi -f
	- docker volume ls -q | xargs docker volume rm
	echo "\n\nDESTROYED DOCKER RESOURCES!\n\n"



docker-mathengine:
	docker build -t spacepowermonkey/mathengine .



####	D E M O S
demo-5cubes: docker-mathengine
	echo "\n\nSTARTING MATH ENGINE\n\n"

	docker run --name mathengine \
	--mount type=volume,src=mathengine-data,dst="/data" \
	spacepowermonkey/mathengine python3 -m demo.render_5_cubes

	docker cp -a mathengine:/data/ ./render/

	echo "\n\nEXECUTION SUCCESSFUL!\n\n"

demo-5cyclics: docker-mathengine
	echo "\n\nSTARTING MATH ENGINE\n\n"

	docker run --name mathengine \
	--mount type=volume,src=mathengine-data,dst="/data" \
	spacepowermonkey/mathengine python3 -m demo.render_5_cyclics

	docker cp -a mathengine:/data/ ./render/

	echo "\n\nEXECUTION SUCCESSFUL!\n\n"

demo-64elms: docker-mathengine
	echo "\n\nSTARTING MATH ENGINE\n\n"

	docker run --name mathengine \
	--mount type=volume,src=mathengine-data,dst="/data" \
	spacepowermonkey/mathengine python3 -m demo.render_64_elm_groups

	docker cp -a mathengine:/data/ ./render/

	echo "\n\nEXECUTION SUCCESSFUL!\n\n"

demo-4422perms: docker-mathengine
	echo "\n\nSTARTING MATH ENGINE\n\n"

	docker run --name mathengine \
	--mount type=volume,src=mathengine-data,dst="/data" \
	spacepowermonkey/mathengine python3 -m demo.render_4422_permutations

	docker cp -a mathengine:/data/ ./render/

	echo "\n\nEXECUTION SUCCESSFUL!\n\n"



####	P A P E R S
paper_shapes_as_di: docker-mathengine
	echo "\n\nSTARTING MATH ENGINE\n\n"

	docker run --name mathengine \
	--mount type=volume,src=mathengine-data,dst="/data" \
	spacepowermonkey/mathengine python3 -m papers.shapes_as_digital_images

	docker cp -a mathengine:/data/ ./render/

	echo "\n\nEXECUTION SUCCESSFUL!\n\n"

paper_shapes_have_ops: docker-mathengine
	echo "\n\nSTARTING MATH ENGINE\n\n"

	docker run --name mathengine \
	--mount type=volume,src=mathengine-data,dst="/data" \
	spacepowermonkey/mathengine python3 -m papers.shapes_have_operations

	docker cp -a mathengine:/data/ ./render/

	echo "\n\nEXECUTION SUCCESSFUL!\n\n"

