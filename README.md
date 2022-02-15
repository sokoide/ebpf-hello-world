# eBPF hello world

## About

* eBPF Hello world examples from the followings
  * [Beginners guide to eBPF](https://www.youtube.com/watch?v=lrSExTfS-iQ)
  * [eBPF load balancer](https://www.youtube.com/watch?v=ZNtVedFsD-k&t=0s)

## Env

* Ubunttu 20.04 LTS x64 VM

## How to install

* Install eBPF

```sh
sudo apt install bpfcc-tools

# quicktest (you need '-bofcc' postfix)
sudo execsnoop-bpfcc -Tx
# ctrl-c to quit after a few seconds
```

## How to run

### Hello1

* hello ... kprobe. this is not good because it calls `bpf_trace_printk` which serializes in kernel

```sh
sudo python3 ebpf_hello.py

# call 'ls' in a different window

$ sudo python3 epbf_hello.py
b'            bash-1069966 [000] .... 503796.349523: 0: Hello id: 1000'
b'         systemd-1       [002] .... 503796.847050: 0: Hello id: 0'
b'   systemd-udevd-453     [001] .... 503796.848003: 0: Hello id: 0'
b'   systemd-udevd-453     [001] .... 503796.848340: 0: Hello id: 0'
b'   systemd-udevd-453     [001] .... 503796.848651: 0: Hello id: 0'
b'   systemd-udevd-453     [001] .... 503796.848942: 0: Hello id: 0'
b'   systemd-udevd-453     [001] .... 503796.849270: 0: Hello id: 0'
b'   systemd-udevd-453     [001] .... 503796.849645: 0: Hello id: 0'
b'         kubelet-1076665 [005] .... 503796.850939: 0: Hello id: 0'
...
```

### Hello2

* hello2 ... kprobe. improved version by using `BPF_HASH`
* Kernel keeps info (uid, counter) in a hash so that an user mode client can read it anytime

```sh
sudo python3 ebpf_hello2.py

# call 'ls' and 'sudo ls' in a different window

$ sudo python3 epbf_hello2.py
ID 1000: 1
ID 0: 19        ID 1000: 1
```

### Hello3

* hello3 ... kprobe. improved version by using `events.perf_submit`
* Kernel submits info (uid, counter) to a ring buffer (events) so that an user mode client can read it

```sh
$ sudo python3 ./ebpf_hello3.py
[2021-12-12 10:55:56.561067] pid:29436, uid: 1000, comm: b'node'
[2021-12-12 10:55:56.572300] pid:47200, uid: 1000, comm: b'sh'
[2021-12-12 10:55:56.572404] pid:47200, uid: 1000, comm: b'sh'
```

### Hello4

* hello4 ... system call tracepoints to capture syscall arguments.
* hello4b ... replaced bpf_probe_read_user with bpf_probe_read for old OS
* <https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md>

```sh
sudo python3 ./ebpf_hello4.py
[2022-01-26 10:05:15.729691] pid:1441800, uid: 1000, syscall: openat, comm: b'go', file: b'/tmp/go-build1646927981/b001/exe/foo'
[2022-01-26 10:05:15.733258] pid:1441872, uid: 1000, syscall: openat, comm: b'foo', file: b''
[2022-01-26 10:05:15.734138] pid:1441803, uid: 1000, syscall: openat, comm: b'go', file: b'/home/scott/.cache/go-build/trim.txt'
```

### TCP tracer

* eBPF TCP tracer

```sh
sudo apt install linux-tools-common linux-tools-generic libpcap-dev gcc-multilib
sudo ln -s /usr/include/asm-generic/ /usr/include/asm

git submodule update --init --recursive
scott@lab2:~/repo/ebpf/hello/tcptrace$

make xdp_kernel.o
sudo make

# try curl to the host from another host
curl $HOSTNAME
curl: (7) Failed to connect to lab2 port 80: Connection refused

# check trace
$ sudo cat /sys/kernel/debug/tracing/trace| tail
          <idle>-0       [000] ..s. 509531.991320: 0: Got something
          <idle>-0       [000] ..s. 509531.991322: 0: TCP packet from c902a8c0 to ca02a8c0
          <idle>-0       [005] ..s. 509531.991908: 0: Got something
          <idle>-0       [005] ..s. 509531.991909: 0: TCP packet from c902a8c0 to ca02a8c0
          <idle>-0       [005] ..s. 509531.991910: 0: Got something

# stop and unload it
sudo make clean
```

## Links

* Youtoube videos
  * [Beginners guide to eBPF](https://www.youtube.com/watch?v=lrSExTfS-iQ)
  * [eBPF summit 2021 Day 1](https://www.youtube.com/watch?v=Kp3PHPuFkaA)
    * [States and future of eBPF](https://www.youtube.com/watch?v=Kp3PHPuFkaA&t=528s)
	* [Getting Started with BPF Observability](https://www.youtube.com/watch?v=Kp3PHPuFkaA&t=1886s)
    * [Using eBPF as an SRE](https://www.youtube.com/watch?v=Kp3PHPuFkaA&t=4974s)
  * [eBPF summit 2021 Day 2](https://www.youtube.com/watch?v=ZNtVedFsD-k&t=0s)
    * [eBPF load balancer](https://www.youtube.com/watch?v=ZNtVedFsD-k&t=0s)
* eBPF usage examples (Japanese)
  * [eBPFのコンパイラーに対応したツールでさまざまな挙動を可視化する](https://gihyo.jp/admin/serial/01/ubuntu-recipe/0688)
  * [BCCでeBPFのコードを書いてみる](https://gihyo.jp/admin/serial/01/ubuntu-recipe/0690)
  * [sysfsやbpftoolを用いたeBPFの活用](https://gihyo.jp/admin/serial/01/ubuntu-recipe/0692)
