import unittest
from nose.exc import SkipTest
import tempfile

from .. import solver
from ..lang import Int64, op
from ..tools import build_formula_index

class SolverTestCase(unittest.TestCase):

    def test_top_level_const(self):
        self.assertEquals(solver._solve("(lambda (t) 0)", 0), 0)
        self.assertEquals(solver._solve("(lambda (t) 1)", 0), 1)

    def test_top_level_arg(self):
        self.assertEquals(solver._solve("(lambda (t) t)", 31337), 31337)

    def test_top_level_op1(self):
        self.assertEquals(solver._solve("(lambda (t) (not 0))", 0), op.not_(0))
        self.assertEquals(solver._solve("(lambda (t) (not t))", 8), op.not_(8))
        self.assertEquals(solver._solve("(lambda (t) (shl1 t))", 8), op.shl1(8))

    def test_top_level_fold(self):
        self.assertEquals(solver._solve("(lambda (x) (fold x 1 (lambda (y z) z)))", 1), 1)
        self.assertEquals(solver._solve("(lambda (x_19527) (fold x_19527 0 (lambda (x_19527 x_19528) "
                                       "(shr1 (if0 (and (shr4 x_19528) (and x_19527 x_19527)) "
                                       "x_19527 x_19528)))))", Int64(0x123123)), 0)
        self.assertEquals(solver._solve("(lambda (x) (fold x 0 (lambda (y z) (or y z))))",
                                       Int64(0x1122334455667788)), 0x00000000000000FF)
        self.assertEquals(
            solver._solve("(lambda (x_45397) (fold x_45397 0 (lambda (x_45397 x_45398) "
                         "(if0 (shr1 (plus (plus (shr4 (shr16 (or (or (shl1 x_45398) 0) x_45397))) "
                          "(shl1 x_45397)) x_45397)) x_45397 x_45397))))", Int64(0x1122334455667788)), 0x0000000000000011)

        self.assertEquals(solver._solve("(lambda (x_31742) (or (or (shr16 (or (shr16 (shr4 0)) " 
                                        "(xor (and (if0 (xor (or 1 0) x_31742) 1 1) x_31742) x_31742))) 0) x_31742))", 
                                        Int64(0xABCDEF1234567890)), 0xABCDEFDFFF567CD6)
        self.assertEquals(solver._solve("(lambda (x_36979) (and (shr16 (plus x_36979 (if0 (shr4 (shl1 x_36979))"
                                        " (shr4 0) (shr4 (shr1 (shr1 (not (if0 (plus (shr4 (xor 1 x_36979)) x_36979)"
                                        " x_36979 x_36979)))))))) x_36979))", 
                                        Int64(0xABCDEF1234567890)), 0x0000AD1234546880)
        self.assertEquals(solver._solve("(lambda (x_36979) (and (shr16 (plus x_36979 (if0 (shr4 (shl1 x_36979))"
                                        " (shr4 0) (shr4 (shr1 (shr1 (not (if0 (plus (shr4 (xor 1 x_36979)) x_36979)"
                                        " x_36979 x_36979)))))))) x_36979))", 
                                        Int64(0xFFFFFFFFFFFFFFFF)), 0x0000FFFFFFFFFFFF)
        inputs = [0x0, 0x1, 0xffffffffffffffff, 0x8044164a475823de, 0x9af456ede8430db1, 0x3355cb24d8979ce8, 0xab1f10fe2010aa37, 0xfacaa2ca1fbc043f, 0x9a438ab61cae1844, 0x974ec7007d1d5c12, 0x5c125a931a3dc0b3, 0xefdd6e1021b407ea, 0x48f5bd620377ab36, 0x91277accef2d4454, 0x2215faec7624b01b, 0x40d5d07bb59a341a, 0xf442da7e0c0981d5, 0x2a09ef7a5bfceb4c, 0x92aca4b3e1be3069, 0xae4b9f5cb075bcc7, 0x5aab4c59bb0bd8e8, 0x63f1cb4a99c98b40, 0x57132f7e9741194d, 0x6dde4bcb82309b30, 0x3981f510896cda0c, 0xb5d734d08500994d, 0xab489cec0780084a, 0x3a1c59d6b7a4a9bc, 0x7aa85383406739fc, 0x46ab7713e3a7a03a, 0x2f1525035d582dcb, 0xb59e824a32d530fa, 0x63dc4c2cd43804b5, 0x85d34e0f88d64874, 0xcdc3009fe8019bda, 0x96b8e2ee664857d, 0x2311d47552ff717b, 0x8dc23bb2f64cd998, 0xec7866c05d7841d, 0x707bb40deb12bfba, 0x5e51e41198914266, 0x72a3c9f5d763c8cf, 0x6113937cc26a6375, 0x6c83b61dab838145, 0x3a745c48efe3183a, 0xb051b2030cdac08c, 0x2fcd819cc5c35241, 0x5cbd8c71273a87a1, 0xa1b8fac9d438d9f0, 0xa8ac9df986ce78f5, 0x718e3895ef7e3724, 0x31d16b6561e97dea, 0x321cb20e1d064a0d, 0x482c4ec1eec292e8, 0x2d9d378f8df0a453, 0xaecf9d2f56c87fc3, 0x4488fd728fdcadeb, 0xbff827ee7124c590, 0xc78aed358fa1ccb8, 0x35dc9c0cd08ba76a, 0x80836f2c5f4aa8f0, 0xa02e1d9e8a2cbf31, 0x79ceb5648edcd3a4, 0xa1d9ad380f614c87]
        outputs = [0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000097, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x00000000000000B5, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000]
        for i, a in enumerate(inputs):
            self.assertEquals(solver._solve("(lambda (id) (fold id 0 (lambda (id2 id3) (if0 id3 id2 0))))", Int64(a)), outputs[i])

        inputs = [0x0, 0x1, 0xffffffffffffffff, 0x2219abe04416f96, 0xa077cf0e37127fc6, 0xab71ae29047479b8, 0x4ac8bbf6614e023, 0xc71cf027608a7c71, 0xfe3096de18a687f1, 0xd620a1df607f2c2a, 0x41ca689d6aef148b, 0x9af769cc362d2b95, 0x537409691dfcee1f, 0x9892e5ef90beaeb5, 0x8f4ba748f96269da, 0x582d08ce34753010, 0x18e9862bd9e76bc5, 0xf2337a6b976bc10e, 0x6328c59ae3c48889, 0x9f7c85698eaf6df6, 0x5a7bf4a0a03bbf9b, 0x8dfb2db7e034967f, 0xe8cdee80940c840f, 0x422111dd0c8d029a, 0x4722f6922e15b9f1, 0xd493baaf9891eec5, 0x42755ecad1914aeb, 0x3ce1c58d13bfc252, 0x35e2320ecfc72482, 0x29ae2aea58ed517f, 0x8112f2a40232b7e4, 0x93d7d718d4cff331, 0x599360cef1447730, 0xf18db68940452498, 0xc8f32bb02c462e44, 0x9faa9427d7c2109, 0x117f5f544c55131, 0x22e09f997d8ee361, 0x542d1aef6403ef68, 0xf721f0fc9eeb2aee, 0x67d357dc18c2470e, 0x6f3f3944afbc4c0a, 0x26a1c0cdd9b9a561, 0xe338181311bd75dd, 0xfbd4bb6a5d745192, 0x364b6e1e1acf3dff, 0x8588c68eeb551be4, 0x94042cdfc05c9078, 0xfd14950d941b5636, 0x3061892191b51444, 0xda2ae8f04f6f93e5, 0xda12c33b1f8344b6, 0xdafe433b3d07428c, 0xdc4d3d9982d37b00, 0xc6c0ef1cb3d6f7c3, 0xb006c6bd748a7885, 0x3984d51596eab3be, 0x177cdfd9bcfb64b3, 0x269ed4476b3b9209, 0x5bcc6c1d92a94ee4, 0x41fce1f1d209a2cd, 0x8aff91ffa442aa48, 0x518f7b68f586ee81, 0xb2280f147f999d63]
        outputs = [0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x00000000000000DC, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000]
        for i, a in enumerate(inputs):
            self.assertEquals(solver._solve("(lambda (id) (fold id 0 (lambda (id2 id3) (if0 id3 id2 0))))", Int64(a)), outputs[i])

    def test_local_params(self):
        self.assertEquals(solver._solve(" (lambda (x_3739) (fold x_3739 0 (lambda (x_3739 x_3740) (if0 x_3740 x_3739 0))))", Int64(0xFFFADCDEFFFF)), 0)

    def _compare_solvers(self, size, allowed_ops):
        inputs1 = [0x0, 0x1, 0xffffffffffffffff, 0x2219abe04416f96, 0xa077cf0e37127fc6, 0xab71ae29047479b8, 0x4ac8bbf6614e023, 0xc71cf027608a7c71, 0xfe3096de18a687f1, 0xd620a1df607f2c2a, 0x41ca689d6aef148b, 0x9af769cc362d2b95, 0x537409691dfcee1f, 0x9892e5ef90beaeb5, 0x8f4ba748f96269da, 0x582d08ce34753010, 0x18e9862bd9e76bc5, 0xf2337a6b976bc10e, 0x6328c59ae3c48889, 0x9f7c85698eaf6df6, 0x5a7bf4a0a03bbf9b, 0x8dfb2db7e034967f, 0xe8cdee80940c840f, 0x422111dd0c8d029a, 0x4722f6922e15b9f1, 0xd493baaf9891eec5, 0x42755ecad1914aeb, 0x3ce1c58d13bfc252, 0x35e2320ecfc72482, 0x29ae2aea58ed517f, 0x8112f2a40232b7e4, 0x93d7d718d4cff331, 0x599360cef1447730, 0xf18db68940452498, 0xc8f32bb02c462e44, 0x9faa9427d7c2109, 0x117f5f544c55131, 0x22e09f997d8ee361, 0x542d1aef6403ef68, 0xf721f0fc9eeb2aee, 0x67d357dc18c2470e, 0x6f3f3944afbc4c0a, 0x26a1c0cdd9b9a561, 0xe338181311bd75dd, 0xfbd4bb6a5d745192, 0x364b6e1e1acf3dff, 0x8588c68eeb551be4, 0x94042cdfc05c9078, 0xfd14950d941b5636, 0x3061892191b51444, 0xda2ae8f04f6f93e5, 0xda12c33b1f8344b6, 0xdafe433b3d07428c, 0xdc4d3d9982d37b00, 0xc6c0ef1cb3d6f7c3, 0xb006c6bd748a7885, 0x3984d51596eab3be, 0x177cdfd9bcfb64b3, 0x269ed4476b3b9209, 0x5bcc6c1d92a94ee4, 0x41fce1f1d209a2cd, 0x8aff91ffa442aa48, 0x518f7b68f586ee81, 0xb2280f147f999d63]
        index_dispatcher = build_formula_index.TreeIndexDispatcher(tempfile.gettempdir())
        index = index_dispatcher.get_index(allowed_ops)
        counter = 0
        for formula in index.generate_formulas(size, allowed_ops):
            counter = counter + 1
            outputs = list(solver.solve_formula(formula, map(lambda x: Int64(x), inputs1)))
            for i, a in enumerate(inputs1):
                str_output = solver._solve(formula['s'], Int64(a))
                if (str_output != outputs[i]):
                    print formula['s']
                    print 'Input: %s, String_output: %s, Tree_output: %s' % (a, str_output, outputs[i])
                    self.fail('Tree solver and String solver mismatch')
        self.assertGreater(counter, 0)


    def test_compare_solvers_xor(self):
        self._compare_solvers(5, ['xor'])
    def test_compare_solvers_shr16(self):
        self._compare_solvers(3, ['shr16'])
    def test_compare_solvers_shr4(self):
        self._compare_solvers(3, ['shr4'])
    def test_compare_solvers_not(self):
        self._compare_solvers(3, ['not'])
    def test_compare_solvers_and(self):
        self._compare_solvers(5, ['and', 'not'])
    def test_compare_solvers_or(self):
        self._compare_solvers(5, ['or', 'not'])
    def test_compare_solvers_if0(self):
            self._compare_solvers(9, ['if0', 'not'])
    def test_compare_solvers_fold_plus(self):
        self._compare_solvers(9, ['fold', 'not'])
    def test_compare_solvers_tfold_if0(self):
        self._compare_solvers(9, ['tfold', 'if0'])
    def test_compare_solvers_plus(self):
        self._compare_solvers(5, ['plus'])
    def test_compare_solvers_size_7(self):
        self._compare_solvers(7, None)

