from bcc import BPF
import time

# kernel space code
program = """
BPF_HASH(clones);

int kprobe__sys_clone(void *ctc) {
  u64 uid;
  u64 counter = 0;
  u64 *p;

  /* uid id bottom 4 bytes */
  uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
  p = clones.lookup(&uid);
  if (p != 0) {
    counter = *p;
  }

  /* Not serializing it in kernel, but push it in the hash */
  counter++;
  clones.update(&uid, &counter);

  return 0;
}
"""

# user space code
b = BPF(text=program)

while True:
    time.sleep(2)
    s = ''
    if len(b['clones'].items()):
        for k, v in b['clones'].items():
            s += 'ID {}: {}\t'.format(k.value, v.value)
        print(s)
    else:
        print('No entry')
