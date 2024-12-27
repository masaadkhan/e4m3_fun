E4M3_BIAS = 7

SIGN_BITS = 1
EXP_BITS = 4
MANT_BITS = 3

# def extract_e4m3_info(fp_int):
#   tmp_fp = fp_int

#   print(f"tmp_fp: {tmp_fp}")
#   sign = tmp_fp[0]

#   tmp_fp = tmp_fp[1:]
#   print(f"tmp_fp: {tmp_fp}")

#   mant = tmp_fp[-MANT_BITS:]
#   exp = tmp_fp[:-MANT_BITS]
#   print(f"tmp_fp: {tmp_fp}")

#   # print(f"sign: {sign}")
#   # print(f"exp: {exp}")
#   # print(f"mant: {mant}")

#   total = sign + exp + mant

#   # print(f"Total: {total}")
#   # print(f"fp_int: {fp_int}")

#   if (total != fp_int):
#     exit("ERROR: The combination is not the same!!!")

#   return (sign, int(exp, 2) - E4M3_BIAS, mant)

def verilog_width(*args):
  if (len(args) == 2):
    bin_str = args[0]
    bit_pos = len(bin_str) - args[1] - 1

    return bin_str[bit_pos]

  elif (len(args) == 3):
    bin_str = args[0]

    start = len(bin_str) - args[1] - 1
    end = len(bin_str) - args[2]

    if (args[1] - args[2] + 1) != len(bin_str[start : end]):
      exit("ERROR: verilog_width doesn't match!!!")

    return bin_str[start : end]

  else:
    exit("ERROR!")

def mant_str_to_float(exp, mant_str):
  # Subnormal
  if (exp == 0):
    mant = 0
  else:
    mant = 1

  tmp_exp = -1
  for ele in mant_str:
    if (ele == "1"):
      mant = mant + 2**tmp_exp
      # print(mant)
    tmp_exp -= 1

  return mant

def e4m3_min_val():
  min_exp = 0
  # E4M3 specific
  min_mant = mant_str_to_float(0, ("0" * (MANT_BITS - 1)) + "1")
  return -1 * min_mant * (2**(min_exp - E4M3_BIAS))

# E4M3
# S.1111.110
# 15 - 7 = 8
# 1.875 * 2^(8)
def e4m3_max_val():
  max_exp = 2**EXP_BITS - 1
  # E4M3 specific
  max_mant = mant_str_to_float(max_exp, ("1" * (MANT_BITS - 1)) + "0")
  return max_mant * (2**(max_exp - E4M3_BIAS))

def e4m3_min_subnormal_val():
  # E4M3 specific
  min_mant = mant_str_to_float(0, ("0" * (MANT_BITS - 1)) + "1")
  min_sub_exp = E4M3_BIAS - 1

  print(f"1 * {min_mant} * 2^({-min_sub_exp})")
  return min_mant * (2**(-min_sub_exp))

def e4m3_max_subnormal_val():
  # E4M3 specific
  max_mant = mant_str_to_float(0, "1" * MANT_BITS)
  max_sub_exp = E4M3_BIAS - 1

  print(f"1 * {max_mant} * 2^({-max_sub_exp})")
  return max_mant * (2**(-max_sub_exp))

def int_to_e4m3_val(fp_num):
  if (fp_num > e4m3_max_val()):
    exit("ERROR: fp_num is too big...")
  if (fp_num < e4m3_min_val()):
    exit("ERROR: fp_num is too small...")

  # print(f"INT_STR: {bin(fp_num)[2:]}")
  # print(f"INT_STR: {bin(fp_num)[2:].zfill(8)}")

  int_str = bin(fp_num)[2:].zfill(8)

  if (len(int_str) != (SIGN_BITS + EXP_BITS + MANT_BITS)):
    exit("Too many bits in the provided integer... Integer too big....")

  sign_str = verilog_width(int_str, 7)
  mant_str = verilog_width(int_str, 2, 0)
  exp_str = verilog_width(int_str, 6, 3)

  if (exp_str == "1111" and mant_str == "111"):
    # NaN
    return "NaN"

  if (sign_str == "1"):
    if (exp_str == "0000" and mant_str == "000"):
      # Negative 0
      return "-0"
  else:
    if (exp_str == "0000" and mant_str == "000"):
      # Positive 0
      return "+0"

  exp_int = int(exp_str, 2)
  # sign_str, exp_val, mant_str = extract_e4m3_info(int_str)
  mant = mant_str_to_float(exp_int, mant_str)
  exp_val = exp_int - E4M3_BIAS

  # print(f"mantissa: {mant}")
  # print(f"exponent: {exp_val}")
  print(f"{"-1" if (sign_str == "1") else "1"} * {mant} * 2^({exp_val})")

  return (-1 if (sign_str == "1") else 1) * mant * (2 ** exp_val)
