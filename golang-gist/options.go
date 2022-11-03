package golang_gist

import "time"

type Server struct {
	options *Options

	Name string
	Host string
	Port int
}

type Options struct {
	Options1 string
	Options2 int
	Options3 time.Duration
}

type option func(options *Options)

func WithOptions1(op1 string) option {
	return func(options *Options) {
		options.Options1 = op1
	}
}

func WithOptions2(op2 int) option {
	return func(options *Options) {
		options.Options2 = op2
	}
}

func WithOptions3(op3 time.Duration) option {
	return func(options *Options) {
		options.Options3 = op3
	}
}

func NewServer(name, host string, port int, ops ...option) *Server {
	server := &Server{
		Name: name,
		Host: host,
		Port: port,
	}

	options := &Options{}
	for _, op := range ops {
		op(options)
	}

	server.options = options

	return server
}

func main() {
	_ = NewServer(
		"server",
		"",
		10000,
		WithOptions1("ooo"),
		WithOptions2(2),
		WithOptions3(time.Second),
	)
}
