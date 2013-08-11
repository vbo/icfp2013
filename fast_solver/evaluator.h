#ifndef _EVALUATOR
#define _EVALUATOR

#include <stdint.h>

typedef uint64_t bv_int64;

typedef enum {
    ZERO,
    ONE,
    ID,
    ID2,
    ID3,
    IF0,
    FOLD,
    XOR,
    OR,
    AND,
    PLUS,
    NOT,
    SHL1,
    SHR1,
    SHR4,
    SHR16
} bv_operator_id;

typedef struct bv_program_struct {
    bv_operator_id operator_id;
    unsigned char argc;
    struct bv_program_struct **args;
} bv_program;

bv_program *bv_parse(char *formula);
bv_int64 bv_eval(bv_program *p, bv_int64 x);
void bv_free(bv_program *bv);

#endif
