from flask import Flask, render_template, request
import math
app = Flask(__name__)
def generate_wallace_verilog_code(N, Modulename):
 def wallace_tree_multiplier(N, Modulename):
    verilog_code = """
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
    verilog_code += ""
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

 return wallace_tree_multiplier(N, Modulename)
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
            [f"    booth_step1 step{i}(A{i}, Q{i}, q0[{i}], b, A{i + 1}, Q{i + 1}, q0[{i + 1}]);" for i in
             range(1, n - 1)])

        verilog_code += booth_step1_instances + f"""
        booth_step1 step{n - 1}(A{n - 1}, Q{n - 1}, q0[{n - 1}], b, p[{2 * n - 1}:{n}], p[{n - 1}:0], qout);
    endmodule
        """
        return verilog_code
def generate_kogge_stone_verilog_code(N, Modulename):


    def kogge_stone(N, Modulename):
        verilog_code = """
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
        ports = f"input [{N - 1}:0] x,y,\noutput [{N - 1}:0] sum,\noutput cout\n"
        W = f"wire [{N - 1}:0]"
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

        verilog_code += f"module {Modulename} (\n{ports});\n\n{W}\n\n{a}\n{b}\n{c}\nendmodule"
        return verilog_code

    return kogge_stone(N, Modulename)

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    verilog_code = None

    if request.method == 'POST':
        try:
            if 'num_bits' in request.form:
                num_bits = int(request.form['num_bits'])
                verilog_code = generate_wallace_verilog_code(num_bits, "wallace_tree_multiplier")
            elif 'booth_bits' in request.form:
                booth_bits = int(request.form['booth_bits'])
                verilog_code = generate_booth_multiplier_verilog(booth_bits)
            elif 'kogge_bits' in request.form:
                kogge_bits = int(request.form['kogge_bits'])
                verilog_code = generate_kogge_stone_verilog_code(kogge_bits, "KoggeStoneAdder")

        except Exception as e:
            error_message = str(e)

    return render_template('index.html', verilog_code=verilog_code, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)