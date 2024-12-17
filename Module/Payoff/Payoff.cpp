#include "Payoff.h"
#include "../ImpliedVolatility/Bisection.h"
#include "../ImpliedVolatility/NewtonRaphson.h"
#include "../Greeks/Greeks.cpp"

double PayOff::Value_perVol(double Vol_) const
{	
	return Value(Expiry, Spot ,Vol_,r);
	
}

double PayOff::Vega_perVol(double Vol_) const
{
	double h = 1.e-4;
	return (Value_perVol(Vol_ + h ) - Value_perVol(Vol_ - h ))/(2*h);

}
double PayOff::ImpliedVolBisection(double MtM, double Low, double High, double  accuracy = 1.e-4 ) const
{	
	double impliedVol;
	impliedVol = Bisection< PayOff, &PayOff::Value_perVol>(MtM, Low, High,accuracy, *this);
	return impliedVol;
}
double PayOff::ImpliedVolNewtonRaphson(double MtM, double Start, double accuracy = 1.e-4) const
{	
	double impliedVol;
	impliedVol = NewtonRaphson<PayOff,&PayOff::Value_perVol,&PayOff::Vega_perVol >(MtM, Start ,accuracy, *this);
	return impliedVol;
}

std::map<std::string,double> PayOff::Greeks() const
{
	Greeks greeks_obj(*this);
	return greeks_obj.compute_Greeks();
}