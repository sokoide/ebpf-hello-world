# eBPF hello world

## About

* Hello world examples from <https://www.youtube.com/watch?v=lrSExTfS-iQ>

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

* hello ... this is not good because it calls `bpf_trace_printk` which serializes in kernel

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

* hello2 ... improved version
```sh
sudo python3 ebpf_hello2.py

# call 'ls' and 'sudo ls' in a different window

$ sudo python3 epbf_hello2.py
ID 1000: 1
ID 0: 19        ID 1000: 1
```


## Links

* Youtoube videos
  * [Beginners guide to eBPF](https://www.youtube.com/watch?v=lrSExTfS-iQ)
  * [eBPF summit 2021 Day 1](https://www.youtube.com/watch?v=Kp3PHPuFkaA)
    * [States and future of eBPF](https://www.youtube.com/watch?v=Kp3PHPuFkaA&t=528s)
	* [Getting Started with BPF Observability](https://www.youtube.com/watch?v=Kp3PHPuFkaA&t=1886s)
    * [Using eBPF as an SRE](https://www.youtube.com/watch?v=Kp3PHPuFkaA&t=4974s)
  * [eBPF summit 2021 Day 2](https://www.youtube.com/watch?v=ZNtVedFsD-k&t=0s)
* eBPF usage examples (Japanese)
  * [eBPFのコンパイラーに対応したツールでさまざまな挙動を可視化する](https://gihyo.jp/admin/serial/01/ubuntu-recipe/0688)
  * [BCCでeBPFのコードを書いてみる](https://gihyo.jp/admin/serial/01/ubuntu-recipe/0690)
  * [sysfsやbpftoolを用いたeBPFの活用](https://gihyo.jp/admin/serial/01/ubuntu-recipe/0692)
