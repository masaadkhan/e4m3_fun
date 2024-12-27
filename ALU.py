from e4m3 import *

def find_leading_one(fp_str):
  i = 0
  while (i < len(fp_str)):
    if (fp_str[i] == "1"):
      return i
    i += 1

def zrfill(fp_str, size):
  if (len(fp_str) < size):
    i = size - len(fp_str)
    while (i >= 1): # One-indexed
      fp_str += "0"
      i -= 1
  else:
    fp_str = fp_str[:3]

  return fp_str


def multiply(a, b):
  print("")
  print(f"Multiplying {a} and {b}")
  print("")

  a_sign = a[0]
  a_exp = a[SIGN_BITS : EXP_BITS + 1]
  a_mant = a[SIGN_BITS + EXP_BITS :]
  a_adjusted_mant = "1" + a_mant

  b_sign = b[0]
  b_exp = b[SIGN_BITS : EXP_BITS + 1]
  b_mant = b[SIGN_BITS + EXP_BITS :]
  b_adjusted_mant = "1" + b_mant

  a_sign = -1 if (a_sign == "1") else 1
  b_sign = -1 if (a_sign == "1") else 1

  c_sign = a_sign * b_sign
  c_sign = "1" if (c_sign == -1) else "0"
  c_exp = bin((int(a_exp, 2) - E4M3_BIAS) + (int(b_exp, 2) - E4M3_BIAS) + E4M3_BIAS)[2:].zfill(EXP_BITS)

  # print(a_adjusted_mant)
  # print(b_adjusted_mant)

  c_preadjust_mant = bin(int(a_adjusted_mant, 2) * int(b_adjusted_mant, 2))[2:].zfill(MANT_BITS)
  leading_idx = find_leading_one(c_preadjust_mant)
  
  # print(f"preadjusted_mant: {c_preadjust_mant}")
  # print(f"Leading index: {leading_idx}")
  c_preadjust_mant = c_preadjust_mant[leading_idx + 1: ]
  c_preadjust_mant = zrfill(c_preadjust_mant, MANT_BITS)
  # print(f"preadjusted_mant: {c_preadjust_mant}")
  c_mant = c_preadjust_mant

  # exit()

  # shift = count_exp_shift(c_preadjust_mant)
  # c_exp += shift

  print(f"c_sign: {c_sign}")
  print(f"c_exp: {c_exp}")
  print(f"c_mant: {c_mant}")

  print(f"c: {c_sign}{c_exp}{c_mant}")


# Takes in an fp number, positive or negative, < 0 or >= 0 and creates an 8-bit binary string
def fp_bin(fp_num):
  fp_str = ""

  if (fp_num > e4m3_max_val() or fp_num < -e4m3_max_val()):
    exit("ERROR: Passed an FP number that can't be represented")

  # fp_num[7]
  i = None
  raw_sign = None
  if (fp_num < 0):
    fp_str += "1"
    i = 6
    raw_sign = 1
  elif (fp_num == 0):
    return "00000000"
  else:
    # fp_str += "0"
    i = 7
    raw_sign = 0
    pass

  # imagine fp_num == 1
  tmp = fp_num
  leading_one_idx = None
  while (len(fp_str) != 8):
    if (fp_num > 0):
      print(f"This is tmp: {tmp}")
      if (tmp == 0):
        fp_str += "0"
      else:
        calc = tmp - 2**i
        print(f"calc: {calc}, i: {i}, fp_str: {fp_str}")

        if (len(fp_str) != 0):
          if (calc < 0):
            fp_str += "0"
          if (calc == 0 and len(fp_str) != 0):
            # print("Hit")
            fp_str += "1"
            tmp = calc

        elif (calc >= 0):
          if (len(fp_str) == 0):
            leading_one_idx = i
          fp_str += "1"
          tmp = calc

    i -= 1
    input()
  
  # print(f"This is the fp_str: {fp_str}")
  # print(f"This is the exponent of the leading one: {leading_one_idx}")

  # Denormal number...
  if (leading_one_idx < 0):
    print("Found a denormal number")
    return "00000000"
  else:
    if (len(fp_str) != 8):
      exit("FP_STR is not the correct size!!!")

    derived_mant = fp_str[1:1+MANT_BITS]
    derived_bias_exp = bin(leading_one_idx + E4M3_BIAS)[2:].zfill(EXP_BITS)

    # print(f"Raw sign: {raw_sign}")
    # print(f"Derived exp: {derived_bias_exp}")
    # print(f"Derived this mantissa: {derived_mant}")

    # print(f"E4M3 representation: {raw_sign}{derived_bias_exp}{derived_mant}")
    return f"{raw_sign}{derived_bias_exp}{derived_mant}"




def convert_int_to_e4m3_raw(num):
  # Technically if you want to do subnormal numbers or something, you'd have to use floating point or something

  # Wonder how you'd represent the number "5" using this method, maybe you have to find the smaller/bigger estimate and then convert to E4M3

  # num_bin = bin(num)[2:].zfill(8)
  fp_str = fp_bin(num)
  # print(f"num_bin: {num_bin}")
  # exit()

  # if (len(num_bin) != 8):
  #   exit("ERROR: num_bin size does not fit in E4M3 size....")

  # i = 0
  # while (i < len(num_bin)):
  #   if (num_bin[i] == "1"):
  #     break
  #   i += 1
  # i += 1 # One-index

  # print(f"Found leading one at idx: {i}")
  # raw_exp = (SIGN_BITS + EXP_BITS + MANT_BITS) - i
  # biased_exp = raw_exp + E4M3_BIAS
  # mant = num_bin[i:]

  # if (num < 0):
  #   raw_sign = "1"
  # else:
  #   raw_sign = "0"

  # biased_exp_str = bin(biased_exp)[2:].zfill(EXP_BITS)
  # mant_str = mant.zfill(MANT_BITS)

  raw_sign_str = fp_str[0]
  biased_exp_str = fp_str[SIGN_BITS : EXP_BITS + 1]
  mant_str = fp_str[SIGN_BITS + EXP_BITS :]

  # print(f"This is the parsed raw_sign: {raw_sign_str}")
  # print(f"This is the parsed biased_exp: {biased_exp_str}")
  # print(f"This is the parsed mantissa: {mant_str}")

  # print(f"E4M3 number: {raw_sign_str}{biased_exp_str}{mant_str}")
  return f"{raw_sign_str}{biased_exp_str}{mant_str}"

if __name__ == "__main__":
  # We want to multiply 2 E4M3 numbers

  # Wonder how you would write a function converting a floating point to a raw E4M3 int?

  # Write a function that takes an int and converts an E4M3 raw int
  # Int: 3 ; E4M3_RAW: S.1000.100
  # Convert the int to binary
  # Find the leading 1
  # Shift the bin such that the leading 1 is used for mantissa

  # print(f"E4M3 min val: {e4m3_min_val()}\n")
  # print(f"E4M3 max val: {e4m3_max_val()}\n")
  # print(f"E4M3 max subnormal val: {e4m3_max_subnormal_val()}\n")
  # print(f"E4M3 min subnormal val: {e4m3_min_subnormal_val()}\n")

  # print(f"int ({254}) to e4m3 ({int_to_e4m3_val(254)})")

  # print(f"First: {zrfill("", 3)}")
  # print(f"Second: {zrfill("00", 3)}")
  # print(f"Third: {zrfill("000", 3)}")
  # print(f"Fourth: {zrfill("0000", 3)}")
  # exit()

  # a = convert_int_to_e4m3_raw(1)
  # b = convert_int_to_e4m3_raw(1)
  # multiply(a, b)

  # a = convert_int_to_e4m3_raw(3)
  # b = convert_int_to_e4m3_raw(4)
  # multiply(a, b)

  # a = convert_int_to_e4m3_raw(1)
  # b = convert_int_to_e4m3_raw(4)
  # multiply(a, b)

  # a = convert_int_to_e4m3_raw(3)
  # b = convert_int_to_e4m3_raw(1)
  # multiply(a, b)

  # a = convert_int_to_e4m3_raw(5)
  # b = convert_int_to_e4m3_raw(1)
  # multiply(a, b)

  # a = convert_int_to_e4m3_raw(1)
  # b = convert_int_to_e4m3_raw(5)
  # multiply(a, b)

  # a = convert_int_to_e4m3_raw(2)
  # b = convert_int_to_e4m3_raw(12)
  # multiply(a, b)

  a = convert_int_to_e4m3_raw(448)
  b = convert_int_to_e4m3_raw(12)
  multiply(a, b)
