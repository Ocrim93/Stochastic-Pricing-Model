#include <stdio.h>
#include <time.h>

template< class T, double (T::*Value)(double) const, double (T::*Derivative)(double) const>
double NewtonRaphson(double Target,
					 double Start,
					 double accuracy,
					 const T& Object)

{	
	printf("Starting NewtonRaphson \n");
	clock_t t = clock();
	double y = (Object.*Value)(Start);
	double x = Start;
	while( fabs( y- Target) > accuracy)
	{
		double d = (Object.*Derivative)(x);
		x += (Target - y)/d;
		y = (Object.*Value)(x);
	}
	t = clock() -t;
	printf(" NewtonRaphson took %0.3f seconds, accuracy %0.4f --> %0.4f %% \n", ((float)t)/CLOCKS_PER_SEC, accuracy,x*100);
	return x;
}