#include "DoubleDigital.h"
#include "../Payoff/Payoff.h"

DoubleDigital::DoubleDigital(double LowerLevel_, double UpperLevel_, double Expiry_)
	:LowerLevel(LowerLevel_),UpperLevel(UpperLevel_), Expiry(Expiry_){

	}

PayOff* DoubleDigital::clone()
{
	return new DoubleDigital(*this);
}

// DoubleDigital payOff . It pays 1 if spot is between two values and 0 otherwise
double DoubleDigital::operator()(double Spot) const{
	if (Spot <= LowerLevel){
		return 0;
	}
	if (Spot >= UpperLevel){
		return 0;
	}
	return 1;
}

double DoubleDigital::GetExpiry()
{
	return Expiry;
}

double DoubleDigital::Value(double Spot,
						  double Vol,
						  double r,
						  double q,
						  unsigned long NumberOfPaths) const
{
	return  BlackScholesPathIndependent( *this->clone() , Spot,Vol,r, q,NumberOfPaths);
}