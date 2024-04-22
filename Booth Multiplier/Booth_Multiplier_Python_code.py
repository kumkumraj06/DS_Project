#Booth Multiplier

def generate_booth_multiplier_verilog(n):
    verilog_code = f"""
module full_adder(a,b,cin,s,cout);
    input a,b,cin;
    output s,cout;
    wire r,r1,r2;
    xor (s,a, b, cin);
    and (r, a, b);
    and (r1, b, cin);
    and (r2, a, cin);
    or (cout, r, r1, r2);
endmodule

module subtractor(a, b, sum);
    input [{n - 1}:0] a, b;
    output [{n - 1}:0] sum;
    wire [{n - 1}:0] ib;
    wire cout;

    """
    not_gate = "\n".join([f"    not (ib[{i}], b[{i}]);" for i in range(n)])

    verilog_code += not_gate + f"""

    wire [{n - 1}:0] q;
    full_adder full_adder0(a[0], ib[0], 1'b1, sum[0], q[0]);
    """
    full_adder_instances = "\n".join(
        [f"    full_adder full_adder{i}(a[{i}], ib[{i}], q[{i - 1}], sum[{i}], q[{i}]);" for i in range(1, n - 1)])

    verilog_code += full_adder_instances + f"""
    full_adder full_adder{n - 1}(a[{n - 1}], ib[{n - 1}], q[{n - 2}], sum[{n - 1}], cout);
endmodule

module Adder(a, b, sum);
    input [{n - 1}:0] a, b;
    output [{n - 1}:0] sum;
    wire cout;
    wire [{n - 1}:0] q;

    full_adder full_adder0(a[0], b[0], 1'b0, sum[0], q[0]);
    """
    full_adder_instances = "\n".join(
        [f"    full_adder full_adder{i}(a[{i}], b[{i}], q[{i - 1}], sum[{i}], q[{i}]);" for i in range(1, n - 1)])

    verilog_code += full_adder_instances + f"""
    full_adder full_adder{n - 1}(a[{n - 1}], b[{n - 1}], q[{n - 2}], sum[{n - 1}], cout);
endmodule

module booth_step1(input [{n - 1}:0] a, Q, input q0, input [{n - 1}:0] m, output reg [{n - 1}:0] f8, output reg [{n - 1}:0] l8, output reg cq0);
    wire [{n - 1}:0] r, s;
    Adder add(a, m, r);
    subtractor sub(a, m, s);
    always @(*) begin
        if (Q[0] == q0) begin
            cq0 = Q[0];
            l8 = Q >> 1;
            l8[{n - 1}] = a[0];
            f8 = a >> 1;
            if (a[{n - 1}] == 1)
                f8[{n - 1}] = 1;
        end
        else if (Q[0] == 1 && q0 == 0) begin
            cq0 = Q[0];
            l8 = Q >> 1;
            l8[{n - 1}] = s[0];
            f8 = s >> 1;
            if (s[{n - 1}] == 1)
                f8[{n - 1}] = 1;
        end
        else begin
            cq0 = Q[0];
            l8 = Q >> 1;
            l8[{n - 1}] = r[0];
            f8 = r >> 1;
            if (r[{n - 1}] == 1)
                f8[{n - 1}] = 1;
        end
    end
endmodule

module booth_multiplier(input [{n - 1}:0] a, b, output [{2 * n - 1}:0] p);
    wire [{n - 1}:0] {'Q' + ', '.join([f'Q{i}' for i in range(n)])};
    wire [{n - 1}:0] m;
    wire [{n - 1}:0] {'A' + ', '.join([f'A{i}' for i in range(n)])};
    wire [{n - 1}:0] q0;
    wire qout;

    booth_step1 step0(0, a, 1'b0, b, A1, Q1, q0[1]);
    """
    booth_step1_instances = "\n".join(
        [f"    booth_step1 step{i}(A{i}, Q{i}, q0[{i}], b, A{i + 1}, Q{i + 1}, q0[{i + 1}]);" for i in range(1, n - 1)])

    verilog_code += booth_step1_instances + f"""
    booth_step1 step{n - 1}(A{n - 1}, Q{n - 1}, q0[{n - 1}], b, p[{2 * n - 1}:{n}], p[{n - 1}:0], qout);
endmodule
    """
    return verilog_code


# Example usage: Generate Verilog code for a 16-bit Booth multiplier
n_bits = 16
verilog_code_16bit = generate_booth_multiplier_verilog(n_bits)
print(verilog_code_16bit)