
template< class T, double (T::*Value)(double) const, double (T::*Derivative)(double) const>
double NewtonRaphson(double Target,
					 double Start,
					 double accuracy,
					 const T& Object)

{
	double y = (Object.*Value)(Start);
	double x = Start;
	while( fabs( y- Target) > accuracy)
	{
		double d = (Object.*Derivative)(x);
		x += (Target - y)/d;
		y = (Object.*Value)(x);
	}
	return x;
}