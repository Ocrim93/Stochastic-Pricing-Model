#include "Vanilla.h"
#include <algorithm>
#include "../../BlackScholes/BlackScholes.cpp"
//#include "../../Greeks/Greeks.h"

VanillaCall::VanillaCall(double Strike_, double Expiry_, double Spot_ ,double Vol_ ,double r_, double q_ = 0 )
	: Strike(Strike_), q(q_)
{	
	Expiry = Expiry_;
	Spot = Spot_;
	Vol = Vol_;
	r= r_;
	NumberOfPaths = 1e6	;
}

double VanillaCall::operator() (double Spot) const
{
	return std::max(Spot - Strike,0.0);
}

PayOff* VanillaCall::clone() const
{
	return new VanillaCall(*this);
}

double VanillaCall::Value(double Expiry_ = 0.0 , double Spot_ = 0.0, double Vol_= 0.0, double r_ = 0.0 ) const
{	
	if (Expiry_ == 0.0) Expiry_ = Expiry;
	if (Spot_ == 0.0) Spot_ = Spot;
	if (Vol_ == 0.0) Vol_ = Vol;
	if (r_ == 0.0) r_ = r;

	return  BlackScholesPathIndependent( *this , Expiry_, Spot_,Vol_,r_, q, NumberOfPaths);
}

void VanillaCall::SetNumberOfPaths(unsigned long NumberOfPaths_)
{
	this->NumberOfPaths = NumberOfPaths_;
}


//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VanillaPut %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
