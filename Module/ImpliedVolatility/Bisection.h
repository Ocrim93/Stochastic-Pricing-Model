#include <stdio.h>
#include <time.h>

template<class T, double (T::*Value)(double) const >
double Bisection(double Target,
				 double Low,
				 double High,
				 double accuracy,
				 const T& Object)
{	
	printf("Startin Bisection \n");
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
	printf(" Bisection took %0.3f seconds\n", ((float)t)/CLOCKS_PER_SEC);
	return x;
}