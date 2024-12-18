stubs:
	python -m grpc_tools.protoc \
		-I protos \
		--python_out=distlock/stubs \
		--pyi_out=distlock/stubs \
		--grpc_python_out=distlock/stubs \
		protos/distlock.proto
