#define INVALID_EXP (-9999)
#define E4M3_MAX_BIAS_EXP_VAL (8)
#define E4M3_NUM_MANT_BITS (3)

#include <string>
#include <iostream>

// TODO: First take in integers, and then floats afterwards...
void
approximate_int_to_bin_str(int fp_number, int& leading_one_exp, std::string& mant_str) {
  // Convert this int to a binary string
  // Find the leading "1" in the binary string and start recording the next 8 digits
  float tmp_fp_number = fp_number;

  // 78 - 128 = negative
  // 78 - 64 = positive
  // 64 - 64 = 0

  // leading_one_exp = 1
  // 2 digit fp
  // go two more
  // -1

  int exp = E4M3_MAX_BIAS_EXP_VAL;
  leading_one_exp = INVALID_EXP;

  while (mant_str.size() < 7) {
    std::cout << "mant_str: " << mant_str << std::endl;

    if (tmp_fp_number == 0) {
      mant_str += "0";
      continue;
    }

    int exponent_remainder = tmp_fp_number - std::pow(2, exp);
    std::cout << "tmp_fp_number: " << tmp_fp_number << " " <<
                 "exp: " << exp << " " <<
                 "exponent_remainder: " << exponent_remainder << std::endl;

    if (exponent_remainder >= 0) {
      // Found a one
      if (leading_one_exp == INVALID_EXP) {
        leading_one_exp = exp;
        std::cout << "Found leading_one_exp: " << leading_one_exp << std::endl;
      }
      tmp_fp_number = exponent_remainder;
      mant_str += "1";
    } else if (mant_str.size() != 0) {
      mant_str += "0";
    }

    exp -= 1;
  }

  // std::cout << "Not sure if we should even hit this right now..." << std::endl;
  // std::exit(1);
  // return mant_str;
}

void
convert_bin_str_to_e4m3(int leading_exp, std::string bin_str) {

}

int
main (void) {
  std::string bin_str = "";
  int leading_one = INVALID_EXP;

  approximate_int_to_bin_str(1, leading_one, bin_str);
  std::cout << "This is the value of leading_one: " << leading_one << std::endl;
  std::cout << "This is the value of bin_str: " << bin_str << std::endl;
  convert_bin_str_to_exp(leading_one, bin_str);

  // std::cout << "This is the bin_str: " << approximate_int_to_bin_str(1, leading_one, mant) << std::endl;
}
