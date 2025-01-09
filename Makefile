stubs:
	python -m grpc_tools.protoc \
		-I protos \
		--python_out=distlock/stubs \
		--pyi_out=distlock/stubs \
		--grpc_python_out=distlock/stubs \
		protos/distlock.proto
	sed 's/^import distlock_pb2 as distlock__pb2$$/from . import distlock_pb2 as distlock__pb2/' distlock/stubs/distlock_pb2_grpc.py > tmp && mv tmp distlock/stubs/distlock_pb2_grpc.py
