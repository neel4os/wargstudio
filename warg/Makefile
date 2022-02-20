proto:
	mkdir -p generated/protobuf
	protoc -I protobuf --go_out=./generated/protobuf --go_opt=paths=source_relative --go-grpc_out=./generated/protobuf --go-grpc_opt=paths=source_relative ./protobuf/*.proto