from cupy import RawKernel

polevl_definition = """
template<int N> static __device__ double polevl(double x, double coef[])
{
    double ans;
    double *p;
    p = coef;
    ans = *p++;
    for (int i = 0; i < N; ++i){
        ans = ans * x + *p++;
    }
    return ans;
}
"""

cosm1_definition = """
__constant__ double coscof[7] = {
    4.7377507964246204691685E-14,
    -1.1470284843425359765671E-11,
    2.0876754287081521758361E-9,
    -2.7557319214999787979814E-7,
    2.4801587301570552304991E-5,
    -1.3888888888888872993737E-3,
    4.1666666666666666609054E-2,
};
__constant__ double PI_4 = 0.7853981633974483;

double cosm1(double x)
{
    double xx;

    if ((x < -PI_4) || (x > PI_4))
    return (cos(x) - 1.0);
    xx = x * x;
    xx = -0.5 * xx + xx * xx * polevl<7>(xx, coscof);
    return xx;
}
"""

cosm1_kernel = RawKernel(cosm1_definition, "cosm1", preamble=polevl_definition)
