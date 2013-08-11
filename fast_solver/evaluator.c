#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "evaluator.h"

// Public API

typedef struct {
    bv_int64 id;
    bv_int64 id2;
    bv_int64 id3;
    bv_program *program;
} bv_eval_state;


static bv_int64 _bv_eval(bv_eval_state *);

bv_int64 bv_eval(bv_program *p, bv_int64 x)
{
    bv_eval_state state;
    state.id = x;
    state.program = p;
    return _bv_eval(&state);
}


static bv_int64 _bv_eval_arg(bv_eval_state *state, bv_program *arg)
{
    bv_program *prev = state->program;
    state->program = arg;
    bv_int64 val = _bv_eval(state);
    state->program = prev;
    return val;
}


#define CALL_BINARY_ON_EVALED(program, func) \
    func(_bv_eval_arg(state, program->args[0]), \
         _bv_eval_arg(state, program->args[1]))

#define HANDLE_BINARY_CASE(operator, func) case (operator): { \
    return CALL_BINARY_ON_EVALED(state->program, func); \
}

#define CALL_UNARY_ON_EVALED(program, func) \
    func(_bv_eval_arg(state, program->args[0]))


#define HANDLE_UNARY_CASE(operator, func) case (operator): { \
    return CALL_UNARY_ON_EVALED(state->program, func); \
}

#define FOLD_ITERATION() { \
    state->id2 = iterable & 255; \
    state->id3 = _bv_eval_arg(state, state->program->args[2]); \
    iterable >>= 8; \
}


bv_int64 xor(bv_int64 a, bv_int64 b)
{
    return a ^ b;
}


bv_int64 and(bv_int64 a, bv_int64 b)
{
    return a & b;
}


bv_int64 or(bv_int64 a, bv_int64 b)
{
    return a |  b;
}


bv_int64 plus(bv_int64 a, bv_int64 b)
{
    return a + b;
}


bv_int64 not(bv_int64 a)
{
    return ~a;
}


bv_int64 shl1(bv_int64 a)
{
    return a << 1;
}


bv_int64 shr1(bv_int64 a)
{
    return a >> 1;
}


bv_int64 shr4(bv_int64 a)
{
    return a >> 4;
}


bv_int64 shr16(bv_int64 a)
{
    return a >> 16;
}

// Implementation starts
static bv_int64 _bv_eval(bv_eval_state *state)
{

    bv_operator_id operator_id = state->program->operator_id;

    //printf("EVAL %d\n", operator_id);

    switch (operator_id)
    {
        case ZERO: return 0;
        case ONE: return 1;
        case ID: return state->id;
        case ID2: return state->id2;
        case ID3: return state->id3;

        HANDLE_BINARY_CASE(XOR, xor);
        HANDLE_BINARY_CASE(OR, or);
        HANDLE_BINARY_CASE(AND, and);
        HANDLE_BINARY_CASE(PLUS, plus);

        HANDLE_UNARY_CASE(NOT, not);
        HANDLE_UNARY_CASE(SHL1, shl1);
        HANDLE_UNARY_CASE(SHR1, shr1);
        HANDLE_UNARY_CASE(SHR4, shr4);
        HANDLE_UNARY_CASE(SHR16, shr16);

        case IF0: {
            bv_int64 predicate = _bv_eval_arg(state, state->program->args[0]);

            if (predicate == 0)
            {
                return _bv_eval_arg(state, state->program->args[1]);
            }
            else
            {
                return _bv_eval_arg(state, state->program->args[2]);
            }
        };
        case FOLD: {
            // id3 -- accumulator
            state->id3 = _bv_eval_arg(state, state->program->args[1]);

            bv_int64 iterable = _bv_eval_arg(state, state->program->args[0]);

            FOLD_ITERATION();
            FOLD_ITERATION();
            FOLD_ITERATION();
            FOLD_ITERATION();
            FOLD_ITERATION();
            FOLD_ITERATION();
            FOLD_ITERATION();
            FOLD_ITERATION();

            return state->id3;
        };
        default: break;
    }

    return state->id;
}
