#Wallace Tree

module_print = """
`timescale 1ns / 1ps

module full_adder(a,b,cin,cout,s);
input a,b,cin;
output s,cout;
wire r,r1,r2;
xor(s,a,b,cin);
and(r,a,b);
and(r1,b,cin);
and(r2,a,cin);
or(cout,r,r1,r2);
endmodule

module half_adder(input a,input b,output cout,output s);
xor(s,a,b);
and(cout,a,b);
endmodule
"""
print(module_print)


def wallace_tree_multiplier(N, Modulename):
    verilog_code = ""
    verilog_code += f"module {Modulename} (\n"
    verilog_code += f"\tinput [{N - 1}:0] a,\n"
    verilog_code += f"\tinput [{N - 1}:0] b,\n"
    verilog_code += f"\toutput [{2 * N - 1}:0] p\n"
    verilog_code += ");\n"
    verilog_code += "\n"

    for k in range(N):
        verilog_code += f"wire [{N - 1}:0] partial_product{k + 1};\n"

    for i in range(1, N - 1):
        verilog_code += f"wire [{N - 2}:0] s{i};\n"
        verilog_code += f"wire [{N - 1}:0] c{i};\n"

    verilog_code += f"wire [{N - 1}:0] c{N - 1};\n"
    verilog_code += "wire c;\n"
    verilog_code += f"wire [{2 * N - 1}:0] p;\n"
    verilog_code += f"wire [{N - 1}:0] si;\n"

    count = 0
    for k in range(N - 1):
        for j in range(N):
            verilog_code += f"and (partial_product{k + 1}[{j}], b[{k}], a[{j}]);\n"
            count += 1
        verilog_code += f"not (si[{k}], partial_product{k + 1}[{N - 1}]);\n"

    for i in range(N):
        verilog_code += f"and (partial_product{N}[{i}], b[{N - 1}], ~a[{i}]);\n"
    verilog_code += f"not (si[{N - 1}], partial_product{N}[{N - 1}]);\n"

    s, r, t = 1, 1, 1

    verilog_code += f"half_adder ha{s} (partial_product1[1], partial_product2[0], c1[0], p[1]);\n"
    s += 1
    for i in range(1, N - 1):
        verilog_code += f"full_adder fa{r}_{t} (partial_product1[{i + 1}], partial_product2[{i}], partial_product3[{i - 1}], c1[{i}], s1[{i - 1}]);\n"
        t += 1
    r += 1
    verilog_code += f"full_adder fa{r}_{t} (si[0], si[1], partial_product3[{N - 2}], c1[{N - 1}], s1[{N - 2}]);\n"

    for i in range(2, N - 1):
        t = 0
        verilog_code += f"// layer {i}\n"
        verilog_code += f"half_adder ha{s} (s{i - 1}[0], c{i - 1}[0], c{i}[0], p[{i}]);\n"
        s += 1
        for j in range(1, N - 1):
            verilog_code += f"full_adder fa{r}_{t} (s{i - 1}[{j}], c{i - 1}[{j}], partial_product{i + 2}[{j - 1}], c{i}[{j}], s{i}[{j - 1}]);\n"
            t += 1
        verilog_code += f"full_adder fa{r}_{t} (si[{i}], c{i - 1}[{N - 1}], partial_product{i + 2}[{N - 2}], c{i}[{N - 1}], s{i}[{N - 2}]);\n"
        r += 1

    # Last layer
    verilog_code += f"full_adder fad{N - 1}_{t} (s{N - 2}[0], c{N - 2}[0], b[{N - 1}], c{N - 1}[0], p[{N - 1}]);\n"
    t += 1
    for i in range(1, N - 1):
        verilog_code += f"full_adder fad{N - 1}_{t} (s{N - 2}[{i}], c{N - 2}[{i}], c{N - 1}[{i - 1}], c{N - 1}[{i}], p[{N + i - 1}]);\n"
        t += 1
    verilog_code += f"full_adder fad{N - 1}_{t} (si[{N - 1}], c{N - 2}[{N - 1}], c{N - 1}[{N - 2}], c{N - 1}[{N - 1}], p[{2 * N - 2}]);\n"
    verilog_code += f"half_adder ha{N} (c{N - 1}[{N - 1}], 1'b1, c, p[{2 * N - 1}]);\n"
    verilog_code += "assign p[0] = partial_product1[0];\n"

    verilog_code += "endmodule\n"

    return verilog_code


# Example usage:
N = 16  # Number of bits
Modulename = "WallaceTreeMultiplier"
verilog_code = wallace_tree_multiplier(N, Modulename)
print(verilog_code)