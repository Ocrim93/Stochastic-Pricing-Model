#include "Greeks.h"


Greeks::Greeks(const &PayOff_T PayOff_) : PayOffObject(PayOff_)
{	
	double step_size = 1.e-4; 
	DerivativeObject(PayOff_T::Value, step_size_);
}

Greeks::Delta() const
{
	return DerivativeObject.first_compute<1>(double Expiry,double Spot, double Vol, double r, double q);
}