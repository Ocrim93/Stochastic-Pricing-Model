#include <stdio.h>
#include <time.h>

template< class T, double (T::*Value)(double) const, double (T::*Derivative)(double) const>
double NewtonRaphson(double Target,
					 double Start,
					 double accuracy,
					 const T& Object)

{	
	printf("Startin NewtonRaphson \n");
	clock_t t = clock()
	double y = (Object.*Value)(Start);
	double x = Start;
	while( fabs( y- Target) > accuracy)
	{
		double d = (Object.*Derivative)(x);
		x += (Target - y)/d;
		y = (Object.*Value)(x);
	}
	t = clock() -t;
	printf(" NewtonRaphson took %0.3f seconds\n", ((float)t)/CLOCKS_PER_SEC);
	return x;
}