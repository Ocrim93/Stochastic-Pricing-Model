#include <stdio.h>
#include <time.h>

template<class T, double (T::*Value)(double) const >
double Bisection(double Target,
				 double Low,
				 double High,
				 double accuracy,
				 const T& Object)
{	
	printf("Starting Bisection \n");
	clock_t t = clock();
	double x = 0.5*(High+Low);
	double y = (Object.*Value)(x);
	do
	{
		if (y < Target)
			Low = x;
		if( y > Target)
			High = x;
		x = 0.5*(High+Low);
		y = (Object.*Value)(x);
	}while( fabs( y - Target) > accuracy );
	t = clock() -t;
	printf(" Bisection took %0.3f seconds, accuracy %0.4f --> %0.4f %% \n", ((float)t)/CLOCKS_PER_SEC, accuracy,x*100);
	return x;
}