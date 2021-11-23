#include "xdp_kernel.h"

#define IP_ADDRESS(x) (unsigned int)(172 + (17 << 8) + (0 << 16) + (x << 24))

#define BACKEND_A 2
#define BACKEND_B 3
#define CLIENT 4
#define LB 5

SEC("xdp_trace")
int xdp_tracer(struct xdp_md *ctx)
{
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    bpf_printk("Got something\n");

    struct ethhdr *eth = data;
    if (data + sizeof(struct ethhdr) > data_end)
        return XDP_ABORTED;

    if (bpf_ntohs(eth->h_proto) != ETH_P_IP)
        return XDP_PASS;

    struct iphdr *iph = data + sizeof(struct ethhdr);
    if (data + sizeof(struct ethhdr) + sizeof(struct iphdr) > data_end)
        return XDP_ABORTED;

    if (iph->protocol != IPPROTO_TCP)
        return XDP_PASS;

    bpf_printk("TCP packet from %x to %x\n", iph->saddr, iph->daddr);
    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
