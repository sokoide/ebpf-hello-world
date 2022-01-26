CC=clang

CFLAGS=-target bpf \
	    -D __BPF_TRACING__ \
		-Wall \
	    -Wno-unused-value \
	    -Wno-pointer-sign \
	    -Wno-compare-distinct-pointer-types \
	    -Werror \
	    -I../submodules/libbpf/src\
	    -O2 -emit-llvm

default: run

run: xdp_kernel.o
	bpftool net detach xdpgeneric dev eth0
	rm -f /sys/fs/bpf/xdp_trace
	bpftool prog load xdp_kernel.o /sys/fs/bpf/xdp_trace
	bpftool net attach xdpgeneric pinned /sys/fs/bpf/xdp_trace dev eth0

xdp_kernel.o: xdp_kernel.c
	$(CC) -S \
		$(CFLAGS) \
	    -c -o ${@:.o=.ll} $<
		llc -march=bpf -filetype=obj -o $@ ${@:.o=.ll}

clean:
	bpftool net detach xdpgeneric dev eth0
	rm -f /sys/fs/bpf/xdp_trace
	rm xdp_kernel.o
	rm xdp_kernel.ll
