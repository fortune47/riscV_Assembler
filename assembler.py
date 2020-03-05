r_type = {}
r_type["add"] = {}
r_type["add"]["opcode"] = "0110011"
r_type["add"]["funct3"] = "000"
r_type["add"]["funct7"] = "0000000"

r_type["sll"] = {}
r_type["sll"]["opcode"] = "0110011"
r_type["sll"]["funct3"] = "001"
r_type["sll"]["funct7"] = "0000000"

r_type["srl"] = {}
r_type["srl"]["opcode"] = "0110011"
r_type["srl"]["funct3"] = "101"
r_type["srl"]["funct7"] = "0000000"

r_type["xor"] = {}
r_type["xor"]["opcode"] = "0110011"
r_type["xor"]["funct3"] = "100"
r_type["xor"]["funct7"] = "0000000"

r_type["mul"] = {}
r_type["mul"]["opcode"] = "0110011"
r_type["mul"]["funct3"] = "000"
r_type["mul"]["funct7"] = "0000001"


i_type = {}
i_type["addi"] = {}
i_type["addi"]["opcode"] = "0010011"
i_type["addi"]["funct3"] = "000"


i_type["slli"] = {}
i_type["slli"]["opcode"] = "0010011"
i_type["slli"]["funct3"] = "001"


i_type["srli"] = {}
i_type["srli"]["opcode"] = "0010011"
i_type["srli"]["funct3"] = "101"


i_type["ori"] = {}
i_type["ori"]["opcode"] = "0010011"
i_type["ori"]["funct3"] = "110"
#i_type["ori"]["shift"] = "000000"

i_type["andi"] = {}
i_type["andi"]["opcode"] = "0010011"
i_type["andi"]["funct3"] = "111"
#i_type["andi"]["shift"] = "000000"


b_type = {}
b_type["beq"] = {}
b_type["beq"]["opcode"] = "1100011"
b_type["beq"]["funct3"] = "000"

b_type["bne"] = {}
b_type["bne"]["opcode"] = "1100011"
b_type["bne"]["funct3"] = "001"


registers = {}
registers["zero"] = 0
registers["ra"] = 1
registers["sp"] = 2
registers["gp"] = 3
registers["tp"] = 4
registers["t0"] = 5
registers["t1"] = 6
registers["t2"] = 7
registers["s0"] = 8
registers["fp"] = 8
registers["s1"] = 9
registers["a0"] = 10
registers["a1"] = 11
registers["a2"] = 12
registers["a3"] = 13
registers["a4"] = 14
registers["a5"] = 15
registers["a6"] = 16
registers["a7"] = 17
registers["s2"] = 18
registers["s3"] = 19
registers["s4"] = 20
registers["s5"] = 21
registers["s6"] = 22
registers["s7"] = 23
registers["s8"] = 24
registers["s9"] = 25
registers["s10"] = 26
registers["s11"] = 27
registers["t3"] = 28
registers["t4"] = 29
registers["t5"] = 30
registers["t6"] = 31


registers["x0"] = 0
registers["x1"] = 1
registers["x2"] = 2
registers["x3"] = 3
registers["x4"] = 4
registers["x5"] = 5
registers["x6"] = 6
registers["x7"] = 7
registers["x8"] = 8
registers["x9"] = 9
registers["x10"] = 10
registers["x11"] = 11
registers["x12"] = 12
registers["x13"] = 13
registers["x14"] = 14
registers["x15"] = 15
registers["x16"] = 16
registers["x17"] = 17
registers["x18"] = 18
registers["x19"] = 19
registers["x20"] = 20
registers["x21"] = 21
registers["x22"] = 22
registers["x23"] = 23
registers["x24"] = 24
registers["x25"] = 25
registers["x26"] = 26
registers["x27"] = 27
registers["x28"] = 28
registers["x29"] = 29
registers["x30"] = 30
registers["x31"] = 31

def padZeros(binStr, size):
	while len(binStr) < size:
		binStr = "0" + binStr

	return binStr


def getBinFromBase10(register):
	return str(bin(registers[register]))[2:]


def getMachineCode(statement):

	if statement.find(":"):
		statement = statement[statement.find(":") + 1:].strip()
	
	command = statement[ : statement.find(" ")]
	regs = statement[ statement.find(" ") : ].split(",")
	for i in range(len(regs)):
		regs[i] = regs[i].strip()

	machine_code = ""

	if command in r_type:
		f7 = r_type[command]["funct7"]
		rs2 = getBinFromBase10(regs[2])
		rs1 = getBinFromBase10(regs[1])
		rd = getBinFromBase10(regs[0])
		f3 = r_type[command]["funct3"]
		opcode = r_type[command]["opcode"]

		rs2 = padZeros(rs2, 5)
		rs1 = padZeros(rs1, 5)
		rd = padZeros(rd, 5)

		machine_code = f7 + rs2 + rs1 + f3 + rd + opcode

		machine_code = hex(int(machine_code, 2))

	elif command in i_type:
		immd = regs[2]
		immd = (bin(int(immd)&0b111111111111)).replace("-0b", "")
		immd = str(immd)
		immd = immd.replace("0b", "")
		rs1 = getBinFromBase10(regs[1])
		f3 = i_type[command]["funct3"]
		rd = getBinFromBase10(regs[0])
		opcode = i_type[command]["opcode"]

		immd = padZeros(immd, 12)
		rs1 = padZeros(rs1, 5)
		rd = padZeros(rd, 5)

		machine_code = immd + rs1 + f3 + rd + opcode

		machine_code = hex(int(machine_code, 2))
		
	elif command in b_type:
		immd = regs[2]
		immd = bin(int(immd)&0b1111111111111)
		immd = str(immd)
		immd = immd.replace("-0b", "")
		immd = immd.replace("0b", "")
		immd = padZeros(immd, 13)

		rs2 = getBinFromBase10(regs[1])
		rs1 = getBinFromBase10(regs[0])
		f3 = b_type[command]["funct3"]
		opcode = b_type[command]["opcode"]

		rs2 = padZeros(rs2, 5)
		rs1 = padZeros(rs1, 5)

		machine_code = immd[0] + immd[2:8] + rs2 + rs1 + f3 + immd[8:12] + immd[1] + opcode

		machine_code = hex(int(machine_code, 2))

	machine_code = str(machine_code)[2:]
	machine_code = padZeros(machine_code, 8)
	machine_code = "0x" + machine_code
	return machine_code

if __name__ == "__main__":

	with open("test_code.s", "r") as f:
		while True:
			statement = f.readline()
			if not statement:
				break

			print(getMachineCode(statement))
