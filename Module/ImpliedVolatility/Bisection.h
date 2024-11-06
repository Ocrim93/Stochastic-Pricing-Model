template<class T, (T::*Value)(double) const >
double Bisection(double Target,
				 double Low,
				 double High,
				 double accuracy,
				 const T& Object)
{	
	double x = 0.5*(High+Low);
	double y = (Object.*Value)(x);
	do
	{
		if (y < Target)
			Low = x;
		if( y > Target)
			High = x;
		x = 0.5*(High+Low);
	}while( fabs( y - Target) > accuracy );
	
	return x;
}