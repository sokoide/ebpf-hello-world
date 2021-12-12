from bcc import BPF
import datetime
import ctypes as ct

# kernel space code
program = """
# include <linux/sched.h>

struct data_t {
  u32 pid;
  u32 uid;
  char comm[TASK_COMM_LEN];
};

BPF_PERF_OUTPUT(events);

int kprobe__sys_clone(void *ctx) {
  u32 pid;
  u32 uid;

  pid = bpf_get_current_pid_tgid() & 0xFFFFFFFF;
  uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

  struct data_t data = {pid, uid};
  bpf_get_current_comm(&data.comm, sizeof(data.comm));

  events.perf_submit(ctx, &data, sizeof(data));

  return 0;
}
"""

# user space code
b = BPF(text=program)


class Data(ct.Structure):
    # TASK_COMM_LEN is 16, 24 or etc
    _fields_ = [("pid", ct.c_uint32), ("uid", ct.c_uint32),
                ("comm", ct.c_char * 16), ]


def print_event(cpu, data, size):
    event = ct.cast(data, ct.POINTER(Data)).contents
    print('[{}] pid:{}, uid: {}, comm: {}'.format(
        datetime.datetime.now(), event.pid, event.uid, event.comm))
    # print('[{}] uid: {}'.format(
    #     datetime.datetime.now(), event.uid))


b["events"].open_perf_buffer(print_event)
while True:
    b.perf_buffer_poll()
