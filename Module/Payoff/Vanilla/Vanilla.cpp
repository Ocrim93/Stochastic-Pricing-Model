#include "Vanilla.h"
#include <algorithm>
#include "../../BlackScholes/BlackScholes.cpp"
#include "../../ImpliedVolatility/Bisection.h"

VanillaCall::VanillaCall(double Strike_, double Expiry_, double Spot_ ,double Vol_ ,double r_, double q_ )
	: Strike(Strike_), Expiry(Expiry_),Spot(Spot_),  Vol(Vol_), r(r_), q(q_)
{
	this->NumberOfPaths = 1e6;
	this->accuracy = 1e-4;
}

double VanillaCall::operator() (double Spot) const
{
	return std::max(Spot - Strike,0.0);
}

PayOff* VanillaCall::clone() const
{
	return new VanillaCall(*this);
}

double VanillaCall::Value() const
{	
	return  BlackScholesPathIndependent( *this , Expiry, Spot,Vol,r, q, NumberOfPaths);
}


double VanillaCall::Value_perVol(double Vol_) const
{
	return BlackScholesPathIndependent( *this ,Expiry, Spot,Vol_,r, q, NumberOfPaths);
}


double VanillaCall::ImpliedVolBisection(double MtM, double Low, double High) const
{	
	return Bisection< VanillaCall, &VanillaCall::Value_perVol>(MtM, Low, High,accuracy, *this);
}

void VanillaCall::SetNumberOfPaths(unsigned long NumberOfPaths_)
{
	this->NumberOfPaths = NumberOfPaths_;
}

void VanillaCall::SetAccuracy(double accuracy_)
{
	this->accuracy = accuracy_;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VanillaPut %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
