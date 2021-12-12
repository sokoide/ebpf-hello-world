from bcc import BPF
from time import sleep

program = """
int kprobe__sys_clone(void *ctc) {
  u64 uid;
  /* uid id bottom 4 bytes */
  uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

  /* Not good to serialize in kernel */
  bpf_trace_printk("Hello id: %d\\n", uid);
  return 0;
}
"""

b = BPF(text=program)
b.trace_print()
