#Kogge stone adder

import math

module_print = """
`timescale 1ns / 1ps

module b_box(Gkj, Pik, Gik, Pkj, G, P);
 input Gkj, Pik, Gik, Pkj;
 output G, P;
 wire Y;
 and(Y, Gkj, Pik);
 or(G, Gik, Y);
 and(P, Pkj, Pik);
endmodule

module g_box(Gkj, Pik, Gik, G);
 input Gkj, Pik, Gik;
 output G;
 wire Y;
 and(Y, Gkj, Pik);
 or(G, Y, Gik);
endmodule

module pg_box(a, b, p, g);
 input a, b;
 output p, g;
 xor(p, a, b);
 and(g, a, b);
endmodule 
"""
print(module_print)

def kogge_stone(N, Modulename):
    ports = f"input [{N-1}:0] x,y,\noutput [{N-1}:0] sum,\noutput cout\n"
    W = f"wire [{N-1}:0]"
    for i in range(1, round(math.log(N) / math.log(2)) + 2):
        W += f" G{i}, P{i},"
    W = W[:-1] + ";\n"

    a = ""
    for j in range(1, round((math.log(N) / math.log(2)) + 1) + 1):
        a += f"// Level {j}\n"
        if j < round((math.log(N) / math.log(2))) + 1:
            a += f"g_box g{j}0 (1'b0, P{j}[{2 ** (j - 1) - 1}], G{j}[{2 ** (j - 1) - 1}], G{j + 1}[{2 ** (j - 1) - 1}]);\n"
        for k in range(1, 2 ** (j - 1)):
            if j >= 3 and k == 1 and j != round((math.log(N) / math.log(2))) + 1:
                a += f"g_box g{j}{k} (G2[{k - 1}], P{j}[{(2 ** (j - 1)) + k - 1}], G{j}[{(2 ** (j - 1)) + k - 1}], G{j + 1}[{(2 ** (j - 1)) + k - 1}]);\n"
            elif (2 ** (j - 1)) + k - 1 < N:
                a += f"g_box g{j}{k} (G{j}[{k - 1}], P{j}[{(2 ** (j - 1)) + k - 1}], G{j}[{(2 ** (j - 1)) + k - 1}], G{j + 1}[{(2 ** (j - 1)) + k - 1}]);\n"
            else:
                a += f"g_box g{j}0 (1'b0, P{j}[{2 ** (j - 1) - 1}], G{j}[{2 ** (j - 1) - 1}], cout);\n"
                break
        for r in range(1, N - (2 ** (j - 1) - 1) - 2 ** (j - 1) + 1):
            a += f"b_box b{j}{r} (G{j}[{2 ** (j - 1) + (r - 2)}], P{j}[{2 ** (j) - 1 + (r - 1)}], G{j}[{2 ** (j) - 1 + (r - 1)}], P{j}[{2 ** (j - 1) + (r - 2)}], G{j + 1}[{2 ** (j) - 1 + (r - 1)}], P{j + 1}[{2 ** (j) - 1 + (r - 1)}]);\n"
        a += "\n"

    b = ""
    for s in range(N):
        b += f"pg_box Z{s} (x[{s}], y[{s}], P1[{s}], G1[{s}]);\n"

    c = f"xor x0 (sum[0], 1'b0, P1[0]);\n"
    count = 1
    for e in range(2, round(math.log(N) / math.log(2)) + 2):
        for p in range(2 ** (e - 2)):
            c += f"xor x{count} (sum[{count}], G{e}[{count - 1}], P1[{count}]);\n"
            count += 1

    verilog_code = f"module {Modulename} (\n{ports});\n\n{W}\n\n{a}\n{b}\n{c}\nendmodule"

    print(verilog_code)

kogge_stone(8,"kogg")