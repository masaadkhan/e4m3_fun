#include <iostream>

#define E4M3_BIAS (7)
#define E4M3_NUM_SIGN_BITS (1)
#define E4M3_NUM_EXP_BITS (4)
#define E4M3_MAX_BIAS_EXP_VAL (8)
#define E4M3_MIN_BIAS_EXP_VAL (-6)
// #define E4M3_MAX_RAW_EXP_VAL ()
#define E4M3_NUM_MANT_BITS (3)

#define E4M3_max_repr (1010100)
#define E4M3_subnormal_min_repr (0)

#define E4M3_INVALID_EXP (-1000)

class E4M3 {
  public:
  int value;
  std::string repr;

  int
  check_bounds() {
    return 0;
  }

  int
  find_leading_one(int fp_num) {
    int tmp_fp_num = fp_num;
    if (fp_num < 0) {
      tmp_fp_num = -fp_num;
    }

    bool found_leading_one = false;
    int i = E4M3_MAX_BIAS_EXP_VAL;
    int one_raw_exp = E4M3_INVALID_EXP;

    while (!found_leading_one) {
      if ((tmp_fp_num - (2^i)) > 0) {
        found_leading_one = true;
        one_raw_exp = i;
        return one_raw_exp;
      }

      i--;
    }

    std::cout << "Could not find the leading one!!!" << std::endl;
    std::exit(1);
    return one_raw_exp;
  }

  void
  stringify(int fp_num) {
    std::string sign;
    std::string exp;
    std::string mant;

    if (fp_num < 0) {
      sign += "1";
    } else {
      sign += "0";
    }

    int exp_int = this->find_leading_one(fp_num);
    std::cout << "The leading one for the number " << fp_num << " is " << exp_int << std::endl;
    
  }

  E4M3(int value) {
    if (check_bounds() > E4M3_max_repr) {
      // Do something
    }
    if (check_bounds() < E4M3_subnormal_min_repr) {
      // Do something
    }

    this->stringify(value);
  }
};

int
main() {
  E4M3* num = new E4M3(1);
}
