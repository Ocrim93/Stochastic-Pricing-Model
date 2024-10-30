#include "Vanilla.h"
#include "../Payoff.h"
#include <algorithm>

VanillaCall::VanillaCall(double Strike_, double Expiry_) : Strike(Strike_), Expiry(Expiry_)
{

}

double VanillaCall::operator() (double Spot) const
{
	return std::max(Spot - Strike,0.0);
}

PayOff* VanillaCall::clone() const
{
	return new VanillaCall(*this);
}

double VanillaCall::GetExpiry() const
{
	return Expiry;
}

VanillaPut::VanillaPut(double Strike_, double Expiry_) : Strike(Strike_), Expiry(Expiry_)
{

}

double VanillaPut::operator() (double Spot) const
{
	return std::max(Strike - Spot,0.0);
}


PayOff* VanillaPut::clone() const
{
	return new VanillaPut(*this);
}

double VanillaPut::GetExpiry() const
{
	return Expiry;
}