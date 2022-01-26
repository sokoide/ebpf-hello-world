from bcc import BPF
import datetime
import ctypes as ct

# kernel space code
program = """
# include <linux/sched.h>
# include <linux/bpf.h>

const int PATHLEN=128;

#pragma pack(8)
struct data_t {
  u32 pid;
  u32 uid;
  u32 ty;
  char file[PATHLEN];
  char comm[TASK_COMM_LEN];
};
#pragma pack()

BPF_PERF_OUTPUT(events);

enum {
  tyClone = 0,
  tyExecve,
  tyNanosleep,
  tyOpenat,
  tyOpen,
  tyCreat
};

static int submit(void *ctx, int ty, const char* file) {
  u32 pid, uid;
  pid = bpf_get_current_pid_tgid() & 0xFFFFFFFF;
  uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

  struct data_t data = {pid, uid, ty};
  bpf_get_current_comm(&data.comm, sizeof(data.comm));

  if (file == NULL) {
    data.file[0] = 0;
  } else {
    __builtin_memset(data.file, 0, sizeof(data.file));
    bpf_probe_read_user(data.file, sizeof(data.file), (void *)file);
  }

  events.perf_submit(ctx, &data, sizeof(data));

  return 0;
}

int kprobe__sys_clone(void *ctx) {
  return submit(ctx, tyClone, NULL);
}

int syscall__nanosleep(struct pt_regs *ctx, const struct timespec *req, struct timespec *rem) {
  return submit(ctx, tyNanosleep, NULL);
}

// if you want to get args, it must be in the format of syscall__$syscallname
int syscall__execve(struct pt_regs *ctx, const char __user *filename)
{
  return submit(ctx, tyExecve, filename);
}


int syscall__openat(struct pt_regs *ctx, int dirfd, const char __user *pathname, int flags) {
  return submit(ctx, tyOpenat, pathname);
}

int syscall__open(struct pt_regs *ctx, const char __user *pathname, int flags) {
  return submit(ctx, tyOpen, pathname);
}

int syscall__creat(struct pt_regs *ctx, const char __user *pathname, int flags) {
  return submit(ctx, tyCreat, pathname);
}
"""

# user space code
b = BPF(text=program)
b.attach_kprobe(event=b.get_syscall_fnname(
    "nanosleep"), fn_name="syscall__nanosleep")
b.attach_kprobe(
    event=b.get_syscall_fnname("execve"),
    fn_name="syscall__execve")
b.attach_kprobe(
    event=b.get_syscall_fnname("openat"),
    fn_name="syscall__openat")
b.attach_kprobe(
    event=b.get_syscall_fnname("open"),
    fn_name="syscall__open")
b.attach_kprobe(
    event=b.get_syscall_fnname("creat"),
    fn_name="syscall__creat")


class Data(ct.Structure):
    PATHLEN = 128
    TASK_COMM_LEN = 16

    _pack_ = 8
    _fields_ = [
        ("pid", ct.c_uint32), ("uid", ct.c_uint32), ("ty", ct.c_uint32),
        ("file", ct.c_char * PATHLEN), ("comm", ct.c_char * TASK_COMM_LEN)]


def print_event(cpu, data, size):
    types = ['clone', 'execve', 'nanosleep', 'openat', 'open', 'creat']
    event = ct.cast(data, ct.POINTER(Data)).contents
    if event.ty == 1 or event.ty == 3:
        print(
            '[{}] pid:{}, uid: {}, syscall: {}, comm: {}, file: {}'.format(
                datetime.datetime.now(),
                event.pid,
                event.uid,
                types[event.ty],
                event.comm,
                event.file))
    else:
        print(
            '[{}] pid:{}, uid: {}, syscall: {}, comm: {}'.format(
                datetime.datetime.now(),
                event.pid,
                event.uid,
                types[event.ty],
                event.comm))


b["events"].open_perf_buffer(print_event)
while True:
    b.perf_buffer_poll()
