#include "Vanilla.h"
#include <algorithm>
#include "../../BlackScholes/BlackScholes.cpp"


VanillaCall::VanillaCall(double Strike_)
	: Strike(Strike_)
{
	this->NumberOfPaths = 1e6;
}
VanillaCall::VanillaCall(double Strike_, double Expiry_, double Spot_ ,double Vol_ ,double r_, double q_ )
	: Strike(Strike_)
{	
	Expiry = Expiry_;
	Spot = Spot_;
	Vol = Vol_;
	r= r_;
	q= q_;
	NumberOfPaths = 1e6;
}

double VanillaCall::operator() (double Spot) const
{
	return std::max(Spot - Strike,0.0);
}

PayOff* VanillaCall::clone() const
{
	return new VanillaCall(*this);
}

double VanillaCall::Value(double Expiry_ = 0.0 , double Spot_ = 0.0, double Vol_= 0.0, double r_ = 0.0 , double q_ = 0.0) const
{	
	if (Expiry_ == 0.0) Expiry_ = Expiry;
	if (Spot_ == 0.0) Spot_ = Spot;
	if (Vol_ == 0.0) Vol_ = Vol;
	if (r_ == 0.0) r_ = r;
	if (q_ == 0.0) q_ = q;

	return  BlackScholesPathIndependent( *this , Expiry_, Spot_,Vol_,r_, q_, NumberOfPaths);
}

void VanillaCall::SetNumberOfPaths(unsigned long NumberOfPaths_)
{
	this->NumberOfPaths = NumberOfPaths_;
}


//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VanillaPut %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
